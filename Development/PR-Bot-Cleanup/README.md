# PR Bot Thread Cleanup Playbook

A Maestro Auto Run playbook for cleaning up unresolved PR review threads from bot reviewers such as CodeRabbit and Greptile without widening scope or trampling the branch.

## Requirements

**Agent Prompt**: This playbook works with Maestro's default agent prompt.

**GitHub Access**: Best results require Maestro's GitHub integration and a working `gh` CLI session. The playbook should prefer Maestro GitHub tools first and use `gh` only when thread-level metadata or check details are unavailable.

## Overview

This playbook creates an automated loop that:
1. Reconstructs the live PR context and local branch state
2. Finds unresolved bot-authored review threads and captures them in working artifacts
3. Evaluates each thread against the current PR head to separate stale findings from real work
4. Implements the smallest valid fix batch, validates it, pushes it, and resolves newly stale bot threads
5. Repeats until no unresolved bot threads remain or a hard blocker is documented precisely

## Document Chain

| Document | Purpose | Reset on Completion? |
|----------|---------|---------------------|
| `1_ANALYZE.md` | Reconstruct PR metadata, branch state, validation commands, and loop context | No |
| `2_FIND_THREADS.md` | Enumerate unresolved bot threads and latest GitHub check state | No |
| `3_EVALUATE.md` | Adjudicate each bot thread as stale, duplicate, real, or blocked and create the next fix plan | No |
| `4_IMPLEMENT.md` | Apply one small coherent fix batch, validate, push, and resolve now-stale bot threads | No |
| `5_PROGRESS.md` | Continue looping only when real unresolved bot work remains | **Yes** |

## Generated Files

Each loop iteration creates working documents in the Auto Run folder:

- `LOOP_{{LOOP_NUMBER}}_CONTEXT.md` - PR metadata, branch state, worktree path, validation plan
- `LOOP_{{LOOP_NUMBER}}_THREADS.md` - Unresolved bot thread inventory with URLs and file/line references
- `LOOP_{{LOOP_NUMBER}}_PLAN.md` - Thread dispositions and next implementation batch
- `BOT_THREAD_LEDGER.md` - Cumulative record of pushes, resolved thread URLs, and blockers
- `FINAL_SUMMARY.md` - Final handoff when the playbook exits cleanly

## Supported Review Bots

This playbook is intentionally bot-focused. It should:

- Include unresolved threads from CodeRabbit and Greptile
- Tolerate minor variations in bot login names
- Ignore human review threads completely
- Resolve stale bot threads only when the current PR head proves the issue is already fixed or no longer applicable

## How It Works

### Loop Control

`5_PROGRESS.md` is the gate:

- If `LOOP_{{LOOP_NUMBER}}_PLAN.md` still contains `PENDING` findings that are real and safe to fix automatically, it resets documents 1-4 and the next loop starts.
- If the only remaining items are `STALE`, `DUPLICATE`, `IMPLEMENTED`, `BLOCKED`, or `MANUAL`, it does not reset documents 1-4 and the pipeline exits.

### One Batch Per Loop

Document 4 should handle only one coherent batch per loop. That keeps validation tight, commits small, and thread resolution obvious after each push.

## Recommended Setup

### Standard Cleanup Run

```text
Loop Mode: ON
Max Loops: 10
Documents:
  1_ANALYZE.md       [Reset: OFF]
  2_FIND_THREADS.md  [Reset: OFF]
  3_EVALUATE.md      [Reset: OFF]
  4_IMPLEMENT.md     [Reset: OFF]
  5_PROGRESS.md      [Reset: ON]
```

### Review-First Dry Run

```text
Loop Mode: OFF
Run once to inspect LOOP_1_THREADS.md and LOOP_1_PLAN.md before allowing automated fixes
```

## Template Variables Used

- `{{AGENT_NAME}}` - Name of the Maestro agent
- `{{AGENT_PATH}}` - Root path of the target repository
- `{{AUTORUN_FOLDER}}` - Path to this Auto Run folder
- `{{LOOP_NUMBER}}` - Current loop iteration
- `{{DATE}}` - Current date
- `{{CWD}}` - Current working directory

## Safety Rules

1. Never resolve human review threads.
2. Never assume a bot finding is still real without checking the current PR head.
3. Never broaden scope into unrelated cleanup.
4. Never hand-wave a validation failure. Record the exact command and exact blocker.
5. Keep scratch artifacts in the Auto Run folder or other untracked working locations unless the repo already tracks a scratch area by convention.

## Tips

1. Start with Maestro GitHub tools and fall back to `gh` only when needed.
2. Match the local worktree SHA to the remote PR head before editing code.
3. Resolve stale bot threads immediately after a push while evidence is fresh.
4. Prefer focused validation before umbrella project commands.
5. Exit cleanly when only documented blockers remain.
