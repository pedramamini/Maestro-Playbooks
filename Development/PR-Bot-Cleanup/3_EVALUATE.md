# Document 3: Evaluate Findings

## Context

- **Playbook**: PR Bot Thread Cleanup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Loop**: {{LOOP_NUMBER}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Tasks

- [ ] **Read configured values**: Read the agent prompt for `[PR_URL]` and `[BOT_REVIEWERS]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

- [ ] Re-read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_THREADS.md`, inspect the current PR head for each unresolved bot thread, and create `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` with one section per thread that classifies it as `STALE`, `DUPLICATE`, `PENDING`, `BLOCKED`, or `MANUAL`, plus the concrete evidence used for that judgment.

- [ ] Resolve any bot thread that is already fixed, stale, or duplicated on the current head immediately on GitHub, record the thread URL and reason in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`, and append the same action to `{{AUTORUN_FOLDER}}/BOT_THREAD_LEDGER.md`; do not touch human review threads.

- [ ] For each thread that remains `PENDING`, search the repository for nearby existing implementations and patterns before proposing changes, then update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` with the smallest safe batch grouping so the next implementation step addresses one coherent concern only.

- [ ] For each thread that cannot be resolved safely, mark it `BLOCKED` or `MANUAL` in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` with the exact missing context, failing command, missing secret, missing dependency, or policy decision that prevents automated closure.
