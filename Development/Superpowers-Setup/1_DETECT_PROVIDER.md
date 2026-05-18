# Document 1: Detect Provider

## Context

- **Playbook**: Superpowers Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Identify which AI coding harness this playbook is running inside. Every later step branches on this single fact.

The agent running this playbook **is** the harness we are setting up. Detection is therefore introspective — the agent knows its own identity by virtue of being it. We cross-check that self-identification against the harness's CLI binary on `PATH` as a sanity check, then map the result to one of Maestro's canonical agent types: `claude-code`, `codex`, `opencode`, `factory-droid`, `copilot-cli`, `gemini-cli`, `qwen3-coder`.

## Tasks

### Task 1: Self-identify

- [ ] **State your harness**: You are running inside an AI coding harness right now. Without checking files, name the harness you are running inside (Claude Code, Codex, OpenCode, Factory Droid, GitHub Copilot CLI, Gemini CLI, Qwen3 Coder, or other). If you are uncertain, say so explicitly — do not guess. Also map your answer to the canonical Maestro `toolType` value (`claude-code`, `codex`, `opencode`, `factory-droid`, `copilot-cli`, `gemini-cli`, or `qwen3-coder`).

### Task 2: Cross-check via binary on PATH

- [ ] **Probe for harness CLIs**: Run each of these and record which succeed (exit 0 with a real path):

  ```bash
  which claude    || true
  which codex     || true
  which opencode  || true
  which droid     || true
  which copilot   || true
  which gemini    || true
  which qwen      || true
  ```

  A binary on `PATH` is corroborating evidence but not proof of which harness is currently driving this session — multiple harnesses may be installed on the same machine. Some harnesses (notably some Claude Code distributions) do not require their CLI on `PATH` at all, so a not-found result for the self-identified harness is not necessarily wrong.

### Task 3: Reconcile and write `PROVIDER.md`

- [ ] **Pick one provider with confidence**: Reconcile self-identification against the PATH probe. The self-identification is authoritative — you know what you are. The PATH probe is a sanity check that should not contradict it; if it does (e.g. you self-identified as Claude Code but found `codex` on `PATH` and not `claude`), state the discrepancy in the notes and degrade confidence to `medium`.

- [ ] **Write `{{AUTORUN_FOLDER}}/PROVIDER.md`** with this exact structure:

  ```markdown
  # Detected Provider

  - **Provider (Maestro toolType)**: <claude-code | codex | opencode | factory-droid | copilot-cli | gemini-cli | qwen3-coder | unknown>
  - **Confidence**: <high | medium | low>
  - **Detected on**: {{DATE}}

  ## Signals

  ### Self-identification
  <one-line description of what the agent identifies as, including the canonical toolType mapping>

  ### PATH probe
  - `claude`: `<path or not-found>`
  - `codex`: `<path or not-found>`
  - `opencode`: `<path or not-found>`
  - `droid`: `<path or not-found>`
  - `copilot`: `<path or not-found>`
  - `gemini`: `<path or not-found>`
  - `qwen`: `<path or not-found>`

  ## Reconciliation Notes
  <1-3 sentences. If self-identification and PATH probe disagreed, explain. If confidence is medium or low, say what would raise it.>

  ## Supported by Superpowers?
  <yes | no | partial>

  - `claude-code`, `codex`, `opencode`, `factory-droid`, `copilot-cli`, `gemini-cli` → yes
  - `qwen3-coder` → no (no upstream install path documented)
  - `unknown` → no (cannot proceed; document 2 will exit cleanly)
  ```

## Success Criteria

- A single canonical provider value is recorded in `PROVIDER.md`.
- Both signal sections are filled in (with `not-found` where applicable).
- Confidence is honestly stated.

## Status

Mark complete when `PROVIDER.md` exists and contains all four sections.

---

## Fast-skip path (Maestro 0.16.17-RC+)

If the detected provider has no upstream Superpowers install path (currently: `qwen3-coder`, or `unknown` when detection is inconclusive), the playbook short-circuits at this document via the Auto Run **halt marker**. Documents 2-5 will not run; the summary must come from this document.

### Task 4: Halt-and-summarize for unsupported providers

- [ ] **Decide whether to halt**. Halt when **either** is true:

  - The canonical provider value is `qwen3-coder` (no documented Superpowers install path upstream).
  - The canonical provider value is `unknown` (detection is inconclusive — self-identification was uncertain and the PATH probe could not confirm any single harness).

  Otherwise — provider is one of `claude-code`, `codex`, `opencode`, `factory-droid`, `copilot-cli`, `gemini-cli` — **do not halt**. Skip the rest of this task and let document 2 read the recipe.

- [ ] **Write `{{AUTORUN_FOLDER}}/SUPERPOWERS_SETUP.md` now** (since documents 2-5 will not run):

  ```markdown
  # Superpowers Setup — Summary

  - **Agent**: {{AGENT_NAME}}
  - **Provider**: <qwen3-coder | unknown>
  - **Date**: {{DATE}}
  - **Status**: Skipped

  ---

  ## What is Superpowers?

  [Superpowers](https://github.com/obra/superpowers) is a software-development methodology delivered to coding agents as a bundle of composable skills (brainstorming, writing-plans, using-git-worktrees, test-driven-development, requesting-code-review, finishing-a-development-branch, and more). Skills trigger based on context, so the agent gains a built-in TDD/YAGNI/DRY workflow and can run autonomously for longer without losing the plan.

  ## Why this playbook stopped

  <Pick the one that matches:

   - "Provider is Qwen3 Coder. Superpowers' upstream repo does not document an install path for this harness as of the date this playbook was authored. Check <https://github.com/obra/superpowers> for community-contributed paths."

   - "Provider could not be confidently identified. Self-identification was uncertain and the PATH probe did not confirm any single harness. Re-run this playbook in an agent whose harness is clearly one of: Claude Code, Codex, OpenCode, Factory Droid, GitHub Copilot CLI, Gemini CLI."
  >

  ## Re-running this playbook

  This document (`1_DETECT_PROVIDER.md`) carries a `<!-- maestro:halt: ... -->` marker at the bottom. Maestro will refuse to launch the playbook again until the marker is removed (the safety belt prevents silent replays of halted work). Edit `{{AUTORUN_FOLDER}}/1_DETECT_PROVIDER.md`, delete the trailing `<!-- maestro:halt: ... -->` line, and launch again.

  ## Reference

  - Superpowers: <https://github.com/obra/superpowers>
  - Maestro Playbooks: <https://github.com/RunMaestro/Maestro-Playbooks>
  ```

- [ ] **Append the halt marker to the bottom of `1_DETECT_PROVIDER.md`** using `Edit`:

  ```text
  <!-- maestro:halt: provider is <qwen3-coder|unknown>; no upstream Superpowers install path -->
  ```

  Auto Run detects this on the next dispatch boundary and stops the playbook.

---

**Next**: Document 2 reads `PROVIDER.md` and the install recipe to produce a concrete plan (only if the playbook did not halt above).
