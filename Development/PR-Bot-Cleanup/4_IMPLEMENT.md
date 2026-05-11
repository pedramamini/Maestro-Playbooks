# Document 4: Implement One Fix Batch

## Context

- **Playbook**: PR Bot Thread Cleanup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Loop**: {{LOOP_NUMBER}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Tasks

- [ ] **Read configured values**: Read the agent prompt for `[PR_URL]` and `[BOT_REVIEWERS]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

- [ ] Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`, choose the next smallest coherent group of `PENDING` findings, and implement only the minimal code changes required to address that batch while reusing existing project patterns and avoiding unrelated cleanup.

- [ ] Run focused validation for the touched files or subsystem first, then run the most relevant branch-level validation command discovered earlier, and append the exact commands, exact outcomes, and any exact blocker text to both `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` and `{{AUTORUN_FOLDER}}/BOT_THREAD_LEDGER.md`.

- [ ] If the batch changed the branch, commit and push only the current PR head branch using the repository's normal workflow, then re-poll unresolved threads from `[BOT_REVIEWERS]` plus the latest GitHub checks and append the new head SHA, resolved thread URLs, remaining unresolved counts, and latest check state to `{{AUTORUN_FOLDER}}/BOT_THREAD_LEDGER.md`.

- [ ] After the push, resolve any bot thread that is now provably stale or fixed on the pushed head, record each resolution in `{{AUTORUN_FOLDER}}/BOT_THREAD_LEDGER.md`, and update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` so completed work is marked `IMPLEMENTED`.

- [ ] If no `PENDING` findings existed at the start of this document, append a no-op note with the current head SHA and reason for skipping implementation to `{{AUTORUN_FOLDER}}/BOT_THREAD_LEDGER.md`.
