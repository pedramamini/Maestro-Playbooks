# Document 3: Install

## Context

- **Playbook**: Superpowers Setup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Execute the **Automatable Steps** from `INSTALL_PLAN.md`, capture results, and stage the **User-Required Steps** as a single clean checklist the user can paste into their harness.

## Inputs

- `{{AUTORUN_FOLDER}}/INSTALL_PLAN.md` — produced by document 2

## Tasks

### Task 1: Load the plan

- [ ] **Read `INSTALL_PLAN.md`**. If it has a non-empty **Skip / Block** section, do not run any install steps. Write `{{AUTORUN_FOLDER}}/INSTALL_LOG.md` with a single line:

  ```text
  SKIPPED: <reason from Skip / Block>
  ```

  Then mark all remaining tasks in this document complete and exit.

### Task 2: Execute automatable steps

- [ ] **Run each automatable step in order**. For each step:
  - Run the exact command (Bash) or perform the exact file edit (Edit / Write) as written in the plan.
  - Capture stdout/stderr (or the diff) verbatim.
  - Stop on the first failure. Do not invent recovery commands.

- [ ] **Provider-specific notes** (apply only to your detected provider):

  - **`opencode`**: when editing `opencode.json`, parse it as JSON, mutate the in-memory object, and write it back as valid JSON with 2-space indentation. Do not use string-replace on the JSON. If the file does not exist, create it with `{ "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"] }`. If `plugin` is present but is not an array, surface this as a failure rather than overwriting it — it likely means the user has a customized config we should not silently rewrite.

  - **`gemini-cli` / `copilot-cli` / `factory-droid`**: run the documented shell commands. If the marketplace-add step fails because the marketplace is already added, treat that as success and continue to the install step. Any other non-zero exit is a real failure — record it and stop.

  - **`claude-code` / `codex`**: there are no automatable steps for these providers (the install is fully user-required). Skip directly to Task 3.

### Task 3: Stage user-required steps

- [ ] **Compose `{{AUTORUN_FOLDER}}/USER_ACTIONS.md`** containing only the user-required steps from the plan, in the exact order the user should perform them. Use this structure (the outer fence here uses four backticks so the inner three-backtick fences render correctly — replicate that when you write the file):

  ````markdown
  # User Actions Required

  Superpowers cannot finish installing without these interactive steps. Run them in your **<provider>** session in this order.

  ## Steps

  1. <one-line description>

     ```text
     <exact command to paste>
     ```

     Expected result: <one line>

  2. ...

  ## Verification

  After completing the steps above, run this in your **<provider>** session:

  ```text
  Tell me about your superpowers
  ```

  The agent should respond with a description of the bundled skills (brainstorming, writing-plans, using-git-worktrees, test-driven-development, etc.).
  ````

  If the provider has zero user-required steps, write `USER_ACTIONS.md` with a single line: `No user actions required — installation is complete.`

### Task 4: Write the install log

- [ ] **Write `{{AUTORUN_FOLDER}}/INSTALL_LOG.md`** summarizing what happened:

  ```markdown
  # Install Log

  - **Provider**: <value>
  - **Date**: {{DATE}}

  ## Automatable Steps Executed
  <Numbered list. For each: the step description, the command or file edit performed, and "OK" or "FAILED: <reason>". If no automatable steps existed, write "(none)".>

  ## User-Required Steps Staged
  <"See USER_ACTIONS.md" or "(none)".>

  ## Files Modified
  <Bulleted list of any files this document changed, with absolute paths. Empty list is fine.>

  ## Outcome
  <one of: "AUTOMATED_COMPLETE" (all steps automatable and succeeded) | "AWAITING_USER" (automatable steps done, user-required steps staged) | "FAILED" (an automatable step failed) | "SKIPPED" (provider unsupported or prerequisite missing)>
  ```

## Success Criteria

- `INSTALL_LOG.md` exists with an explicit **Outcome** value.
- If user-required steps existed, `USER_ACTIONS.md` exists and is paste-ready.
- All file edits are valid (e.g. `opencode.json` still parses as JSON).

## Status

Mark complete when `INSTALL_LOG.md` records the outcome.

---

**Next**: Document 4 verifies the install (where verifiable without the user) and notes anything the user still needs to do.
