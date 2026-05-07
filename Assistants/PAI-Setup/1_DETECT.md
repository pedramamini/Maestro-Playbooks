# Document 1: Detect Provider and Probe Environment

## Context

- **Playbook**: PAI Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Identify the harness this agent is running inside, capture the state of `~/.claude/`, and probe the prerequisites the PAI bootstrap will need. The bootstrap installs to `~/.claude/` regardless of harness; the detected provider mostly informs the post-install guidance the user gets in document 5.

Per the PAI homepage, supported AI agent systems are Claude Code, OpenCode, and Pi (Codex support is in development per the maintainer). For Maestro agents, expected `toolType` values are `claude-code`, `opencode`, `codex`, `factory-droid`, `copilot-cli`, `gemini-cli`, `qwen3-coder`. Document 2 will use the value recorded here to decide whether to proceed with the bootstrap or skip cleanly with an upstream pointer.

## Tasks

### Task 1: Self-identify

- [ ] **State your harness**: You are running inside an AI coding harness right now. Without checking files, name the harness you are running inside (Claude Code, Codex, OpenCode, Factory Droid, GitHub Copilot CLI, Gemini CLI, Qwen3 Coder, or other). If you are uncertain, say so explicitly — do not guess.

### Task 2: Cross-check via Maestro

- [ ] **Look up your Maestro `toolType`**: The agent name is `{{AGENT_NAME}}`. Use the first command that works:

  ```bash
  maestro-cli list agents --json
  ```

  Fallback if `maestro-cli` is not on `PATH` (macOS default):

  ```bash
  node "/Applications/Maestro.app/Contents/Resources/maestro-cli.js" list agents --json
  ```

  Find the entry whose `name` matches `{{AGENT_NAME}}`. If multiple agents share the name, narrow by `cwd` matching `{{AGENT_PATH}}`. Read the matching record's `toolType` field. Record the value (or `unavailable` if both commands failed).

### Task 3: Cross-check via binary on PATH

- [ ] **Probe for the Claude CLI**:

  ```bash
  which claude || true
  ```

  A `claude` binary on `PATH` is corroborating evidence (and is what the PAI bundled installer probes for). Absence is not blocking — Claude Code is also available as a desktop / IDE-extension harness whose CLI may not be in the agent's `PATH`.

### Task 4: Probe prerequisites for the PAI bootstrap

- [ ] **Run each prereq probe** and record the version (or `not-found`):

  ```bash
  uname -s
  curl --version | head -1
  bash --version | head -1
  rsync --version | head -1
  tar --version | head -1
  bun --version 2>/dev/null || echo not-found
  git --version 2>/dev/null || echo not-found
  ```

  - `curl`, `bash`, `rsync`, `tar` → required by the bootstrap. Missing any of these is a hard blocker.
  - `bun` → required by the bundled wizard. Absent is **recoverable** but it is best for the user to install it before running the bootstrap (the bootstrap's auto-install path requires a TTY and is not reliable from a Maestro Bash subprocess).
  - `git` → not required by the v5.0.0 bootstrap (it streams a tarball over HTTPS), but the bundled wizard checks for it and tries to install it via `brew` / `apt-get` / `yum` if missing. Note its presence either way.

  - Record the OS (`Darwin` is fully supported; `Linux` is partial — Pulse menu bar is macOS-only; anything else is unsupported).

### Task 5: Check the existing `~/.claude/` state

- [ ] **Determine whether `~/.claude/` already exists** and characterize it:

  ```bash
  if [ -e "$HOME/.claude" ]; then
    echo "EXISTS"
    ls -la "$HOME/.claude" | head -30
    [ -d "$HOME/.claude/PAI" ] && echo "PAI_PRESENT" || echo "PAI_ABSENT"
    [ -f "$HOME/.claude/install.sh" ] && echo "BUNDLE_INSTALLER_PRESENT" || echo "BUNDLE_INSTALLER_ABSENT"
  else
    echo "MISSING"
  fi
  ```

  If `~/.claude/PAI/` already exists, this is an **upgrade** scenario. If `~/.claude/` exists without a `PAI/` subdirectory, the user has a non-PAI Claude Code config that the bootstrap will back up and replace. If it does not exist at all, this is a clean install.

  - If the directory exists, also probe its size (`du -sh "$HOME/.claude" 2>/dev/null`) — a multi-GB existing directory is worth flagging so the user knows their backup will be large.

### Task 6: Reconcile and write `PAI_DETECT.md`

- [ ] **Pick one provider with confidence**: Reconcile self-identification, the Maestro `toolType` lookup, and the `which claude` probe. They should agree. If they disagree, prefer the Maestro `toolType`.

- [ ] **Write `{{AUTORUN_FOLDER}}/PAI_DETECT.md`** with this exact structure:

  ```markdown
  # PAI Setup — Detection

  - **Provider (Maestro toolType)**: <claude-code | codex | opencode | factory-droid | copilot-cli | gemini-cli | qwen3-coder | unknown>
  - **Confidence**: <high | medium | low>
  - **PAI Status**: <native (claude-code) | listed-by-upstream (opencode) | in-development (codex) | not-listed (other)>
  - **Detected on**: {{DATE}}

  ## Provider signals

  ### Self-identification
  <one line>

  ### Maestro toolType lookup
  - Command used: `<the command that worked, or "both failed">`
  - Matched `toolType`: `<value | unavailable>`

  ### `which claude`
  - `claude`: `<path | not-found>`

  ## Platform

  - OS: `<Darwin | Linux | other>`
  - Pulse menu bar supported: <yes (Darwin) | no (Linux/other)>

  ## Prerequisites

  | Tool | Status | Notes |
  |---|---|---|
  | `curl` | <version | MISSING> | required |
  | `bash` | <version | MISSING> | required |
  | `rsync` | <version | MISSING> | required |
  | `tar` | <version | MISSING> | required |
  | `bun` | <version | MISSING> | required by wizard; install before bootstrap |
  | `git` | <version | not-found> | wizard tries to auto-install if missing |

  ## Existing `~/.claude/`

  - State: <MISSING | EXISTS_WITHOUT_PAI | EXISTS_WITH_PAI>
  - Size: `<du -sh output | n/a>`
  - PAI directory present: <yes | no>
  - Bundled installer (`install.sh`) present: <yes | no>
  - Notes: <one line; e.g. "Bootstrap will move this to ~/.claude.backup-{TIMESTAMP}" or "First-time install">

  ## Reconciliation Notes

  <1-3 sentences. If signals disagreed, explain why you chose the value above. If confidence is medium or low, say what would raise it.>
  ```

## Success Criteria

- A single canonical provider value is recorded.
- All prerequisite rows are filled in (with `MISSING` / `not-found` where applicable).
- The `~/.claude/` state row is one of the three canonical values.
- The **PAI Status** field reflects the upstream support state:
  - `claude-code` → `native`
  - `opencode` → `listed-by-upstream`
  - `codex` → `in-development`
  - everything else → `not-listed`

## Fast-skip path

If you record `PAI Status` as anything other than `native` (claude-code), or if a required prereq (`curl` / `bash` / `rsync` / `tar`) is `MISSING`, or if the OS is neither `Darwin` nor `Linux`, the playbook short-circuits at this document via the Auto Run **halt marker** (Maestro `0.16.17-RC`+). Documents 2-5 will not run. Complete the next task before stopping.

### Task 7: Halt-and-summarize for skip branches

- [ ] **Decide whether to halt**. Halt when any of the following is true:

  - `PAI Status` is not `native` (i.e. provider is `opencode`, `codex`, `factory-droid`, `copilot-cli`, `gemini-cli`, `qwen3-coder`, or `unknown`). PAI v5.0.0 ships an installable bundle for Claude Code only.
  - OS is not `Darwin` or `Linux`.
  - A required prereq (`curl` / `bash` / `rsync` / `tar`) is `MISSING`.

  If none of those are true (provider is `claude-code`, OS supported, all required prereqs present), **do not halt** — skip the rest of this task and let document 2 take over.

- [ ] **Write a complete `PAI_SETUP.md` now.** Documents 2-5 will not run, so the summary must come from this document. Use this structure (do not include all five branches — pick the one that applies):

  ```markdown
  # PAI Setup — Summary

  - **Agent**: {{AGENT_NAME}}
  - **Provider**: <detected provider>
  - **Date**: {{DATE}}
  - **Status**: <Skipped | Blocked>
  - **Reason**: <one line>

  ---

  ## What is PAI?

  [Personal AI Infrastructure (PAI)](https://github.com/danielmiessler/Personal_AI_Infrastructure) is a Life Operating System — the context layer between today's agent technology and what you are trying to accomplish. The upstream homepage lists Claude Code, OpenCode, and Pi as supported AI agent systems, with Codex support in development. As of v5.0.0, the installable bundle ships only for Claude Code.

  ## Why this playbook stopped

  <Pick the one that matches:

   - "Provider is `<value>`. PAI's upstream repo does not currently ship an installable bundle for this harness. Watch <https://github.com/danielmiessler/Personal_AI_Infrastructure> for status, or create a Claude Code agent in Maestro and re-run this playbook."

   - "Provider is Codex. Codex support is in development per the maintainer; no install path exists yet. Check <https://github.com/danielmiessler/Personal_AI_Infrastructure> and re-run when it ships."

   - "OS is `<value>`. PAI v5.0.0 supports macOS (full) and Linux (full); Windows is not supported. See <https://github.com/danielmiessler/Personal_AI_Infrastructure/blob/main/PLATFORM.md>."

   - "Required prerequisite missing: `<tool>`. Install it (see PAI_DETECT.md for the version probe), then remove the halt marker from `1_DETECT.md` and re-run the playbook."
  >

  ## Re-running this playbook

  This document carries a `<!-- maestro:halt: ... -->` marker at the bottom. Maestro will refuse to launch the playbook again until the marker is removed (this is intentional — it forces acknowledgement of the halt). Edit `{{AUTORUN_FOLDER}}/1_DETECT.md`, delete the trailing `<!-- maestro:halt: ... -->` line, and launch again.

  ## Reference

  - PAI: <https://github.com/danielmiessler/Personal_AI_Infrastructure>
  - Maestro Playbooks: <https://github.com/RunMaestro/Maestro-Playbooks>
  ```

- [ ] **Append the halt marker to the bottom of `1_DETECT.md`** (this is the document you are currently in). Use `Edit` to append a line with the format:

  ```text
  <!-- maestro:halt: <one-line reason matching the summary's Reason field> -->
  ```

  Example reasons:

  - `<!-- maestro:halt: provider is qwen3-coder; PAI ships installer for claude-code only -->`
  - `<!-- maestro:halt: provider is codex; PAI codex support in development upstream -->`
  - `<!-- maestro:halt: required prereq missing: rsync -->`
  - `<!-- maestro:halt: unsupported OS: Windows -->`

  After the marker is in the file, the Auto Run engine will detect it on the next dispatch boundary and stop the playbook. Do **not** mark this task `[x]` if a precondition is unfinishable in a way the user must inspect — leave `[ ]` so the user can see the exact stopping point. For the skip cases above, the task IS finished from this document's perspective (you wrote the summary and emitted the marker), so check it.

## Status

Mark complete when `PAI_DETECT.md` exists and contains all sections.

---

**Next**: Document 2 reads `PAI_DETECT.md` and the install notes asset to produce a concrete plan, including a clean exit if the provider is not Claude Code.
