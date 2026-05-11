# Test Coverage Gate - [COVERAGE_TARGET] Target

## Context
- **Playbook:** Testing
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Purpose

This document is the **coverage gate** for the testing pipeline. It checks whether we've reached the [COVERAGE_TARGET] coverage target. **This is the only document with Reset ON** - it controls loop continuation by resetting tasks in documents 1-4 when more work is needed.

## Instructions

1. **Run coverage analysis** to get current metrics
2. **Check if line coverage is [COVERAGE_TARGET] or higher**
3. **If coverage < [COVERAGE_TARGET] AND there are PENDING items** with [AUTO_TEST_TESTABILITY] testability and [AUTO_TEST_IMPORTANCE] importance in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`: Reset all tasks in documents 1-4 to continue the loop
4. **If coverage >= [COVERAGE_TARGET] OR no such PENDING items**: Do NOT reset - pipeline exits

## Coverage Check

- [ ] **Read configured values**: Read the agent prompt for `[COVERAGE_TARGET]`, `[AUTO_TEST_TESTABILITY]`, and `[AUTO_TEST_IMPORTANCE]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

- [ ] **Check coverage and decide**: Run coverage analysis. If line coverage is below [COVERAGE_TARGET] AND there are still `PENDING` items with [AUTO_TEST_TESTABILITY] testability and [AUTO_TEST_IMPORTANCE] importance in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`, then reset documents 1-4 to continue the loop. If coverage >= [COVERAGE_TARGET] OR no auto-testable items remain, do NOT reset anything - allow the pipeline to exit.

## Reset Tasks (Only if coverage < [COVERAGE_TARGET] AND auto-testable PENDING items exist)

If the coverage check above determines we need to continue, reset all tasks in the following documents:

- [ ] **Reset 1_ANALYZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md`
- [ ] **Reset 2_FIND_GAPS.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_FIND_GAPS.md`
- [ ] **Reset 3_EVALUATE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md`
- [ ] **Reset 4_IMPLEMENT.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_IMPLEMENT.md`

**IMPORTANT**: Only reset documents 1-4 if coverage is below [COVERAGE_TARGET] AND there are PENDING items with [AUTO_TEST_TESTABILITY] testability and [AUTO_TEST_IMPORTANCE] importance. If coverage target is met, or only HARD/VERY HARD items remain, leave these reset tasks unchecked to allow the pipeline to exit.

## Decision Logic

```
IF line_coverage >= [COVERAGE_TARGET]:
    → Do NOT reset anything (TARGET REACHED - EXIT)

ELSE IF no PENDING items matching [AUTO_TEST_TESTABILITY] testability AND [AUTO_TEST_IMPORTANCE] importance:
    → Do NOT reset anything (NO MORE AUTO-IMPLEMENTABLE WORK - EXIT)

ELSE:
    → Reset documents 1-4 (CONTINUE TO NEXT LOOP)
```

## How This Works

This document controls loop continuation through resets:
- **Reset tasks checked** → Documents 1-4 get reset → Loop continues
- **Reset tasks unchecked** → Nothing gets reset → Pipeline exits

### Exit Conditions (Do NOT Reset)

1. **Target Reached**: Coverage is [COVERAGE_TARGET] or higher
2. **No Work Remaining**: All PENDING items are IMPLEMENTED
3. **Only Hard Items Left**: Remaining items are HARD/VERY HARD testability
4. **Only Low Priority Left**: Remaining items are LOW/MEDIUM importance
5. **Max Loops Reached**: Hit the loop limit in Batch Runner

### Continue Conditions (Reset Documents 1-4)

1. Coverage is below [COVERAGE_TARGET]
2. There are PENDING items matching [AUTO_TEST_TESTABILITY] testability AND [AUTO_TEST_IMPORTANCE] importance
3. We haven't hit max loops

## Current Status

Before making a decision, run coverage and record:

| Metric | Value |
|--------|-------|
| **Current Line Coverage** | ___ % |
| **Target** | [COVERAGE_TARGET] |
| **Gap** | ___ % |
| **PENDING (matching auto-test policy)** | ___ |
| **PENDING (other)** | ___ |
| **IMPLEMENTED** | ___ |

## Coverage History

Track progress across loops:

| Loop | Coverage | Tests Added | Cumulative Gain | Decision |
|------|----------|-------------|-----------------|----------|
| 1 | ___ % | ___ | +___ % | [CONTINUE / EXIT] |
| 2 | ___ % | ___ | +___ % | [CONTINUE / EXIT] |
| ... | ... | ... | ... | ... |

## Manual Override

**To force exit before [COVERAGE_TARGET]:**
- Leave all reset tasks unchecked regardless of coverage

**To continue past [COVERAGE_TARGET]:**
- Check the reset tasks to keep improving coverage

**To pause for review:**
- Leave unchecked
- Review TEST_LOG and plan file
- Restart when ready

## Notes

- The [COVERAGE_TARGET] target is **line coverage**, not branch coverage
- Some code may be legitimately untestable (generated, deprecated)
- It's okay to stop early if remaining gaps are all HARD/VERY HARD
- Quality matters more than hitting exactly [COVERAGE_TARGET]
