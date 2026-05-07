# Document 4: Verify

## Context

- **Playbook**: Superpowers Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Confirm that whatever could be installed has been installed, and clearly mark anything that still depends on the user.

The agent is verifying its **own** environment. This is unusual, and there is a real subtlety: for several harnesses, the install only takes effect after the harness reloads or the user runs an interactive command. The verification has to be honest about what it can and cannot prove from inside the current session.

## Inputs

- `{{AUTORUN_FOLDER}}/PROVIDER.md`
- `{{AUTORUN_FOLDER}}/INSTALL_PLAN.md`
- `{{AUTORUN_FOLDER}}/INSTALL_LOG.md`
- `{{AUTORUN_FOLDER}}/USER_ACTIONS.md` (may not exist if no user actions were needed)

## Tasks

### Task 1: Read the install outcome

- [ ] **Load `INSTALL_LOG.md`** and read the **Outcome** field. Branch:
  - `SKIPPED` → write `VERIFY.md` recording the skip reason and mark all remaining tasks complete.
  - `FAILED` → write `VERIFY.md` recording the failure step and mark all remaining tasks complete.
  - `AUTOMATED_COMPLETE` or `AWAITING_USER` → continue to Task 2.

### Task 2: Run provider-appropriate verification

- [ ] **Use the verification command for the detected provider**:

  | Provider | Verification command | What "good" looks like |
  |---|---|---|
  | `claude-code` | `/plugin` (user-required) | `superpowers` listed as enabled |
  | `codex` | `/plugins` (user-required) | `superpowers` listed as enabled |
  | `opencode` | `opencode run --print-logs "hello" 2>&1 \| grep -i superpowers` | output mentions superpowers loading |
  | `factory-droid` | `droid plugin list` | `superpowers` in the output |
  | `copilot-cli` | `copilot plugin list` | `superpowers` in the output |
  | `gemini-cli` | `gemini extensions list` | `superpowers` in the output |

  For shell-based verifications (everything except `claude-code` and `codex`): run the command and capture the output. For slash-command verifications: do not attempt to run them — record that they are user-required.

- [ ] **For `opencode` specifically**: also re-read the `opencode.json` you edited and confirm:
  - The file still parses as valid JSON.
  - The `plugin` array contains a `superpowers@...` entry.
  - The full file content (or at least the `plugin` array) is recorded in `VERIFY.md`.

  Note explicitly that OpenCode picks up the new plugin **only after restart** — even if the file is correct, the running session may not have superpowers active until the user restarts OpenCode.

### Task 3: Probe Superpowers itself (best-effort)

- [ ] **Check whether the current session has Superpowers loaded** by looking for any of:
  - A skill, plugin, or extension named `superpowers` exposed in your environment.
  - A `superpowers` directory under the harness's plugin/extension/skill paths (e.g. `~/.claude/plugins/`, `~/.config/opencode/plugins/`, `~/.gemini/extensions/`).
  - Documentation or auto-loaded instructions that mention Superpowers skills like `brainstorming`, `writing-plans`, `using-git-worktrees`.

  Record what you find. A negative result here is not necessarily a failure — for several harnesses the install only takes effect on the next session.

### Task 4: Write `VERIFY.md`

- [ ] **Write `{{AUTORUN_FOLDER}}/VERIFY.md`** (the outer fence here uses four backticks so the inner three-backtick fences render correctly — replicate that when you write the file):

  ````markdown
  # Verification Report

  - **Provider**: <value>
  - **Date**: {{DATE}}

  ## Provider-level check
  - Command run: `<command, or "user-required: <command>">`
  - Output (truncated to ~20 lines):

    ```text
    <captured output, or "n/a — user-required">
    ```

  - Verdict: <PASS | FAIL | DEFERRED-TO-USER>

  ## Config sanity check (opencode only — omit otherwise)
  - File: `<path>`
  - Parses as JSON: <yes | no>
  - `plugin` contains superpowers entry: <yes | no>
  - Restart-required: yes (OpenCode does not hot-reload plugin changes)

  ## In-session probe
  <one paragraph: what you looked for, what you found. State explicitly if Superpowers is not yet active in this session and whether that is expected.>

  ## Final verdict
  One of:

  - "INSTALLED-AND-ACTIVE" — verification passed inside this session
  - "INSTALLED-PENDING-RELOAD" — files are in place, harness needs restart/new session
  - "PENDING-USER-ACTION" — user-required steps from USER_ACTIONS.md are not yet performed
  - "FAILED" — install did not succeed; see notes
  - "SKIPPED" — provider unsupported or prerequisite missing

  ## Notes
  <anything the user should know — restart needed, paste these slash commands, missing prerequisite, etc.>
  ````

## Success Criteria

- `VERIFY.md` exists with a single explicit **Final verdict** value.
- The verdict is honest: `INSTALLED-PENDING-RELOAD` and `PENDING-USER-ACTION` are not failures and should be used when accurate.

## Status

Mark complete when `VERIFY.md` is written.

---

**Next**: Document 5 produces the human-facing summary and links to `USER_ACTIONS.md` if anything still requires the user.
