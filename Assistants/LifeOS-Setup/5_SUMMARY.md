# Document 5: Summarize and Hand Off

## Context

- **Playbook**: LifeOS Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Write the human-facing summary the user actually reads — `LIFEOS_SETUP.md` — pulling together the detection, plan, install log, and verdict into a clear "here's what happened and here's your next step." This is the last document; the playbook does not loop.

The single most important thing to convey: **the automated part installed the *logistics*; the *meaning* comes from the Interview.** LifeOS only becomes yours after you run the Interview (name your assistant, capture your TELOS / current→ideal state, pull in your own sources), which seeds Pulse with real data. Until then it's a working but empty install.

## Tasks

### Task 1: Gather the artifacts

- [ ] **Read `LIFEOS_DETECT.md`, `LIFEOS_INSTALL_PLAN.md`, `LIFEOS_INSTALL_LOG.md`, and `LIFEOS_VERIFY.md`.** Reconcile them into a single coherent story: what was detected, what was planned, what ran, and the verified result.

### Task 2: Write the summary

- [ ] **Write `{{AUTORUN_FOLDER}}/LIFEOS_SETUP.md`** with:
  - **Status** — the verdict from `LIFEOS_VERIFY.md`, in plain language.
  - **What was installed** — Core (skill + ~50-skill library + `LIFEOS/` runtime + USER tree + system prompt), which enhancements, and whether the `lifeos` launch command was wired.
  - **Where** — the resolved config root, and the **scope / blast radius**: `user` scope means the skill and any hooks are shared across every Claude Code agent on this machine; `project` scope means it is isolated to this agent. Say which one plainly.
  - **Your next step** — the table below, matched to the verdict.

### Task 3: State the next step precisely

- [ ] **Give the user the exact next action** for their verdict:

  | Verdict | Next step |
  |---|---|
  | `INSTALLED-ACTIVE` / `INSTALLED-PENDING-INTERVIEW` | Launch LifeOS with the constitution — run **`lifeos`** in a fresh terminal (the alias wired in step 7). Then run **`/lifeos-setup`** and go through the **Interview**: name your assistant, capture your TELOS (current state → ideal state), pull in any notes/exports you have. That seeds Pulse with real data. |
  | `INSTALLED-UNCONSTITUTED` | Add the launch command by hand, then continue as above: `alias lifeos='bun <configRoot>/LIFEOS/TOOLS/lifeos.ts -s <configRoot>/LIFEOS/LIFEOS_SYSTEM_PROMPT.md'` (from `LIFEOS_INSTALL_LOG.md`). |
  | `INSTALLED-DEGRADED` (non-Claude harness) | You have the skill, USER tree, Pulse, and per-session context. Always-on hooks aren't wired on this harness yet (roadmap). Run `/lifeos-setup` for the Interview via the skill. |
  | `INSTALLED-PULSE-PENDING` | Bind Pulse: `launchctl load ~/Library/LaunchAgents/*lifeos*pulse*.plist` (or log out / back in), then open `http://localhost:31337`. |
  | `FAILED` | Read `LIFEOS_INSTALL_LOG.md` and `lifeos-bootstrap.out`. Nothing of yours was clobbered (the install is additive); a prior LifeOS skill, if any, is at `<skills>/LifeOS.backup-<TS>`. |
  | `BLOCKED` | Install the missing prerequisite (usually `bun`: `curl -fsSL https://bun.sh/install | bash`), then re-run this playbook. |
  | `SKIPPED` | Capability gate (chat-only assistant) or LifeOS source tree. Run from a coding harness like Claude Code, or point the agent at a non-source project. |

  Always mention: open the **Life Dashboard** at `http://localhost:31337` after the Interview (if Pulse was installed), and that plain `claude` stays vanilla — you opt into LifeOS by launching `lifeos`.

### Task 4: Print the summary and the next-step commands

- [ ] **Output the contents of `LIFEOS_SETUP.md`** as your final message so the user sees the result without opening the file.

- [ ] **End your final message with an explicit, copy-pasteable next-step block** — this is the last thing the user sees in the Maestro history, so it must name the exact commands to run, not a vague pointer. Close with a section headed **`▶ Next step`** that gives the literal command(s) for the verdict from `LIFEOS_VERIFY.md`:

  - **`INSTALLED-ACTIVE` / `INSTALLED-PENDING-INTERVIEW`** — the two commands, in order:
    ```
    lifeos            # launch Claude Code with the LifeOS constitution loaded
    /lifeos-setup     # run inside that session: finishes Setup, then the Interview (TELOS current→ideal state, seeds Pulse)
    ```
  - **`INSTALLED-UNCONSTITUTED`** — first the manual alias line from `LIFEOS_INSTALL_LOG.md` (`alias lifeos='bun <configRoot>/LIFEOS/TOOLS/lifeos.ts -s <configRoot>/LIFEOS/LIFEOS_SYSTEM_PROMPT.md'`), then `lifeos`, then `/lifeos-setup`.
  - **`INSTALLED-DEGRADED`** (non-Claude harness) — the harness's launch-with-system-prompt command, then `/lifeos-setup` for the Interview via the skill.
  - **`INSTALLED-PULSE-PENDING`** — `launchctl load ~/Library/LaunchAgents/*lifeos*pulse*.plist`, then `lifeos` + `/lifeos-setup`.
  - **`BLOCKED`** — `curl -fsSL https://bun.sh/install | bash`, then re-run this playbook.
  - **`FAILED`** — point at `LIFEOS_INSTALL_LOG.md` + `lifeos-bootstrap.out`; note the additive install clobbered nothing.
  - **`SKIPPED`** — state the gate (chat-only assistant or LifeOS source tree) and that they should run from a coding harness on a non-source project.

  The literal strings **`lifeos`** and **`/lifeos-setup`** must appear in the final message for any `INSTALLED-*` verdict — do not paraphrase them away. If Pulse was installed, add the one line: open the Life Dashboard at `http://localhost:31337` after the Interview.
