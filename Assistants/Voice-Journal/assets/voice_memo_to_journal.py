#!/usr/bin/env python3
"""
voice_memo_to_journal.py

Append today's new Apple Voice Memos (as transcribed by Apple on-device) to a
daily Markdown journal file, renaming each memo with a title derived from its
first words.

Flow:
  1. List memos whose local-date matches the target date AND whose title
     still starts with "New Recording" (Apple's default for fresh captures).
  2. For each, read Apple's native transcript (the `tsrp` atom inside the
     audio file) via the sibling `voice_memos.py` helper. If Apple hasn't
     transcribed yet, fall back to local Apple-Silicon-native Whisper via
     `whisperkit-cli` running directly on the audio file.
  3. Derive a title from the first ~N words of the transcript.
  4. Rename the memo in the Voice Memos database (the helper snapshots the
     DB first and refuses to write while Voice Memos is open).
  5. Append each entry to `<JOURNAL_DIR>/YYYY-MM-DD.md`, preserving existing
     content with newline separation.

Idempotency: two-layer. The primary filter excludes memos whose title no
longer starts with "New Recording". The secondary (authoritative) check
scans the journal file for `<!-- vm:<id> -->` anchors and skips memos
already written, so re-runs are safe even if CloudKit restores the old
title after a rename.

Configuration (in order of precedence):
  --journal-dir PATH              CLI flag
  $VOICE_MEMO_JOURNAL_DIR         environment variable
  ~/Journal                       default

  --timezone NAME                 CLI flag (IANA tz, e.g. "America/Chicago")
  $VOICE_MEMO_TZ                  environment variable
  system local timezone           default

Usage:
    python3 voice_memo_to_journal.py                    # process today
    python3 voice_memo_to_journal.py --date 2026-04-23
    python3 voice_memo_to_journal.py --dry-run
    python3 voice_memo_to_journal.py --journal-dir ~/MyVault/Journal
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

SCRIPT_DIR = Path(__file__).resolve().parent
HELPER = SCRIPT_DIR / "voice_memos.py"
DEFAULT_JOURNAL_DIR = Path(
    os.environ.get("VOICE_MEMO_JOURNAL_DIR") or (Path.home() / "Journal")
).expanduser()
DEFAULT_TITLE_PREFIX = "new recording"
TITLE_MAX_WORDS = 8
ANCHOR_RE = re.compile(r"<!--\s*vm:(\d+)\s*-->")

# Local Whisper fallback (whisperkit-cli — Apple-Silicon-native).
# Used when Apple's on-device Voice Memos transcription hasn't landed yet.
WHISPERKIT_MODEL = os.environ.get("VOICE_MEMO_WHISPERKIT_MODEL", "openai_whisper-small")
WHISPERKIT_MODEL_ROOT = Path(
    os.environ.get("VOICE_MEMO_WHISPERKIT_MODEL_ROOT")
    or (Path.home() / "Documents" / "huggingface" / "models"
        / "argmaxinc" / "whisperkit-coreml")
).expanduser()


def journaled_ids(journal_path: Path) -> set[int]:
    if not journal_path.exists():
        return set()
    return {int(m) for m in ANCHOR_RE.findall(journal_path.read_text())}


def resolve_timezone(name: str | None) -> dt.tzinfo:
    if name:
        return ZoneInfo(name)
    env = os.environ.get("VOICE_MEMO_TZ")
    if env:
        return ZoneInfo(env)
    local = dt.datetime.now().astimezone().tzinfo
    return local or dt.timezone.utc


def run_helper(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(HELPER), *args],
        capture_output=True,
        text=True,
        check=check,
    )


def list_memos_for_date(target_date: dt.date, tz: dt.tzinfo) -> list[dict]:
    since = (target_date - dt.timedelta(days=1)).isoformat()
    r = run_helper(["list", "--since", since, "--json"])
    memos = json.loads(r.stdout)
    out = []
    for m in memos:
        title = (m.get("title") or "").strip().lower()
        if not title.startswith(DEFAULT_TITLE_PREFIX):
            continue
        created_utc = dt.datetime.fromisoformat(m["created_utc"])
        local = created_utc.astimezone(tz)
        if local.date() != target_date:
            continue
        m["local_dt"] = local
        out.append(m)
    out.sort(key=lambda m: m["local_dt"])
    return out


def fetch_native_transcript(memo_id: int) -> str | None:
    r = run_helper(["transcribe", str(memo_id), "--native-only"], check=False)
    if r.returncode != 0:
        return None
    text = r.stdout.strip()
    return text or None


def fetch_whisperkit_transcript(audio_path: Path) -> str | None:
    """Local Apple-Silicon-native Whisper fallback via whisperkit-cli.

    Invoked when Apple's on-device Voice Memos transcription hasn't landed
    yet. Install with `brew install whisperkit-cli`. Model is auto-downloaded
    on first use if the model path doesn't exist locally.
    """
    # Try PATH first, then the Homebrew default — cron has a minimal PATH,
    # so shutil.which may miss the binary even when it's installed.
    whisperkit = shutil.which("whisperkit-cli") or "/opt/homebrew/bin/whisperkit-cli"
    # whisperkit-cli prints CoreAudio failures to stdout and still exits 0,
    # so rely on is_file() to guarantee there's a real file to transcribe.
    if not Path(whisperkit).is_file() or not audio_path.is_file():
        return None
    cmd = [whisperkit, "transcribe", "--audio-path", str(audio_path),
           "--model", WHISPERKIT_MODEL]
    model_path = WHISPERKIT_MODEL_ROOT / WHISPERKIT_MODEL
    if model_path.exists():
        cmd += ["--model-path", str(model_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return None
    text = r.stdout.strip()
    if not text or text.startswith("Error "):
        return None
    return text


def derive_title(transcript: str, max_words: int = TITLE_MAX_WORDS) -> str | None:
    first_sentence = re.split(r"(?<=[.!?])\s+|\n", transcript, maxsplit=1)[0]
    words = first_sentence.split()[:max_words]
    if not words:
        return None
    candidate = " ".join(words).strip(" ,;:-—\"'`")
    if not candidate:
        return None
    return candidate[0].upper() + candidate[1:]


def rename_memo(memo_id: int, title: str) -> tuple[bool, str]:
    r = run_helper(["rename", str(memo_id), title, "--quit-app"], check=False)
    ok = r.returncode == 0
    return ok, (r.stderr or r.stdout).strip()


def append_to_journal(
    target_date: dt.date,
    entries: list[dict],
    journal_dir: Path,
    dry_run: bool,
) -> Path:
    journal_dir.mkdir(parents=True, exist_ok=True)
    path = journal_dir / f"{target_date.isoformat()}.md"
    existing = path.read_text() if path.exists() else ""

    blocks = []
    for e in entries:
        blocks.append(
            f"<!-- vm:{e['id']} -->\n"
            f"🎙️ {e['transcript']}\n"
        )

    addition = "\n".join(blocks)
    if not addition.endswith("\n"):
        addition += "\n"

    if existing:
        sep = "" if existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
        final = existing + sep + addition
    else:
        final = addition

    if dry_run:
        print(f"[dry-run] would write {path} ({len(addition)} bytes appended)")
        print("---")
        print(addition)
        print("---")
        return path

    path.write_text(final)
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1] if __doc__ else "")
    ap.add_argument("--date", default=None,
                    help="Target date YYYY-MM-DD (local). Default: today.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show actions, don't rename or write journal.")
    ap.add_argument("--journal-dir", default=str(DEFAULT_JOURNAL_DIR),
                    help="Directory to write YYYY-MM-DD.md files into. "
                         "Overrides $VOICE_MEMO_JOURNAL_DIR. Default: ~/Journal.")
    ap.add_argument("--timezone", default=None,
                    help="IANA timezone for 'today' (e.g. America/Chicago). "
                         "Overrides $VOICE_MEMO_TZ. Default: system local.")
    args = ap.parse_args()

    tz = resolve_timezone(args.timezone)
    journal_dir = Path(args.journal_dir).expanduser()
    date_str = args.date or dt.datetime.now(tz).date().isoformat()

    try:
        target_date = dt.date.fromisoformat(date_str)
    except ValueError:
        print(f"error: invalid --date: {date_str}", file=sys.stderr)
        return 2

    if not HELPER.exists():
        print(f"error: helper not found at {HELPER}. "
              f"Place voice_memos.py next to this script.", file=sys.stderr)
        return 2

    memos = list_memos_for_date(target_date, tz)
    if not memos:
        print(f"No untitled voice memos for {target_date}.")
        return 0

    already = journaled_ids(journal_dir / f"{target_date.isoformat()}.md")

    print(f"Found {len(memos)} untitled memo(s) for {target_date}:")
    entries = []
    for m in memos:
        mid = m["id"]
        time_str = m["local_dt"].strftime("%H:%M")
        print(f"  • [{mid}] {m['title']} @ {time_str} ({m['duration_s']:.1f}s)")

        if mid in already:
            print(f"      skip: already journaled (vm:{mid} anchor present)")
            continue

        transcript = fetch_native_transcript(mid)
        source = "native"
        if not transcript:
            resolved = m.get("resolved_path")
            if resolved and Path(resolved).is_file():
                transcript = fetch_whisperkit_transcript(Path(resolved))
                source = "whisperkit"
            else:
                print(f"      skip: audio not yet downloaded from iCloud (resolved_path empty)")
                continue
        if not transcript:
            print(f"      skip: no native transcript and whisperkit-cli unavailable / failed")
            continue
        print(f"      transcript ready via {source} ({len(transcript)} chars)")

        new_title = derive_title(transcript)
        if not new_title:
            print(f"      skip: could not derive title from transcript")
            continue

        entry = {
            "id": mid,
            "title": new_title,
            "local_dt": m["local_dt"],
            "transcript": transcript,
        }
        entries.append(entry)

        if args.dry_run:
            print(f"      [dry-run] rename → \"{new_title}\"")
        else:
            ok, msg = rename_memo(mid, new_title)
            if ok:
                print(f"      renamed → \"{new_title}\"")
            else:
                print(f"      rename FAILED: {msg}")
                entries.pop()

    if not entries:
        print("Nothing to append.")
        return 0

    path = append_to_journal(target_date, entries, journal_dir, dry_run=args.dry_run)
    if not args.dry_run:
        print(f"Appended {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
