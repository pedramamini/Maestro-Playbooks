# Refactoring Discovery - Find Specific Issues

## Context
- **Playbook:** Refactor
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Execute ONE tactic from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md` to find specific refactoring candidates. Output findings to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md`** to see available investigation tactics
2. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`** (if it exists) to see which tactics have already been executed
3. **Select ONE unexecuted tactic** from the game plan
4. **Execute the tactic**: Search the codebase using the specified patterns
5. **Document findings** in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`

## Task

- [ ] **Read configured values**: Read the agent prompt for `[MAX_FILE_LOC]`, `[MAX_FUNCTION_LOC]`, `[MAX_NESTING_DEPTH]`, `[MAX_PARAMETERS]`, `[AUTO_IMPLEMENT_RISK]`, and `[AUTO_IMPLEMENT_BENEFIT]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

- [ ] **Execute one tactic (or mark exhausted)**: Read {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md and check for unexecuted tactics. If ALL tactics are already marked `[EXECUTED]`, append a section `## ALL_TACTICS_EXHAUSTED` to {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md and mark this task complete. Otherwise, pick one unexecuted tactic, search the codebase for matching issues, append findings to {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md, and mark the tactic as `[EXECUTED]` in the game plan.

## Output Format

Append to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md` using this format:

```markdown
---

## [Tactic Name] - Executed [YYYY-MM-DD HH:MM]

### Finding 1: [Brief Description]
- **Category:** [File Size / Duplication / Complexity / Dead Code / Organization]
- **Location:** `path/to/file:LINE-LINE`
- **Current State:** [Describe what's wrong]
- **Proposed Change:** [Brief description of the refactoring]
- **Code Context:**
  ```
  // Relevant code snippet showing the issue
  ```

### Finding 2: [Brief Description]
...

### Tactic Summary
- **Issues Found:** [count]
- **Files Affected:** [count]
- **Status:** EXECUTED
```

## What to Look For

### File Size Candidates
- Files over [MAX_FILE_LOC] LOC → Consider splitting by concern
- Single file with multiple unrelated exports → Extract to separate modules
- Component files with embedded utilities → Move utilities to shared location

### Duplication Candidates
- Two functions that differ only in variable names → Parameterize
- Repeated code blocks (3+ occurrences) → Extract to utility
- Similar components → Create shared base or composition

### Complexity Candidates
- Functions with [MAX_NESTING_DEPTH]+ levels of nesting → Extract to smaller functions
- Functions over [MAX_FUNCTION_LOC] LOC → Break into logical steps
- Complex conditionals → Extract to named boolean functions
- Many parameters → Use options object pattern

### Dead Code Candidates
- Functions with no callers → Remove (verify first)
- Commented-out code → Remove (it's in git history)
- Unused imports → Remove
- Unused variables → Remove or investigate

### Organization Candidates
- Utilities in component files → Move to utils/
- Constants scattered → Consolidate to constants/
- Types in multiple files → Consolidate to types/

## Guidelines

- **One tactic per run**: Only execute ONE tactic, then stop. This allows the pipeline to iterate.
- **Be thorough within the tactic**: Search comprehensively for the pattern specified
- **Be specific**: Include exact file paths and line numbers
- **Show context**: Include code snippets that illustrate the issue
- **One issue per candidate**: Don't bundle unrelated issues
- **Skip trivials**: Focus on issues worth the refactoring effort
- **Note dependencies**: If a change might affect other files, note it
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
