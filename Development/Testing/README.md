# Test Coverage Playbook

A systematic Auto Run playbook for achieving and maintaining 80% test coverage through incremental test creation.

## Overview

This playbook creates an automated pipeline that:
1. **Analyzes** your codebase to measure current test coverage
2. **Finds** untested or under-tested code paths
3. **Evaluates** each candidate by testability and importance
4. **Implements** high-value tests for critical code paths
5. **Loops** until 80% coverage is achieved or no auto-testable work remains

## Document Chain

| Document | Purpose | Reset on Completion? |
|----------|---------|---------------------|
| `1_ANALYZE.md` | Survey codebase, measure current coverage | No |
| `2_FIND_GAPS.md` | Find untested functions, branches, modules | No |
| `3_EVALUATE.md` | Rate each candidate by testability & importance | No |
| `4_IMPLEMENT.md` | Write tests for HIGH importance targets | No |
| `5_PROGRESS.md` | Coverage gate - resets 1-4 if below 80%, exits if met | **Yes** |

## Generated Files

Each loop iteration creates working documents:

- `LOOP_N_COVERAGE_REPORT.md` - Current coverage metrics and analysis
- `LOOP_N_GAPS.md` - Specific untested code paths found
- `LOOP_N_PLAN.md` - Evaluated candidates with ratings
- `TEST_LOG_{{AGENT_NAME}}_{{DATE}}.md` - Cumulative log of all tests added

## Coverage Target: 80%

The playbook uses **80% line coverage** as the exit condition. This target is:
- **Achievable** without excessive effort
- **Meaningful** for catching regressions
- **Industry standard** for production code

### Coverage Types Tracked

| Type | Description | Weight |
|------|-------------|--------|
| **Line Coverage** | Percentage of code lines executed by tests | Primary |
| **Branch Coverage** | Percentage of conditional branches taken | Secondary |
| **Function Coverage** | Percentage of functions called by tests | Reference |

## How It Works

### The Loop Control Mechanism

The key to understanding this playbook is how `5_PROGRESS.md` controls the loop:

- **Documents 1-4** have `Reset: OFF` - they don't auto-reset
- **Document 5** has `Reset: ON` - it's the only one that resets, and it manually resets 1-4

When `5_PROGRESS.md` runs:
1. It runs coverage analysis and checks against the 80% target
2. **If coverage < 80% AND there are PENDING items** with EASY/MEDIUM testability and HIGH/CRITICAL importance: It resets all tasks in documents 1-4
   - This triggers a fresh pass through the pipeline
   - The loop continues
3. **If coverage >= 80% OR no such PENDING items**: It does NOT reset documents 1-4
   - Documents 1-4 remain completed
   - The pipeline exits (target reached or no more auto-testable work)

### Single Pass (No Loop)
1. Documents execute in order: 1 → 2 → 3 → 4 → 5
2. Each document reads outputs from previous steps
3. `5_PROGRESS.md` evaluates coverage and PENDING items
4. If coverage < 80% and auto-testable work remains, it resets tasks in docs 1-4 → loop continues
5. If coverage >= 80% or no such items remain, it does NOT reset → pipeline exits

### Loop Mode Flow
1. Enable loop mode in Batch Runner settings
2. First pass: Analyze → Find Gaps → Evaluate → Implement → Check Progress
3. `5_PROGRESS.md` checks coverage:
   - Below 80% with auto-testable PENDING items? Reset docs 1-4 → continue
   - At 80% or no auto-testable work? Don't reset → exit
4. Each new loop creates `LOOP_N_*` files with incremented loop number
5. Loop exits when 80% coverage is reached or no auto-testable work remains

## Recommended Setup

### For Automated Test Generation
```
Loop Mode: ON
Max Loops: 10 (reasonable upper bound)
Documents:
  1_ANALYZE.md      [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  2_FIND_GAPS.md    [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  3_EVALUATE.md     [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  4_IMPLEMENT.md    [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  5_PROGRESS.md     [Reset: ON]  ← Controls loop: resets 1-4 if <80%, exits if >=80%
```

### For Review-First Approach
```
Loop Mode: OFF (run once)
Review LOOP_1_PLAN.md
Change statuses manually:
  - PENDING → WON'T DO (skip hard-to-test code)
  - PENDING → PENDING - REFACTOR FIRST (needs cleanup)
Then run again with loop mode on
```

## Status Flow

Candidates in `LOOP_N_PLAN.md` have these statuses:

| Status | Meaning | Auto-Implements? |
|--------|---------|------------------|
| `PENDING` | Ready to write tests for | Yes (if EASY/MEDIUM testability + HIGH/CRITICAL importance) |
| `IMPLEMENTED` | Tests written in this loop | No |
| `WON'T DO` | Skipped (deprecated, too complex) | No |
| `PENDING - REFACTOR FIRST` | Code needs cleanup before testing | No |

## Importance Assessment Criteria

| Level | Description |
|-------|-------------|
| `CRITICAL` | Core business logic, security-sensitive code |
| `HIGH` | Frequently used utilities, API handlers |
| `MEDIUM` | Supporting modules, helpers |
| `LOW` | Edge cases, rarely-executed paths |

## Testability Assessment Criteria

| Level | Description |
|-------|-------------|
| `EASY` | Pure functions, no dependencies, clear inputs/outputs |
| `MEDIUM` | Some mocking required, manageable dependencies |
| `HARD` | Heavy mocking, external services, complex state |
| `VERY HARD` | Requires significant refactoring to test |

## Template Variables Used

These variables are automatically substituted:

- `{{AGENT_NAME}}` - Name of your Maestro agent
- `{{AGENT_PATH}}` - Root path of the project
- `{{AUTORUN_FOLDER}}` - Path to this Auto Run folder
- `{{LOOP_NUMBER}}` - Current loop iteration (1, 2, 3...)
- `{{DATE}}` - Today's date (YYYY-MM-DD)

## Test Writing Guidelines

### Quality Standards
1. **One assertion per concept** - Test one behavior at a time
2. **Clear naming** - `describe` what, `it` should do what
3. **Arrange-Act-Assert** - Clear test structure
4. **No test interdependence** - Tests should run in isolation

### Test Types to Generate

| Type | When to Use |
|------|-------------|
| **Unit Tests** | Individual functions, pure logic |
| **Integration Tests** | Component interactions, API calls |
| **Edge Case Tests** | Boundary conditions, error handling |

### What NOT to Test
- Third-party library internals
- Framework boilerplate
- Simple getters/setters
- Auto-generated code

## Tips

1. **Start with critical paths** - Business logic first
2. **Check existing test patterns** - Match project conventions
3. **Run tests after each loop** - Verify new tests pass
4. **Watch for flaky tests** - Avoid non-deterministic assertions
5. **Commit after reaching milestones** - 60%, 70%, 80%

## Exit Conditions

The pipeline exits when ANY of these are true:
1. Coverage reaches 80% or higher
2. Max loop limit reached (if set)
3. No more PENDING items with HIGH/CRITICAL importance and EASY/MEDIUM testability
4. All remaining gaps are marked VERY HARD or WON'T DO
