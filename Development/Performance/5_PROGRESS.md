# Performance Pipeline Progress Gate

## Context
- **Playbook:** Performance
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Purpose

This document is the **progress gate** for the performance pipeline. It checks whether there are still `PENDING` performance fixes to implement. **This is the only document with Reset ON** - it controls loop continuation by resetting tasks in documents 1-4 when more work is needed.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`** to check for remaining work
2. **Check if there are any `PENDING` items** (not `IMPLEMENTED`, not `WON'T DO`, not `PENDING - MANUAL REVIEW`)
3. **If PENDING items exist**: Reset all tasks in documents 1-4 to continue the loop
4. **If NO PENDING items exist**: Do NOT reset - pipeline exits

## Progress Check

- [ ] **Check for remaining work**: Read LOOP_{{LOOP_NUMBER}}_PLAN.md and check if there are any items with status exactly `PENDING`. If PENDING items exist, reset documents 1-4 to continue the loop. If no PENDING items remain (all are IMPLEMENTED, WON'T DO, or PENDING - MANUAL REVIEW), do NOT reset anything - allow the pipeline to exit.

## Reset Tasks (Only if PENDING items exist)

If the progress check above determines we need to continue, reset all tasks in the following documents:

- [ ] **Reset 1_ANALYZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md`
- [ ] **Reset 2_FIND_ISSUES.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_FIND_ISSUES.md`
- [ ] **Reset 3_EVALUATE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md`
- [ ] **Reset 4_IMPLEMENT.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_IMPLEMENT.md`

**IMPORTANT**: Only reset documents 1-4 if there are PENDING items to implement. If all items are IMPLEMENTED, WON'T DO, or PENDING - MANUAL REVIEW, leave these reset tasks unchecked to allow the pipeline to exit.

## Decision Logic

```
IF LOOP_{{LOOP_NUMBER}}_PLAN.md doesn't exist:
    → Do NOT reset anything (PIPELINE JUST STARTED - LET IT RUN)

ELSE IF no items with status exactly `PENDING`:
    → Do NOT reset anything (ALL AUTOMATABLE WORK DONE - EXIT)

ELSE:
    → Reset documents 1-4 (CONTINUE TO NEXT LOOP)
```

## How This Works

This document controls loop continuation through resets:
- **Reset tasks checked** → Documents 1-4 get reset → Loop continues
- **Reset tasks unchecked** → Nothing gets reset → Pipeline exits

### Exit Conditions (Do NOT Reset)

1. **No Work Remaining**: All items in the plan are `IMPLEMENTED`
2. **All Skipped**: All items are `WON'T DO`
3. **Only Manual Items**: All remaining items are `PENDING - MANUAL REVIEW`
4. **Max Loops**: Hit the loop limit in Batch Runner

### Continue Conditions (Reset Documents 1-4)

1. There are items with status exactly `PENDING` in LOOP_{{LOOP_NUMBER}}_PLAN.md
2. We haven't hit max loops

## Current Status

Before making a decision, check the plan file:

| Metric | Value |
|--------|-------|
| **PENDING Items** | ___ |
| **IMPLEMENTED Items** | ___ |
| **WON'T DO Items** | ___ |
| **PENDING - MANUAL REVIEW Items** | ___ |

## Progress History

Track progress across loops:

| Loop | Fixes Implemented | Items Remaining | Decision |
|------|-------------------|-----------------|----------|
| 1 | ___ | ___ | [CONTINUE / EXIT] |
| 2 | ___ | ___ | [CONTINUE / EXIT] |
| ... | ... | ... | ... |

## Manual Override

**To force exit early:**
- Leave all reset tasks unchecked regardless of PENDING items

**To continue despite no PENDING items:**
- Check the reset tasks to force another analysis pass

**To pause for manual review:**
- Leave unchecked
- Review PERF_LOG and plan file
- Restart when ready

## Notes

- This playbook focuses on LOW complexity fixes with MEDIUM or HIGH gain
- MEDIUM and HIGH complexity fixes are marked for manual review
- Each loop iteration implements ONE fix at a time for safety
- The PERF_LOG tracks all changes across loops for easy review
