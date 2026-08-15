# Voice Memo Journal Agent Prompt

**IMPORTANT: Configure the placeholders below before running this playbook.**

---

## Configuration

### Where the journal lives

<!-- CONFIGURE: The directory that will receive YYYY-MM-DD.md files. It will be
     created if it does not exist. Use an absolute path or a ~ path. -->
**JOURNAL_DIR:** `~/Journal`

<!-- Examples:
- ~/Documents/Journal
- ~/Obsidian/MyVault/Journal
- ~/Obsidian/MyVault/Claude/Journal
-->

<!-- CONFIGURE: IANA timezone used to decide which day a memo belongs to.
     Leave `system` to use the Mac's local timezone. -->
**JOURNAL_TZ:** `system`

<!-- Examples: America/Chicago, Europe/Berlin, Asia/Tokyo -->

### Behavior

<!-- CONFIGURE: Install the local Whisper fallback so a memo is transcribed
     immediately instead of waiting for Apple's async on-device pass.
     Adds a ~1GB brew install. `yes` | `no` -->
**INSTALL_WHISPER_FALLBACK:** `yes`

<!-- CONFIGURE: How often the ingest runs. -->
**SCHEDULE:** `hourly`

<!-- Valid values:
- hourly     0 * * * *     (recommended — smooths over Apple's async transcription)
- every-15   */15 * * * *
- daily      0 21 * * *    (9pm)
- none       install the scripts, skip scheduling entirely
-->

<!-- CONFIGURE: Where the two Python files get installed. -->
**INSTALL_DIR:** `~/bin/voice-memo-journal`

### Backfill

<!-- CONFIGURE: On first successful run, also ingest memos from the last N days.
     `0` means today only. Existing journal content is never overwritten —
     transcripts append. -->
**BACKFILL_DAYS:** `0`

---

## Agent Instructions

You are installing a macOS pipeline that reads Apple's **on-device** Voice Memos
transcripts and appends them to a daily markdown journal. Nothing leaves the
machine: no API keys, no cloud transcription, no network calls.

Two scripts do the work and both ship with this playbook in
`{{AUTORUN_FOLDER}}/assets`:

- `voice_memos.py` — a Voice Memos CLI. Reads the `tsrp` MP4 atom where Apple
  hides the transcript, handles both `.m4a` and `.qta` containers, and can
  rename memos in the Voice Memos database.
- `voice_memo_to_journal.py` — the hourly job. Finds today's untitled memos,
  pulls each transcript, derives a title from the first words, renames the memo,
  and appends the text to `JOURNAL_DIR/YYYY-MM-DD.md`.

**The one thing you cannot do for the user** is grant Full Disk Access. Voice
Memos data lives under `~/Library/Group Containers/`, which is TCC-protected.
`/usr/sbin/cron` needs FDA or the scheduled job fails silently with
`unable to open database file`. Detect that state in document 1, install into a
**safe, disarmed** state anyway, and hand the user a two-click leave-behind in
document 5. Never install an armed schedule you know will fail.

Configured values appear in the task documents as `[JOURNAL_DIR]`,
`[JOURNAL_TZ]`, `[INSTALL_WHISPER_FALLBACK]`, `[SCHEDULE]`, `[INSTALL_DIR]`,
and `[BACKFILL_DAYS]`. Read them from this prompt — do not guess.
