# PAI Setup Playbook

A Maestro Auto Run playbook that installs [Daniel Miessler's Personal AI Infrastructure (PAI)](https://github.com/danielmiessler/Personal_AI_Infrastructure) — verifying prerequisites, classifying what the agent can automate vs. what the user must run interactively, staging the official one-liner installer, and verifying the result.

## What This Playbook Does

PAI is a "Life Operating System" — the context layer between today's agent technology and what you're trying to accomplish. It ships skills, hooks, the Algorithm, and the Pulse Life Dashboard at `http://localhost:31337`. PAI is designed to sit underneath multiple AI agent systems (the homepage at <https://ourpai.ai> lists **Claude Code**, **OpenCode**, and **Pi**, with Codex support in development), and the v5.0.0 release bootstrap installs everything to `~/.claude/`.

For Claude Code agents the playbook performs an **end-to-end unattended install**: the wizard supports `PAI_TEST_AUTOMATED=1`, which makes every prompt return its sensible default (`promptText` → empty with caller fallbacks like `User`/`PAI`; `promptChoice` → first option; `promptConfirm` → defaultYes), and the bootstrap's post-wizard `exec zsh ... pai` step gracefully degrades to a printed instruction when there is no controlling TTY. The result is a working install with placeholder identity that the user customizes afterwards by running `/interview` in a fresh Claude Code session.

For non-Claude-Code agents, the playbook short-circuits — PAI v5.0.0 ships an installable bundle for Claude Code only (Pi has a separate `Releases/Pi/` scaffold that is not a Maestro `toolType`; OpenCode is on the homepage diagram but has no shipped scaffold yet; Codex support is in development per the maintainer).

1. **Detects** the running provider, prerequisites (`curl`, `bash`, `rsync`, `tar`, `bun`), and the existing `~/.claude/` state. Writes `PAI_DETECT.md`. If the provider is not Claude Code, the playbook still runs but downstream documents short-circuit cheaply.
2. **Plans** the strategy and step list. For Claude Code: `AUTOMATED_FRESH_INSTALL` / `AUTOMATED_INSTALL_OVER_BACKUP` / `AUTOMATED_UPGRADE`. For everything else: `SKIP_NO_UPSTREAM_PATH` / `SKIP_IN_DEVELOPMENT` / `SKIP_UNSUPPORTED_OS` / `BLOCKED_PREREQ`. Writes `PAI_INSTALL_PLAN.md`.
3. **Installs**: ensures `bun` is on `PATH`, then runs `PAI_TEST_AUTOMATED=1 curl -sSL https://ourpai.ai/install.sh | bash`. Captures full bootstrap output to `pai-bootstrap.out` and the per-step outcome to `PAI_INSTALL_LOG.md`. Skipped or blocked plans short-circuit here with a one-line log.
4. **Verifies** the live state: `~/.claude/PAI/` exists, `~/.claude/PAI/ALGORITHM/LATEST` is readable, `~/Library/LaunchAgents/com.pai.pulse.plist` is loaded, `localhost:31337/api/pulse/health` responds. Writes `PAI_VERIFY.md` with one of `INSTALLED-AND-ACTIVE` / `INSTALLED-PARTIAL` / `INSTALLED-PENDING-WIZARD` / `FAILED` / `BLOCKED` / `SKIPPED`.
5. **Summarizes** in `PAI_SETUP.md` with the next step: open the Life Dashboard, then run `/interview` in a fresh Claude Code session to make the install yours.

## Provider Status

The PAI homepage lists Claude Code, OpenCode, and Pi as supported AI agent systems. As of v5.0.0, only **Claude Code** has an installable bundle in the upstream repo (`Releases/v5.0.0/.claude/`). Pi has a separate scaffold at `Releases/Pi/` that requires `npm install @mariozechner/pi-coding-agent` and a manual `cp -r` to `~/.config/PAI-pi/` — not exposed via a Maestro `toolType`. OpenCode appears in the homepage diagram but no scaffold ships in the repo. Codex support is in development per the maintainer.

| Maestro `toolType` | Status | Playbook behavior |
|---|---|---|
| `claude-code` | Installable | Automated end-to-end install via `PAI_TEST_AUTOMATED=1` |
| `opencode` | No upstream scaffold | Skip; point user at upstream for status |
| `codex` | In development | Skip; point user at upstream for status |
| `factory-droid` | Not listed | Skip |
| `copilot-cli` | Not listed | Skip |
| `gemini-cli` | Not listed | Skip |
| `qwen3-coder` | Not listed | Skip |

For non-Claude-Code agents the playbook still runs all five documents but each one short-circuits in its first task — total cost is a handful of cheap sessions producing a `PAI_SETUP.md` that explains the skip and points at the upstream repo.

## Document Chain

| Document | Purpose | Reset on Completion? |
|---|---|---|
| `1_DETECT.md` | Identify the running harness, probe prerequisites, and capture the existing `~/.claude/` state. Writes `PAI_DETECT.md` | No |
| `2_PLAN.md` | Decide install path (fresh vs. upgrade), classify steps as automatable / user-required, surface blockers. Writes `PAI_INSTALL_PLAN.md` | No |
| `3_INSTALL.md` | Run automatable prereq fixups; stage the install + wizard commands for the user. Writes `PAI_INSTALL_LOG.md` and `PAI_USER_ACTIONS.md` | No |
| `4_VERIFY.md` | Post-install verification (or honest "deferred to user" if the user has not yet run the installer). Writes `PAI_VERIFY.md` | No |
| `5_SUMMARY.md` | Human-facing summary with explicit next steps. Writes `PAI_SETUP.md` | No |

This is a **linear, non-looping** playbook. Each document runs once.

## Generated Files

| File | Purpose |
|---|---|
| `PAI_DETECT.md` | Detected provider, prereq check results, existing `~/.claude/` state |
| `PAI_INSTALL_PLAN.md` | Concrete plan with automatable / user-required classification |
| `PAI_INSTALL_LOG.md` | Outcome of any automatable steps the agent ran |
| `PAI_USER_ACTIONS.md` | Paste-ready install instructions for the user |
| `PAI_VERIFY.md` | Verification result with explicit verdict |
| `PAI_SETUP.md` | The summary the user reads |

## Assets

- `assets/INSTALL_NOTES.md` — pinned reference of the one-line install command, manual install fallback, what the wizard asks for, and the post-install verification surface (Pulse launchd label, dashboard URL, expected `~/.claude/` subtree). Documents 2-4 read this. Edit this file as PAI's upstream install path evolves.

## Recommended Setup

```text
Loop Mode: OFF
Max Loops: N/A
Documents:
  1_DETECT.md     [Reset: OFF]
  2_PLAN.md       [Reset: OFF]
  3_INSTALL.md    [Reset: OFF]
  4_VERIFY.md     [Reset: OFF]
  5_SUMMARY.md    [Reset: OFF]
```

## Prerequisites

The PAI bootstrap requires `curl`, `bash`, `rsync`, `tar`, and `bun`. The bootstrap will offer to install `bun` automatically if missing, but only when stdin is a TTY — running it inside a Maestro Bash subprocess will not satisfy that check. Install `bun` first if it is missing:

```bash
curl -fsSL https://bun.sh/install | bash
```

The bundled wizard also expects `git` and the `claude` CLI to be available; both are warned-but-not-fatal in the wizard, but installing them first avoids surprises.

The playbook itself uses `maestro-cli` to confirm the agent's `toolType`. If `maestro-cli` is unavailable on `PATH`, the playbook falls back to the macOS default path (`/Applications/Maestro.app/Contents/Resources/maestro-cli.js`).

## Outcome Statuses

`PAI_SETUP.md` will land in one of these states:

| Status | Meaning | What to do |
|---|---|---|
| **Installed** | `~/.claude/PAI/` exists, Pulse responds at `localhost:31337` | Open the dashboard, then run `/interview` in a fresh Claude Code session to customize the placeholder identity |
| **Installed (Pulse pending)** | Files in place; Pulse not yet bound to :31337 | `launchctl load ~/Library/LaunchAgents/com.pai.pulse.plist` or log out / back in |
| **Installed (wizard incomplete)** | v5 bundle copied but wizard did not finish | `cd ~/.claude && PAI_TEST_AUTOMATED=1 ./install.sh` |
| **Failed** | Bootstrap exited non-zero | Read `pai-bootstrap.out` (full output) and `PAI_INSTALL_LOG.md` (last lines + diagnosis); the prior `~/.claude/` is at `~/.claude.backup-<TS>` for restore |
| **Blocked** | Required prereq missing on the host | Read `PAI_USER_ACTIONS.md` for the prereq install commands, then re-run the playbook |
| **Skipped** | Provider not in PAI's installable upstream set, or unsupported OS | Create a Claude Code agent in Maestro and re-run |

## How the Automation Works (Claude Code)

The Claude Code path is fully automated — the agent runs the install end-to-end without prompting the user. Three things make this work:

1. **`PAI_TEST_AUTOMATED=1`** — propagated through the bootstrap to the bundled wizard. The wizard's prompt helpers (`Releases/v5.0.0/.claude/PAI/PAI-Install/cli/prompts.ts`) check this flag (or non-TTY stdin) and return sensible defaults: empty for text/secret (callers fall back to `User`/`PAI`), first-choice for picker, defaultYes for confirm. All 9 wizard steps complete: system-detect, prerequisites, api-keys, identity, repository, configuration, voice, telegram, validation.
2. **Pre-installing `bun`** — the bootstrap's bun-auto-install path requires a TTY (`[ -t 0 ]`) and CI unset. Inside a Maestro Bash subprocess that fails, so document 3 installs bun first via its own `curl … | bash`, which works without TTY. Then bun is on `PATH` and the bootstrap's bun check passes.
3. **No `/dev/tty` graceful degradation** — at the end of the wizard, the bundled `install.sh` checks `[ -r /dev/tty ]` before `exec`-ing `zsh -i -c 'pai'`. In a Maestro subprocess `/dev/tty` is not readable, so the script prints `Install complete. To start pai, run: source ~/.zshrc && pai` and exits zero. No hang.

The trade-offs the playbook accepts:

- **Generic identity**: automated runs use `principalName="User"` (or git's `user.name` if set) and `aiName="PAI"`. The user runs `/interview` afterwards to customize. This is non-blocking and the wizard's own post-install message says exactly this.
- **`~/.claude/` swap window**: the bootstrap moves `~/.claude/` → `~/.claude.backup-<TS>`, then `rsync`s the new tree in place. There's a brief window (a few seconds) where hooks/skills cannot be resolved; rarely matters because Claude Code reads them lazily and the agent running the playbook is mostly executing Bash during that window.
- **No interactive customization during install**: voice = first-picker default (will not actually speak without an ElevenLabs key, which is fine — voice falls back to desktop notifications). Telegram = skipped.

## Template Variables Used

- `{{AGENT_NAME}}` — used to look up `toolType` via `maestro-cli`
- `{{AGENT_PATH}}` — used to disambiguate when multiple agents share a name
- `{{AUTORUN_FOLDER}}` — where all generated artifacts and `assets/` live
- `{{DATE}}` — recorded in every generated file

## Reference

- PAI: <https://github.com/danielmiessler/Personal_AI_Infrastructure>
- PAI install script: <https://ourpai.ai/install.sh>
- PAI v5.0.0 release notes: <https://github.com/danielmiessler/Personal_AI_Infrastructure/tree/main/Releases/v5.0.0>
- Pulse Life Dashboard: <http://localhost:31337> (after install)
- Maestro: <https://maestro.sh>
- Maestro Playbooks repo: <https://github.com/RunMaestro/Maestro-Playbooks>
