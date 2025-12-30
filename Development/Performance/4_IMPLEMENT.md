# Performance Fix Implementation

## Context
- **Playbook:** Performance
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Implement ONE performance fix from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` that has status `PENDING`. Log all changes to `{{AUTORUN_FOLDER}}/PERF_LOG_{{AGENT_NAME}}_{{DATE}}.md`.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`** to find evaluated performance fixes
2. **Filter for actionable items**: Only consider fixes where:
   - **Status = `PENDING`** (exactly - not `PENDING - MANUAL REVIEW` or `WON'T DO`)
   - These are LOW complexity items with MEDIUM or HIGH gain
3. **Select ONE fix** that meets the criteria (prioritize HIGH gain over MEDIUM)
4. **Implement the fix**: Make the code changes as specified in the proposed fix
5. **Verify the change**: Ensure the code still works (syntax check, no obvious errors)
6. **Log the change** to `{{AUTORUN_FOLDER}}/PERF_LOG_{{AGENT_NAME}}_{{DATE}}.md`
7. **Update status** in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` to `IMPLEMENTED`

## Task

- [ ] **Implement one PENDING fix (or skip if none)**: Read {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md. If the file doesn't exist OR contains no items with status exactly `PENDING`, mark this task complete without changes. Otherwise, find an item with status exactly `PENDING`, implement the fix, log to {{AUTORUN_FOLDER}}/PERF_LOG_{{AGENT_NAME}}_{{DATE}}.md, and mark as IMPLEMENTED in {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md.

## Implementation Checklist

Before implementing, verify:
- [ ] The status is exactly `PENDING` (not `PENDING - MANUAL REVIEW`)
- [ ] The fix is clearly specified with before/after code
- [ ] No other changes are required (no dependencies)

## Output Format

Append to `{{AUTORUN_FOLDER}}/PERF_LOG_{{AGENT_NAME}}_{{DATE}}.md` using this format:

```markdown
---

## [YYYY-MM-DD HH:MM] - [Brief Title]

**Agent:** {{AGENT_NAME}}
**Project:** {{AGENT_NAME}}
**Loop:** {{LOOP_NUMBER}}
**File:** `path/to/file.ext`
**Line(s):** [line numbers affected]
**Change Type:** [caching | algorithm optimization | lazy loading | etc.]

### What Was Changed
[1-2 sentence description of the change]

### Before
```[language]
// Original code
```

### After
```[language]
// New code
```

### Expected Impact
[Brief description of expected performance improvement]

### Verification
- [ ] Code compiles/parses without errors
- [ ] No linter errors introduced
- [ ] Change matches the proposed fix from LOOP_{{LOOP_NUMBER}}_PLAN.md
```

## Guidelines

- **Only `PENDING` items**: Do NOT implement `PENDING - MANUAL REVIEW` or `WON'T DO` items
- **One fix per run**: Implement exactly ONE fix, then stop. This keeps changes small and reviewable.
- **Follow the plan**: Implement exactly what was proposed in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`, don't improvise
- **Update both files**: Log to `{{AUTORUN_FOLDER}}/PERF_LOG_{{AGENT_NAME}}_{{DATE}}.md` AND update status in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
- **Be conservative**: If anything is unclear about the fix, skip it and note why in the log file

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Implemented a fix:**
1. You've implemented exactly ONE fix from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. You've appended the change details to `{{AUTORUN_FOLDER}}/PERF_LOG_{{AGENT_NAME}}_{{DATE}}.md`
3. You've updated the item status in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` to `IMPLEMENTED`

**Option B - No PENDING fixes available:**
1. `LOOP_{{LOOP_NUMBER}}_PLAN.md` doesn't exist, OR
2. It contains no items with status exactly `PENDING`
3. Mark this task complete without making changes

This graceful handling allows the pipeline to continue when a loop iteration produces no actionable fixes.

## When No Fixes Are Available

If there are no items with status exactly `PENDING` in the plan file, append to `{{AUTORUN_FOLDER}}/PERF_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
---

## [YYYY-MM-DD HH:MM] - Loop {{LOOP_NUMBER}} Complete

**Agent:** {{AGENT_NAME}}
**Project:** {{AGENT_NAME}}
**Loop:** {{LOOP_NUMBER}}
**Status:** No PENDING fixes available

**Summary:**
- Items IMPLEMENTED: [count]
- Items WON'T DO: [count]
- Items PENDING - MANUAL REVIEW: [count]

**Recommendation:** [Either "All automatable wins implemented" or "Remaining items need manual review"]
```

This signals to the pipeline that this loop iteration is complete.
