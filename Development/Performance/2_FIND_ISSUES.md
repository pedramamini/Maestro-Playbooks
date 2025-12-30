# Performance Issue Discovery

## Context
- **Playbook:** Performance
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Execute ONE tactic from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md` to find specific performance issues. Output findings to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md`** to see available investigation tactics
2. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`** (if it exists) to see which tactics have already been executed
3. **Select ONE unexecuted tactic** from the game plan
4. **Execute the tactic**: Search the codebase using the specified patterns
5. **Document findings** in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`

## Task

- [ ] **Execute one tactic (or mark exhausted)**: Read {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md and check for unexecuted tactics. If ALL tactics are already marked `[EXECUTED]`, append a section `## ALL_TACTICS_EXHAUSTED` to {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md and mark this task complete. Otherwise, pick one unexecuted tactic, search the codebase for matching issues, append findings to {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md, and mark the tactic as `[EXECUTED]` in the game plan.

## Output Format

Append to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md` using this format:

```markdown
---

## [Tactic Name] - Executed [YYYY-MM-DD HH:MM]

### Finding 1: [Brief Title]
- **File:** `path/to/file.ext`
- **Line(s):** [line numbers or range]
- **Pattern Found:** [The specific code pattern that matches]
- **Context:** [Brief explanation of what this code does]

### Finding 2: [Brief Title]
...

### Tactic Summary
- **Issues Found:** [count]
- **Files Affected:** [count]
- **Status:** EXECUTED
```

## Guidelines

- **One tactic per run**: Only execute ONE tactic, then stop. This allows the pipeline to iterate.
- **Be thorough within the tactic**: Search comprehensively for the pattern specified
- **Include context**: Don't just list line numbers - explain what the code does
- **Skip false positives**: If a match isn't actually a performance issue, don't include it
- **Mark as executed**: Update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md` to show which tactics have been run (add `[EXECUTED]` prefix)

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Executed a tactic:**
1. You've executed exactly ONE tactic from the game plan
2. You've appended all findings to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`
3. You've marked the tactic as `[EXECUTED]` in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md`

**Option B - All tactics exhausted:**
1. All tactics in the game plan are already marked as `[EXECUTED]`
2. You've appended `## ALL_TACTICS_EXHAUSTED` to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`

The `ALL_TACTICS_EXHAUSTED` marker signals to downstream documents that discovery is complete.
