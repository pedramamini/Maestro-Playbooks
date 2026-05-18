# Document 2: Plan the Install

## Context

- **Playbook**: Superpowers Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Turn the detected provider into a concrete, ordered list of install actions. Distinguish actions the agent can run itself from actions the user must perform interactively, and check prerequisites before document 3 starts touching anything.

## Inputs

- `{{AUTORUN_FOLDER}}/PROVIDER.md` — produced by document 1
- `{{AUTORUN_FOLDER}}/assets/INSTALL_RECIPES.md` — per-provider recipe lookup

## Tasks

### Task 1: Load inputs

- [ ] **Read `PROVIDER.md`** and extract the canonical provider value and the "Supported by Superpowers?" verdict.

- [ ] **Read the recipe section for the detected provider** in `{{AUTORUN_FOLDER}}/assets/INSTALL_RECIPES.md`. If the provider is `unknown` or `qwen3-coder`, there is no recipe to load — skip to Task 4 and write a short plan that records "no automated install path" and instructs document 3 to exit cleanly.

### Task 2: Check prerequisites

- [ ] **Verify `git` is available**:

  ```bash
  git --version
  ```

  Record the version (or note absence — every recipe assumes `git`).

- [ ] **Verify the harness CLI is on `PATH`** for the detected provider, where applicable:

  | Provider | Command to probe |
  |---|---|
  | `claude-code` | `which claude` |
  | `codex` | `which codex` |
  | `opencode` | `which opencode` |
  | `factory-droid` | `which droid` |
  | `copilot-cli` | `which copilot` |
  | `gemini-cli` | `which gemini` |

  Record found / not-found. A missing harness CLI is not always blocking (e.g. Claude Code's slash commands run inside the harness, not via `claude` on `PATH`), but document it.

- [ ] **Provider-specific prerequisite check**:

  - `opencode`: locate the active config file. Check in this order: `<{{AGENT_PATH}}>/opencode.json`, then `~/.config/opencode/opencode.json`. Record which one (if any) exists. If neither, document 3 will create `~/.config/opencode/opencode.json`.
  - All other providers: no extra prerequisite check.

### Task 3: Decide automation strategy

- [ ] **Classify each step from the recipe** as `automatable` (the playbook agent can execute it via Bash, Edit, or Write) or `user-required` (the harness only accepts the command from interactive input). Use the recipe's own automatable / user-required labels as the default; deviate only with a written reason.

- [ ] **Decide on a marketplace choice for `claude-code`**: pick exactly one of:
  - `claude-plugins-official` (single-step, requires the official marketplace already registered)
  - `superpowers-marketplace` (two-step: marketplace add, then install)

  Default to `superpowers-marketplace` for portability — it works on a fresh install without depending on an Anthropic-registered marketplace.

### Task 4: Write `INSTALL_PLAN.md`

- [ ] **Write `{{AUTORUN_FOLDER}}/INSTALL_PLAN.md`** using this structure:

  ```markdown
  # Install Plan

  - **Provider**: <value from PROVIDER.md>
  - **Supported**: <yes | no | partial>
  - **Date**: {{DATE}}

  ## Prerequisites
  - `git`: <version | MISSING>
  - Harness CLI (`<binary>`): <path | not-on-PATH | n/a>
  - Provider-specific: <one-line note, e.g. "OpenCode config: ~/.config/opencode/opencode.json (exists)" | "OpenCode config: none found, will create global">

  ## Strategy
  <one paragraph: what document 3 will do, in plain language>

  ## Automatable Steps
  <Numbered list. Each step has: a one-line description, the exact command or file edit, and the expected outcome. Empty list is fine if the provider is fully user-required.>

  1. <step>
     - Action: `<exact command, OR "Edit <path>: <change>">`
     - Expects: <success signal — exit 0, file content matches, etc.>

  ## User-Required Steps
  <Numbered list of steps the user must perform interactively in the harness, with verbatim commands to paste. Empty list is fine if the provider is fully automatable.>

  1. <step>
     - Run in <harness>: `<exact command>`
     - Expects: <success signal>

  ## Skip / Block
  <Use this section only if Supported is "no" or a prerequisite is missing. State the blocker plainly. Document 3 will see this and exit without changes.>
  ```

### Task 5: Sanity-check the plan

- [ ] **Re-read `INSTALL_PLAN.md`** and confirm: every step is either fully under the agent's control (Bash / Edit / Write) or fully under the user's control (paste into harness). No half-steps. If a step requires a restart of the harness (OpenCode does), it belongs in **User-Required Steps**, even if the file edit before it was automatable.

## Success Criteria

- `INSTALL_PLAN.md` exists with all sections filled in.
- Every action is unambiguously classified as automatable or user-required.
- If the provider is unsupported or a prerequisite is missing, the **Skip / Block** section explains why.

## Status

Mark complete when `INSTALL_PLAN.md` is written and self-checked.

---

**Next**: Document 3 executes the **Automatable Steps** and stages the **User-Required Steps** for the user.
