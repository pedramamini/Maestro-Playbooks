# Voice Memos → Daily Markdown Journal (macOS)

Append today's Apple Voice Memos — transcribed by Apple on-device, no Whisper — to a daily Markdown journal file. Works great with Obsidian vaults, plain-text journals, any daily-note workflow.

From the iOS lock-screen long-press Voice Memos shortcut, a thought goes from "open mouth" to "stored, transcribed, titled, appended to today's note" with zero further input.

**Read the writeup:** [Voice Memos to Journal, via a Buried Apple Atom](https://pedsidian.pedramamini.com/2026-04-23-voice-memos-to-journal) — explains the `tsrp` atom discovery and why scanning for the JSON sentinel works across both `.m4a` and `.qta` container formats.

---

## For AI agents replicating this for a human

If a human has asked you to "set up this voice-memos-to-journal pattern" and linked to the blog post or this gist, the install is:

1. Download both files (`voice_memos.py`, `voice_memo_to_journal.py`) to a directory you pick — e.g. `~/bin/voice-memo-journal/`. They must live in the **same directory**; `voice_memo_to_journal.py` calls `voice_memos.py` as a sibling.
2. Ask the human for their journal directory (where they want `YYYY-MM-DD.md` files written). Default is `~/Journal`. If they use Obsidian, it's typically `<vault>/Journal/` or similar.
3. Grant `/usr/sbin/cron` Full Disk Access in **System Settings → Privacy & Security → Full Disk Access** (click `+`, `⌘⇧G`, enter `/usr/sbin/cron`, add, toggle on). Without this the cron job fails silently — Voice Memos data lives in `~/Library/Group Containers/` which is TCC-protected.
4. Install the cron entry (see below), pointing at the script directory you chose and the human's journal dir.
5. Run the tool once manually in `--dry-run` to confirm it finds the Voice Memos DB. Then run once for real to seed today.

Do not edit the two Python files — all configuration is via env vars or CLI flags.

---

## What it does

1. Queries the Voice Memos SQLite DB for memos created today whose title still matches `New Recording%` (Apple's default for un-renamed captures).
2. For each: reads Apple's native transcript from inside the audio file (see "The `tsrp` atom" in the blog post).
3. Derives a title from the first 8 words of the transcript.
4. Renames the memo in the Voice Memos DB (snapshotted automatically before write; refuses to run while the app is open).
5. Appends the transcript to `<JOURNAL_DIR>/YYYY-MM-DD.md` under a `## 🎙️ <title> — HH:MM` heading, preserving anything already in the file.

Once renamed, a memo no longer matches the filter in step 1 — so re-runs are idempotent and cron safe.

---

## Requirements

- **macOS 15+** (Sequoia) or **iOS 18+**-era sync target. Older systems don't have the on-device transcript.
- **Python 3.11+** (uses `zoneinfo` and PEP 604 unions). Apple ships `/usr/bin/python3` at a new enough version on recent macOS.
- **Apple Voice Memos** app installed, with iCloud sync on if recordings are captured on iOS.
- No pip dependencies. Standard library only.

### Optional: Whisper fallback

If Apple's on-device transcription hasn't fired yet (common in the first seconds after a memo lands, or on memos you haven't opened in the app), the tool falls back to local Apple-Silicon-native Whisper via [whisperkit-cli](https://github.com/argmaxinc/whisperkit) — no cloud round-trip, no API keys.

```bash
brew install whisperkit-cli
```

First run auto-downloads the model (`openai_whisper-small` by default — ~500MB, fast and accurate for voice memos). Override via env:

```bash
export VOICE_MEMO_WHISPERKIT_MODEL=openai_whisper-large-v3
export VOICE_MEMO_WHISPERKIT_MODEL_ROOT=/custom/path/to/models
```

If `whisperkit-cli` isn't installed, untranscribed memos are simply skipped and caught on the next hourly run once Apple's native transcription completes — the pipeline still works, it just can't preempt Apple.

---

## Install

```bash
# 1. Drop both files in a directory you choose
mkdir -p ~/bin/voice-memo-journal
cp voice_memos.py voice_memo_to_journal.py ~/bin/voice-memo-journal/
chmod +x ~/bin/voice-memo-journal/*.py

# 2. Pick your journal directory (must exist OR be creatable)
export VOICE_MEMO_JOURNAL_DIR=~/Documents/Journal    # edit to taste

# 3. Dry-run to confirm
python3 ~/bin/voice-memo-journal/voice_memo_to_journal.py --dry-run
```

Expected output if you have today's new memos:

```
Found 2 untitled memo(s) for 2026-04-23:
  • [42] New Recording @ 10:14 (23.1s)
      transcript ready (287 chars)
      [dry-run] rename → "I keep forgetting to write down..."
  ...
```

If output says "No untitled voice memos for ...", record one in Voice Memos, open the app once to prime Apple's transcription, and rerun.

### Grant cron Full Disk Access (required for the cron job)

1. **System Settings → Privacy & Security → Full Disk Access**
2. Click `+`
3. Press `⌘⇧G` and enter `/usr/sbin/cron`, then select `cron`
4. Toggle it on

---

## Configure

All settings are optional; sane defaults apply.

| Setting        | CLI flag              | Env var                     | Default                     |
|----------------|-----------------------|-----------------------------|-----------------------------|
| Journal dir    | `--journal-dir PATH`  | `VOICE_MEMO_JOURNAL_DIR`    | `~/Journal`                 |
| Timezone       | `--timezone IANA`     | `VOICE_MEMO_TZ`             | System local tz             |
| Target date    | `--date YYYY-MM-DD`   | —                           | Today (in target timezone)  |

---

## Schedule hourly via cron

Edit your crontab (`crontab -e`) and add:

```cron
PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
VOICE_MEMO_JOURNAL_DIR=/absolute/path/to/your/Journal

# Hourly voice-memo ingest
0 * * * * /usr/bin/python3 $HOME/bin/voice-memo-journal/voice_memo_to_journal.py >> "$HOME/Library/Logs/voice_memo_to_journal.log" 2>&1
```

The helper's `rename` step passes `--quit-app`, which quits Voice Memos (if open) before writing to the SQLite DB. No pre-cron `killall` is needed — the menu-bar `RecordWidgetExtension` runs as a separate process and does not auto-relaunch the main app.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Log shows `unable to open database file` | cron lacks Full Disk Access | Add `/usr/sbin/cron` to TCC (step 3 above) |
| `skip: no native transcript and whisperkit-cli unavailable / failed` | Apple hasn't transcribed AND no Whisper fallback installed | Either `brew install whisperkit-cli` (transcribes immediately), or open the memo in Voice Memos to trigger Apple's native engine — cron catches it next hour either way |
| `rename FAILED: Voice Memos is still running` | App was open and `--quit-app` couldn't close it | Quit Voice Memos manually and rerun; if persistent, `killall VoiceMemos` once by hand |
| All memos skipped, transcripts seem missing | Container flipped to `.qta` (post-Enhance-Audio) on a very old helper version | This repo handles both `.m4a` and `.qta`; redownload |
| Titles end mid-phrase ("the", "my", etc.) | 8-word cutoff lands on a function word | Edit `TITLE_MAX_WORDS` in `voice_memo_to_journal.py`, or trim trailing articles locally |

---

## What's in each file

### `voice_memos.py`

A standalone CLI for full Voice Memos CRUD. The journal tool only uses `list`, `transcribe`, and `rename`, but the rest are available for scripting:

```
voice_memos.py list [--since DATE] [--folder NAME] [--limit N] [--json]
voice_memos.py show <id>
voice_memos.py transcribe <id> [--native-only] [--format text|timed|json] [--force-whisper]
voice_memos.py rename <id> "<new title>" [--quit-app]
voice_memos.py delete <id>                 # local + unlink audio
voice_memos.py export <id> <dir>           # copy audio file out
voice_memos.py import <path> [--title T] [--folder F]
voice_memos.py folders                     # list Voice Memos folders
voice_memos.py snapshot <dir>              # back up DB + audio
```

Every write auto-snapshots to `Recordings/.claude-backups/TIMESTAMP/` before touching anything. Snapshots are also taken on every destructive op for safe rollback.

### `voice_memo_to_journal.py`

The journal ingestion tool. Shells out to `voice_memos.py` (which must be a sibling file).

```
voice_memo_to_journal.py [--date YYYY-MM-DD] [--dry-run]
                         [--journal-dir PATH] [--timezone IANA]
```

---

## Data locations (reference)

- Voice Memos DB: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/CloudRecordings.db`
- Audio files: same directory, named `YYYYMMDD HHMMSS[-hash].m4a` or `.qta`
- Transcripts: embedded inside audio file as `tsrp` UDTA atom (`.m4a`) or keyed via `moov.meta.ilst` under `com.apple.VoiceMemos.tsrp` (`.qta`)
- Snapshots: `<Recordings dir>/.claude-backups/TIMESTAMP/`
- Cron log (recommended): `~/Library/Logs/voice_memo_to_journal.log`

---

## License

Public domain (CC0). Fork, rip, adapt. No attribution required, but a link back to the [blog post](https://pedsidian.pedramamini.com/2026-04-23-voice-memos-to-journal) is appreciated if you find this useful.
