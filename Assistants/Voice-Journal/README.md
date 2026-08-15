# Voice Memo Journal Playbook

Installs a macOS pipeline that turns a long-press on your lock screen into a
dated journal entry.

Long-press Voice Memos. Talk. Stop. iCloud syncs the recording to your Mac, and
a scheduled job reads the transcript **Apple already generated on-device**,
titles the memo from its first words, and appends the text to
`Journal/YYYY-MM-DD.md`.

No API keys. No cloud transcription. No network calls. Apple did the
transcription work already — it just filed the output inside the audio file, in
a custom MP4 atom called `tsrp`.

## Overview

| | |
|---|---|
| **Category** | Assistants |
| **Platform** | macOS 15 (Sequoia) or newer |
| **Loops** | No — a five-document setup run |
| **Needs** | Python 3.11+, Voice Memos, **Full Disk Access** (see below) |
| **Writes** | `INSTALL_DIR`, `JOURNAL_DIR`, your crontab (backed up first) |
| **Bundled** | `assets/voice_memos.py`, `assets/voice_memo_to_journal.py` |

## The permission problem, and how this handles it

Voice Memos data lives under `~/Library/Group Containers/`, which macOS protects
with TCC. **No script can grant itself access.** There are two separate grants
and they are easy to conflate:

| Grant | Needed for | Can the agent check it? |
|---|---|---|
| Maestro / terminal | the install, the dry run, and every verify | Yes — by attempting the read |
| `/usr/sbin/cron` | the hourly scheduled job | No — TCC has no query API |

So the playbook does this instead of guessing:

1. **Document 1 attempts the privileged read and catches the failure.** The
   verdict is evidence, not an assumption.
2. **Document 2 decides the arming state in writing.** Cron grant unconfirmed
   means the schedule gets installed **commented out**.
3. **Document 3 installs to that state exactly** — it never arms a job it knows
   will fail silently every hour.
4. **Document 4 is re-runnable standalone.** Grant the permission, re-run one
   document, get a real verdict.
5. **Document 5 opens the settings pane** with an `x-apple.systempreferences:`
   deep link and reduces the remaining work to two clicks and one uncomment.

An armed cron job without cron's FDA grant is worse than no job: it runs every
hour, fails into a log nobody reads, and looks installed. Disarmed-but-honest
beats armed-but-broken.

## Document chain

| # | Document | Does |
|---|----------|------|
| 1 | `1_DETECT` | Platform, Python, **the read probe**, whisperkit, existing install |
| 2 | `2_PLAN` | The arming decision, every literal command with paths resolved |
| 3 | `3_INSTALL` | Copies scripts, dry-runs, merges the crontab (backup first) |
| 4 | `4_VERIFY` | Re-runnable. Probes the **journal file**, not the log |
| 5 | `5_SUMMARY` | Handoff, deep link to the FDA pane, two-click leave-behind |

## Configuration

| Variable | Default | What it does |
|---|---|---|
| `JOURNAL_DIR` | `~/Journal` | Destination for `YYYY-MM-DD.md` |
| `JOURNAL_TZ` | `system` | IANA timezone deciding which day a memo belongs to |
| `INSTALL_WHISPER_FALLBACK` | `yes` | Local Whisper so a memo transcribes immediately |
| `SCHEDULE` | `hourly` | `hourly` / `every-15` / `daily` / `none` |
| `INSTALL_DIR` | `~/bin/voice-memo-journal` | Where the two scripts go |
| `BACKFILL_DAYS` | `0` | Also ingest the last N days on install |

`hourly` is the right default. Apple's on-device transcription is asynchronous —
it usually fires seconds after a save but sometimes waits until you open the
memo. An hourly cadence smooths that over; anything a memo misses is caught on
the next pass.

## Why probe the product, not the process

`4_VERIFY` deliberately checks the **journal file**, not
`voice_memo_to_journal.log`.

The log is appended to on every run *including total failure*. A log-freshness
check reports green while the pipeline does nothing, indefinitely. The journal
file with a transcript in it could not exist unless the work happened. That is
the only honest signal available, and it is the difference between a verified
install and a confident nothing.

## Bundled assets

Both Python files ship in `assets/` rather than being fetched at install time,
so the version installed is the version these documents were written against.

> **Exchange only.** The `assets/` folder travels with Playbook Exchange
> installs. Maestro's peer-to-peer share flow transports markdown only and drops
> `assets/`. If you received this playbook by share, install it from the Exchange
> instead, or pull the scripts from the source gist:
> <https://gist.github.com/pedramamini/f4efacfe7080e07e18f54e13d8243dc1>

`assets/GIST_README.md` is the upstream documentation, kept alongside the code as
the reference for flags and data locations.

## Safety

- Your crontab is read, merged, and written back — never overwritten blind.
  The original is saved to `{{AUTORUN_FOLDER}}/crontab.backup`.
- Only `voice_memo_to_journal` lines are touched. Your other cron jobs survive.
- The ingest is idempotent: a memo is renamed once processed, so it no longer
  matches the `New Recording%` filter on the next pass.
- Journal entries **append**. Existing content in `YYYY-MM-DD.md` is preserved.
- Everything runs locally. No API keys are requested, stored, or needed.

## Origin

Derived from [Voice Memos to Journal, via a Buried Apple Atom](https://pedsidian.pedramamini.com/Claude/Blog/2026-04-23-voice-memos-to-journal).
Scripts by Pedram Amini, released public domain.
