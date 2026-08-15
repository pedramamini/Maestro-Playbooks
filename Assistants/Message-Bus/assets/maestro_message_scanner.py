#!/usr/bin/env python3
"""
maestro_message_scanner.py, the cheap gatekeeper for the "@maestro" message bus.

Runs every 3 min as a Maestro Cue command node (https://www.runmaestro.ai). Scans
iMessage for new messages containing the marker "@maestro" that the owner authored
himself, and dispatches each one to a handler agent via `maestro-cli send`. If nothing
new is found it exits silently, so no agent (and no tokens) are spent unless there is
real work.

Detection is a direct read-only SQLite scan: on modern macOS the chat.db `text`
column is NULL for outbound messages (content lives in the `attributedBody` blob),
and most tooling only matches `text`, so it CANNOT see the messages we care about
(your own outbound commands). The marker is plain ASCII, so it appears verbatim in
the attributedBody bytes, we byte-match there. Command text + thread context are
then decoded via `imsg history`, which does decode attributedBody.

`imsg` is the terminal iMessage CLI this relies on: https://github.com/openclaw/imsg
(install: `brew install steipete/tap/imsg`). It needs Full Disk Access to read chat.db.

Dedup: a rowid high-water mark in state/message_bus_watermark.json. Only messages
with id > watermark qualify; the watermark is seeded to the current max rowid on
first run so historical mentions never backfire.

Safety: default (no flag) prints what it WOULD dispatch and does NOT send or advance
the watermark. Pass --live to actually dispatch. Dispatch also requires
HANDLER_AGENT_ID to be set (empty => dry-run only).
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# ----------------------------------------------------------------------------- config
MARKER = "@maestro"            # this marker, authored by you, triggers the bus
REPLY_PREFIX = "🎶 Maestro: "  # bot replies carry this; contains no marker, so it never re-triggers

# Handler agent that fulfills commands (its Maestro agent id). Empty => dispatch
# disabled (dry-run only). Set MAESTRO_HANDLER_AGENT_ID to YOUR agent's id.
HANDLER_AGENT_ID = os.environ.get("MAESTRO_HANDLER_AGENT_ID", "")

# Sender scope. None => only your own outbound messages (is_from_me) trigger.
# To open access to others later, set to a list of handles, e.g. ["+15125551212", "a@b.com"].
ALLOWED_SENDERS: list[str] | None = None

CONTEXT_LIMIT = 50  # recent messages handed to the handler for context (resolves follow-ups)

# Point these at your own vault / working dir. Paths here are illustrative.
VAULT = Path(os.environ.get("VAULT_DIR", str(Path.home() / "Obsidian" / "YourVault")))
STATE_DIR = VAULT / "automation/state"
STATE_FILE = STATE_DIR / "message_bus_watermark.json"
DISPATCH_LOG = STATE_DIR / "message_bus_dispatch.log"
LOCK_FILE = STATE_DIR / "scanner.lock"
SPEC_DOC = "automation/Maestro-Message-Channel.md"  # behavior + voice spec the handler reads

CHAT_DB = Path.home() / "Library/Messages/chat.db"
MAESTRO_CLI = os.environ.get(
    "MAESTRO_CLI_PATH", "/Applications/Maestro.app/Contents/Resources/maestro-cli.js"
)
NODE_BIN = os.environ.get("NODE_BIN", "/opt/homebrew/bin/node")  # absolute: cron PATH may lack node
DISPATCH_TIMEOUT = 600  # seconds to wait for one handler run before giving up
MAX_DRAIN = 50          # safety cap on commands processed in one drain pass


# ----------------------------------------------------------------------------- helpers
def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    line = f"{ts} {msg}"
    print(line, file=sys.stderr)
    try:
        DISPATCH_LOG.parent.mkdir(parents=True, exist_ok=True)
        with DISPATCH_LOG.open("a") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def run(cmd: list[str], timeout: int = 60) -> str:
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if res.returncode != 0:
        raise RuntimeError(f"cmd failed ({res.returncode}): {' '.join(cmd)}\n{res.stderr.strip()}")
    return res.stdout


def parse_jsonl(blob: str) -> list[dict]:
    """imsg emits either JSONL (one object per line) or a JSON array."""
    blob = blob.strip()
    if not blob:
        return []
    if blob.startswith("["):
        try:
            return json.loads(blob)
        except json.JSONDecodeError:
            pass
    out = []
    for line in blob.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def current_max_rowid() -> int:
    out = run(["sqlite3", "-readonly", str(CHAT_DB), "SELECT IFNULL(MAX(ROWID),0) FROM message;"])
    return int(out.strip() or "0")


def load_watermark() -> int | None:
    if not STATE_FILE.exists():
        return None
    try:
        return int(json.loads(STATE_FILE.read_text())["watermark"])
    except (OSError, KeyError, ValueError, json.JSONDecodeError):
        return None


def save_watermark(value: int) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {"watermark": value, "updated_at": datetime.now(timezone.utc).isoformat()}
    fd, tmp = tempfile.mkstemp(dir=str(STATE_FILE.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(payload, fh)
        os.replace(tmp, STATE_FILE)  # atomic
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def find_candidates(watermark: int) -> list[dict]:
    """Direct read-only chat.db scan for outbound, marker-bearing, non-reaction messages.

    Returns dicts {id, chat_id} sorted ascending by id. Marker is byte-matched against
    the attributedBody blob (and text, for completeness). Reactions/tapbacks
    (associated_message_type != 0) and non-text items (item_type != 0) are excluded.
    """
    where_self = "m.is_from_me = 1" if ALLOWED_SENDERS is None else "1=1"
    # mode=ro only (NOT immutable=1): chat.db is live and WAL-backed, so immutable
    # ignores the -wal log and goes blind to just-arrived messages. This bus would
    # miss fresh @maestro commands until they were checkpointed. Read with the WAL.
    con = sqlite3.connect(f"file:{CHAT_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(f"""
            SELECT m.ROWID AS id, m.is_from_me, m.text, m.attributedBody,
                   c.ROWID AS chat_id
            FROM message m
            JOIN chat_message_join cmj ON cmj.message_id = m.ROWID
            JOIN chat c ON c.ROWID = cmj.chat_id
            WHERE m.ROWID > ?
              AND {where_self}
              AND m.associated_message_type = 0
              AND m.item_type = 0
            ORDER BY m.ROWID ASC
        """, (watermark,)).fetchall()
    finally:
        con.close()

    marker_b = MARKER.encode()
    marker_lower = MARKER.lower()
    out = []
    for r in rows:
        body = r["attributedBody"] or b""
        text = r["text"] or ""
        if marker_b not in body and marker_lower not in text.lower():
            continue
        if text.startswith(REPLY_PREFIX):  # never act on our own replies
            continue
        out.append({"id": r["id"], "chat_id": r["chat_id"]})
    return out


def chat_history(chat_id: int, limit: int = CONTEXT_LIMIT) -> list[dict]:
    """Decoded recent messages for a chat (imsg decodes attributedBody)."""
    try:
        blob = run(["imsg", "history", "--chat-id", str(chat_id),
                    "--limit", str(limit), "--json"])
    except (RuntimeError, subprocess.SubprocessError):
        return []
    return parse_jsonl(blob)


def format_context(rows: list[dict]) -> str:
    lines = []
    for r in rows:
        who = "me" if r.get("is_from_me") else (r.get("sender_name") or r.get("sender") or "them")
        lines.append(f"[{r.get('created_at','?')}] {who}: {r.get('text','')}")
    return "\n".join(lines) if lines else "(no recent context)"


def command_text(rows: list[dict], msg_id: int) -> str:
    for r in rows:
        if r.get("id") == msg_id:
            return r.get("text") or ""
    return ""


def strip_marker(text: str) -> str:
    low = text.lower()
    idx = low.find(MARKER.lower())
    if idx < 0:
        return text.strip(" :,-")
    return text[idx + len(MARKER):].strip(" :,-")


def build_payload(chat_id: int, raw_text: str, chat_name: str, context: str) -> str:
    return f"""[MAESTRO MESSAGE BUS]
You are the agent running under a Maestro Cue pipeline (https://www.runmaestro.ai), handling a
command ("{MARKER}") the owner dropped into an iMessage thread.
FIRST read the behavior spec: {SPEC_DOC} (voice, reply mechanics, logging format).

Source thread: chat_id={chat_id} | name={json.dumps(chat_name)}
Triggering message: {json.dumps(raw_text)}
Command (marker stripped): {json.dumps(strip_marker(raw_text))}

Recent thread context (oldest first):
{context}

You have the full toolset your agent is configured with (your cwd loads the project CLAUDE.md).
Before deciding you can't do something, consult your tool index. Typical capabilities: contacts +
iMessage/SMS, calendar/email/docs, web + browser automation, semantic search, content ingestion.

IDENTITY: If the command asks who or what you are, say you are the agent running under a
Maestro Cue pipeline (https://www.runmaestro.ai).

Do the work with whatever tools you need. Then send EXACTLY ONE concise reply in the owner's
texting voice, prefixed "{REPLY_PREFIX}", to chat-id {chat_id}:
  imsg send --chat-id {chat_id} --text "..."
You MUST reply on success AND on failure. Keep it to 1-2 sentences, SMS-length. Never include
the trigger marker ("{MARKER}") in your reply, or it would re-trigger the scanner.

AUDIT LOG: automation/Maestro-Message-Log.md, your durable memory across runs. READ it for
prior-task context (you have no memory of previous runs), and ALWAYS append one row after acting:
date | thread (chat-id + name) | general task | outcome | reply sent."""


def payload_for(msg: dict) -> tuple[int, str, str, str]:
    """Build the dispatch payload for one candidate. Returns (chat_id, chat_name, raw_text, payload).

    History is fetched FRESH per command, on purpose: do NOT reuse a cross-command
    snapshot. During a multi-minute drain a newer command can land in the same thread,
    and a snapshot taken before that command existed resolves its text to "" — which
    dispatches a BLANK command. If the target message has aged out of the recent window
    (busy thread or backlog delay), widen the fetch once to recover its text.
    """
    chat_id = msg["chat_id"]
    rows = chat_history(chat_id, CONTEXT_LIMIT)
    raw_text = command_text(rows, msg["id"])
    if not raw_text:  # target not in the recent window — widen the lookup once
        raw_text = command_text(chat_history(chat_id, CONTEXT_LIMIT * 6), msg["id"])
    chat_name = next((r.get("chat_name") for r in rows if r.get("chat_name")), "")
    return chat_id, chat_name, raw_text, build_payload(chat_id, raw_text, chat_name, format_context(rows))


def dispatch(payload: str) -> bool:
    """Run ONE handler turn synchronously and wait for it. Serialized by drain() so the single
    handler agent is never hit concurrently, concurrent `send`s get dropped, which silently
    lost commands when an initial backlog fired all at once."""
    cmd = [NODE_BIN, MAESTRO_CLI, "send", HANDLER_AGENT_ID, payload]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=DISPATCH_TIMEOUT)
    except subprocess.TimeoutExpired:
        log("dispatch TIMEOUT")
        return False
    if res.returncode != 0:
        log(f"dispatch nonzero ({res.returncode}): {res.stderr.strip()[:200]}")
        return False
    return True


def drain() -> int:
    """Process the backlog ONE command at a time, oldest first, waiting for each handler run to
    finish before the next. Holds an exclusive lock so overlapping cron ticks can't start two
    drains (the burst-concurrency bug). Crash-safe: the watermark advances per completed command,
    so a failure simply retries on the next tick."""
    if not HANDLER_AGENT_ID:
        log("ERROR: drain with empty HANDLER_AGENT_ID")
        return 1
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    lock_fh = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        log("drain already running; skipping")
        return 0
    try:
        processed = 0
        while processed < MAX_DRAIN:
            wm = load_watermark() or 0
            candidates = find_candidates(wm)
            if not candidates:
                break
            msg = candidates[0]  # oldest first
            chat_id, chat_name, raw_text, payload = payload_for(msg)
            if not raw_text.strip():
                # Could not resolve the command text even after widening. Never dispatch a
                # blank command: the handler can't act on it and may misfire. Advance past
                # it so an unresolvable message can't wedge the queue, but log loudly so it
                # is never silently lost.
                log(f"UNRESOLVED command id={msg['id']} chat_id={chat_id} ({chat_name!r}): "
                    f"empty text after widen; advancing watermark to avoid wedge, NOT dispatched")
                save_watermark(msg["id"])
                continue
            if not dispatch(payload):
                log(f"dispatch FAILED id={msg['id']} chat_id={chat_id}; stopping, will retry next tick")
                break
            save_watermark(msg["id"])
            processed += 1
            log(f"handled id={msg['id']} chat_id={chat_id} ({chat_name!r}); watermark -> {msg['id']}")
        if processed:
            log(f"drain done, {processed} command(s) handled")
        return 0
    finally:
        fcntl.flock(lock_fh, fcntl.LOCK_UN)
        lock_fh.close()


# ----------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="Scan iMessage for @maestro commands.")
    ap.add_argument("--live", action="store_true",
                    help="Cron mode: if commands exist, spawn a detached serial drainer.")
    ap.add_argument("--drain", action="store_true",
                    help="Process the backlog one-at-a-time under a lock (spawned by --live).")
    ap.add_argument("--reseed", action="store_true",
                    help="Reset watermark to the current max rowid and exit.")
    args = ap.parse_args()

    if args.reseed:
        mx = current_max_rowid()
        save_watermark(mx)
        log(f"reseeded watermark to {mx}")
        return 0

    watermark = load_watermark()
    if watermark is None:
        mx = current_max_rowid()
        save_watermark(mx)
        log(f"first run: seeded watermark to {mx}, nothing processed")
        return 0

    if args.drain:
        return drain()

    candidates = find_candidates(watermark)
    if not candidates:
        log(f"no new @maestro commands (watermark={watermark})")
        return 0

    if args.live:
        # Don't process inline: that would block this agent session and fire concurrent
        # sends at the handler. Hand off to a detached, lock-guarded serial drainer.
        log(f"found {len(candidates)} command(s); spawning detached serial drainer")
        subprocess.Popen(
            [sys.executable, os.path.abspath(__file__), "--drain"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True,
        )
        return 0

    # dry-run: show what would be dispatched, change nothing
    log(f"found {len(candidates)} command(s) above watermark {watermark} [DRY-RUN]")
    for msg in candidates:
        chat_id, chat_name, raw_text, payload = payload_for(msg)
        print("\n" + "=" * 70)
        print(f"WOULD DISPATCH id={msg['id']} chat_id={chat_id} chat={chat_name!r}"
              + ("  [!! UNRESOLVED EMPTY TEXT — would be skipped, not dispatched]" if not raw_text.strip() else ""))
        print("-" * 70)
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
