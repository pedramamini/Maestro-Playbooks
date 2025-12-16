# Code Refactoring Playbook

A systematic Auto Run playbook for simplifying code, eliminating duplication, and breaking up large files.

## Overview

This playbook creates an automated pipeline that:
1. **Analyzes** your codebase to identify refactoring opportunities
2. **Finds** specific issues: duplicated code, overly complex functions, large files
3. **Evaluates** each candidate with risk/benefit ratings
4. **Implements** safe, high-value refactors automatically
5. **Loops** to find additional improvements until no LOW risk + HIGH benefit items remain

## Document Chain

| Document | Purpose | Reset on Completion? |
|----------|---------|---------------------|
| `1_ANALYZE.md` | Survey codebase, identify refactoring categories | No |
| `2_FIND_ISSUES.md` | Find specific duplication, complexity, size issues | No |
| `3_EVALUATE.md` | Rate each candidate by risk & benefit | No |
| `4_IMPLEMENT.md` | Implement LOW risk + HIGH benefit refactors | No |
| `5_PROGRESS.md` | Progress gate - resets 1-4 if PENDING items exist, exits if none | **Yes** |

## Generated Files

Each loop iteration creates working documents with the loop number:

- `LOOP_1_GAME_PLAN.md` - Categories of refactoring opportunities
- `LOOP_1_CANDIDATES.md` - Specific refactoring targets found
- `LOOP_1_PLAN.md` - Evaluated candidates with ratings
- `REFACTOR_LOG_{{AGENT_NAME}}_{{DATE}}.md` - Cumulative log of all changes

## Refactoring Categories

### Code Duplication
- Copy-pasted functions with minor variations
- Similar logic in multiple files
- Repeated patterns that could be abstracted

### File Size Reduction
- Files over 500 LOC that should be split
- Components with too many responsibilities
- Modules that violate single-responsibility principle

### Complexity Simplification
- Functions over 50 LOC
- Deeply nested conditionals (3+ levels)
- Complex boolean expressions
- Functions with too many parameters (5+)

### Code Organization
- Dead code removal
- Unused imports/exports
- Inconsistent naming patterns
- Missing or misplaced utilities

## How It Works

### The Loop Control Mechanism

The key to understanding this playbook is how `5_PROGRESS.md` controls the loop:

- **Documents 1-4** have `Reset: OFF` - they don't auto-reset
- **Document 5** has `Reset: ON` - it's the only one that resets, and it manually resets 1-4

When `5_PROGRESS.md` runs:
1. It reads `LOOP_{{LOOP_NUMBER}}_PLAN.md` to check for PENDING items with LOW risk and HIGH/VERY HIGH benefit
2. **If such PENDING items exist**: It resets all tasks in documents 1-4
   - This triggers a fresh pass through the pipeline
   - The loop continues
3. **If NO such PENDING items**: It does NOT reset documents 1-4
   - Documents 1-4 remain completed
   - The pipeline exits (no more automatable work)

### Single Pass (No Loop)
1. Documents execute in order: 1 → 2 → 3 → 4 → 5
2. Each document reads outputs from previous steps
3. `5_PROGRESS.md` evaluates whether auto-implementable PENDING items exist
4. If PENDING items exist (LOW risk, HIGH+ benefit), it resets tasks in docs 1-4 → loop continues
5. If no such items remain, it does NOT reset → pipeline exits

### Loop Mode Flow
1. Enable loop mode in Batch Runner settings
2. First pass: Analyze → Find Issues → Evaluate → Implement → Check Progress
3. `5_PROGRESS.md` checks for auto-implementable items:
   - PENDING items with LOW risk + HIGH benefit? Reset docs 1-4 → continue
   - No such items? Don't reset → exit
4. Each new loop creates `LOOP_N_*` files with incremented loop number
5. Loop exits when no LOW risk + HIGH benefit PENDING items remain

## Recommended Setup

### For Automated Refactoring
```
Loop Mode: ON
Documents:
  1_ANALYZE.md      [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  2_FIND_ISSUES.md  [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  3_EVALUATE.md     [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  4_IMPLEMENT.md    [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  5_PROGRESS.md     [Reset: ON]  ← Controls loop: resets 1-4 if work remains, exits if done
```

### For Cautious Refactoring
```
Loop Mode: OFF (run once)
Review LOOP_1_PLAN.md
Change statuses manually:
  - PENDING → WON'T DO (skip)
  - PENDING → PENDING - MANUAL REVIEW (needs tests first)
Then run again with loop mode on
```

## Status Flow

Candidates in `LOOP_N_PLAN.md` have these statuses:

| Status | Meaning | Auto-Implements? |
|--------|---------|------------------|
| `PENDING` | Ready to implement | Yes (if LOW risk + HIGH benefit) |
| `IMPLEMENTED` | Done in this loop | No |
| `WON'T DO` | Skipped (breaks API, too risky) | No |
| `PENDING - MANUAL REVIEW` | Needs human review | No |

## Risk Assessment Criteria

| Risk Level | Description |
|------------|-------------|
| `LOW` | Internal-only changes, no API changes, easy to verify |
| `MEDIUM` | May affect callers, requires careful testing |
| `HIGH` | Breaking changes, API modifications, complex migrations |

## Benefit Assessment Criteria

| Benefit Level | Description |
|---------------|-------------|
| `LOW` | Minor improvement, cosmetic |
| `MEDIUM` | Moderate improvement to maintainability |
| `HIGH` | Significant reduction in complexity or duplication |
| `VERY HIGH` | Major architectural improvement |

## Template Variables Used

These variables are automatically substituted:

- `{{AGENT_NAME}}` - Name of your Maestro agent
- `{{AGENT_PATH}}` - Root path of the project
- `{{AUTORUN_FOLDER}}` - Path to this Auto Run folder
- `{{LOOP_NUMBER}}` - Current loop iteration (1, 2, 3...)
- `{{DATE}}` - Today's date (YYYY-MM-DD)

## Safety Guidelines

1. **Run tests before and after** - Verify nothing breaks
2. **Commit after each loop** - Easy to revert if needed
3. **Review REFACTOR_LOG** - Track all changes made
4. **Don't break APIs** - Public interfaces should stay stable
5. **Preserve behavior** - Refactoring = same behavior, better code

## Tips

1. **Start without loop mode** to review what it finds first
2. **Focus on LOW risk items** initially
3. **Check test coverage** before refactoring untested code
4. **One type at a time** - Do all extractions, then all simplifications
5. **Document decisions** in `WON'T DO` rationale
