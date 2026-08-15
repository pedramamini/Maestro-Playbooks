#!/usr/bin/env python3
"""Voice Memos CRUD helper.

Wraps Apple Voice Memos' Core Data / NSPersistentCloudKitContainer SQLite DB
and the loose audio files on disk. Reads are safe; writes quit the app and
snapshot first.

See the sibling SKILL.md for schema, caveats, and CloudKit sync realities.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sqlite3
import struct
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

RECORDINGS_DIR = Path(
    os.path.expanduser(
        "~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
    )
)
DB_PATH = RECORDINGS_DIR / "CloudRecordings.db"
BACKUP_DIR = RECORDINGS_DIR / ".claude-backups"
CORE_DATA_EPOCH_OFFSET = 978307200  # 2001-01-01 UTC in Unix seconds
AUDIO_EXTS = (".m4a", ".qta")
TSRP_ATOM = b"tsrp"
_CONTAINER_ATOMS = (
    b"moov",
    b"trak",
    b"mdia",
    b"minf",
    b"stbl",
    b"udta",
    b"meta",
    b"ilst",
)


# ---------- helpers ----------


def zdate_to_iso(z: float | None) -> str:
    if z is None:
        return ""
    return dt.datetime.fromtimestamp(
        z + CORE_DATA_EPOCH_OFFSET, tz=dt.timezone.utc
    ).isoformat(timespec="seconds")


def iso_to_zdate(s: str) -> float:
    parsed = dt.datetime.fromisoformat(s)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.timestamp() - CORE_DATA_EPOCH_OFFSET


def resolve_audio_path(zpath: str | None) -> Path | None:
    """ZPATH may name an .m4a whose actual file is .qta (or vice versa)."""
    if not zpath:
        return None
    direct = RECORDINGS_DIR / zpath
    if direct.exists():
        return direct
    stem = Path(zpath).stem
    for ext in AUDIO_EXTS:
        candidate = RECORDINGS_DIR / f"{stem}{ext}"
        if candidate.exists():
            return candidate
    return None


_TRANSCRIPT_SENTINEL = b'{"attributedString":'


def read_native_transcript(audio_path: Path) -> dict | None:
    """Extract Apple's native transcript JSON from a Voice Memos recording.

    Returns the parsed JSON (keys: `attributedString`, `locale`) or `None` if
    no transcript has been written yet. Apple embeds per-word timings and
    locale info directly inside the recording after the app finishes
    transcribing.

    Two known container layouts in the wild:

    1. Older `.m4a` files: transcript JSON is the body of a direct `tsrp`
       UDTA atom inside `moov.udta`.
    2. Newer `.qta` files (post Enhance Audio / trim): transcript JSON lives
       inside `moov.meta.ilst[1]` keyed by `com.apple.VoiceMemos.tsrp` via a
       QuickTime-style `mdta` `keys` atom — no `tsrp` tag at any atom header.

    Rather than thread both container walkers, this scans the raw bytes for
    the JSON object sentinel, which appears uniquely in either layout. We
    then expand a balanced-brace window forward and JSON-parse the first
    valid match.
    """
    try:
        data = audio_path.read_bytes()
    except OSError:
        return None
    i = 0
    while True:
        i = data.find(_TRANSCRIPT_SENTINEL, i)
        if i < 0:
            return None
        # Walk forward counting braces (with string-literal awareness) until
        # the object closes, then try to parse. Bail on first success.
        depth = 0
        in_str = False
        escape = False
        for j in range(i, len(data)):
            b = data[j]
            if in_str:
                if escape:
                    escape = False
                elif b == 0x5C:  # backslash
                    escape = True
                elif b == 0x22:  # "
                    in_str = False
                continue
            if b == 0x22:
                in_str = True
            elif b == 0x7B:  # {
                depth += 1
            elif b == 0x7D:  # }
                depth -= 1
                if depth == 0:
                    candidate = data[i:j + 1]
                    try:
                        return json.loads(candidate)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        break
        i += len(_TRANSCRIPT_SENTINEL)


def native_transcript_as_text(parsed: dict) -> str:
    runs = parsed.get("attributedString", {}).get("runs", [])
    return "".join(runs[::2])


def native_transcript_timed(parsed: dict) -> list[dict]:
    a = parsed.get("attributedString", {})
    runs = a.get("runs", [])
    attrs = a.get("attributeTable", [])
    out = []
    for i in range(0, len(runs), 2):
        tok = runs[i]
        idx = runs[i + 1] if i + 1 < len(runs) else 0
        tr = (attrs[idx].get("timeRange") if idx < len(attrs) else None) or [
            None,
            None,
        ]
        out.append({"start": tr[0], "end": tr[1], "token": tok})
    return out


def voice_memos_running() -> bool:
    r = subprocess.run(
        ["pgrep", "-x", "VoiceMemos"], capture_output=True, text=True
    )
    return r.returncode == 0


def quit_voice_memos(timeout_s: float = 5.0) -> None:
    if not voice_memos_running():
        return
    subprocess.run(
        ["osascript", "-e", 'tell application "Voice Memos" to quit'],
        check=False,
    )
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if not voice_memos_running():
            return
        time.sleep(0.25)
    raise RuntimeError(
        "Voice Memos is still running after quit request; refusing to write."
    )


def ensure_app_closed() -> None:
    if voice_memos_running():
        raise RuntimeError(
            "Voice Memos is running. Quit it first or use --quit-app."
        )


def snapshot(extra_files: list[Path] | None = None) -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    dest = BACKUP_DIR / stamp
    dest.mkdir()
    for name in (
        "CloudRecordings.db",
        "CloudRecordings.db-wal",
        "CloudRecordings.db-shm",
    ):
        src = RECORDINGS_DIR / name
        if src.exists():
            shutil.copy2(src, dest / name)
    for p in extra_files or []:
        if p and p.exists():
            shutil.copy2(p, dest / p.name)
    return dest


def connect(readonly: bool = True) -> sqlite3.Connection:
    if readonly:
        uri = f"file:{DB_PATH}?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
    else:
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("PRAGMA foreign_keys=ON;")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- subcommands ----------


def cmd_list(args: argparse.Namespace) -> int:
    clauses: list[str] = []
    params: list = []
    if args.since:
        clauses.append("r.ZDATE >= ?")
        params.append(iso_to_zdate(args.since))
    if args.until:
        clauses.append("r.ZDATE < ?")
        params.append(iso_to_zdate(args.until))
    if args.folder:
        clauses.append("f.ZENCRYPTEDNAME = ?")
        params.append(args.folder)
    if args.search:
        clauses.append(
            "(LOWER(r.ZENCRYPTEDTITLE) LIKE ? OR LOWER(r.ZCUSTOMLABEL) LIKE ?)"
        )
        needle = f"%{args.search.lower()}%"
        params.extend([needle, needle])
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""

    sql = f"""
        SELECT r.Z_PK AS id,
               r.ZDATE AS zdate,
               r.ZDURATION AS duration,
               COALESCE(r.ZENCRYPTEDTITLE, r.ZCUSTOMLABEL) AS title,
               r.ZPATH AS path,
               f.ZENCRYPTEDNAME AS folder
        FROM ZCLOUDRECORDING r
        LEFT JOIN ZFOLDER f ON r.ZFOLDER = f.Z_PK
        {where}
        ORDER BY r.ZDATE DESC
        LIMIT ?
    """
    params.append(args.limit)

    with connect() as conn:
        rows = [dict(r) for r in conn.execute(sql, params).fetchall()]

    for r in rows:
        r["created_utc"] = zdate_to_iso(r.pop("zdate"))
        r["duration_s"] = round(r.pop("duration") or 0.0, 2)
        resolved = resolve_audio_path(r["path"])
        r["resolved_path"] = str(resolved) if resolved else None

    if args.json:
        json.dump(rows, sys.stdout, indent=2, default=str)
        print()
    else:
        for r in rows:
            print(
                f"[{r['id']:>4}] {r['created_utc']}  "
                f"{r['duration_s']:>6.1f}s  "
                f"{(r['folder'] or '-'):<20}  "
                f"{r['title'] or '<default>'}"
            )
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM ZCLOUDRECORDING WHERE Z_PK=?", (args.id,)
        ).fetchone()
        if not row:
            print(f"No recording with id={args.id}", file=sys.stderr)
            return 1
        d = dict(row)
        if d.get("ZFOLDER"):
            f = conn.execute(
                "SELECT ZENCRYPTEDNAME FROM ZFOLDER WHERE Z_PK=?",
                (d["ZFOLDER"],),
            ).fetchone()
            d["folder_name"] = f["ZENCRYPTEDNAME"] if f else None
    d["created_utc"] = zdate_to_iso(d.get("ZDATE"))
    resolved = resolve_audio_path(d.get("ZPATH"))
    d["resolved_path"] = str(resolved) if resolved else None
    composition = RECORDINGS_DIR / f"{Path(d['ZPATH']).stem}.composition"
    d["composition_dir"] = str(composition) if composition.exists() else None
    if resolved:
        parsed = read_native_transcript(resolved)
        d["native_transcript_available"] = parsed is not None
        if parsed:
            d["native_transcript_locale"] = parsed.get("locale", {}).get(
                "identifier"
            )
            d["native_transcript_token_count"] = (
                len(parsed.get("attributedString", {}).get("runs", [])) // 2
            )
    # Drop binary blobs so JSON stays readable.
    for k in (
        "ZAUDIOFUTUREUUIDS",
        "ZAUDIODIGEST",
        "ZAUDIOFUTURE",
        "ZMTAUDIOFUTURE",
        "ZVERSIONEDAUDIOFUTURE",
    ):
        if d.get(k) is not None:
            d[k] = f"<{len(d[k])} bytes>"
    json.dump(d, sys.stdout, indent=2, default=str)
    print()
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    with connect() as conn:
        row = conn.execute(
            "SELECT ZPATH, ZENCRYPTEDTITLE, ZCUSTOMLABEL "
            "FROM ZCLOUDRECORDING WHERE Z_PK=?",
            (args.id,),
        ).fetchone()
    if not row:
        print(f"No recording with id={args.id}", file=sys.stderr)
        return 1
    src = resolve_audio_path(row["ZPATH"])
    if not src:
        print(
            f"Audio file not found for ZPATH={row['ZPATH']!r}", file=sys.stderr
        )
        return 1
    dest = Path(args.dest).expanduser()
    if dest.is_dir():
        label = row["ZENCRYPTEDTITLE"] or row["ZCUSTOMLABEL"] or src.stem
        safe = "".join(c if c.isalnum() or c in " _-." else "_" for c in label)
        dest = dest / f"{safe}{src.suffix}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(dest)
    return 0


def cmd_transcribe(args: argparse.Namespace) -> int:
    with connect() as conn:
        row = conn.execute(
            "SELECT ZPATH FROM ZCLOUDRECORDING WHERE Z_PK=?", (args.id,)
        ).fetchone()
    if not row:
        print(f"No recording with id={args.id}", file=sys.stderr)
        return 1
    src = resolve_audio_path(row["ZPATH"])
    if not src:
        print(f"Audio file missing for id={args.id}", file=sys.stderr)
        return 1

    # Prefer the transcript Apple's Voice Memos already wrote into the file.
    if not args.force_whisper:
        parsed = read_native_transcript(src)
        if parsed:
            if args.format == "timed":
                for row in native_transcript_timed(parsed):
                    start = row["start"] if row["start"] is not None else 0.0
                    end = row["end"] if row["end"] is not None else 0.0
                    print(f"{start:7.2f} -> {end:7.2f}  {row['token']!r}")
            elif args.format == "json":
                json.dump(parsed, sys.stdout, ensure_ascii=False)
                print()
            else:
                print(native_transcript_as_text(parsed))
            return 0
        if args.native_only:
            print(
                "No native Apple transcript (tsrp atom) found. "
                "Open this memo in Voice Memos once to trigger transcription, "
                "or rerun without --native-only to fall back to whisper.",
                file=sys.stderr,
            )
            return 1

    whisper_cli = shutil.which("whisper-cli") or shutil.which("whisper-cpp")
    whisper_py = shutil.which("whisper")

    if whisper_cli:
        model = args.model or os.path.expanduser(
            "~/.whisper/models/ggml-base.en.bin"
        )
        if not Path(model).exists():
            print(
                f"whisper-cli model not found at {model}. "
                "Download a ggml model or pass --model.",
                file=sys.stderr,
            )
            return 1
        cmd = [whisper_cli, "-m", model, "-f", str(src), "-nt"]
        return subprocess.run(cmd).returncode

    if whisper_py:
        model = args.model or "base.en"
        # Whisper writes .txt/.srt/.vtt/.json into the output dir; stash them.
        with tempfile.TemporaryDirectory() as td:
            cmd = [
                whisper_py,
                str(src),
                "--model",
                model,
                "--output_format",
                "txt",
                "--output_dir",
                td,
            ]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                sys.stderr.write(r.stderr)
                return r.returncode
            txt = next(Path(td).glob("*.txt"), None)
            if txt:
                sys.stdout.write(txt.read_text())
            return 0

    print(
        "No whisper binary found and no native transcript present. "
        "Install whisper-cpp (`brew install whisper-cpp`) "
        "or openai-whisper (`pipx install openai-whisper`), or open the "
        "memo in Voice Memos to let Apple transcribe it.",
        file=sys.stderr,
    )
    return 2


def cmd_rename(args: argparse.Namespace) -> int:
    if args.quit_app:
        quit_voice_memos()
    else:
        ensure_app_closed()
    snapshot_dir = snapshot()
    with connect(readonly=False) as conn:
        cur = conn.execute(
            "UPDATE ZCLOUDRECORDING "
            "SET ZENCRYPTEDTITLE=?, "
            "    ZCUSTOMLABEL=COALESCE(ZCUSTOMLABEL, ?), "
            "    ZCUSTOMLABELFORSORTING=? "
            "WHERE Z_PK=?",
            (args.title, args.title, args.title.lower(), args.id),
        )
        conn.commit()
        if cur.rowcount == 0:
            print(f"No recording with id={args.id}", file=sys.stderr)
            return 1
    print(f"Renamed id={args.id} -> {args.title!r} (backup: {snapshot_dir})")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    if args.quit_app:
        quit_voice_memos()
    else:
        ensure_app_closed()

    with connect() as conn:
        row = conn.execute(
            "SELECT ZPATH FROM ZCLOUDRECORDING WHERE Z_PK=?", (args.id,)
        ).fetchone()
    if not row:
        print(f"No recording with id={args.id}", file=sys.stderr)
        return 1
    audio = resolve_audio_path(row["ZPATH"])
    waveform = RECORDINGS_DIR / f"{Path(row['ZPATH']).stem}-track0.waveform"
    composition = RECORDINGS_DIR / f"{Path(row['ZPATH']).stem}.composition"

    snapshot_dir = snapshot(
        extra_files=[p for p in (audio, waveform) if p and p.exists()]
    )
    if composition.exists():
        shutil.copytree(
            composition, snapshot_dir / composition.name, dirs_exist_ok=True
        )

    with connect(readonly=False) as conn:
        conn.execute("DELETE FROM ZCLOUDRECORDING WHERE Z_PK=?", (args.id,))
        if args.mark_cloud_delete:
            conn.execute(
                "UPDATE ANSCKRECORDMETADATA "
                "SET ZNEEDSCLOUDDELETE=1 WHERE ZENTITYPK=?",
                (args.id,),
            )
        conn.commit()

    for p in (audio, waveform):
        if p and p.exists():
            p.unlink()
    if composition.exists():
        shutil.rmtree(composition)

    print(
        f"Deleted id={args.id} (backup: {snapshot_dir}, "
        f"cloud-delete-flag={'set' if args.mark_cloud_delete else 'unset'})"
    )
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    src = Path(args.file).expanduser()
    if not src.exists():
        print(f"Source file not found: {src}", file=sys.stderr)
        return 1
    if src.suffix.lower() not in AUDIO_EXTS:
        print(
            f"Refusing to import {src.suffix}; expected .m4a or .qta.",
            file=sys.stderr,
        )
        return 1

    if args.quit_app:
        quit_voice_memos()
    else:
        ensure_app_closed()

    duration = 0.0
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        r = subprocess.run(
            [
                ffprobe,
                "-v",
                "quiet",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(src),
            ],
            capture_output=True,
            text=True,
        )
        try:
            duration = float(r.stdout.strip())
        except ValueError:
            duration = 0.0

    now = dt.datetime.now(tz=dt.timezone.utc)
    zdate = now.timestamp() - CORE_DATA_EPOCH_OFFSET
    stamp = now.strftime("%Y%m%d %H%M%S")
    suffix = uuid.uuid4().hex[:8].upper()
    new_name = f"{stamp}-{suffix}{src.suffix.lower()}"
    dest_audio = RECORDINGS_DIR / new_name

    snapshot_dir = snapshot()
    shutil.copy2(src, dest_audio)

    folder_pk = None
    with connect(readonly=False) as conn:
        if args.folder:
            f = conn.execute(
                "SELECT Z_PK FROM ZFOLDER WHERE ZENCRYPTEDNAME=?",
                (args.folder,),
            ).fetchone()
            if not f:
                print(
                    f"Folder {args.folder!r} not found. Use `folders` to list.",
                    file=sys.stderr,
                )
                dest_audio.unlink(missing_ok=True)
                return 1
            folder_pk = f["Z_PK"]

        ent = conn.execute(
            "SELECT Z_ENT FROM ZCLOUDRECORDING LIMIT 1"
        ).fetchone()
        z_ent = ent["Z_ENT"] if ent else 4
        title = args.title or "Imported Recording"
        iso_stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        cur = conn.execute(
            "INSERT INTO ZCLOUDRECORDING "
            "(Z_ENT, Z_OPT, ZFLAGS, ZSHAREDFLAGS, ZFOLDER, ZDATE, "
            "ZDURATION, ZLOCALDURATION, ZENCRYPTEDTITLE, ZCUSTOMLABEL, "
            "ZCUSTOMLABELFORSORTING, ZPATH, ZUNIQUEID, ZPLAYBACKRATE, "
            "ZPLAYBACKSPEED, ZPLAYBACKPOSITION, ZSKIPSILENCEENABLED, "
            "ZSTUDIOMIXENABLED) "
            "VALUES (?, 1, 0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1.0, 1.0, 0.0, 0, 0)",
            (
                z_ent,
                folder_pk,
                zdate,
                duration,
                duration,
                title,
                iso_stamp,
                iso_stamp.lower(),
                new_name,
                str(uuid.uuid4()).upper(),
            ),
        )
        new_pk = cur.lastrowid
        conn.commit()

    print(
        f"Imported {src} as id={new_pk} ({new_name}, "
        f"{duration:.1f}s, backup: {snapshot_dir})"
    )
    print(
        "Note: CloudKit mirror rows were NOT written; this record is "
        "local-first. Open Voice Memos to let it reconcile."
    )
    return 0


def cmd_folders(_args: argparse.Namespace) -> int:
    with connect() as conn:
        rows = conn.execute(
            "SELECT Z_PK, ZENCRYPTEDNAME, ZRANK, ZCOUNTOFRECORDINGS, ZUUID "
            "FROM ZFOLDER ORDER BY ZRANK"
        ).fetchall()
    for r in rows:
        print(
            f"[{r['Z_PK']:>3}] rank={r['ZRANK']}  "
            f"count={r['ZCOUNTOFRECORDINGS']:>3}  "
            f"{r['ZENCRYPTEDNAME']}  ({r['ZUUID']})"
        )
    return 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    dest = Path(args.dest).expanduser()
    dest.mkdir(parents=True, exist_ok=True)
    for name in (
        "CloudRecordings.db",
        "CloudRecordings.db-wal",
        "CloudRecordings.db-shm",
    ):
        src = RECORDINGS_DIR / name
        if src.exists():
            shutil.copy2(src, dest / name)
    if args.include_audio:
        audio_dest = dest / "audio"
        audio_dest.mkdir(exist_ok=True)
        for p in RECORDINGS_DIR.iterdir():
            if p.suffix.lower() in AUDIO_EXTS:
                shutil.copy2(p, audio_dest / p.name)
    print(dest)
    return 0


# ---------- argparse wiring ----------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Voice Memos CRUD helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list", help="List recordings")
    pl.add_argument("--limit", type=int, default=25)
    pl.add_argument("--since", help="ISO date/datetime, inclusive lower bound")
    pl.add_argument("--until", help="ISO date/datetime, exclusive upper bound")
    pl.add_argument("--folder", help="Exact folder name match")
    pl.add_argument("--search", help="Substring match on title (case-insensitive)")
    pl.add_argument("--json", action="store_true")
    pl.set_defaults(func=cmd_list)

    ps = sub.add_parser("show", help="Show one recording")
    ps.add_argument("id", type=int)
    ps.set_defaults(func=cmd_show)

    pe = sub.add_parser("export", help="Copy audio file out")
    pe.add_argument("id", type=int)
    pe.add_argument("dest", help="Destination file or directory")
    pe.set_defaults(func=cmd_export)

    pt = sub.add_parser(
        "transcribe",
        help="Return transcript (Apple's native tsrp if present, else whisper)",
    )
    pt.add_argument("id", type=int)
    pt.add_argument(
        "--format",
        choices=["text", "timed", "json"],
        default="text",
        help="Output format for native transcript (whisper always prints text)",
    )
    pt.add_argument(
        "--native-only",
        action="store_true",
        help="Fail rather than fall back to whisper",
    )
    pt.add_argument(
        "--force-whisper",
        action="store_true",
        help="Skip the native tsrp atom and run whisper",
    )
    pt.add_argument("--model", help="whisper model path or name (fallback only)")
    pt.set_defaults(func=cmd_transcribe)

    pr = sub.add_parser("rename", help="Rename (retitle) a recording")
    pr.add_argument("id", type=int)
    pr.add_argument("title")
    pr.add_argument("--quit-app", action="store_true", help="Quit Voice Memos first")
    pr.set_defaults(func=cmd_rename)

    pd = sub.add_parser("delete", help="Delete a recording (local; audio unlinked)")
    pd.add_argument("id", type=int)
    pd.add_argument("--quit-app", action="store_true")
    pd.add_argument(
        "--mark-cloud-delete",
        action="store_true",
        help="Flag ANSCKRECORDMETADATA for cloud deletion too",
    )
    pd.set_defaults(func=cmd_delete)

    pi = sub.add_parser("import", help="Import an audio file as a new memo")
    pi.add_argument("file", help="Path to .m4a or .qta")
    pi.add_argument("--title")
    pi.add_argument("--folder", help="Target folder name (must exist)")
    pi.add_argument("--quit-app", action="store_true")
    pi.set_defaults(func=cmd_import)

    pf = sub.add_parser("folders", help="List folders")
    pf.set_defaults(func=cmd_folders)

    pn = sub.add_parser(
        "snapshot", help="Copy DB (and optionally audio) elsewhere"
    )
    pn.add_argument("dest")
    pn.add_argument("--include-audio", action="store_true")
    pn.set_defaults(func=cmd_snapshot)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not DB_PATH.exists():
        print(f"CloudRecordings.db not found at {DB_PATH}", file=sys.stderr)
        return 2
    try:
        return args.func(args)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
