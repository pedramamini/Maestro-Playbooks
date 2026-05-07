# Document 5: Summary

## Context

- **Playbook**: PAI Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Produce a single human-facing document that says, in plain language, what state PAI is in, what (if anything) the user still needs to do, and what to do first after install. This is the only file the user is expected to read.

## Inputs

- `{{AUTORUN_FOLDER}}/PAI_DETECT.md`
- `{{AUTORUN_FOLDER}}/PAI_INSTALL_PLAN.md`
- `{{AUTORUN_FOLDER}}/PAI_INSTALL_LOG.md`
- `{{AUTORUN_FOLDER}}/PAI_VERIFY.md`
- `{{AUTORUN_FOLDER}}/PAI_USER_ACTIONS.md` (may not exist)

## Tasks

### Task 1: Pull the headline facts

- [ ] **Read all input files** and extract:
  - Provider value from `PAI_DETECT.md`
  - Outcome from `PAI_INSTALL_PLAN.md`
  - Verdict from `PAI_VERIFY.md`
  - Whether `PAI_USER_ACTIONS.md` exists and is non-empty

- [ ] **Map the verdict to a single status word for the summary header**:

  | Verdict | Status |
  |---|---|
  | `INSTALLED-AND-ACTIVE` | Installed |
  | `INSTALLED-PARTIAL` | Installed (Pulse pending) |
  | `INSTALLED-PENDING-WIZARD` | Installed (wizard incomplete) |
  | `FAILED` | Failed |
  | `BLOCKED` | Blocked |
  | `SKIPPED` | Skipped |

### Task 2: Write `PAI_SETUP.md`

- [ ] **Write `{{AUTORUN_FOLDER}}/PAI_SETUP.md`**:

  ```markdown
  # PAI Setup — Summary

  - **Agent**: {{AGENT_NAME}}
  - **Provider**: <detected provider>
  - **Date**: {{DATE}}
  - **Status**: <Installed | Installed (Pulse pending) | Installed (wizard incomplete) | Action required | Failed | Blocked | Skipped>

  ---

  ## What is PAI?

  [Personal AI Infrastructure (PAI)](https://github.com/danielmiessler/Personal_AI_Infrastructure) is a Life Operating System — the context layer between today's agent technology and what you are trying to accomplish. It captures who you are, what you care about, and where you are trying to go, then helps you get there using AI that knows you. Three layers stack: PAI itself (skills, memory, the Algorithm, your TELOS, your identity files), Pulse (the Life Dashboard at `localhost:31337`), and the DA (your Digital Assistant — the voice and personality you talk to). PAI is designed to sit underneath multiple AI agent systems; the upstream homepage lists Claude Code, OpenCode, and Pi, with Codex support in development.

  ## What this playbook did

  <2-4 sentences. Plain language. Examples:

   - "Detected Claude Code, installed bun, then ran the PAI bootstrap unattended with PAI_TEST_AUTOMATED=1. The wizard completed all 9 steps (system-detect, prerequisites, api-keys, identity, repository, configuration, voice, telegram, validation) using sensible defaults — identity is User/PAI, voice is the first picker option, no Telegram. ~/.claude/ was backed up to ~/.claude.backup-<TS>. Pulse is registered as a launchd agent and (verdict-dependent) responding at localhost:31337."

   - "This agent is running on <provider>, which is not in PAI's installable upstream set yet. PAI v5.0.0 ships an installer for Claude Code only (the homepage diagram lists OpenCode and Pi as future engines; Pi has a separate non-Maestro scaffold)."
  >

  ## What you need to do next

  <Pick exactly one block matching the actual status; do not include the others.>

  ### If status is "Installed"

  Your install is generic — it has the v5.0.0 bundle, Pulse, and a placeholder DA named "PAI" — but it doesn't yet know who you are. Two things to do:

  1. **Open the Life Dashboard**: <http://localhost:31337>
  2. **Make it yours** in a fresh Claude Code session (the agent that ran this playbook had `~/.claude/` swapped underneath it; restart for a clean state):

     ```text
     /interview
     ```

     The DA walks you through TELOS, Ideal State, Preferences, and Identity. Without TELOS, the DA has nothing to optimize against. You can pause and resume this anytime.

  3. **(Optional) Migrate your existing context**: tell your DA `Help me migrate my context into PAI/USER/.` It intakes from `.md`/`.txt`, Obsidian, Notion, Apple Notes, etc., and classifies each chunk against the v5 taxonomy (TELOS, KNOWLEDGE, PROJECTS, FEED).

  ### If status is "Installed (Pulse pending)"

  - Files are in place but Pulse is not running yet. Two ways to bring it up:
    - Easiest: log out and back in (`launchd` will load `com.pai.pulse` on login).
    - Manual: `launchctl load ~/Library/LaunchAgents/com.pai.pulse.plist`
  - Then verify: `curl -s http://localhost:31337/api/pulse/health` — and continue with the "Installed" steps above.

  ### If status is "Installed (wizard incomplete)"

  - The bootstrap placed the v5 bundle but the wizard did not finish (so the DA identity is unset, Pulse is not registered, etc.).
  - Re-run the wizard in a fresh Terminal:

    ```bash
    cd ~/.claude && ./install.sh
    ```

  ### If status is "Blocked"

  - One or more bootstrap prerequisites are missing. The exact list is in `{{AUTORUN_FOLDER}}/PAI_INSTALL_PLAN.md` under **Prerequisite install commands**.
  - Install them, then re-run this playbook.

  ### If status is "Failed"

  - Full bootstrap output is at `{{AUTORUN_FOLDER}}/pai-bootstrap.out`; failing step and last 30-50 lines are in `{{AUTORUN_FOLDER}}/PAI_INSTALL_LOG.md`.
  - To restore your prior `~/.claude/`: `rm -rf ~/.claude && mv ~/.claude.backup-<TS> ~/.claude` (the backup path is in the log).
  - Common causes: network failure during tarball download, `bun` install failed (was missing and could not auto-install), Pulse launchd registration failed, write permission on `~/Library/LaunchAgents/`.

  ### If status is "Skipped"

  Read `PAI_INSTALL_PLAN.md` → **Skip / Block** for the exact reason. Common cases:

  - **Provider is Codex**: Codex support is in development upstream. Check <https://github.com/danielmiessler/Personal_AI_Infrastructure> for status. In the meantime, create a Claude Code agent in Maestro and re-run.
  - **Provider is OpenCode**: PAI's homepage diagram lists OpenCode as a future engine, but the v5.0.0 release does not ship an OpenCode-specific installer or scaffold. Watch the upstream repo. (Pi has a separate `Releases/Pi/` scaffold that is not run via a Maestro `toolType`.)
  - **Provider is unlisted** (`factory-droid`, `copilot-cli`, `gemini-cli`, `qwen3-coder`, `unknown`): no documented PAI install path. PAI's homepage lists Claude Code, OpenCode, and Pi as supported engines.
  - **OS is unsupported**: PAI v5.0.0 supports macOS (full) and Linux (full); Windows is not supported. See <https://github.com/danielmiessler/Personal_AI_Infrastructure/blob/main/PLATFORM.md>.

  Action: in Maestro, create a Claude Code agent and re-run this playbook.

  ## Files generated by this playbook

  | File | Purpose |
  |---|---|
  | `PAI_DETECT.md` | Detected provider, prereqs, existing `~/.claude/` state |
  | `PAI_INSTALL_PLAN.md` | Concrete plan and outcome decision |
  | `PAI_INSTALL_LOG.md` | What the agent did (typically nothing — install is user-required) |
  | `PAI_USER_ACTIONS.md` | Paste-ready install instructions (only when relevant) |
  | `PAI_VERIFY.md` | Verification verdict with all probe outputs |
  | `PAI_SETUP.md` | This summary |

  ## Reference

  - PAI: <https://github.com/danielmiessler/Personal_AI_Infrastructure>
  - PAI v5.0.0 release notes: <https://github.com/danielmiessler/Personal_AI_Infrastructure/tree/main/Releases/v5.0.0>
  - PAI install script (inspect before piping): <https://ourpai.ai/install.sh>
  - Pulse Life Dashboard: <http://localhost:31337> (after install)
  - Maestro Playbooks: <https://github.com/RunMaestro/Maestro-Playbooks>
  ```

### Task 3: Surface the result

- [ ] **State the outcome plainly** in your final response: which provider was detected, the status (Installed / Action required / Failed / Skipped / etc.), and the path to `PAI_SETUP.md`. Keep it to ~3 sentences. The user reads this in their session log.

## Success Criteria

- `PAI_SETUP.md` exists and includes only the block matching the actual status (do not include all six "What you need to do next" branches).
- The status field at the top is one of the seven canonical values.
- The summary references generated files by `{{AUTORUN_FOLDER}}/`-relative path so the user can open them.

## Status

Mark complete when `PAI_SETUP.md` is written and the outcome is summarized in the session.

---

**Playbook complete.** No looping.
