# Document 2: Review Code Quality

## Context

- **Playbook**: Code Review
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Perform a thorough code review focusing on correctness, best practices, and code quality.

## Prerequisites

- `{{AUTORUN_FOLDER}}/REVIEW_SCOPE.md` exists from Document 1

## Tasks

### Task 1: Read Scope Document

- [ ] **Load context**: Read `{{AUTORUN_FOLDER}}/REVIEW_SCOPE.md` to understand what files to review.

### Task 2: Review for Correctness

- [ ] **Check logic errors**: For each changed file, verify:
  - Conditional logic is correct (no off-by-one, correct operators)
  - Loop termination conditions are correct
  - Null/undefined handling is proper
  - Edge cases are handled
  - Error paths return appropriate values

- [ ] **Verify data flow**: Ensure:
  - Variables are initialized before use
  - Types are correct and consistent
  - Data transformations are accurate
  - State mutations are intentional

### Task 3: Review for Best Practices

- [ ] **Code style**: Check for:
  - Consistent naming conventions
  - Appropriate function/method sizes
  - Single responsibility principle
  - DRY (Don't Repeat Yourself) violations
  - Dead code or unused imports

- [ ] **Error handling**: Verify:
  - Errors are caught appropriately
  - Error messages are informative
  - Errors don't expose sensitive information
  - Async errors are handled (promises, try/catch)

- [ ] **Code organization**: Check:
  - Proper separation of concerns
  - Appropriate abstraction levels
  - Clear module boundaries
  - Reasonable file sizes

### Task 4: Review API Changes

- [ ] **Breaking changes**: If APIs are modified:
  - Are changes backward compatible?
  - Are deprecation warnings added?
  - Is versioning considered?

- [ ] **Interface contracts**: Verify:
  - Function signatures are clear
  - Return types are correct
  - Required vs optional parameters

### Task 5: Document Issues

- [ ] **Create CODE_ISSUES.md**: Write findings to `{{AUTORUN_FOLDER}}/CODE_ISSUES.md`:

```markdown
# Code Review Issues

## Critical Issues
[Must fix before merge]

## Major Issues
[Should fix, significant problems]

## Minor Issues
[Nice to fix, improvements]

## Suggestions
[Optional improvements, style preferences]

## Positive Observations
[Good practices worth noting]
```

For each issue include:
- File and line number
- Description of the issue
- Suggested fix (if applicable)
- Severity: Critical / Major / Minor / Suggestion

## Success Criteria

- ✅ All changed files reviewed for correctness
- ✅ Best practices evaluated
- ✅ API changes assessed
- ✅ CODE_ISSUES.md created with categorized findings

## Status

Mark complete when code review document is created.

---

**Next**: Document 3 will perform security-focused analysis.
