# Document 4: Verify the Install

## Context

- **Playbook**: LifeOS Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Verify the live state of the install with **real evidence**, not assumptions, and write a single unambiguous verdict to `LIFEOS_VERIFY.md`. LifeOS's own Setup workflow verifies against three evidence classes; mirror that here and never claim a pass you did not observe.

## Tasks

### Task 1: Load context and short-circuit

- [ ] **Read `{{AUTORUN_FOLDER}}/LIFEOS_INSTALL_LOG.md`** (and `LIFEOS_INSTALL_PLAN.md`). If the install was `BLOCKED` or `ABORTED`, write `LIFEOS_VERIFY.md` with verdict `BLOCKED` or `SKIPPED` (echo the reason) and mark remaining tasks complete without changes. Otherwise proceed. Use the resolved `configRoot` recorded in the log.

### Task 2: Verify Core (always checked)

- [ ] **The skill and runtime are present, and the identity imports resolve.** Check:

  ```bash
  ls -d "<configRoot>/skills/LifeOS" && echo "skill: OK"
  ls -d "<configRoot>/LIFEOS/ALGORITHM" && echo "runtime: OK"
  grep -c "@LIFEOS/" "<configRoot>/CLAUDE.md" && echo "imports present"
  ```

  Confirm the `@LIFEOS/...` imports in `CLAUDE.md` are **active** (uncommented) and their targets exist. Core failing here is a hard fail — no amount of enhancements compensates.

### Task 3: Verify the launch command (constitution)

- [ ] **The `lifeos` launch command is wired** (this is what actually loads the operating contract; without it, Core is installed but launches un-constituted):

  ```bash
  grep -n "alias lifeos=" "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.config/fish/config.fish" 2>/dev/null
  ```

  If `[WIRE_LAUNCH_ALIAS]` was `no`, confirm instead that the manual one-line launch command was recorded for the user. If neither is true, flag **un-constituted**.

### Task 4: Verify Enhancements that were installed

- [ ] **Check only the components the log says were applied** (skip the rest — never report a component you did not install):
  - **`hooks`** → the hook block is present in `settings.json` (`grep -c '"hooks"' "<configRoot>/settings.json"`), and if feasible note that a probe session would show the mode banner. If hooks were **declined**, surface the caveat plainly: the mode banner and the memory/voice loop are hook-enforced, so Core runs un-bannered and un-augmented without them.
  - **`statusline` / `tooltips` / `spinnerverbs`** → re-read `settings.json` shows the corresponding key set.
  - **`agents`** → files present under `<configRoot>/agents/`.
  - **`pulse`** (macOS) → `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:31337/healthz` returns `200`. If it does not, Pulse files may be in place but the `launchd` service is not bound yet — record `pulse-pending`, not a failure.
  - **`worksweep` / `derivedsync`** (macOS) → `launchctl print` shows the label loaded.

### Task 5: Write the verdict

- [ ] **Write `{{AUTORUN_FOLDER}}/LIFEOS_VERIFY.md`** with one verdict and the evidence behind it:

  | Verdict | Meaning |
  |---|---|
  | `INSTALLED-ACTIVE` | Core present, imports resolve, `lifeos` alias wired, all chosen enhancements verified. |
  | `INSTALLED-PENDING-INTERVIEW` | Core + enhancements in place, but no personal data yet — the user still needs to run the Interview to seed identity/TELOS/Pulse. (Expected outcome for a clean automated run.) |
  | `INSTALLED-UNCONSTITUTED` | Core present but the `lifeos` launch command is not wired — the constitution won't load until it is. |
  | `INSTALLED-DEGRADED` | Non-Claude harness: skill + USER + context loaded, but always-on hooks not wired (roadmap). |
  | `INSTALLED-PULSE-PENDING` | Everything in place except Pulse not yet bound to `:31337`. |
  | `FAILED` | Core verification failed (skill/runtime/imports missing). |
  | `BLOCKED` / `SKIPPED` | Prereq blocker, or capability-gate/dev-tree short-circuit. |

  Record exactly which checks passed and which did not. End with a one-line **VERIFY SUMMARY**.
