# Document 2: Plan the Install

## Context

- **Playbook**: LifeOS Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Read `LIFEOS_DETECT.md` and decide **exactly what document 3 will do**. Write the decision to `LIFEOS_INSTALL_PLAN.md`.

LifeOS installs in **two tiers**, and the plan must reflect that:

- **Core** — one bundle, all-or-nothing: the LifeOS skill, the ~50-skill library, the `LIFEOS/` runtime (Algorithm, docs, tools, statusline, version, USER templates), the system prompt, and the `lifeos` launch command that actually loads it. Installing Core *is* installing LifeOS; declining Core means not installing LifeOS.
- **Enhancements** — à la carte, some/all/none: `hooks`, `statusline`, `tooltips`, `spinnerverbs`, `agents`, `pulse`, `worksweep`, `derivedsync`. Each is independently deployable, idempotent, and reversible. The `launchd`-backed ones (`pulse`, `worksweep`, `derivedsync`) are macOS-only.

The agent running this playbook **is** "the AI you hand LifeOS to." The user consented by launching this Auto Run, so document 3 self-consents at each mutation and drives the install Tools directly — it does not pause for interactive approval. The one thing that genuinely cannot be automated is the **Interview** (naming your assistant, capturing your TELOS / current→ideal state, seeding Pulse with your real data). That stays a human conversation the user runs afterwards. This playbook automates the *logistics*, not the *meaning*.

## Tasks

### Task 1: Read the config from the agent prompt

- [ ] **Read the agent prompt for `[LIFEOS_ENHANCEMENTS]`, `[WIRE_LAUNCH_ALIAS]`, and `[INSTALL_SCOPE]`.** These are set in the Auto Run panel prompt when the playbook is launched. Record the resolved values (fall back to the defaults below if the prompt does not set them):
  - **`[LIFEOS_ENHANCEMENTS]`** — comma-separated subset of `hooks,statusline,tooltips,spinnerverbs,agents,pulse,worksweep,derivedsync`, or `none`. Default: `hooks`.
  - **`[WIRE_LAUNCH_ALIAS]`** — `yes` / `no`. Whether document 3 appends the `lifeos` alias to the shell rc so the constitution loads. Default: `yes`.
  - **`[INSTALL_SCOPE]`** — `user` (install into the shared `~/.claude`, visible to every Claude Code agent on this machine) or `project` (install into `{{AGENT_PATH}}/.claude`, scoped to this agent only). Default: `user`. See the isolation note below.

### Task 2: Read detection and choose the path

- [ ] **Read `{{AUTORUN_FOLDER}}/LIFEOS_DETECT.md`** and select one install path:

  | Detected state | Plan |
  |---|---|
  | `chat-only-blocked` (no file/command access) | **`BLOCKED_CAPABILITY_GATE`** — cannot install from here; document 5 tells the user to run from a coding harness. |
  | LifeOS source tree (`isDevTree`) | **`ABORT_DEV_TREE`** — never mutate the maintainer's source. Document 3 stops. |
  | `bun` missing | Plan still proceeds; document 3 installs `bun` first (its own `curl … | bash`, works without a TTY). Note it as a **prereq step**, not a blocker. |
  | Existing LifeOS skill/runtime present | **`UPDATE`** — idempotent re-overlay (Tools are `copyMissing`/backup-before-write; nothing gets clobbered). |
  | Claude Code, fresh | **`FRESH_CORE`** + chosen enhancements + `lifeos` alias. Full always-on tier. |
  | Other harness (Cursor/Cline/Codex/Gemini), fresh | **`FRESH_CORE_DEGRADED`** — Core installs; `hooks` are a Claude Code mechanism and are **not** wired on other harnesses. Instead write an `AGENTS.md` / rules file pointing the harness at the LifeOS tree, and use the harness's own system-prompt flag for the constitution. |

### Task 3: Resolve the concrete step list

- [ ] **Write the ordered step list document 3 will execute**, resolved against the chosen path and the config values. The canonical Core sequence (defer to the skill's own `INSTALL.md` and `Workflows/Setup.md` for exact flags, since they ship in the payload and are authoritative):

  1. Ensure `bun` on `PATH`.
  2. Drop the skill (bootstrap `curl -fsSL https://ourlifeos.ai/install.sh | bash`, or a scope-targeted fetch for `project` scope).
  3. `bun Tools/DetectEnv.ts` — authoritative env; **stop if `isDevTree`**.
  4. `bun Tools/ScanConflicts.ts` — read-only conflict surface.
  5. **Core**: system overlay (`CLAUDE.md`, `LIFEOS_SYSTEM_PROMPT.md`, `settings.system.json`) → `bun Tools/DeployCore.ts` (dry-run then `--apply`) → `bun Tools/ScaffoldUser.ts` → `bun Tools/LinkUser.ts`.
  6. **Enhancements** (only the chosen set): `hooks` → `bun Tools/InstallHooks.ts`; everything else → `bun Tools/DeployComponents.ts --apply --components <csv>`. Skip `launchd` components on non-macOS.
  7. `bun Tools/ActivateImports.ts` — turn on the identity `@`-imports.
  8. If `[WIRE_LAUNCH_ALIAS]=yes`: append the `lifeos` alias to the shell rc (back up first, idempotent).

  For **`FRESH_CORE_DEGRADED`**, substitute step 6's `hooks` with the `AGENTS.md`/rules pointer and note the honest degrade.

### Task 4: Record the isolation decision

- [ ] **Document the scope explicitly.** LifeOS is *additive* (non-clobbering) but not *isolated* by default:
  - **`user` scope** (`~/.claude`): the skill and any installed hooks land in the **shared** user config root — the LifeOS skill becomes visible to *every* Claude Code agent on this machine, and enabled hooks fire for *every* Claude Code session. Only the `lifeos` alias is opt-in-per-launch (plain `claude` stays vanilla).
  - **`project` scope** (`{{AGENT_PATH}}/.claude`): the skill and settings are scoped to this project/agent, so other agents are unaffected. This is the isolation path. Note that Pulse (`launchd` on `:31337`) is machine-wide regardless of scope.

  Record which scope was chosen and its blast radius so document 5 can report it honestly.

### Task 5: Write the plan

- [ ] **Write `{{AUTORUN_FOLDER}}/LIFEOS_INSTALL_PLAN.md`** containing: the selected path, the resolved config root, the chosen enhancement set, whether the launch alias will be wired, the install scope + blast radius, the ordered step list from Task 3, and a one-line **PLAN SUMMARY**. If the path is `BLOCKED_CAPABILITY_GATE` or `ABORT_DEV_TREE`, say so plainly and stop — document 3 will short-circuit.
