# Performance Optimization Playbook

A systematic Auto Run playbook for finding and fixing performance issues in your codebase.

## Overview

This playbook creates an automated pipeline that:
1. **Analyzes** your codebase to identify performance-sensitive areas
2. **Finds** specific performance issues using tactical search patterns
3. **Evaluates** each candidate with complexity/gain ratings
4. **Implements** high-gain, low-complexity fixes automatically
5. **Loops** to find additional improvements until no PENDING items remain

## Document Chain

| Document | Purpose | Reset on Completion? |
|----------|---------|---------------------|
| `1_ANALYZE.md` | Survey codebase, create investigation tactics | No |
| `2_FIND_ISSUES.md` | Execute tactics, find specific candidates | No |
| `3_EVALUATE.md` | Rate each candidate by complexity & gain | No |
| `4_IMPLEMENT.md` | Implement LOW complexity / HIGH gain fixes | No |
| `5_PROGRESS.md` | Progress gate - resets 1-4 if PENDING items exist, exits if none | **Yes** |

## Generated Files

Each loop iteration creates working documents with the loop number:

- `LOOP_1_GAME_PLAN.md` - Investigation tactics from analysis
- `LOOP_1_CANDIDATES.md` - Specific performance issues found
- `LOOP_1_PLAN.md` - Evaluated candidates with ratings
- `PERF_LOG_{{AGENT_NAME}}_{{DATE}}.md` - Cumulative log of all changes

## How It Works

### The Loop Control Mechanism

The key to understanding this playbook is how `5_PROGRESS.md` controls the loop:

- **Documents 1-4** have `Reset: OFF` - they don't auto-reset
- **Document 5** has `Reset: ON` - it's the only one that resets, and it manually resets 1-4

When `5_PROGRESS.md` runs:
1. It reads `LOOP_{{LOOP_NUMBER}}_PLAN.md` to check for PENDING items
2. **If PENDING items exist**: It resets all tasks in documents 1-4
   - This triggers a fresh pass through the pipeline
   - The loop continues
3. **If NO PENDING items**: It does NOT reset documents 1-4
   - Documents 1-4 remain completed
   - The pipeline exits (no more uncompleted work)

### Single Pass (No Loop)
1. Documents execute in order: 1 → 2 → 3 → 4 → 5
2. Each document reads outputs from previous steps
3. `5_PROGRESS.md` evaluates whether PENDING items exist
4. If PENDING items exist, it resets tasks in docs 1-4 → loop continues
5. If no PENDING items remain, it does NOT reset → pipeline exits

### Loop Mode Flow
1. Enable loop mode in Batch Runner settings
2. First pass: Analyze → Find Issues → Evaluate → Implement → Check Progress
3. `5_PROGRESS.md` checks for PENDING items:
   - PENDING items exist? Reset docs 1-4 → continue
   - No PENDING items? Don't reset → exit
4. Each new loop creates `LOOP_N_*` files with incremented loop number
5. Loop exits when no PENDING items remain

## Recommended Setup

### For Automated Optimization
```
Loop Mode: ON
Documents:
  1_ANALYZE.md      [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  2_FIND_ISSUES.md  [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  3_EVALUATE.md     [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  4_IMPLEMENT.md    [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  5_PROGRESS.md     [Reset: ON]  ← Controls loop: resets 1-4 if PENDING, exits if none
```

### For Manual Review First
```
Loop Mode: OFF (run once)
Review LOOP_1_PLAN.md
Change statuses manually:
  - PENDING → WON'T DO (skip)
  - PENDING → PENDING - MANUAL REVIEW (do later)
Then run again with loop mode on
```

## Status Flow

Candidates in `LOOP_N_PLAN.md` have these statuses:

| Status | Meaning | Auto-Implements? |
|--------|---------|------------------|
| `PENDING` | Ready to implement | Yes |
| `IMPLEMENTED` | Done in this loop | No |
| `WON'T DO` | Skipped (too risky, not worth it) | No |
| `PENDING - MANUAL REVIEW` | Needs human review | No |

## Template Variables Used

These variables are automatically substituted:

- `{{AGENT_NAME}}` - Name of your Maestro agent
- `{{AGENT_PATH}}` - Root path of the project
- `{{AUTORUN_FOLDER}}` - Path to this Auto Run folder
- `{{LOOP_NUMBER}}` - Current loop iteration (1, 2, 3...)
- `{{DATE}}` - Today's date (YYYY-MM-DD)

## Customization

### Adjusting Aggressiveness
Edit `4_IMPLEMENT.md` to change which fixes get auto-implemented:
- Default: `LOW` complexity + `HIGH` gain only
- More aggressive: Include `MEDIUM` complexity
- Conservative: Require `VERY HIGH` gain

### Adding Custom Tactics
Edit `1_ANALYZE.md` to add domain-specific investigation patterns for your tech stack.

### Changing Output Location
All documents reference `{{AUTORUN_FOLDER}}` for outputs. Files stay in your Auto Run folder by default.

## Tips

1. **Start without loop mode** to review what it finds first
2. **Review `LOOP_1_PLAN.md`** before enabling loop mode
3. **Check the PERF_LOG** to see cumulative changes across loops
4. **Run tests** after each batch of changes
5. **Commit frequently** - each loop iteration is a good commit point
