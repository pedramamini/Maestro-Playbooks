# Refactoring Pipeline Progress Gate

## Context
- **Playbook:** Refactor
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Purpose

This document is the **progress gate** for the refactoring pipeline. It checks whether there are still `PENDING` refactoring items with LOW risk and HIGH/VERY HIGH benefit to implement. **This is the only document with Reset ON** - it controls loop continuation by resetting tasks in documents 1-4 when more work is needed.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`** to check for remaining work
2. **Check if there are any `PENDING` items** with LOW risk AND HIGH/VERY HIGH benefit (not `IMPLEMENTED`, not `WON'T DO`, not `PENDING - MANUAL REVIEW`)
3. **If auto-implementable PENDING items exist**: Reset all tasks in documents 1-4 to continue the loop
4. **If NO auto-implementable PENDING items exist**: Do NOT reset - pipeline exits

## Progress Check

- [ ] **Check for remaining work**: Read LOOP_{{LOOP_NUMBER}}_PLAN.md and check if there are any items with status exactly `PENDING` that have LOW risk AND HIGH or VERY HIGH benefit. If such items exist, reset documents 1-4 to continue the loop. If no auto-implementable items remain, do NOT reset anything - allow the pipeline to exit.

## Reset Tasks (Only if auto-implementable PENDING items exist)

If the progress check above determines we need to continue, reset all tasks in the following documents:

- [ ] **Reset 1_ANALYZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md`
- [ ] **Reset 2_FIND_ISSUES.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_FIND_ISSUES.md`
- [ ] **Reset 3_EVALUATE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md`
- [ ] **Reset 4_IMPLEMENT.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_IMPLEMENT.md`

**IMPORTANT**: Only reset documents 1-4 if there are PENDING items with LOW risk and HIGH/VERY HIGH benefit. If all such items are IMPLEMENTED, or only MEDIUM/HIGH risk items remain, leave these reset tasks unchecked to allow the pipeline to exit.

## Decision Logic

```
IF LOOP_{{LOOP_NUMBER}}_PLAN.md doesn't exist:
    → Do NOT reset anything (PIPELINE JUST STARTED - LET IT RUN)

ELSE IF no items with status `PENDING` AND risk=LOW AND benefit=HIGH/VERY HIGH:
    → Do NOT reset anything (ALL AUTOMATABLE WORK DONE - EXIT)

ELSE:
    → Reset documents 1-4 (CONTINUE TO NEXT LOOP)
```

## How This Works

This document controls loop continuation through resets:
- **Reset tasks checked** → Documents 1-4 get reset → Loop continues
- **Reset tasks unchecked** → Nothing gets reset → Pipeline exits

### Exit Conditions (Do NOT Reset)

1. **No Plan File**: `LOOP_{{LOOP_NUMBER}}_PLAN.md` doesn't exist (nothing found)
2. **All Implemented**: All LOW risk + HIGH benefit items are `IMPLEMENTED`
3. **All Skipped**: All items are `WON'T DO`
4. **Only Manual Items**: All remaining items are `PENDING - MANUAL REVIEW`
5. **Only Risky Items**: All remaining `PENDING` items have MEDIUM or HIGH risk
6. **Only Low Value Items**: All remaining `PENDING` items have LOW or MEDIUM benefit
7. **Max Loops**: Hit the loop limit in Batch Runner

### Continue Conditions (Reset Documents 1-4)

1. There are `PENDING` items with LOW risk AND HIGH/VERY HIGH benefit
2. We haven't hit max loops

## Current Status

Before making a decision, check the plan file:

| Metric | Value |
|--------|-------|
| **PENDING (LOW risk, HIGH+ benefit)** | ___ |
| **PENDING (other)** | ___ |
| **IMPLEMENTED** | ___ |
| **WON'T DO** | ___ |
| **PENDING - MANUAL REVIEW** | ___ |

## Progress History

Track progress across loops:

| Loop | Refactors Implemented | Items Remaining | Decision |
|------|----------------------|-----------------|----------|
| 1 | ___ | ___ | [CONTINUE / EXIT] |
| 2 | ___ | ___ | [CONTINUE / EXIT] |
| ... | ... | ... | ... |

## Manual Override

**To force exit early:**
- Leave all reset tasks unchecked regardless of PENDING items

**To continue despite no auto-implementable items:**
- Check the reset tasks to force another analysis pass

**To pause for manual review:**
- Leave unchecked
- Review REFACTOR_LOG and plan file
- Restart when ready

## Notes

- This playbook focuses on LOW risk refactors with HIGH or VERY HIGH benefit
- MEDIUM and HIGH risk refactors are marked for manual review
- Each loop iteration implements ONE refactor at a time for safety
- The REFACTOR_LOG tracks all changes across loops for easy review
- Always run tests after each loop to verify behavior is preserved
