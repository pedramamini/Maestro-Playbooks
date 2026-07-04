# Document 1: Analyze PR Context

## Context

- **Playbook**: PR Bot Thread Cleanup
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Loop**: {{LOOP_NUMBER}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Tasks

- [ ] **Read configured values**: Read the agent prompt for `[PR_URL]` and `[BOT_REVIEWERS]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

- [ ] Identify the target pull request from `[PR_URL]` in the agent prompt (preferred), or fall back to Maestro GitHub metadata / current task context only if the prompt is unset. Write `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CONTEXT.md` with the repository, PR number, PR URL, base branch, head branch, current remote head SHA, and the source of truth used for each field.

- [ ] Inspect the repository before changing code by checking project docs and validation hints in files such as `README*`, `CONTRIBUTING*`, `package.json`, `pnpm-workspace.yaml`, `turbo.json`, `Makefile`, `justfile`, `pyproject.toml`, `.github/workflows/*`, and any repo-specific developer guides, then append the likely fast validation commands, likely branch-level validation commands, package manager or task runner details, and any repo-specific constraints to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CONTEXT.md`.

- [ ] Check `git status --short`, the current branch, and whether the current worktree already matches the PR head branch and remote head SHA; if it does not or the tree is not safely reusable, create or switch to an isolated worktree using repo-native helpers when available and otherwise `git worktree`, then append the final worktree path, branch name, HEAD SHA, and whether a new worktree was created to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CONTEXT.md`.

- [ ] Fetch or sync the PR head branch locally, verify local `HEAD` matches the remote PR head SHA, and record any mismatch or recovery step in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CONTEXT.md`; if matching the remote head is impossible, document the exact blocker and stop without editing code.

- [ ] Create or update `{{AUTORUN_FOLDER}}/BOT_THREAD_LEDGER.md` with a short section for loop `{{LOOP_NUMBER}}` that records the starting PR URL, starting head SHA, starting worktree path, and the validation commands you expect to use later in the loop.
