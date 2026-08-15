# Document 1: Detect Environment and Probe Permissions

## Context

- **Playbook**: Voice Memo Journal
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Establish, before anything is installed, whether this machine can actually run
the pipeline — and specifically whether the **privileged read succeeds right
now**.

The permission question is the one that matters. Voice Memos data lives under
`~/Library/Group Containers/`, which macOS protects with TCC. No script can
grant itself access. So rather than assume, this document **attempts the read
and catches the failure**, and every downstream document behaves differently
depending on the answer.

Detect early, act late. The user does not find out about a missing permission
at the end of a run that has already installed a broken cron job.

## Tasks

### Task 1: Read the configuration

- [ ] **Read the agent prompt** and record `[JOURNAL_DIR]`, `[JOURNAL_TZ]`,
      `[INSTALL_WHISPER_FALLBACK]`, `[SCHEDULE]`, `[INSTALL_DIR]`, and
      `[BACKFILL_DAYS]`. Expand `~` to the real home directory and record the
      absolute paths.

### Task 2: Confirm the platform

- [ ] **Check macOS and Python**:

      ```bash
      sw_vers
      /usr/bin/python3 --version
      command -v python3 && python3 --version
      ls -d /System/Applications/VoiceMemos.app 2>/dev/null || echo "VoiceMemos.app: MISSING"
      ```

      Requirements: **macOS 15 (Sequoia) or newer** for on-device transcription,
      and **Python 3.11+** for `zoneinfo` and PEP 604 unions. Apple's
      `/usr/bin/python3` is new enough on recent macOS — prefer it for the cron
      entry, since a Homebrew Python can disappear out from under a scheduled job.

      If macOS is older than 15, or Python is older than 3.11, or Voice Memos is
      not installed, do this:

      Write a **halt marker** into this document, directly below this
      task: an HTML comment whose entire body is

      ```text
      maestro:halt: Platform requirement not met. See the run log.
      ```

      The marker is described rather than shown, because a literal one sitting
      in this file would halt the playbook the moment the document is read.

      Leave this task unchecked and state plainly which requirement failed and
      what version was found. Do not install anything.

### Task 3: Probe the privileged read — this is the important one

- [ ] **Attempt to read the Voice Memos store, and catch the failure**:

      ```bash
      RECDIR="$HOME/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
      ls -d "$RECDIR" 2>&1 | head -3
      ls "$RECDIR" 2>&1 | head -5
      /usr/bin/python3 -c "
      import sqlite3, pathlib, sys
      db = pathlib.Path.home()/'Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/CloudRecordings.db'
      try:
          con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
          n = con.execute('select count(*) from ZCLOUDRECORDING').fetchone()[0]
          print(f'TCC_AGENT: GRANTED ({n} recordings visible)')
      except Exception as e:
          print(f'TCC_AGENT: DENIED ({type(e).__name__}: {e})')
      "
      ```

      Record the result as **`TCC_AGENT: GRANTED`** or **`TCC_AGENT: DENIED`**.

      An `unable to open database file` or `operation not permitted` error is
      the TCC denial, not a missing file. Do not conclude that Voice Memos is
      uninstalled because the read failed — those are different problems with
      different fixes.

      Note which process needs the grant: this probe runs as the agent's shell,
      so a `GRANTED` here means **Maestro** (or the terminal hosting it) has FDA.
      That is necessary for the install and the verify step, but it is **not**
      the same grant the scheduled job needs — see the next task.

### Task 4: Probe cron's separate grant

- [ ] **Check whether `/usr/sbin/cron` is itself in the FDA list**: There is no
      API to query TCC directly, so record this as **`TCC_CRON: UNKNOWN`** unless
      you have positive evidence. Positive evidence is one of:

      - a working crontab entry on this machine that already reads protected
        paths, or
      - the user tells you it is granted.

      Report `UNKNOWN` honestly. Do not report it as granted because the agent's
      own read worked — they are two separate TCC entries, and conflating them
      is exactly how a job ends up installed, armed, and silently failing.

      If `[SCHEDULE]` is `none`, this probe is not blocking; record it and move on.

### Task 5: Probe the optional Whisper fallback

- [ ] **Check `whisperkit-cli` and Homebrew**:

      ```bash
      command -v brew    || echo "brew: MISSING"
      command -v whisperkit-cli && whisperkit-cli --help 2>&1 | head -2 || echo "whisperkit-cli: MISSING"
      ```

      This is optional. Without it, a memo Apple has not transcribed yet is
      skipped and picked up on a later run. With it, the memo is transcribed
      immediately. If `[INSTALL_WHISPER_FALLBACK]` is `yes` and `brew` is
      missing, downgrade to `no` and record the downgrade — a missing Homebrew
      is not a reason to fail the install.

### Task 6: Check the journal destination

- [ ] **Check `[JOURNAL_DIR]`**: does it exist, is it writable, does it already
      contain `YYYY-MM-DD.md` files? An existing journal means the pipeline will
      **append** to files that already have content — confirm the script's
      append behavior is what the user wants and note the file count.

      Also check for an existing install: is there already a crontab entry
      mentioning `voice_memo_to_journal`, or files in `[INSTALL_DIR]`? If so this
      is an **update**, not a fresh install.

      ```bash
      crontab -l 2>/dev/null | grep -n voice_memo || echo "no existing crontab entry"
      ls -la "<INSTALL_DIR>" 2>/dev/null || echo "no existing install dir"
      ```

### Task 7: Write the detection report

- [ ] **Write `{{AUTORUN_FOLDER}}/VOICE_DETECT.md`** with:

      - **Platform**: macOS version, Python path and version, Voice Memos present.
      - **Permissions**: `TCC_AGENT: GRANTED|DENIED` and `TCC_CRON: UNKNOWN|GRANTED`,
        each with the evidence that produced the verdict.
      - **Toolchain**: `brew`, `whisperkit-cli`, and any downgrade applied.
      - **Destination**: resolved `[JOURNAL_DIR]`, whether it exists, existing
        file count.
      - **Existing state**: fresh install vs. update.
      - A one-line **DETECT SUMMARY** the planning document reads at a glance,
        of the form:
        `READY | READY-DISARMED | BLOCKED — <reason>`

        - `READY` — agent read works, cron grant confirmed. Install armed.
        - `READY-DISARMED` — agent read works, cron grant unknown or denied.
          Install everything, but the schedule goes in **commented out**.
        - `BLOCKED` — the agent's own read failed. Nothing can be verified, so
          install nothing and send the user to grant FDA first.
