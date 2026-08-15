# Document 4: Verify

## Context

- **Playbook**: Voice Memo Journal
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Prove the install works with evidence that could not exist unless it works.

**This document is deliberately re-runnable on its own.** After the user grants
cron its Full Disk Access, they should be able to re-run this one document and
get a real verdict — not re-run the whole playbook.

The standard here is the same one that separates a five-week silent failure from
a working system: **probe the product, never the process.** A log file proves a
script ran. A journal file with a transcript in it proves the script worked.

## Tasks

### Task 1: Read the install log

- [ ] **Read `{{AUTORUN_FOLDER}}/VOICE_INSTALL_LOG.md` and
      `{{AUTORUN_FOLDER}}/VOICE_DETECT.md`.** Note the final arming state and the
      resolved paths. If the log does not exist, this document is being run
      standalone — recover the paths from `VOICE_INSTALL_PLAN.md`, or from the
      crontab entry itself.

### Task 2: Verify the scripts are in place

- [ ] **Check both files exist and import cleanly**:

      ```bash
      ls -la "<INSTALL_DIR>"
      /usr/bin/python3 -c "import sys; sys.path.insert(0, '<INSTALL_DIR>'); import voice_memos; print('import OK')"
      ```

      An import failure here usually means the two files did not land in the
      same directory.

### Task 3: Verify the privileged read still works

- [ ] **Re-run the read probe** from document 1, Task 3. This is the check that
      changes state after a user grants permission, so it is the reason this
      document is re-runnable:

      ```bash
      /usr/bin/python3 -c "
      import sqlite3, pathlib
      db = pathlib.Path.home()/'Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/CloudRecordings.db'
      try:
          con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
          print('READ: OK —', con.execute('select count(*) from ZCLOUDRECORDING').fetchone()[0], 'recordings')
      except Exception as e:
          print('READ: FAILED —', e)
      "
      ```

### Task 4: Verify the product, not the process

- [ ] **Look for real output**: list `[JOURNAL_DIR]` and check for
      `YYYY-MM-DD.md` files. For today's file (or the most recent), read it and
      confirm it contains actual transcript text, not just a heading.

      ```bash
      ls -lat "<JOURNAL_DIR>" | head -5
      ```

      Record the newest file, its size, and its modification time.

      **Do not accept a log line as evidence.** `voice_memo_to_journal.log` is
      appended to on every run including total failure, so its freshness proves
      only that cron fired. The journal file with a transcript in it is the only
      honest signal that the pipeline did its job.

      If there are no memos to ingest yet, this check cannot pass and that is not
      a failure — record it as `NO-DATA-YET` and say what the user should do to
      generate evidence (record a ten-second memo, wait for the next tick).

### Task 5: Verify the schedule

- [ ] **Confirm the crontab state matches the intended arming state**:

      ```bash
      crontab -l 2>/dev/null | grep -n -B2 -A2 voice_memo || echo "NO CRONTAB ENTRY"
      ```

      Check whether the lines are live or commented, and confirm that matches the
      install log. A live line where the log says DISARMED (or the reverse) is a
      real discrepancy — report it rather than reconciling it silently.

- [ ] **Check the cron log if the job has had time to fire**:

      ```bash
      tail -20 "$HOME/Library/Logs/voice_memo_to_journal.log" 2>/dev/null || echo "no log yet"
      ```

      An `unable to open database file` in this log is the definitive proof that
      `/usr/sbin/cron` lacks Full Disk Access, regardless of what the agent's own
      probe returned. This is the strongest signal available for `TCC_CRON` and it
      upgrades that verdict from `UNKNOWN` to `DENIED`.

### Task 6: Write the verdict

- [ ] **Write `{{AUTORUN_FOLDER}}/VOICE_VERIFY.md`** with each check, its
      evidence, and one of these verdicts:

      | Verdict | Meaning |
      |---|---|
      | `ACTIVE` | Scripts installed, read works, schedule live, journal file has real content |
      | `ACTIVE-NO-DATA` | Everything installed and armed; no memos have been recorded yet to prove it end to end |
      | `DISARMED` | Scripts installed and dry-run works; schedule is commented out pending cron's FDA grant |
      | `PARTIAL` | Scripts installed, but something concrete failed — name it |
      | `FAILED` | The install did not produce a working dry run |

      For any verdict other than `ACTIVE`, state the single next action that
      would change it. Not a list of possibilities — the one action.
