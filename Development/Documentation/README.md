# Documentation Coverage Playbook

A systematic Auto Run playbook for achieving and maintaining `[COVERAGE_TARGET]` documentation coverage through incremental doc generation.

## Requirements

**Agent Prompt**: This playbook works with Maestro's **default agent prompt**. No custom agent configuration required.

## Overview

This playbook creates an automated pipeline that:
1. **Analyzes** your codebase to measure current documentation coverage
2. **Finds** undocumented exports: functions, classes, types, modules
3. **Evaluates** each gap by visibility and importance
4. **Implements** documentation for high-visibility, high-importance exports
5. **Loops** until `[COVERAGE_TARGET]` documentation coverage is achieved

## Document Chain

| Document | Purpose | Reset on Completion? |
|----------|---------|---------------------|
| `1_ANALYZE.md` | Measure current coverage, identify doc patterns | No |
| `2_FIND_GAPS.md` | Find specific undocumented exports | No |
| `3_EVALUATE.md` | Rate each gap by visibility & importance | No |
| `4_IMPLEMENT.md` | Write docs for `[AUTO_DOC_IMPORTANCE]` importance, `[AUTO_DOC_VISIBILITY]` exports | No |
| `5_PROGRESS.md` | Coverage gate - resets 1-4 if below `[COVERAGE_TARGET]`, exits if met | **Yes** |

## Generated Files

Each loop iteration creates working documents with the loop number:

- `LOOP_1_DOC_REPORT.md` - Coverage metrics and analysis
- `LOOP_1_GAPS.md` - Specific undocumented exports found
- `LOOP_1_PLAN.md` - Evaluated gaps with ratings
- `DOC_LOG_{{AGENT_NAME}}_{{DATE}}.md` - Cumulative log of all documentation added

## Documentation Categories

> The default policy auto-documents exports matching `AUTO_DOC_VISIBILITY` × `AUTO_DOC_IMPORTANCE` (defaults: `PUBLIC,INTERNAL` × `CRITICAL,HIGH`). Configure both in the Auto Run panel. The full rubric below shows all available rating values; the configured policy decides which combinations are eligible.

### By Visibility
| Level | Description |
|-------|-------------|
| **PUBLIC** | Exported for external consumers, part of public API |
| **INTERNAL** | Used across modules within the project |
| **UTILITY** | Helper functions, used in limited scope |
| **IMPLEMENTATION** | Private/internal details |

### By Importance
| Level | Description |
|-------|-------------|
| **CRITICAL** | Core functionality, widely used, error-prone |
| **HIGH** | Frequently used, non-obvious behavior |
| **MEDIUM** | Moderately used, mostly straightforward |
| **LOW** | Rarely used, self-explanatory |

### What Gets Documented
- Exported functions without doc comments
- Public classes without class descriptions
- Complex types without explanation
- Non-obvious constants without comments
- Modules without overview documentation

### What Gets Skipped
- Private/internal functions (not exported)
- Test files and test utilities
- Auto-generated code
- Self-explanatory, simple code

## How It Works

### The Loop Control Mechanism

The key to understanding this playbook is how `5_PROGRESS.md` controls the loop:

- **Documents 1-4** have `Reset: OFF` - they don't auto-reset
- **Document 5** has `Reset: ON` - it's the only one that resets, and it manually resets 1-4

When `5_PROGRESS.md` runs:
1. It checks current documentation coverage against the `[COVERAGE_TARGET]` target
2. **If coverage < `[COVERAGE_TARGET]` AND there are PENDING items**: It resets all tasks in documents 1-4
   - This triggers a fresh pass through the pipeline
   - The loop continues
3. **If coverage >= `[COVERAGE_TARGET]` OR no PENDING items**: It does NOT reset documents 1-4
   - Documents 1-4 remain completed
   - The pipeline exits (no more uncompleted work)

### Single Pass (No Loop)
1. Documents execute in order: 1 → 2 → 3 → 4 → 5
2. Each document reads outputs from previous steps
3. `5_PROGRESS.md` evaluates the exit conditions
4. If target not met and work remains, it resets tasks in docs 1-4 → loop continues
5. If target met or no work remains, it does NOT reset → pipeline exits

### Loop Mode Flow
1. Enable loop mode in Batch Runner settings
2. First pass: Analyze → Find Gaps → Evaluate → Implement → Check Progress
3. `5_PROGRESS.md` checks coverage:
   - Below `[COVERAGE_TARGET]` with PENDING items? Reset docs 1-4 → continue
   - At `[COVERAGE_TARGET]` or no more work? Don't reset → exit
4. Each new loop creates `LOOP_N_*` files with incremented loop number
5. Loop exits when `[COVERAGE_TARGET]` coverage is reached or no documentable work remains

## Recommended Setup

### For Automated Documentation
```
Loop Mode: ON
Max Loops: 10 (reasonable upper bound)
Documents:
  1_ANALYZE.md      [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  2_FIND_GAPS.md    [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  3_EVALUATE.md     [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  4_IMPLEMENT.md    [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  5_PROGRESS.md     [Reset: ON]  ← Controls loop: resets 1-4 if <`[COVERAGE_TARGET]`, exits if >=`[COVERAGE_TARGET]`
```

### For Review-First Approach
```
Loop Mode: OFF (run once)
Review LOOP_1_PLAN.md
Change statuses manually:
  - PENDING → WON'T DO (skip self-explanatory code)
  - PENDING → PENDING - NEEDS CONTEXT (needs domain knowledge)
Then run again with loop mode on
```

## Status Flow

Candidates in `LOOP_N_PLAN.md` have these statuses:

| Status | Meaning | Auto-Documents? |
|--------|---------|-----------------|
| `PENDING` | Ready to document | Yes (if `[AUTO_DOC_IMPORTANCE]` importance, `[AUTO_DOC_VISIBILITY]` visibility) |
| `IMPLEMENTED` | Documented in this loop | No |
| `WON'T DO` | Skipped (private, self-explanatory) | No |
| `PENDING - NEEDS CONTEXT` | Needs maintainer input | No |

## Template Variables Used

These variables are automatically substituted:

- `{{AGENT_NAME}}` - Name of your Maestro agent
- `{{AGENT_PATH}}` - Root path of the project
- `{{AUTORUN_FOLDER}}` - Path to this Auto Run folder
- `{{LOOP_NUMBER}}` - Current loop iteration (1, 2, 3...)
- `{{DATE}}` - Today's date (YYYY-MM-DD)

## Documentation Quality Standards

### Always Include
- **Description**: What does it do? (1-2 sentences)
- **Parameters**: Type, name, description for each
- **Returns**: What comes back, including edge cases

### Include When Relevant
- **Examples**: For complex or non-obvious usage
- **Throws/Raises**: Error conditions
- **See Also**: Related functions or types

### Avoid
- Implementation details that may change
- Obvious information ("param x: the x value")
- Overly long descriptions
- Outdated examples

## Tips

1. **Start without loop mode** to review what it finds first
2. **Match existing style** - Follow project conventions
3. **Document public APIs first** - External consumers need docs most
4. **Group related exports** - Document together for consistency
5. **Commit after reaching milestones** - 60%, 70%, 80%, 90%

## Exit Conditions

The pipeline exits when ANY of these are true:
1. Coverage reaches `[COVERAGE_TARGET]` or higher
2. Max loop limit reached (if set)
3. No more PENDING items with `[AUTO_DOC_IMPORTANCE]` importance
4. All remaining gaps are marked NEEDS CONTEXT or WON'T DO
