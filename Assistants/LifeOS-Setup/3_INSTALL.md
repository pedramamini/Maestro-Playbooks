# Document 3: Install LifeOS

## Context

- **Playbook**: LifeOS Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Execute the plan from `LIFEOS_INSTALL_PLAN.md`: ensure `bun`, drop the LifeOS skill, then drive the install Tools to deploy **Core** + the chosen **Enhancements**, wire the `lifeos` launch command, and log everything to `LIFEOS_INSTALL_LOG.md`.

**You are the AI LifeOS is being handed to.** The user consented by launching this Auto Run, so you self-consent at each mutation and drive the Tools directly — do not wait for interactive approval. The install is **additive**: the Tools are `existsSync`-guarded / `copyMissing` / backup-before-write and never clobber a populated file. Two hard stops still apply: **never mutate the LifeOS source tree** (`isDevTree`), and **never write a harness config it won't read** (honest degrade beats an inert install).

**Source of truth for exact commands:** once the skill is dropped, the canonical, version-matched instructions ship inside it at `INSTALL.md` and `Workflows/Setup.md`. Read those and follow their exact flags/order — this document drives the sequence; the skill's own docs win on specifics.

## Tasks

### Task 1: Load the plan and short-circuit if needed

- [ ] **Read `{{AUTORUN_FOLDER}}/LIFEOS_INSTALL_PLAN.md`.** If the path is `BLOCKED_CAPABILITY_GATE` or `ABORT_DEV_TREE`, write a one-line `LIFEOS_INSTALL_LOG.md` recording the short-circuit reason and mark **all remaining tasks in this document complete without changes**. Otherwise proceed. Also read the agent prompt for `[LIFEOS_ENHANCEMENTS]`, `[WIRE_LAUNCH_ALIAS]`, and `[INSTALL_SCOPE]` if not already carried in the plan.

### Task 2: Ensure bun

- [ ] **Guarantee `bun` is on `PATH`.** If `LIFEOS_DETECT.md` reported `bun` missing, install it now (works without a TTY):

  ```bash
  command -v bun >/dev/null 2>&1 || curl -fsSL https://bun.sh/install | bash
  export PATH="$HOME/.bun/bin:$PATH"
  bun --version
  ```

  Record the resolved `bun` path/version. If `bun` still cannot be installed, mark the plan **`BLOCKED`**, log it, and skip the rest.

### Task 3: Drop the LifeOS skill

- [ ] **Place the skill additively.** For `user` scope, run the bootstrap (it fetches the pinned release, backs up only a prior LifeOS skill, drops `LifeOS/` into the skills dir, and — because you are already inside a harness (`CLAUDECODE` is set) — prints the next step instead of exec-ing a nested session):

  ```bash
  curl -fsSL https://ourlifeos.ai/install.sh 2>&1 | tee "{{AUTORUN_FOLDER}}/lifeos-bootstrap.out"
  ```

  For `project` scope, target the agent's own config tree so the skill does **not** land in the shared `~/.claude`:

  ```bash
  LIFEOS_SKILLS_DIR="{{AGENT_PATH}}/.claude/skills" curl -fsSL https://ourlifeos.ai/install.sh | bash
  ```

  Confirm the skill exists at `<configRoot>/skills/LifeOS` (record the path). Capture the full bootstrap output to `lifeos-bootstrap.out`.

### Task 4: Run the authoritative environment detection

- [ ] **From the dropped skill dir, run `bun Tools/DetectEnv.ts`** and read its JSON (`os`, `harness`, `display`, `bun`, `existingInstall`, `isDevTree`, `settingsExists`, `claudeMdExists`). **If `isDevTree` is true, STOP immediately** — log `ABORT_DEV_TREE` and skip the rest. Otherwise run `bun Tools/ScanConflicts.ts` (read-only) and record what it surfaces (existing hooks, skill-name collisions, populated config tree). Use the resolved `configRoot` from here on — **never hardcode `~/.claude`**.

### Task 5: Deploy Core

- [ ] **Install LifeOS Core (one bundle).** Following the skill's `Workflows/Setup.md`, in order:
  1. **System overlay** — place `install/CLAUDE.template.md` → `CLAUDE.md`, `install/LIFEOS/LIFEOS_SYSTEM_PROMPT.md` → the system prompt, and `install/settings.system.json` → `settings.json` (each `existsSync`-guarded; substitute `{{LIFEOS_VERSION}}` / `{{DA_NAME}}` / `{{PRINCIPAL_NAME}}` placeholders — leave identity placeholders at their defaults; the Interview fills them in later).
  2. **`bun Tools/DeployCore.ts`** — dry-run first, then `--apply`. Copies the ~50-skill library and the `LIFEOS/` runtime into `<configRoot>`. Runs **before** ScaffoldUser. Fails loud (non-zero) if a payload source is missing — do not treat a failure as a no-op.
  3. **`bun Tools/ScaffoldUser.ts`** then **`bun Tools/LinkUser.ts`** — create the empty USER tree from templates and link it into the harness tree. No personal content yet; that is the Interview.

  Record each command's outcome (applied / skipped-because-present / failed).

### Task 6: Deploy the chosen Enhancements

- [ ] **Install only the enhancements in `[LIFEOS_ENHANCEMENTS]`** (skip this task if `none`):
  - **`hooks`** (Claude Code only) → `bun Tools/InstallHooks.ts`. Backs up `settings.json`, merges the hook set additively (idempotent). This is what lights up the mode banner, memory loop, voice, and per-turn context injection.
  - **Everything else** (`statusline`, `tooltips`, `spinnerverbs`, `agents`, `pulse`, `worksweep`, `derivedsync`) → `bun Tools/DeployComponents.ts` — dry-run first, then `--apply --components <csv>` with **only** the chosen set. Skip `launchd` components (`pulse`, `worksweep`, `derivedsync`) cleanly on non-macOS.
  - **Non-Claude harness**: do **not** run `InstallHooks.ts`. Instead write an `AGENTS.md` (or the harness's rules file) pointing at the LifeOS tree so context loads every session, and record the honest degrade (always-on hooks not wired yet on this harness).

  Record which components were applied and which were skipped (and why).

### Task 7: Activate imports and wire the launch command

- [ ] **`bun Tools/ActivateImports.ts`** — uncomment the identity `@`-imports in `CLAUDE.md` (each guarded by `existsSync` of its target).
- [ ] **Wire the `lifeos` launch command** if `[WIRE_LAUNCH_ALIAS]=yes`. The constitution (`LIFEOS_SYSTEM_PROMPT.md`) only loads when the harness is launched with it appended — a plain `claude` session never sees it. Append to the shell rc (back up first, idempotent, use the real `<configRoot>` from DetectEnv — never a hardcoded home path):

  ```bash
  alias lifeos='bun <configRoot>/LIFEOS/TOOLS/lifeos.ts -s <configRoot>/LIFEOS/LIFEOS_SYSTEM_PROMPT.md'
  ```

  For a non-Claude harness, use that harness's own system-prompt flag against the same file. If `[WIRE_LAUNCH_ALIAS]=no`, skip the rc edit and record the exact one-line launch command for document 5 to hand the user instead.

### Task 8: Write the install log

- [ ] **Write `{{AUTORUN_FOLDER}}/LIFEOS_INSTALL_LOG.md`** with: the plan path executed, `bun` resolution, the skill drop path, the DetectEnv/ScanConflicts summary, per-step Core outcomes, per-component Enhancement outcomes, whether the `lifeos` alias was wired (or the manual command recorded), and any failures (with the relevant lines from `lifeos-bootstrap.out`). End with a one-line **INSTALL SUMMARY** verdict: `CORE_INSTALLED`, `CORE+ENHANCEMENTS_INSTALLED`, `DEGRADED_NO_HOOKS`, `UPDATED`, `BLOCKED`, or `ABORTED`.
