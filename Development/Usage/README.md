# README Accuracy Playbook

A systematic Auto Run playbook for auditing and updating your project's README to match actual features in the codebase.

## Overview

This playbook creates an automated pipeline that:
1. **Analyzes** your codebase to discover user-facing features and reads the current README
2. **Finds** discrepancies: undocumented features, stale docs for removed features, inaccuracies
3. **Evaluates** each gap by user importance and fix effort
4. **Implements** README updates for high-importance gaps
5. **Loops** until the README accurately reflects the codebase features

## Document Chain

| Document | Purpose | Reset on Completion? |
|----------|---------|---------------------|
| `1_ANALYZE.md` | Survey codebase for features, scan README | No |
| `2_FIND_GAPS.md` | Compare features vs README, find discrepancies | No |
| `3_EVALUATE.md` | Rate each gap by user importance & fix effort | No |
| `4_IMPLEMENT.md` | Update README for CRITICAL/HIGH importance gaps | No |
| `5_PROGRESS.md` | Accuracy gate - resets 1-4 if gaps remain, exits if accurate | **Yes** |

## Generated Files

Each loop iteration creates working documents with the loop number:

- `LOOP_1_FEATURE_INVENTORY.md` - Features found in code and README
- `LOOP_1_GAPS.md` - Discrepancies between code and README
- `LOOP_1_PLAN.md` - Evaluated gaps with ratings and proposed fixes
- `USAGE_LOG_{{AGENT_NAME}}_{{DATE}}.md` - Cumulative log of all README changes

## Gap Types

### MISSING - Feature in code but not in README
- New features added without documentation
- Major functionality users should know about
- Configuration options not explained

### STALE - Feature in README but removed from code
- Deprecated functionality still documented
- Old command names or syntax
- References to removed features

### INACCURATE - Feature exists but description is wrong
- Changed behavior not reflected in docs
- Incorrect examples or syntax
- Wrong default values

### INCOMPLETE - Feature documented but lacking detail
- Missing important options
- No examples for complex features
- Unclear descriptions

## How It Works

### The Loop Control Mechanism

The key to understanding this playbook is how `5_PROGRESS.md` controls the loop:

- **Documents 1-4** have `Reset: OFF` - they don't auto-reset
- **Document 5** has `Reset: ON` - it's the only one that resets, and it manually resets 1-4

When `5_PROGRESS.md` runs:
1. It reads `LOOP_{{LOOP_NUMBER}}_PLAN.md` to check for PENDING items with CRITICAL/HIGH importance and EASY/MEDIUM effort
2. **If such PENDING items exist**: It resets all tasks in documents 1-4
   - This triggers a fresh pass through the pipeline
   - The loop continues
3. **If NO such PENDING items**: It does NOT reset documents 1-4
   - Documents 1-4 remain completed
   - The pipeline exits (README is accurate)

### Single Pass (No Loop)
1. Documents execute in order: 1 → 2 → 3 → 4 → 5
2. Each document reads outputs from previous steps
3. `5_PROGRESS.md` evaluates whether high-importance PENDING items exist
4. If such items exist, it resets tasks in docs 1-4 → loop continues
5. If no such items remain, it does NOT reset → pipeline exits

### Loop Mode Flow
1. Enable loop mode in Batch Runner settings
2. First pass: Analyze → Find Gaps → Evaluate → Implement → Check Progress
3. `5_PROGRESS.md` checks for remaining work:
   - CRITICAL/HIGH gaps with EASY/MEDIUM effort? Reset docs 1-4 → continue
   - No such gaps? Don't reset → exit
4. Each new loop creates `LOOP_N_*` files with incremented loop number
5. Loop exits when README accurately reflects codebase features

## Recommended Setup

### For Automated README Updates
```
Loop Mode: ON
Max Loops: 5 (README fixes should converge quickly)
Documents:
  1_ANALYZE.md      [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  2_FIND_GAPS.md    [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  3_EVALUATE.md     [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  4_IMPLEMENT.md    [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  5_PROGRESS.md     [Reset: ON]  ← Controls loop: resets 1-4 if gaps remain, exits if accurate
```

### For Review-First Approach
```
Loop Mode: OFF (run once)
Review LOOP_1_PLAN.md
Change statuses manually:
  - PENDING → WON'T DO (intentionally undocumented)
  - PENDING → PENDING - NEEDS REVIEW (needs maintainer input)
Then run again with loop mode on
```

## Status Flow

Gaps in `LOOP_N_PLAN.md` have these statuses:

| Status | Meaning | Auto-Fixes? |
|--------|---------|-------------|
| `PENDING` | Ready to fix | Yes (if CRITICAL/HIGH importance + EASY/MEDIUM effort) |
| `IMPLEMENTED` | Fixed in this loop | No |
| `WON'T DO` | Skipped (intentionally undocumented) | No |
| `PENDING - NEEDS REVIEW` | Needs maintainer input | No |

## User Importance Criteria

| Level | Description |
|-------|-------------|
| `CRITICAL` | Blocks basic usage - installation, getting started, main commands |
| `HIGH` | Affects common workflows - major features, configuration |
| `MEDIUM` | Affects regular usage - secondary features, options |
| `LOW` | Advanced/edge cases - rarely used features |

## Fix Effort Criteria

| Level | Description |
|-------|-------------|
| `EASY` | Simple text addition/removal, clear what to write |
| `MEDIUM` | Moderate investigation, rewrite sections |
| `HARD` | Extensive rewrite, needs deep understanding |

## Template Variables Used

These variables are automatically substituted:

- `{{AGENT_NAME}}` - Name of your Maestro agent
- `{{AGENT_PATH}}` - Root path of the project
- `{{AUTORUN_FOLDER}}` - Path to this Auto Run folder
- `{{LOOP_NUMBER}}` - Current loop iteration (1, 2, 3...)
- `{{DATE}}` - Today's date (YYYY-MM-DD)

## What Gets Documented

### Should Be in README
- Installation and setup steps
- Basic usage and getting started
- Major features and capabilities
- Configuration options
- CLI commands and flags
- Common workflows
- Important limitations

### May Skip (WON'T DO)
- Internal implementation details
- Developer-only features
- Experimental/unstable features
- Features with separate detailed docs

## Tips

1. **Run without loop mode first** - Review what it finds before auto-fixing
2. **Check for stale docs** - Removed features are easy to miss
3. **Match existing style** - Follow the README's formatting conventions
4. **Focus on user impact** - What would confuse a new user?
5. **Review the USAGE_LOG** - Track all changes for easy rollback

## Exit Conditions

The pipeline exits when ANY of these are true:
1. All CRITICAL/HIGH importance gaps are fixed
2. Max loop limit reached (if set)
3. Only HARD effort items remain (need manual work)
4. All remaining gaps are WON'T DO or NEEDS REVIEW
