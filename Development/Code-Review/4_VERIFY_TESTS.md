# Document 4: Verify Test Coverage

## Context

- **Playbook**: Code Review
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Evaluate test coverage for the changed code and assess test quality.

## Prerequisites

- `{{AUTORUN_FOLDER}}/REVIEW_SCOPE.md` exists from Document 1

## Tasks

### Task 1: Load Context

- [ ] **Read scope**: Load `{{AUTORUN_FOLDER}}/REVIEW_SCOPE.md` to identify changed source files.

### Task 2: Identify Test Files

- [ ] **Find related tests**: For each changed source file, locate corresponding test files:
  - Look for `*.test.*`, `*.spec.*` files
  - Check `__tests__/` directories
  - Check `test/` or `tests/` directories
  - Match by filename or module name

- [ ] **Check for new tests**: Verify if new tests were added for new functionality.

### Task 3: Assess Test Coverage

- [ ] **New code coverage**: For each new function/method:
  - Is there at least one test?
  - Are happy path cases covered?
  - Are error cases covered?
  - Are edge cases covered?

- [ ] **Modified code coverage**: For modified code:
  - Do existing tests still pass? (conceptually)
  - Were tests updated to reflect changes?
  - Is new behavior tested?

- [ ] **Coverage gaps**: Identify untested:
  - New public functions/methods
  - New branches/conditions
  - Error handling paths
  - Integration points

### Task 4: Evaluate Test Quality

- [ ] **Test structure**: Check tests for:
  - Clear test names describing behavior
  - Proper setup/teardown
  - Single assertion focus (where appropriate)
  - No test interdependencies

- [ ] **Mocking**: Verify:
  - External dependencies are mocked
  - Mocks are realistic
  - No over-mocking (testing implementation, not behavior)

- [ ] **Assertions**: Check:
  - Meaningful assertions (not just "no error")
  - Correct expected values
  - Appropriate assertion types

- [ ] **Test maintainability**: Look for:
  - Magic numbers without explanation
  - Overly complex test setup
  - Brittle tests (likely to break with minor changes)
  - Test data duplication

### Task 5: Run Tests (if possible)

- [ ] **Execute test suite**: If test runner is available:
  ```bash
  npm test  # or equivalent
  ```
  Note any failures or warnings.

### Task 6: Document Test Gaps

- [ ] **Create TEST_GAPS.md**: Write findings to `{{AUTORUN_FOLDER}}/TEST_GAPS.md`:

```markdown
# Test Coverage Review

## Missing Tests
[New code without test coverage]

## Inadequate Tests
[Tests that don't fully cover the functionality]

## Test Quality Issues
[Problems with existing tests]

## Test Improvements
[Suggestions for better testing]

## Well-Tested Areas
[Positive observations about test coverage]

## Test Execution Results
[If tests were run, note results here]
```

For each gap include:
- Source file and function/method
- What's missing or inadequate
- Suggested test cases
- Priority: High / Medium / Low

## Success Criteria

- ✅ Test files identified for changed code
- ✅ Coverage gaps documented
- ✅ Test quality assessed
- ✅ TEST_GAPS.md created

## Status

Mark complete when test review document is created.

---

**Next**: Document 5 will compile all findings into a summary.
