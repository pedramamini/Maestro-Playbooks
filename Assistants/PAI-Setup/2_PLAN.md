# Document 2: Plan the Install

## Context

- **Playbook**: PAI Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Turn the detection results into a concrete, ordered plan: classify each step as agent-automatable or user-required, and surface any blocker that should stop document 3 from staging anything. Also choose between **fresh install** and **upgrade with auto-backup** based on the existing `~/.claude/` state.

## Inputs

- `{{AUTORUN_FOLDER}}/PAI_DETECT.md` — produced by document 1
- `{{AUTORUN_FOLDER}}/assets/INSTALL_NOTES.md` — pinned reference for the bootstrap command, what the wizard asks for, and what the post-install surface looks like

## Tasks

### Task 1: Load inputs

- [ ] **Read `PAI_DETECT.md`** and extract:
  - Provider value
  - PAI Status (`native` / `listed-by-upstream` / `in-development` / `not-listed`)
  - OS
  - Each prereq's status (`<version>` vs `MISSING` / `not-found`)
  - Existing `~/.claude/` state (`MISSING` / `EXISTS_WITHOUT_PAI` / `EXISTS_WITH_PAI`)

- [ ] **Read `{{AUTORUN_FOLDER}}/assets/INSTALL_NOTES.md`** for the canonical command, wizard expectations, and verification surface. The plan you write should reference these — do not duplicate them inline.

### Task 2: Decide the high-level outcome

- [ ] **Branch on detection results, in this order** (use the first matching rule):

  - **PAI Status is `not-listed` or `listed-by-upstream`** → set the plan's outcome to `SKIP_NO_UPSTREAM_PATH`. PAI v5.0.0 ships an installable bundle only for Claude Code (and a separate Pi scaffold that is not a Maestro `toolType`); no OpenCode install path exists in the upstream repo despite the homepage diagram listing it. Do not list any install steps. Document 3 will write a one-line `INSTALL_LOG.md` and exit; documents 4 and 5 will surface the skip with a pointer to upstream for status.

  - **PAI Status is `in-development` (codex)** → set outcome to `SKIP_IN_DEVELOPMENT`. Same handling; user-facing message says Codex support is on the upstream roadmap and points to <https://github.com/danielmiessler/Personal_AI_Infrastructure>.

  - **OS is not `Darwin` or `Linux`** → `SKIP_UNSUPPORTED_OS`. Same handling.

  - **Required prereq missing** (`curl` / `bash` / `rsync` / `tar`) → `BLOCKED_PREREQ`. Document 3 will not attempt the install. The plan should still list each missing prereq with a paste-ready install command in `PAI_USER_ACTIONS.md`.

  - **PAI Status is `native` (claude-code), OS is supported, all required prereqs present** → set outcome to `AUTOMATED_FRESH_INSTALL` (if `~/.claude/` is `MISSING`), `AUTOMATED_INSTALL_OVER_BACKUP` (if `EXISTS_WITHOUT_PAI`), or `AUTOMATED_UPGRADE` (if `EXISTS_WITH_PAI`). Document 3 will execute the bootstrap with `PAI_TEST_AUTOMATED=1` and verify on the other side.

### Task 3: Decide the strategy for each install step

- [ ] **Classify each install step** as `automatable` (the playbook agent can run it via Bash without driving an interactive TTY) or `user-required` (the user must run it in their own terminal — only used when automation cannot work).

  Use this table as the default classification for the **Claude Code automation path** (see `assets/INSTALL_NOTES.md` § "Automation path"):

  | Step | Classification | Why |
  |---|---|---|
  | Install `bun` (if missing) | automatable | `curl -fsSL https://bun.sh/install \| bash` works without TTY when invoked directly; export `~/.bun/bin` to PATH for the current session |
  | Run `PAI_TEST_AUTOMATED=1 curl -sSL https://ourpai.ai/install.sh \| bash` | automatable | The wizard's `PAI_TEST_AUTOMATED=1` flag returns sensible defaults for every prompt (`User`, `PAI`, first-choice values); `/dev/tty` absence makes the post-install `exec zsh ... pai` degrade to a printed instruction instead of a hang |

- [ ] **For non-Claude-Code providers in the install set** (just OpenCode in the homepage's listed engines, but with no shipped scaffold in the upstream repo as of v5.0.0): there is no automation path. Set the plan's outcome to `SKIP_NO_UPSTREAM_PATH` and note in **Skip / Block** that PAI's upstream repo does not yet ship an OpenCode-specific install (only Claude Code via the bootstrap, plus a separate `Releases/Pi/` scaffold for the Pi runtime). Direct the user to <https://github.com/danielmiessler/Personal_AI_Infrastructure> for status.

- [ ] **Trade-offs the automated install accepts** (record these in the plan's **Strategy** section so they show up in the summary):
  - The agent's own `~/.claude/` is replaced mid-session; there is a brief window (a few seconds) during the `mv` → `rsync` where hooks/skills cannot be resolved.
  - Automated runs produce a generic identity (`principalName="User"`, `aiName="PAI"`). The user is told to run `/interview` afterwards to customize.

### Task 4: Decide on optional choices

- [ ] **ElevenLabs voice**: the wizard prompts for an ElevenLabs API key and is skippable (voice falls back to desktop notifications). Default the plan's recommendation to "skip — start without voice; add the key later by re-running the wizard or editing `~/.claude/.env`". The user can override.

- [ ] **DA identity**: the wizard asks for the DA's name, voice, and personality. There is no good default to suggest — leave this entirely to the user during the wizard.

### Task 5: Write `PAI_INSTALL_PLAN.md`

- [ ] **Write `{{AUTORUN_FOLDER}}/PAI_INSTALL_PLAN.md`** using this structure:

  ```markdown
  # PAI Install Plan

  - **Provider**: <value from PAI_DETECT.md>
  - **OS**: <Darwin | Linux | other>
  - **Outcome**: <AUTOMATED_FRESH_INSTALL | AUTOMATED_INSTALL_OVER_BACKUP | AUTOMATED_UPGRADE | BLOCKED_PREREQ | SKIP_NO_UPSTREAM_PATH | SKIP_IN_DEVELOPMENT | SKIP_UNSUPPORTED_OS>
  - **Date**: {{DATE}}

  ## Strategy

  <one paragraph: what document 3 will do, in plain language. Examples:
   - "Provider is Claude Code, prereqs present. Document 3 will install bun if missing, then run PAI_TEST_AUTOMATED=1 curl -sSL https://ourpai.ai/install.sh | bash to perform an unattended install. The wizard will use placeholder identity (User / PAI); the user runs /interview later to customize. Trade-off: ~/.claude/ is replaced under the running session, with a brief window where hooks/skills cannot be resolved."
   - "Provider is Claude Code with PAI already at ~/.claude/PAI/. Document 3 will run the same automated bootstrap; the bootstrap auto-backs up the current install to ~/.claude.backup-{TIMESTAMP} before placing v5.0.0."
   - "Skip — Codex support is in development per upstream maintainer; no install path exists yet. Pointing the user at the PAI repo for status."
   - "Skip — PAI v5.0.0 only ships an installable bundle for Claude Code in upstream (homepage lists OpenCode/Pi but no scaffold yet for OpenCode; Pi has a separate Releases/Pi/ scaffold that is not a Maestro toolType)."
  >

  ## Prerequisites

  - `curl`: <version | MISSING>
  - `bash`: <version | MISSING>
  - `rsync`: <version | MISSING>
  - `tar`: <version | MISSING>
  - `bun`: <version | install-required | install-optional>
  - `git`: <version | install-recommended>

  ### Prerequisite install commands (only if any are missing)

  <Bulleted list. Each item: which prereq, the user-runnable install command, and one-line rationale. Empty list is fine if all prereqs are present.>

  ## Automatable Steps

  <Numbered list. Each step: one-line description, exact command or file edit, expected outcome. Empty list is the norm — PAI's install is interactive by design.>

  ## User-Required Steps

  <Numbered list. Each step: one-line description, exact paste-ready command, and "Expected: <success signal>". The first step should be installing missing prereqs (if any). The next is the PAI bootstrap one-liner. There may also be steps for completing the wizard itself (DA name, voice, ElevenLabs key prompt, Pulse approval).>

  ## Optional choices the user will make in the wizard

  - ElevenLabs API key: <skip recommended | provide if you want voice>
  - DA name / voice / personality: user picks during wizard
  - Pulse launchd: registered automatically; will start at boot

  ## Skip / Block

  <Use only if outcome is SKIP_* or BLOCKED_PREREQ. State the blocker plainly. Document 3 will see this and exit without staging anything except a short note.>
  ```

### Task 6: Sanity-check the plan

- [ ] **Re-read `PAI_INSTALL_PLAN.md`** and confirm:
  - Every step is unambiguously classified.
  - If outcome is one of the SKIP / BLOCKED values, the **Skip / Block** section is non-empty and the **User-Required Steps** list is empty (or contains only prereq installs in the BLOCKED case).
  - If outcome is one of the install values, the **User-Required Steps** list contains, at minimum, the bootstrap one-liner and references the wizard prompts.

## Success Criteria

- `PAI_INSTALL_PLAN.md` exists with all sections filled.
- The outcome is one of the seven canonical values.
- Every action is unambiguously classified.

## Status

Mark complete when `PAI_INSTALL_PLAN.md` is written and self-checked.

---

**Next**: Document 3 stages the user-required steps and runs whatever (very small) automatable surface remains.
