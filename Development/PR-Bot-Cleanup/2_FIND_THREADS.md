# Document 2: Find Unresolved Bot Threads

## Context

- **Playbook**: PR Bot Thread Cleanup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Loop**: {{LOOP_NUMBER}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Tasks

- [ ] Re-read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CONTEXT.md`, then query the current PR using Maestro GitHub tools first and `gh` only if needed, and create `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_THREADS.md` containing the current PR URL, head SHA, and one section for each unresolved bot-authored review thread with bot name, comment URL, file path, line reference when available, a concise issue summary, and the raw unresolved status.

- [ ] Include unresolved threads from CodeRabbit and Greptile even if their login names vary slightly, but exclude human review threads entirely; if thread-level unresolved state is unavailable from Maestro tools, use `gh api graphql` or another minimal `gh` query and record that fallback in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_THREADS.md`.

- [ ] Query the latest meaningful GitHub check state for the PR head SHA using Maestro GitHub tools first and `gh` fallback second, then append the check summary, any failing job names, and any obvious environment-only caveats to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_THREADS.md`.

- [ ] If zero unresolved bot threads are found, append an explicit zero-count summary for each supported bot to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_THREADS.md` so later documents can exit cleanly without guessing.
