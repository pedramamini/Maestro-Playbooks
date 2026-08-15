# Document 2: Plan the Install

## Context

- **Playbook**: Voice Memo Journal
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Turn the detection report into an explicit, written plan — including the
**arming decision**, which is the one choice in this playbook with a real
consequence.

An armed schedule on a machine without cron's Full Disk Access is worse than no
schedule: it runs every hour, fails silently, and looks installed. Deciding that
here, in writing, means document 3 never has to improvise.

## Tasks

### Task 1: Read detection

- [ ] **Read `{{AUTORUN_FOLDER}}/VOICE_DETECT.md`.** Take the DETECT SUMMARY
      verdict as authoritative.

### Task 2: Stop if blocked

- [ ] **Halt on `BLOCKED`**: If the summary is `BLOCKED`, the agent's own read
      of the Voice Memos store failed, which means nothing can be installed and
      nothing could be verified even if it were.

      Write a **halt marker** into this document, directly below this
      task: an HTML comment whose entire body is

      ```text
      maestro:halt: Full Disk Access denied for this agent. Grant it, then re-run.
      ```

      The marker is described rather than shown, because a literal one sitting
      in this file would halt the playbook the moment the document is read.

      Leave this task unchecked. Then make your final message the grant
      instructions and nothing else:

      > **Nothing was installed.** This agent cannot read the Voice Memos store.
      >
      > Grant Full Disk Access to **Maestro** (and to your terminal, if you plan
      > to test by hand):
      >
      > 1. Open **System Settings → Privacy & Security → Full Disk Access**
      > 2. Click **+**, add **Maestro**, toggle it on
      > 3. Quit and reopen Maestro — the grant only takes effect on relaunch
      >
      > Then delete the `maestro:halt` marker from `2_PLAN.md` and run this
      > playbook again.

      Open that settings pane for them rather than describing where it is:

      ```bash
      open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
      ```

      Do not proceed to document 3.

### Task 3: Decide the arming state

- [ ] **Choose armed or disarmed, and write down why**:

      | DETECT SUMMARY | `[SCHEDULE]` | Decision |
      |---|---|---|
      | `READY` | not `none` | **ARMED** — crontab entry installed live |
      | `READY-DISARMED` | not `none` | **DISARMED** — crontab entry installed **commented out** |
      | any | `none` | **NO SCHEDULE** — scripts only, user runs by hand |

      Disarmed is the default and it is not a failure mode. The scripts are
      installed, the dry-run works, and arming is one uncomment away once the
      user has granted cron its own FDA entry. That is a better place to leave
      someone than an hourly job that fails into a log nobody reads.

### Task 4: Resolve the concrete commands

- [ ] **Write out the literal commands document 3 will run**, with every path
      already expanded — no `~`, no variables to resolve later:

      - the `mkdir -p` for `[INSTALL_DIR]` and `[JOURNAL_DIR]`
      - the two `cp` commands from `{{AUTORUN_FOLDER}}/assets/`
      - the `brew install whisperkit-cli` line, if the fallback survived detection
      - the dry-run: `<python> <INSTALL_DIR>/voice_memo_to_journal.py --dry-run --journal-dir <JOURNAL_DIR>`
      - the crontab line, in full, matching `[SCHEDULE]`:

        | `[SCHEDULE]` | cron expression |
        |---|---|
        | `hourly` | `0 * * * *` |
        | `every-15` | `*/15 * * * *` |
        | `daily` | `0 21 * * *` |

        ```cron
        PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
        VOICE_MEMO_JOURNAL_DIR=<absolute JOURNAL_DIR>
        <expr> /usr/bin/python3 <INSTALL_DIR>/voice_memo_to_journal.py >> "$HOME/Library/Logs/voice_memo_to_journal.log" 2>&1
        ```

        Use the **absolute** interpreter path. cron's `PATH` is minimal and a
        bare `python3` is a coin flip.

        If `[JOURNAL_TZ]` is not `system`, add `VOICE_MEMO_TZ=<tz>` as a third
        environment line.

- [ ] **Plan the crontab edit as a merge, not a replacement**: the user may have
      other cron jobs. Document 3 must read the existing crontab, append or
      replace only the `voice_memo_to_journal` lines, and write the whole thing
      back. Note the backup path it will save the original to:
      `{{AUTORUN_FOLDER}}/crontab.backup`.

### Task 5: Write the plan

- [ ] **Write `{{AUTORUN_FOLDER}}/VOICE_INSTALL_PLAN.md`** containing the arming
      decision with its reason, every resolved path, every literal command in
      execution order, the exact crontab block, and what the user will still owe
      at the end (the cron FDA grant, if disarmed).
