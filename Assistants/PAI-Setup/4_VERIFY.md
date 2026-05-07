# Document 4: Verify

## Context

- **Playbook**: PAI Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Confirm the install actually worked. The typical Claude Code run will see `Outcome: AUTOMATED_INSTALLED` from document 3 and verify that the runtime state matches; a SKIP/FAILED outcome short-circuits with a copy of the reason.

## Inputs

- `{{AUTORUN_FOLDER}}/PAI_DETECT.md`
- `{{AUTORUN_FOLDER}}/PAI_INSTALL_PLAN.md`
- `{{AUTORUN_FOLDER}}/PAI_INSTALL_LOG.md`
- `{{AUTORUN_FOLDER}}/PAI_USER_ACTIONS.md` (may not exist if outcome was SKIPPED)
- `{{AUTORUN_FOLDER}}/assets/INSTALL_NOTES.md` — verification surface reference

## Tasks

### Task 1: Read the install outcome

- [ ] **Load `PAI_INSTALL_LOG.md`** and read **Outcome**:

  - `SKIPPED` → write `PAI_VERIFY.md` with verdict `SKIPPED`, copy the reason from `PAI_INSTALL_PLAN.md`'s Skip / Block section, mark all remaining tasks complete.
  - `BLOCKED` → write `PAI_VERIFY.md` with verdict `BLOCKED`, list the missing prereqs, mark all remaining tasks complete.
  - `FAILED` → write `PAI_VERIFY.md` with verdict `FAILED`, copy the failing command from the log, mark all remaining tasks complete.
  - `AUTOMATED_INSTALLED` / `AUTOMATED_INSTALLED_PARTIAL` → continue to Task 2 to confirm the live state matches.

### Task 2: Probe the install surface

- [ ] **Run each probe** and record the result (do not infer; record what you actually see):

  1. **PAI directory layout**:

     ```bash
     [ -d "$HOME/.claude/PAI" ] && echo "PAI: present" || echo "PAI: absent"
     [ -f "$HOME/.claude/install.sh" ] && echo "bundled-installer: present" || echo "bundled-installer: absent"
     [ -d "$HOME/.claude/PAI/USER" ] && echo "USER: present" || echo "USER: absent"
     ls "$HOME/.claude/PAI/ALGORITHM/LATEST" 2>/dev/null && cat "$HOME/.claude/PAI/ALGORITHM/LATEST" 2>/dev/null || echo "ALGORITHM/LATEST: absent"
     ```

  2. **Backup directory** (the bootstrap creates one if `~/.claude/` already existed):

     ```bash
     ls -d ~/.claude.backup-* 2>/dev/null | head -5 || echo "no-backup-found"
     ```

  3. **Pulse launchd service**:

     ```bash
     launchctl list 2>/dev/null | grep -i 'com.pai.pulse' || echo "pulse-launchd: not-loaded"
     ```

  4. **Pulse dashboard health**:

     ```bash
     curl -sS --max-time 3 http://localhost:31337/api/pulse/health 2>&1 | head -5 || echo "pulse-http: unreachable"
     ```

  5. **DA identity file** (populated by the wizard):

     ```bash
     [ -f "$HOME/.claude/PAI/USER/DA_IDENTITY.md" ] && echo "DA_IDENTITY: present" || echo "DA_IDENTITY: absent"
     ```

### Task 3: Decide the verdict

- [ ] **Apply this decision table** (use the first row that matches):

  | Condition | Verdict |
  |---|---|
  | `PAI: present` AND `pulse-launchd` loaded AND Pulse HTTP responds | `INSTALLED-AND-ACTIVE` |
  | `PAI: present` AND (`pulse-launchd` not loaded OR Pulse HTTP unreachable) | `INSTALLED-PARTIAL` (files in place, Pulse not yet running — usually requires logout/login or a manual `launchctl load`) |
  | `PAI: absent` AND `bundled-installer: present` | `INSTALLED-PENDING-WIZARD` (the v5 bundle is in place but the wizard did not finish — `cd ~/.claude && ./install.sh` will resume) |
  | `PAI: absent` AND log Outcome was `AUTOMATED_*` | `FAILED` (bootstrap exited zero per the log but `~/.claude/PAI/` is missing — surface this discrepancy) |

  Note: `INSTALLED-PARTIAL` is plausible right after install if `launchd` has not yet bound `com.pai.pulse` to port 31337 (the wizard waits 10s for this; longer delays are possible on slow disks). State this explicitly so the user is not alarmed.

### Task 4: Write `PAI_VERIFY.md`

- [ ] **Write `{{AUTORUN_FOLDER}}/PAI_VERIFY.md`**:

  ```markdown
  # PAI Verification Report

  - **Date**: {{DATE}}
  - **Verdict**: <INSTALLED-AND-ACTIVE | INSTALLED-PARTIAL | INSTALLED-PENDING-WIZARD | FAILED | BLOCKED | SKIPPED>

  ## Probes

  ### `~/.claude/` layout
  - `PAI/`: <present | absent>
  - `install.sh`: <present | absent>
  - `PAI/USER/`: <present | absent>
  - `PAI/ALGORITHM/LATEST`: `<contents | absent>`

  ### Backup
  - <newest backup path found, or "no backup directory found">

  ### Pulse launchd
  - `launchctl list | grep com.pai.pulse`:

    ```text
    <captured output, or "not-loaded">
    ```

  ### Pulse HTTP
  - `curl http://localhost:31337/api/pulse/health`:

    ```text
    <captured output (truncated to 5 lines), or "unreachable">
    ```

  ### DA identity
  - `~/.claude/PAI/USER/DA_IDENTITY.md`: <present | absent>

  ## Notes

  <Pick whichever applies:

   - INSTALLED-AND-ACTIVE: "Install completed automatically. Pulse is responding at http://localhost:31337. Identity is the placeholder default (User / PAI) — start a fresh Claude Code session and run /interview to customize."

   - INSTALLED-PARTIAL: "Files are in place but Pulse is not yet active. This sometimes happens right after install — try `launchctl load ~/Library/LaunchAgents/com.pai.pulse.plist`, or log out and back in. If Pulse still does not bind :31337, check ~/.claude/PAI/PULSE/logs/pulse-stderr.log."

   - INSTALLED-PENDING-WIZARD: "The bootstrap copied files but the wizard did not run to completion. Resume with `cd ~/.claude && ./install.sh` (PAI_TEST_AUTOMATED=1 keeps it unattended)."

   - FAILED / BLOCKED / SKIPPED: "<copy the reason from PAI_INSTALL_PLAN.md / PAI_INSTALL_LOG.md>"
  >
  ```

## Success Criteria

- `PAI_VERIFY.md` exists with a single explicit **Verdict** value.
- `PENDING-USER-ACTION` is treated as a normal outcome on the typical run, not a failure.
- Each probe section reflects what was actually observed; no fabricated outputs.

## Status

Mark complete when `PAI_VERIFY.md` is written.

---

**Next**: Document 5 produces the human-facing summary and points the user at the right next step based on the verdict.
