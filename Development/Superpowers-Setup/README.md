# Superpowers Setup Playbook

A Maestro Auto Run playbook that detects the AI coding harness an agent is running inside and installs [obra/superpowers](https://github.com/obra/superpowers) for that specific provider — automating what it can, and handing the user a clean checklist for steps the harness only accepts from interactive input.

## What This Playbook Does

Superpowers ships per-harness, with different install paths for Claude Code, Codex, OpenCode, Factory Droid, GitHub Copilot CLI, and Gemini CLI. Asking the wrong question (e.g. "where do I edit `~/.claude/settings.json` for OpenCode?") wastes time. This playbook:

1. **Detects** which Maestro `toolType` the running agent is (the agent self-identifies — it *is* the harness — with a `PATH` probe as sanity check).
2. **Plans** the install by reading a per-provider recipe from `assets/INSTALL_RECIPES.md` and classifying every step as agent-automatable or user-required.
3. **Installs** what it can — running shell commands for Gemini / Copilot / Droid, editing `opencode.json` for OpenCode, and staging slash commands for Claude Code / Codex.
4. **Verifies** the install where verifiable from inside the current session, and flags `INSTALLED-PENDING-RELOAD` honestly when the harness needs a restart.
5. **Summarizes** the result in a single human-facing `SUPERPOWERS_SETUP.md` with explicit next steps.

Run it once, in any agent. It figures out the rest.

## Supported Providers

| Maestro `toolType` | Install style | Fully automatable? |
|---|---|---|
| `claude-code` | `/plugin install …` slash command | No — user pastes commands |
| `codex` | `/plugins` interactive picker | No — user pastes commands |
| `opencode` | edit `opencode.json` | Yes (restart required) |
| `factory-droid` | `droid plugin install …` shell | Yes |
| `copilot-cli` | `copilot plugin install …` shell | Yes |
| `gemini-cli` | `gemini extensions install …` shell | Yes |
| `qwen3-coder` | (no upstream install path documented) | Skipped with explanation |

The playbook never lies about what got done — when steps are user-required, it writes `USER_ACTIONS.md` with paste-ready commands and tells the user where to find it.

## Document Chain

| Document | Purpose | Reset on Completion? |
|---|---|---|
| `1_DETECT_PROVIDER.md` | Identify the running harness; write `PROVIDER.md` | No |
| `2_PLAN_INSTALL.md` | Read recipe, check prerequisites, classify steps; write `INSTALL_PLAN.md` | No |
| `3_INSTALL.md` | Run automatable steps; stage user-required ones in `USER_ACTIONS.md`; log to `INSTALL_LOG.md` | No |
| `4_VERIFY.md` | Verify from inside the session where possible; write `VERIFY.md` | No |
| `5_SUMMARY.md` | Write the human-facing `SUPERPOWERS_SETUP.md` | No |

This is a **linear, non-looping** playbook (like Best PR Comparison). Each document runs once.

## Generated Files

| File | Purpose |
|---|---|
| `PROVIDER.md` | Detected harness, confidence, signal evidence |
| `INSTALL_PLAN.md` | Per-step plan with prerequisites and automation classification |
| `INSTALL_LOG.md` | Outcome of the automatable steps |
| `USER_ACTIONS.md` | Paste-ready interactive commands (only when needed) |
| `VERIFY.md` | Verification result with explicit verdict |
| `SUPERPOWERS_SETUP.md` | The summary the user reads |

## Assets

- `assets/INSTALL_RECIPES.md` — per-provider recipe lookup. Document 2 reads this; documents 3 and 4 follow the steps it lists. Edit this file to add new providers or update install paths as upstream changes.

## Recommended Setup

```text
Loop Mode: OFF
Max Loops: N/A
Documents:
  1_DETECT_PROVIDER.md  [Reset: OFF]
  2_PLAN_INSTALL.md     [Reset: OFF]
  3_INSTALL.md          [Reset: OFF]
  4_VERIFY.md           [Reset: OFF]
  5_SUMMARY.md          [Reset: OFF]
```

## Prerequisites

- Maestro installed and configured (the playbook itself runs through Maestro Auto Run; provider detection is introspective and does not call `maestro-cli`).
- `git` on `PATH` (every recipe assumes it).
- The agent's harness CLI on `PATH` is helpful but not strictly required — Claude Code's plugin commands run inside the harness, not via `claude` on `PATH`.

## Outcome Statuses

`SUPERPOWERS_SETUP.md` will land in one of these states:

| Status | Meaning | What to do |
|---|---|---|
| **Installed** | Verification passed inside this session | Try `Tell me about your superpowers` |
| **Installed (restart required)** | Files in place; harness needs a restart (typical for OpenCode) | Restart, then verify in the new session |
| **Action required** | Automatable steps done; user-required steps staged | Open `USER_ACTIONS.md` and paste them |
| **Failed** | An automatable step errored | Read `INSTALL_LOG.md` for the failing command |
| **Skipped** | Provider unsupported or prerequisite missing | Read the **Skip / Block** section of `INSTALL_PLAN.md` |

## Template Variables Used

- `{{AGENT_NAME}}` — recorded in generated files for traceability
- `{{AGENT_PATH}}` — recorded in generated files; relevant for OpenCode's per-project config lookup
- `{{AUTORUN_FOLDER}}` — where all generated artifacts and `assets/` live
- `{{DATE}}` — recorded in every generated file

## Design Notes

- **Why a single source of truth in `assets/INSTALL_RECIPES.md`**: superpowers' install instructions drift over time as providers add or rework plugin systems. Keeping the recipe in one bundled asset makes it cheap to update without touching the document chain.
- **Why detection is introspective, not via `maestro-cli`**: the agent running this playbook *is* the harness we're setting up — it knows its own identity by definition, and that knowledge is more reliable than an external lookup that depends on Maestro CLI paths varying across hosts (macOS app bundle vs. Linux SSH remote, for example). The PATH probe is a sanity check, not the source of truth.
- **Why steps are classified automatable vs user-required**: agents in slash-command harnesses (Claude Code, Codex) cannot trigger their own slash commands from inside a session. Pretending otherwise produces silent failures. Classifying upfront means the playbook never claims a step ran when it did not.

## Reference

- Superpowers: <https://github.com/obra/superpowers>
- Maestro: <https://maestro.sh>
- Maestro Playbooks repo: <https://github.com/RunMaestro/Maestro-Playbooks>
