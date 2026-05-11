# Test Gap Discovery - Find Untested Code

## Context
- **Playbook:** Testing
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Using the coverage report from the analysis phase, identify specific untested functions, branches, and code paths that need tests. This document bridges coverage metrics to actionable test targets.

## Instructions

1. **Read the coverage report** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_COVERAGE_REPORT.md`
2. **Examine low-coverage files** to find specific untested functions
3. **Identify untested branches** - conditionals, error handlers, edge cases
4. **Categorize gaps** by type (unit, integration, edge case)
5. **Output findings** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`

## Gap Finding Checklist

- [ ] **Read configured values**: Read the agent prompt for `[COVERAGE_TARGET]`, `[AUTO_TEST_TESTABILITY]`, and `[AUTO_TEST_IMPORTANCE]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

- [ ] **Find untested code (or skip if not needed)**: Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_COVERAGE_REPORT.md`. If the report shows overall line coverage of [COVERAGE_TARGET] or higher, OR there are no files with coverage below [COVERAGE_TARGET], mark this task complete without creating a gaps file—the coverage target has been met. Otherwise, examine low-coverage files, identify specific functions and branches without test coverage. List each gap with file path, function name, and why it matters. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`.

## What to Look For

### Untested Functions
- Functions with 0% coverage
- Public API methods without tests
- Utility functions that are used but not tested
- Event handlers and callbacks

### Untested Branches
- `if` statements where only one branch is tested
- `switch` cases that aren't exercised
- Ternary operators with untested paths
- Short-circuit evaluations (`&&`, `||`)

### Untested Error Handling
- `try/catch` blocks where catch is never reached
- Error callbacks that aren't tested
- Validation logic that rejects invalid input
- Timeout and retry logic

### Untested Edge Cases
- Empty arrays/objects
- Null/undefined inputs
- Boundary values (0, -1, MAX_INT)
- Unicode/special characters
- Concurrent operations

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md` with:

```markdown
# Test Gaps - Loop {{LOOP_NUMBER}}

## Summary
- **Total Gaps Found:** [count]
- **By Type:** [X] Unit, [Y] Integration, [Z] Edge Cases
- **By Priority:** [X] Critical, [Y] High, [Z] Medium

## Gap List

### GAP-001: [Function/Feature Name]
- **File:** `[path/to/file]`
- **Location:** Lines [XX-YY]
- **Type:** [Unit | Integration | Edge Case]
- **Description:** [What is untested]
- **Current Coverage:** [XX%] of this function
- **Why It Matters:** [Impact if this code fails without tests]
- **Test Approach:** [Brief idea of how to test it]

### GAP-002: [Function/Feature Name]
- **File:** `[path/to/file]`
- **Location:** Lines [XX-YY]
- **Type:** [Unit | Integration | Edge Case]
- **Description:** [What is untested]
- **Current Coverage:** [XX%] of this function
- **Why It Matters:** [Impact if this code fails without tests]
- **Test Approach:** [Brief idea of how to test it]

...continue for all gaps...

## Gaps by File

Quick reference of which files have the most gaps:

| File | Gap Count | Types |
|------|-----------|-------|
| `src/foo` | 5 | 3 Unit, 2 Edge |
| `src/bar` | 3 | 2 Unit, 1 Integration |

## Dependencies to Mock

List of external dependencies that will need mocking:

- **[Dependency Name]** - Used in [files], mock strategy: [describe]
- **[Dependency Name]** - Used in [files], mock strategy: [describe]

## Blockers

Code that cannot be tested without changes:

- **[File/Function]** - [Why it's hard to test, what needs to change]
```

## Guidelines

- **Be specific**: Include exact file paths and line numbers
- **Explain impact**: Why does this code need tests?
- **Suggest approach**: How would you test this?
- **Note dependencies**: What needs mocking?
- **Flag blockers**: Some code may need refactoring first

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Coverage target already met:**
1. The coverage report shows overall line coverage of [COVERAGE_TARGET] or higher
2. No gaps file is needed—mark the task complete without changes

**Option B - Gaps identified:**
1. The coverage report shows line coverage below [COVERAGE_TARGET]
2. You've examined low-coverage files and found untested functions/branches
3. You've created `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md` with all findings
