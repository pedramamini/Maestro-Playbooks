# Refactoring Pipeline Progress Gate

## Context
- **Playbook:** Refactor
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Purpose

This document is the **progress gate** for the refactoring pipeline. It checks whether there are still `PENDING` refactoring items matching [AUTO_IMPLEMENT_RISK] risk and [AUTO_IMPLEMENT_BENEFIT] benefit to implement. **This is the only document with Reset ON** - it controls loop continuation by resetting tasks in documents 1-4 when more work is needed.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`** to check for remaining work
2. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`** to check tactic exhaustion status
3. **Check if there are any `PENDING` items** with [AUTO_IMPLEMENT_RISK] risk AND [AUTO_IMPLEMENT_BENEFIT] benefit (not `IMPLEMENTED`, not `WON'T DO`, not `PENDING - MANUAL REVIEW`)
4. **If auto-implementable PENDING items exist OR tactics remain**: Reset all tasks in documents 1-4 to continue the loop
5. **If NO auto-implementable PENDING items AND all tactics exhausted**: Do NOT reset - pipeline exits

## Progress Check

- [ ] **Read configured values**: Read the agent prompt for `[MAX_FILE_LOC]`, `[MAX_FUNCTION_LOC]`, `[MAX_NESTING_DEPTH]`, `[MAX_PARAMETERS]`, `[AUTO_IMPLEMENT_RISK]`, and `[AUTO_IMPLEMENT_BENEFIT]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

- [ ] **Check for remaining work**: Read LOOP_{{LOOP_NUMBER}}_PLAN.md and LOOP_{{LOOP_NUMBER}}_CANDIDATES.md. The loop should CONTINUE (reset docs 1-4) if EITHER: (1) there are items with status exactly `PENDING` matching [AUTO_IMPLEMENT_RISK] risk AND [AUTO_IMPLEMENT_BENEFIT] benefit, OR (2) CANDIDATES.md does NOT contain `## ALL_TACTICS_EXHAUSTED`. The loop should EXIT (do NOT reset) only when BOTH conditions are false: no auto-implementable PENDING items AND all tactics are exhausted.

## Reset Tasks (Only if work remains)

If the progress check above determines we need to continue (auto-implementable PENDING items OR tactics remaining), reset all tasks in the following documents:

- [ ] **Reset 1_ANALYZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md`
- [ ] **Reset 2_FIND_ISSUES.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_FIND_ISSUES.md`
- [ ] **Reset 3_EVALUATE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md`
- [ ] **Reset 4_IMPLEMENT.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_IMPLEMENT.md`

**IMPORTANT**: Only reset documents 1-4 if there is work remaining (auto-implementable PENDING items OR unexplored tactics). If all tactics are exhausted AND all items are IMPLEMENTED, WON'T DO, or PENDING - MANUAL REVIEW, leave these reset tasks unchecked to allow the pipeline to exit.

## Decision Logic

```
IF LOOP_{{LOOP_NUMBER}}_PLAN.md doesn't exist:
    → Do NOT reset anything (PIPELINE JUST STARTED - LET IT RUN)

ELSE IF items with status exactly `PENDING` exist matching [AUTO_IMPLEMENT_RISK] risk AND [AUTO_IMPLEMENT_BENEFIT] benefit:
    → Reset documents 1-4 (CONTINUE TO IMPLEMENT PENDING ITEMS)

ELSE IF LOOP_{{LOOP_NUMBER}}_CANDIDATES.md does NOT contain "ALL_TACTICS_EXHAUSTED":
    → Reset documents 1-4 (CONTINUE TO DISCOVER MORE CANDIDATES)

ELSE:
    → Do NOT reset anything (ALL TACTICS EXHAUSTED AND NO AUTO-IMPLEMENTABLE ITEMS - EXIT)
```

**Key insight:** The loop should continue if EITHER:
1. There are PENDING items matching [AUTO_IMPLEMENT_RISK] risk AND [AUTO_IMPLEMENT_BENEFIT] benefit to implement, OR
2. There are still tactics to execute (no `ALL_TACTICS_EXHAUSTED` marker)

## How This Works

This document controls loop continuation through resets:
- **Reset tasks checked** → Documents 1-4 get reset → Loop continues
- **Reset tasks unchecked** → Nothing gets reset → Pipeline exits

### Exit Conditions (Do NOT Reset)

Exit when ALL of these are true:
1. **Tactics exhausted**: `LOOP_{{LOOP_NUMBER}}_CANDIDATES.md` contains `## ALL_TACTICS_EXHAUSTED`
2. **No auto-implementable PENDING items**: All matching [AUTO_IMPLEMENT_RISK] + [AUTO_IMPLEMENT_BENEFIT] items are `IMPLEMENTED`, `WON'T DO`, or `PENDING - MANUAL REVIEW`

Also exit if:
3. **Max Loops**: Hit the loop limit in Batch Runner

### Continue Conditions (Reset Documents 1-4)

Continue if EITHER is true:
1. There are items with status exactly `PENDING` matching [AUTO_IMPLEMENT_RISK] risk AND [AUTO_IMPLEMENT_BENEFIT] benefit in LOOP_{{LOOP_NUMBER}}_PLAN.md
2. `LOOP_{{LOOP_NUMBER}}_CANDIDATES.md` does NOT contain `## ALL_TACTICS_EXHAUSTED` (more tactics to run)

## Current Status

Before making a decision, check both files:

| Metric | Value |
|--------|-------|
| **PENDING (matching auto-implement policy)** | ___ |
| **PENDING (other)** | ___ |
| **IMPLEMENTED** | ___ |
| **WON'T DO** | ___ |
| **PENDING - MANUAL REVIEW** | ___ |
| **ALL_TACTICS_EXHAUSTED present?** | ___ |

## Progress History

Track progress across loops:

| Loop | Refactors Implemented | Items Remaining | Tactics Exhausted? | Decision |
|------|----------------------|-----------------|-------------------|----------|
| 1 | ___ | ___ | ___ | [CONTINUE / EXIT] |
| 2 | ___ | ___ | ___ | [CONTINUE / EXIT] |
| ... | ... | ... | ... | ... |

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

- This playbook focuses on refactors matching [AUTO_IMPLEMENT_RISK] risk × [AUTO_IMPLEMENT_BENEFIT] benefit
- MEDIUM and HIGH risk refactors are marked for manual review
- Each loop iteration implements ONE refactor at a time for safety
- The REFACTOR_LOG tracks all changes across loops for easy review
- Always run tests after each loop to verify behavior is preserved
