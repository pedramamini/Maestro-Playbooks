# Document 3: Install

## Context

- **Playbook**: PAI Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Execute the automated install for Claude Code, or — for skipped/blocked outcomes — write a one-line `PAI_INSTALL_LOG.md` and exit. The Claude Code automation path uses `PAI_TEST_AUTOMATED=1` so the wizard runs end-to-end without prompting; see `assets/INSTALL_NOTES.md` § "Automation path" for why this works.

## Inputs

- `{{AUTORUN_FOLDER}}/PAI_INSTALL_PLAN.md` — produced by document 2
- `{{AUTORUN_FOLDER}}/PAI_DETECT.md` — produced by document 1
- `{{AUTORUN_FOLDER}}/assets/INSTALL_NOTES.md` — pinned reference

## Tasks

### Task 1: Load the plan

- [ ] **Read `PAI_INSTALL_PLAN.md`**. Branch on the **Outcome** field:

  - `SKIP_NO_UPSTREAM_PATH` / `SKIP_IN_DEVELOPMENT` / `SKIP_UNSUPPORTED_OS` → write `{{AUTORUN_FOLDER}}/PAI_INSTALL_LOG.md` with a single line beginning `SKIPPED: <reason from Skip / Block>`. Do **not** write `PAI_USER_ACTIONS.md` (no install action is useful). Mark all remaining tasks complete and exit.

  - `BLOCKED_PREREQ` → write `{{AUTORUN_FOLDER}}/PAI_USER_ACTIONS.md` containing **only** the prereq install commands from the plan (no PAI bootstrap). Write `PAI_INSTALL_LOG.md` with outcome `BLOCKED`. Then exit.

  - `AUTOMATED_FRESH_INSTALL` / `AUTOMATED_INSTALL_OVER_BACKUP` / `AUTOMATED_UPGRADE` → continue to Task 2.

### Task 2: Pre-bootstrap: ensure `bun` is present

- [ ] **If `bun` was reported MISSING in `PAI_DETECT.md`**, install it now (the bootstrap's auto-install requires a TTY we do not have):

  ```bash
  curl -fsSL https://bun.sh/install | bash
  export PATH="$HOME/.bun/bin:$PATH"
  bun --version
  ```

  Confirm `bun --version` prints a real version (not "command not found"). If it does not, abort with outcome `FAILED` and record the bun-install output in `PAI_INSTALL_LOG.md`.

- [ ] **If `bun` was already present**, skip this task. Note in the log that bun was pre-existing.

### Task 3: Run the bootstrap with `PAI_TEST_AUTOMATED=1`

- [ ] **Notify the user** in your output that the install is starting and that `~/.claude/` will be replaced. State the backup path the bootstrap will create.

- [ ] **Execute the bootstrap**, capturing every line of output:

  ```bash
  PAI_TEST_AUTOMATED=1 bash -c '
    set -o pipefail
    export PATH="$HOME/.bun/bin:$PATH"
    curl -sSL https://ourpai.ai/install.sh | bash
  ' 2>&1 | tee "{{AUTORUN_FOLDER}}/pai-bootstrap.out"
  ```

  Capture the exit status into a variable (e.g. `BOOTSTRAP_EXIT=$?`). The `tee` is for inspectability — the full output also goes back through stdout so you see it.

- [ ] **Do not retry on failure.** If the bootstrap exits non-zero:
  - Read the last 50 lines of `pai-bootstrap.out`.
  - Identify the failing step (the bootstrap announces each as `▸ N/5 ...`; the wizard announces each as a section header).
  - Record this in `PAI_INSTALL_LOG.md` under **Outcome: FAILED** and proceed to Task 5.

- [ ] **Expected wizard behavior under `PAI_TEST_AUTOMATED=1`** (so you know what success looks like, not for you to validate exhaustively):
  - System detect, prerequisites, API keys: all auto-pass with empty / detected values.
  - Identity: `principalName` = git config `user.name` or "User"; `aiName` = "PAI".
  - Repository: copies from the bundle the bootstrap placed (no extra git clone).
  - Configuration: installs Pulse as a launchd agent (`com.pai.pulse`).
  - Voice / Telegram: skipped (no API key) or first-choice defaults.
  - Validation: critical checks pass.

### Task 4: Capture immediate post-install state

- [ ] **Without re-running the bootstrap**, snapshot the post-install state for document 4 to verify against:

  ```bash
  ls -la "$HOME/.claude" 2>&1 | head -10
  [ -d "$HOME/.claude/PAI" ] && echo "PAI: present" || echo "PAI: absent"
  cat "$HOME/.claude/PAI/ALGORITHM/LATEST" 2>/dev/null || echo "ALGORITHM/LATEST: absent"
  ls -d ~/.claude.backup-* 2>/dev/null | head -3 || echo "no-backup"
  launchctl list 2>/dev/null | grep -i 'com.pai.pulse' || echo "pulse-launchd: not-loaded"
  curl -sS --max-time 3 http://localhost:31337/api/pulse/health 2>&1 | head -3 || echo "pulse-http: unreachable"
  ```

### Task 5: Write `PAI_INSTALL_LOG.md`

- [ ] **Write `{{AUTORUN_FOLDER}}/PAI_INSTALL_LOG.md`**:

  ```markdown
  # PAI Install Log

  - **Date**: {{DATE}}
  - **Outcome from plan**: <AUTOMATED_FRESH_INSTALL | AUTOMATED_INSTALL_OVER_BACKUP | AUTOMATED_UPGRADE | BLOCKED_PREREQ | SKIP_NO_UPSTREAM_PATH | SKIP_IN_DEVELOPMENT | SKIP_UNSUPPORTED_OS>

  ## Pre-bootstrap

  - bun: <pre-existing | installed-now (version) | install-failed (error)>

  ## Bootstrap execution

  - Command: `PAI_TEST_AUTOMATED=1 curl -sSL https://ourpai.ai/install.sh | bash`
  - Exit status: <0 | non-zero>
  - Output captured at: `{{AUTORUN_FOLDER}}/pai-bootstrap.out`

  ### Last lines of output

  ```text
  <last 30-50 lines of pai-bootstrap.out>
  ```

  ## Immediate post-install probes

  - `~/.claude/` listing: `<truncated ls output>`
  - `~/.claude/PAI/`: `<present | absent>`
  - `~/.claude/PAI/ALGORITHM/LATEST`: `<contents | absent>`
  - Backup directory: `<path | none>`
  - `com.pai.pulse` in launchctl: `<line | not-loaded>`
  - Pulse HTTP health: `<truncated response | unreachable>`

  ## Files Modified by This Document

  - `~/.claude/` (replaced by bootstrap)
  - `~/.claude.backup-<TS>` (created by bootstrap if applicable)
  - `~/Library/LaunchAgents/com.pai.pulse.plist` (created by wizard)
  - `~/.zshenv`, `~/.zprofile`, `~/.zshrc`, `~/.bash_profile` (PATH export added by wizard if missing)
  - `{{AUTORUN_FOLDER}}/pai-bootstrap.out` (captured output)

  ## Outcome

  <One of:
   - "AUTOMATED_INSTALLED" — bootstrap exited zero AND ~/.claude/PAI/ exists
   - "AUTOMATED_INSTALLED_PARTIAL" — bootstrap exited zero AND ~/.claude/PAI/ exists BUT Pulse launchd is not loaded yet (often resolves on next login)
   - "FAILED" — bootstrap exited non-zero
   - "BLOCKED" — prereqs missing, see PAI_USER_ACTIONS.md
   - "SKIPPED" — provider not supported by current upstream install path
  >
  ```

## Success Criteria

- `PAI_INSTALL_LOG.md` exists with an explicit **Outcome** value reflecting actual observed state.
- For `AUTOMATED_*` plan outcomes, the bootstrap actually ran (its output is in `pai-bootstrap.out`).
- For SKIP / BLOCKED plan outcomes, no install command was run.

## Status

Mark complete when `PAI_INSTALL_LOG.md` records the outcome.

---

**Next**: Document 4 verifies the install rigorously and produces the verdict the summary uses.
