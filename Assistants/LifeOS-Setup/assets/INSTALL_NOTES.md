# LifeOS Install Notes (pinned reference)

This file is the stable reference documents 2–4 read. Edit it as LifeOS's upstream
install path evolves. Everything here reflects **LifeOS v6** (installer pinned to
**v6.0.2**, Algorithm **v6.23.0**). LifeOS was previously **PAI** (Personal AI
Infrastructure); the repo `danielmiessler/Personal_AI_Infrastructure` now redirects
to `danielmiessler/LifeOS`, and the homepage moved from `ourpai.ai` to `ourlifeos.ai`.

## The core idea (what changed from PAI v5)

LifeOS ships as **one self-contained skill** (`LifeOS/`). The install is **additive**:
it drops the skill into your skills dir and never clobbers your other files. There is
**no `PAI_TEST_AUTOMATED` flag** and **no `~/.claude/` clone/rsync** anymore. The
whole system (system prompt, Algorithm, ~50 skills, hooks, agents, Pulse, statusline,
USER + MEMORY scaffolds) rides along under the skill's `install/` payload and is placed
by TypeScript **Tools** (run under `bun`), each with permission and each non-clobbering.

## Install command

Primary (AI-native): hand `INSTALL.md` (served at `https://ourlifeos.ai/install`) to
your AI and say "install this." Terminal shortcut for Claude Code (macOS/Linux):

```bash
curl -fsSL https://ourlifeos.ai/install.sh | bash
```

The bootstrap only **drops the skill** and hands off to the agentic `/lifeos-setup`.
When run inside an existing harness (`CLAUDECODE` set), it prints the next step instead
of exec-ing a nested session — safe to run from a Maestro agent. Scope override:

```bash
LIFEOS_SKILLS_DIR="<configRoot>/skills" curl -fsSL https://ourlifeos.ai/install.sh | bash
```

Local/offline: `LIFEOS_SRC=/path/to/LIFEOS_RELEASES/<version> bash install.sh`.

## Prerequisites

- **`bun`** — hard requirement; the Tools are TypeScript. Bootstrap only auto-installs
  it with a TTY, so install first in a subprocess: `curl -fsSL https://bun.sh/install | bash`.
- `curl`, `bash`, `tar` — fetch + unpack the release.
- `git`, `claude` — useful, not fatal.

## The install Tools (run from the dropped skill dir)

Authoritative order lives in the skill's own `INSTALL.md` and `Workflows/Setup.md`.
Summary:

| Step | Tool / action | Notes |
|---|---|---|
| Detect | `bun Tools/DetectEnv.ts` | → `{os, harness, display, bun, existingInstall, isDevTree, settingsExists, claudeMdExists}`. **Stop if `isDevTree`.** |
| Scan | `bun Tools/ScanConflicts.ts` | Read-only; surfaces existing hooks, skill collisions, populated config tree. |
| Core: overlay | place files | `install/CLAUDE.template.md`→`CLAUDE.md`, `install/LIFEOS/LIFEOS_SYSTEM_PROMPT.md`, `install/settings.system.json`→`settings.json`; substitute `{{LIFEOS_VERSION}}`/`{{DA_NAME}}`/`{{PRINCIPAL_NAME}}`. |
| Core: deploy | `bun Tools/DeployCore.ts` | Dry-run, then `--apply`. Copies the ~50-skill library + `LIFEOS/` runtime. Runs **before** ScaffoldUser. Fails loud if a payload source is missing. |
| Core: user tree | `bun Tools/ScaffoldUser.ts` → `bun Tools/LinkUser.ts` | Create empty USER tree, link into harness tree. No personal content yet. |
| Enh: hooks | `bun Tools/InstallHooks.ts` | Claude Code only. Backs up `settings.json`, merges hooks additively (idempotent). Mode banner + memory + voice + context injection. |
| Enh: others | `bun Tools/DeployComponents.ts --apply --components <csv>` | Dry-run first. `statusline,tooltips,spinnerverbs,agents,pulse,worksweep,derivedsync`. `launchd` ones macOS-only. |
| Imports | `bun Tools/ActivateImports.ts` | Uncomment `@LIFEOS/...` identity imports in `CLAUDE.md`. |
| Launch cmd | append `lifeos` alias | `alias lifeos='bun <configRoot>/LIFEOS/TOOLS/lifeos.ts -s <configRoot>/LIFEOS/LIFEOS_SYSTEM_PROMPT.md'`. Back up rc first, idempotent. |

Other Tools in the skill: `InstallEngine.ts` (the shared engine `DetectEnv` wraps).

## The two-tier model

- **Core** — one consent, all-or-nothing: skill + skill library + `LIFEOS/` runtime +
  USER tree + system prompt + `lifeos` launch command. This IS LifeOS.
- **Enhancements** — à la carte: `hooks` (recommended), `statusline`, `tooltips`,
  `spinnerverbs`, `agents`, `pulse`, `worksweep`, `derivedsync`. Independently
  deployable, idempotent, reversible. `launchd` ones (pulse/worksweep/derivedsync)
  are macOS-only — skip cleanly on Linux/Windows.

## The launch command / constitution (do not skip)

The operating contract lives in `<configRoot>/LIFEOS/LIFEOS_SYSTEM_PROMPT.md` and only
loads when the harness is launched with it appended. A plain `claude` session gets
`CLAUDE.md` but **not** the constitution. The `lifeos` alias (or a harness's own
`--append-system-prompt` flag) is what turns it on. Without it, Core is installed but
launches un-constituted (no mode banner / verification / security layer).

## Verification surface

- **Core** — `<configRoot>/skills/LifeOS` exists; `<configRoot>/LIFEOS/ALGORITHM` exists;
  `@LIFEOS/...` imports in `CLAUDE.md` are active and resolve.
- **Launch** — shell rc contains `alias lifeos=` (or the user was handed the manual line).
- **hooks** — `settings.json` has a `hooks` block.
- **statusline / tooltips / spinnerverbs** — the matching `settings.json` key is set.
- **agents** — files under `<configRoot>/agents/`.
- **pulse** — `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:31337/healthz` = `200`.
- **worksweep / derivedsync** — `launchctl print` shows the label loaded.

## Config format gotcha

LifeOS config is **`.toml`**, never `.yaml` (the legacy `.yaml` template was retired
2026-06-19; `PaiConfig.ts` reads TOML).

## The Interview (not automated)

`/lifeos-setup` runs Setup (logistics — what this playbook automates) then the
**Interview** (meaning): name the assistant, capture TELOS current→ideal state, pull in
the user's own sources, seed Pulse. The Interview needs the human; run it in a fresh
session after this playbook completes.

## Reference

- Repo: <https://github.com/danielmiessler/LifeOS>
- Install page (`INSTALL.md`): <https://ourlifeos.ai/install>
- Install script: <https://ourlifeos.ai/install.sh>
- v6.0.0 release notes: <https://github.com/danielmiessler/LifeOS/tree/main/Releases/v6.0.0>
- Docs: <https://docs.ourlifeos.ai>
