# Documentation Coverage Gate - `[COVERAGE_TARGET]` Target

## Context
- **Playbook:** Documentation
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Purpose

This document is the **coverage gate** for the documentation pipeline. It checks whether we've reached the `[COVERAGE_TARGET]` documentation coverage target for public APIs. **This is the only document with Reset ON** - it controls loop continuation by resetting tasks in documents 1-4 when more work is needed.

## Instructions

1. **Calculate current documentation coverage** - Count documented vs total exports
2. **Check if coverage is `[COVERAGE_TARGET]` or higher**
3. **If coverage < `[COVERAGE_TARGET]` AND there are PENDING items**: Reset all tasks in documents 1-4 (check the reset task below)
4. **If coverage >= `[COVERAGE_TARGET]` OR no more PENDING items**: Do NOT reset - pipeline exits

## Coverage Check

- [ ] **Check coverage and decide**: Calculate current documentation coverage. If coverage is below `[COVERAGE_TARGET]` AND there are still `PENDING` items with `[AUTO_DOC_VISIBILITY]` visibility and `[AUTO_DOC_IMPORTANCE]` importance in LOOP_{{LOOP_NUMBER}}_PLAN.md, then reset documents 1-4 to continue the loop. If coverage >= `[COVERAGE_TARGET]` OR no documentable work remains, do NOT reset anything - allow the pipeline to exit.

## Reset Tasks (Only if coverage < `[COVERAGE_TARGET]` AND work remains)

If the coverage check above determines we need to continue, reset all tasks in the following documents:

- [ ] **Reset 1_ANALYZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md`
- [ ] **Reset 2_FIND_GAPS.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_FIND_GAPS.md`
- [ ] **Reset 3_EVALUATE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md`
- [ ] **Reset 4_IMPLEMENT.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_IMPLEMENT.md`

**IMPORTANT**: Only reset documents 1-4 if coverage < `[COVERAGE_TARGET]` AND there are PENDING items to document. If we've reached `[COVERAGE_TARGET]` or there's no more work, leave these reset tasks unchecked to allow the pipeline to exit.

## Decision Logic

```
IF documentation_coverage >= `[COVERAGE_TARGET]`:
    → Do NOT reset anything (TARGET REACHED - EXIT)

ELSE IF no PENDING items with (`[AUTO_DOC_VISIBILITY]` visibility) AND (`[AUTO_DOC_IMPORTANCE]` importance):
    → Do NOT reset anything (NO MORE AUTO-DOCUMENTABLE WORK - EXIT)

ELSE:
    → Reset documents 1-4 (CONTINUE TO NEXT LOOP)
```

## How This Works

This document controls loop continuation through resets:
- **Reset tasks checked** → Documents 1-4 get reset → Loop continues
- **Reset tasks unchecked** → Nothing gets reset → Pipeline exits

### Exit Conditions (Do NOT Reset)

1. **Target Reached**: Documentation coverage is `[COVERAGE_TARGET]` or higher
2. **No Work Remaining**: All PENDING items are IMPLEMENTED
3. **Only Context-Needed Items**: Remaining items need maintainer input
4. **Only Low Priority**: Remaining items are LOW importance or UTILITY visibility
5. **Max Loops**: Hit the loop limit in Batch Runner

### Continue Conditions (Reset Documents 1-4)

1. Documentation coverage is below `[COVERAGE_TARGET]`
2. There are PENDING items that can be auto-documented
3. We haven't hit max loops

## Current Status

Before making a decision, calculate coverage:

| Metric | Value |
|--------|-------|
| **Documented Exports** | ___ |
| **Total Exports** | ___ |
| **Current Coverage** | ___ % |
| **Target** | `[COVERAGE_TARGET]` |
| **Gap** | ___ % |
| **PENDING Items** | ___ |
| **Auto-Documentable** | ___ |

## Coverage History

Track progress across loops:

| Loop | Coverage | Docs Added | Cumulative Gain |
|------|----------|------------|-----------------|
| 1 | ___ % | ___ | +___ % |
| 2 | ___ % | ___ | +___ % |
| ... | ... | ... | ... |

## Manual Override

**To force exit before `[COVERAGE_TARGET]`:**
- Leave this task unchecked regardless of coverage

**To continue past `[COVERAGE_TARGET]`:**
- Check this task to keep improving documentation

**To pause for context gathering:**
- Leave unchecked
- Gather information for NEEDS CONTEXT items
- Restart when ready

## Remaining Work Summary

Items that still need attention after this loop:

### Needs Context
- [ ] DOC-XXX: [export name] - [what context is needed]

### Won't Document
- [ ] DOC-XXX: [export name] - [reason]

### Blocked
- [ ] DOC-XXX: [export name] - [what it's waiting for]

## Notes

- The `[COVERAGE_TARGET]` target is for **public API coverage**, not all code
- Internal implementation details don't need documentation
- Some exports may be self-explanatory and don't need docs
- Quality matters more than hitting exactly `[COVERAGE_TARGET]`
- Outdated documentation is worse than no documentation
