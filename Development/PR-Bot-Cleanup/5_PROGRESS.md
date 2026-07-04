# Document 5: Progress Gate

## Context

- **Playbook**: PR Bot Thread Cleanup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Loop**: {{LOOP_NUMBER}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Tasks

- [ ] **Read configured values**: Read the agent prompt for `[PR_URL]` and `[BOT_REVIEWERS]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

- [ ] Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`, count how many findings remain in each status bucket, and append a concise loop summary with the current head SHA, status counts, and latest check state to `{{AUTORUN_FOLDER}}/BOT_THREAD_LEDGER.md`.

- [ ] If no `PENDING` findings remain and only `IMPLEMENTED`, `STALE`, `DUPLICATE`, `BLOCKED`, or `MANUAL` findings are left, do not reset documents 1-4 and instead write `{{AUTORUN_FOLDER}}/FINAL_SUMMARY.md` summarizing the PR URL, latest head SHA, threads resolved by bot, latest validation and check status, remaining blockers if any, and whether the PR is accept-ready.

- [ ] Exit cleanly only after `{{AUTORUN_FOLDER}}/FINAL_SUMMARY.md` states one of two outcomes explicitly: `ACCEPT_READY` when no unresolved bot threads remain, or `BLOCKED` when only precisely documented blockers or manual-review items remain.

## Reset Tasks (Only if real bot work remains)

- [ ] If `PENDING` findings still exist and they are safe for automated work, uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md` so the next loop refreshes PR metadata, branch state, and validation commands.

- [ ] If `PENDING` findings still exist and they are safe for automated work, uncheck all tasks in `{{AUTORUN_FOLDER}}/2_FIND_THREADS.md` so the next loop re-polls unresolved bot threads and current check state.

- [ ] If `PENDING` findings still exist and they are safe for automated work, uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md` so the next loop rebuilds the adjudication plan against the latest pushed head.

- [ ] If `PENDING` findings still exist and they are safe for automated work, uncheck all tasks in `{{AUTORUN_FOLDER}}/4_IMPLEMENT.md` so the next loop can execute the next smallest coherent batch.

**Important**: Leave the reset tasks above unchecked when no safe `PENDING` findings remain. That is how the pipeline exits instead of looping forever.
