# Document 3: Install

## Context

- **Playbook**: Voice Memo Journal
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Execute the plan. Nothing here is a judgment call — every decision was made in
document 2 and written down. Run the commands, capture the output, log what
happened.

The one rule: **install to the state the plan says, not the state you wish for.**
If the plan says DISARMED, the crontab line goes in commented out. Do not
improve on the plan mid-run.

## Tasks

### Task 1: Read the plan

- [ ] **Read `{{AUTORUN_FOLDER}}/VOICE_INSTALL_PLAN.md`.** Execute it as written.
      If any of its resolved paths no longer exist, stop and say so rather than
      substituting a guess.

### Task 2: Place the scripts

- [ ] **Create the install directory and copy both scripts** from the playbook's
      bundled assets:

      ```bash
      mkdir -p "<INSTALL_DIR>"
      cp "{{AUTORUN_FOLDER}}/assets/voice_memos.py" "<INSTALL_DIR>/"
      cp "{{AUTORUN_FOLDER}}/assets/voice_memo_to_journal.py" "<INSTALL_DIR>/"
      chmod +x "<INSTALL_DIR>"/*.py
      ls -la "<INSTALL_DIR>"
      ```

      Both files must land in the **same directory** — `voice_memo_to_journal.py`
      imports `voice_memos.py` as a sibling.

      These are bundled with the playbook rather than fetched from the network,
      so the version you install is the version that was tested against these
      documents. If `{{AUTORUN_FOLDER}}/assets/` is missing, the playbook was
      installed through a channel that drops assets — say so plainly and point
      at the source gist
      (`https://gist.github.com/pedramamini/f4efacfe7080e07e18f54e13d8243dc1`)
      rather than failing silently.

- [ ] **Create the journal directory** if it does not exist:
      `mkdir -p "<JOURNAL_DIR>"`.

### Task 3: Install the Whisper fallback (optional)

- [ ] **Install `whisperkit-cli` if the plan calls for it**:

      ```bash
      brew install whisperkit-cli
      ```

      This downloads model weights and is the slowest step in the playbook.
      If it fails, record the failure and continue — the pipeline works without
      it, just with Apple's async transcription latency. A failed optional
      dependency does not fail the install.

### Task 4: Dry run

- [ ] **Run the ingest in dry-run mode and capture the full output**:

      ```bash
      /usr/bin/python3 "<INSTALL_DIR>/voice_memo_to_journal.py" \
        --dry-run --journal-dir "<JOURNAL_DIR>" 2>&1 | tee "{{AUTORUN_FOLDER}}/voice-dryrun.out"
      ```

      Add `--timezone <tz>` if `[JOURNAL_TZ]` is not `system`.

      Read the output and classify it:

      | Output | Means |
      |---|---|
      | Lists memos it would process | Working. Proceed. |
      | `unable to open database file` | TCC denial reached this process after all — record it, and force the arming state to DISARMED regardless of what the plan said. |
      | `no memos found` / empty | Working, but there is nothing to ingest right now. Not a failure. |
      | `skip: no native transcript and whisperkit-cli unavailable` | Working. Apple has not transcribed yet; a later run picks it up. |

      A dry run that produces no output at all is a failure, not a success —
      say so.

### Task 5: Install the schedule

- [ ] **Back up the existing crontab first**:

      ```bash
      crontab -l > "{{AUTORUN_FOLDER}}/crontab.backup" 2>/dev/null || echo "# no prior crontab" > "{{AUTORUN_FOLDER}}/crontab.backup"
      ```

- [ ] **Merge in the schedule block** exactly as the plan specifies. Read the
      current crontab, remove any prior `voice_memo_to_journal` lines and their
      associated `VOICE_MEMO_*` env lines, append the new block, and write the
      whole thing back with `crontab -`. Never `crontab <file>` over the top of
      an unread crontab — that silently deletes the user's other jobs.

      **If the plan says ARMED**, write the block live.

      **If the plan says DISARMED**, write the block with every line prefixed
      `# ` and add this comment directly above it:

      ```cron
      # DISARMED by the Voice Memo Journal playbook: /usr/sbin/cron does not have
      # Full Disk Access, so this job would fail silently every hour.
      # Grant it (System Settings > Privacy & Security > Full Disk Access > + >
      # Cmd-Shift-G > /usr/sbin/cron), then uncomment the three lines below.
      ```

      **If the plan says NO SCHEDULE**, skip this task entirely and record why.

- [ ] **Confirm what actually landed**: `crontab -l | grep -n -A3 voice_memo`.
      Record the literal lines. Do not assume the write succeeded.

### Task 6: Backfill (optional)

- [ ] **Run the backfill if `[BACKFILL_DAYS]` is greater than 0** and the dry run
      was healthy. Iterate the last N days, one `--date YYYY-MM-DD` invocation
      each, live (no `--dry-run`). Record how many entries were written per day.

      If `[BACKFILL_DAYS]` is `0`, skip this and say so in one clause.

### Task 7: Write the install log

- [ ] **Write `{{AUTORUN_FOLDER}}/VOICE_INSTALL_LOG.md`**: every command run in
      order, its exit status, the dry-run classification, the final arming state
      (which may differ from the plan if Task 4 forced a downgrade), the exact
      crontab lines written, backfill results, and anything that failed with its
      error text verbatim.
