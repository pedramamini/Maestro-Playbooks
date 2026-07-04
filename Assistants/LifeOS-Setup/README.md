# LifeOS Setup Playbook

A Maestro Auto Run playbook that installs [Daniel Miessler's **LifeOS**](https://github.com/danielmiessler/LifeOS) — the AI-powered Life Operating System (formerly **PAI**, Personal AI Infrastructure) — onto a Claude Code (or other) agent. It detects the harness and config root, drives the additive install Tools to deploy Core + your chosen enhancements, wires the `lifeos` launch command, and verifies the result with real evidence.

## What changed from PAI

LifeOS **v6.0.0** is the first release under the LifeOS name, and it rearchitected the install. The old PAI playbook is obsolete because the v5 model it automated no longer exists:

| | PAI (v5) | LifeOS (v6) |
|---|---|---|
| Distribution | Full `~/.claude/` directory clone | **One self-contained skill** (`LifeOS/`) dropped into the skills dir |
| Install effect | **Clobbered** `~/.claude` → backup + `rsync` | **Additive** — backs up only a prior LifeOS skill, never your other files |
| Unattended | `PAI_TEST_AUTOMATED=1` env flag | **No flag** — the agent drives the install Tools directly and self-consents |
| Onboarding | `/interview` | **`/lifeos-setup`** (agentic Setup → Interview) |
| Config path | Hardcoded `~/.claude/PAI/` | **`DetectEnv` resolves the config root** — never assume `~/.claude` |
| Other harnesses | Skipped | **Degraded-but-real install** (skill + USER + Pulse + context; no always-on hooks yet) |
| Homepage / installer | `ourpai.ai` | `ourlifeos.ai` (installer pinned to v6.0.2) |

## What this playbook does

LifeOS installs in **two tiers**:

- **Core** (all-or-nothing) — the LifeOS skill, the ~50-skill library, the `LIFEOS/` runtime (Algorithm v6.23.0, docs, tools, statusline, USER templates), the system prompt, and the **`lifeos` launch command** that actually loads the constitution. Installing Core *is* installing LifeOS.
- **Enhancements** (à la carte) — `hooks` (recommended), `statusline`, `tooltips`, `spinnerverbs`, `agents`, `pulse` (the `:31337` Life Dashboard), `worksweep`, `derivedsync`. The `launchd`-backed ones are macOS-only.

The playbook automates the **logistics** (drop the skill, deploy Core + enhancements, wire hooks and the launch alias). It does **not** automate the **Interview** — naming your assistant, capturing your TELOS (current → ideal state), and seeding Pulse with your real data — because that is a human conversation. The user runs `/lifeos-setup` afterwards in a fresh session, exactly as the old playbook deferred to `/interview`.

1. **Detects** the harness, resolves the config root, and probes prerequisites (`curl`, `bash`, `tar`, `bun`). Writes `LIFEOS_DETECT.md`.
2. **Plans** the install path, the enhancement set, whether to wire the launch alias, and the install **scope** (`user` vs `project`). Writes `LIFEOS_INSTALL_PLAN.md`.
3. **Installs**: ensures `bun`, drops the skill, then drives `DetectEnv → ScanConflicts → DeployCore → ScaffoldUser → LinkUser → InstallHooks/DeployComponents → ActivateImports → lifeos alias`. Writes `LIFEOS_INSTALL_LOG.md` and captures `lifeos-bootstrap.out`.
4. **Verifies** with real evidence: skill + runtime present, imports resolve, `lifeos` alias wired, and each installed enhancement (Pulse → `curl :31337/healthz`). Writes `LIFEOS_VERIFY.md`.
5. **Summarizes** in `LIFEOS_SETUP.md` with the exact next step: launch `lifeos` and run the `/lifeos-setup` Interview.

This is a **linear, non-looping** playbook. Each document runs once.

## Isolation: additive ≠ isolated

LifeOS is *non-clobbering* but not *scoped* by default. This matters when you run multiple Maestro agents:

- **`user` scope** (`~/.claude`, the default) — the skill and any installed hooks land in the **shared** user config root. The LifeOS skill becomes visible to **every** Claude Code agent on the machine, and enabled hooks fire for **every** Claude Code session. Only the `lifeos` alias is opt-in-per-launch (plain `claude` stays vanilla).
- **`project` scope** (`{{AGENT_PATH}}/.claude`) — the skill and settings are scoped to this one agent; other agents are unaffected. This is the path for genuine single-agent isolation. Note: Pulse (`launchd` on `:31337`) is machine-wide regardless of scope.

Set the scope via `[INSTALL_SCOPE]` in the agent prompt.

## Provider Status

LifeOS is harness-agnostic by design (built on universal primitives — hooks, skills, context files, agentic routing). Claude Code is the most-tested path (native hooks). Other harnesses get a real but degraded install.

| Maestro `toolType` | Tier | Playbook behavior |
|---|---|---|
| `claude-code` | Full | Core + enhancements incl. native hooks + `lifeos` alias |
| `opencode` / `codex` / `gemini-cli` / other file+command harnesses | Degraded | Core + USER + Pulse + per-session context via `AGENTS.md`/rules; always-on hooks not wired yet (roadmap) |
| chat-only (no files/commands) | Blocked | Fails the capability gate; document 5 points the user at a coding harness |

## Document Chain

| Document | Purpose | Reset on Completion? |
|---|---|---|
| `1_DETECT.md` | Identify the harness, resolve the config root, probe prerequisites. Writes `LIFEOS_DETECT.md` | No |
| `2_PLAN.md` | Choose install path, enhancement set, launch-alias, and scope. Writes `LIFEOS_INSTALL_PLAN.md` | No |
| `3_INSTALL.md` | Ensure `bun`, drop the skill, drive the install Tools. Writes `LIFEOS_INSTALL_LOG.md` | No |
| `4_VERIFY.md` | Evidence-based verification. Writes `LIFEOS_VERIFY.md` | No |
| `5_SUMMARY.md` | Human summary + exact next step. Writes `LIFEOS_SETUP.md` | No |

## Generated Files

| File | Purpose |
|---|---|
| `LIFEOS_DETECT.md` | Harness, config root, prereq results, existing state |
| `LIFEOS_INSTALL_PLAN.md` | Selected path, enhancement set, scope, ordered step list |
| `LIFEOS_INSTALL_LOG.md` | Per-step outcome of the install |
| `lifeos-bootstrap.out` | Full output of the bootstrap skill-drop |
| `LIFEOS_VERIFY.md` | Verification result with an explicit verdict |
| `LIFEOS_SETUP.md` | The summary the user reads |

## Assets

- `assets/INSTALL_NOTES.md` — pinned reference of the install command, the Tools sequence, the two-tier model, the verification surface, and version pins. Documents 2–4 read this. Edit it as LifeOS's upstream install path evolves.

## Agent Prompt Configuration

The manifest `prompt` pre-fills the Auto Run panel. Configure these per run:

- **`LIFEOS_ENHANCEMENTS`** — comma-separated subset of `hooks,statusline,tooltips,spinnerverbs,agents,pulse,worksweep,derivedsync`, or `none`. Default: `hooks`.
- **`WIRE_LAUNCH_ALIAS`** — `yes` / `no`. Whether to append the `lifeos` alias so the constitution loads. Default: `yes`.
- **`INSTALL_SCOPE`** — `user` (shared `~/.claude`) or `project` (`{{AGENT_PATH}}/.claude`, isolated to this agent). Default: `user`.

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

The install runs LifeOS's TypeScript Tools under **`bun`** — the one hard requirement. The bootstrap only auto-installs `bun` when stdin is a TTY (not the case in a Maestro subprocess), so document 3 installs it first if missing:

```bash
curl -fsSL https://bun.sh/install | bash
```

`curl`, `bash`, and `tar` are needed to fetch and unpack the release; `git` and the `claude` CLI are useful but not fatal. The playbook uses `maestro-cli` to confirm the agent's `toolType`, falling back to `/Applications/Maestro.app/Contents/Resources/maestro-cli.js`.

## Template Variables Used

- `{{AGENT_NAME}}` — used to look up `toolType` via `maestro-cli`
- `{{AGENT_PATH}}` — the project root; also the `project`-scope config-root base
- `{{AUTORUN_FOLDER}}` — where all generated artifacts and `assets/` live
- `{{DATE}}` — recorded in every generated file

## Reference

- LifeOS: <https://github.com/danielmiessler/LifeOS>
- LifeOS install page: <https://ourlifeos.ai/install> (`INSTALL.md`)
- LifeOS install script: <https://ourlifeos.ai/install.sh>
- LifeOS v6.0.0 release notes: <https://github.com/danielmiessler/LifeOS/tree/main/Releases/v6.0.0>
- LifeOS docs: <https://docs.ourlifeos.ai>
- Pulse Life Dashboard: <http://localhost:31337> (after install, if `pulse` enabled)
- Maestro: <https://maestro.sh>
- Maestro Playbooks repo: <https://github.com/RunMaestro/Maestro-Playbooks>
