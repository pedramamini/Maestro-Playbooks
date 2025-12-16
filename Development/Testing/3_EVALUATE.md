# Test Candidate Evaluation - Prioritize What to Test

## Context
- **Playbook:** Testing
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Evaluate each test gap from the discovery phase and assign importance and testability ratings. This prioritization ensures we write the most valuable tests first and reach 80% coverage efficiently.

## Instructions

1. **Read the gaps list** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`
2. **Rate each gap** for importance and testability
3. **Assign status** based on ratings
4. **Estimate coverage gain** for each test
5. **Output prioritized plan** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`

## Evaluation Checklist

- [ ] **Evaluate gaps**: Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`, rate each gap by IMPORTANCE (CRITICAL/HIGH/MEDIUM/LOW) and TESTABILITY (EASY/MEDIUM/HARD/VERY HARD). Mark EASY+HIGH or better as PENDING for auto-implementation. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`.

## Rating Criteria

### Importance Levels

| Level | Criteria |
|-------|----------|
| **CRITICAL** | Core business logic, security-sensitive, data integrity, authentication/authorization |
| **HIGH** | Frequently used utilities, API endpoints, state management, error handling |
| **MEDIUM** | Supporting modules, helpers, UI components, formatting |
| **LOW** | Edge cases for unlikely scenarios, deprecated code, cosmetic features |

### Testability Levels

| Level | Criteria |
|-------|----------|
| **EASY** | Pure functions, no external dependencies, clear inputs/outputs, no side effects |
| **MEDIUM** | Some mocking required, manageable dependencies, predictable behavior |
| **HARD** | Heavy mocking needed, external services, complex setup/teardown, state management |
| **VERY HARD** | Needs refactoring first, tightly coupled, race conditions, non-deterministic |

### Auto-Implementation Criteria

Tests will be auto-implemented if:
- **Importance:** HIGH or CRITICAL
- **Testability:** EASY or MEDIUM

Tests marked `PENDING - MANUAL REVIEW` if:
- **Importance:** HIGH/CRITICAL but **Testability:** HARD
- Complex edge cases that need human judgment

Tests marked `WON'T DO` if:
- **Testability:** VERY HARD (needs refactoring)
- **Importance:** LOW and significant effort required
- Deprecated or soon-to-be-removed code

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` with:

```markdown
# Test Implementation Plan - Loop {{LOOP_NUMBER}}

## Summary
- **Total Candidates:** [count]
- **Auto-Implement (PENDING):** [count] - Est. coverage gain: +[X.X%]
- **Manual Review:** [count]
- **Won't Do:** [count]

## Current Coverage: [XX.X%]
## Target Coverage: 80%
## Estimated Post-Loop Coverage: [XX.X%]

---

## PENDING - Ready for Auto-Implementation

### TEST-001: [Function/Feature Name]
- **Status:** `PENDING`
- **File:** `[path/to/file.ts]`
- **Gap ID:** GAP-XXX
- **Importance:** [CRITICAL | HIGH]
- **Testability:** [EASY | MEDIUM]
- **Est. Coverage Gain:** +[X.X%]
- **Test Type:** [Unit | Integration | Edge Case]
- **Test Strategy:**
  - [Specific test case 1]
  - [Specific test case 2]
  - [Specific test case 3]
- **Mocks Needed:** [List any mocks, or "None"]

### TEST-002: [Function/Feature Name]
- **Status:** `PENDING`
...

---

## PENDING - MANUAL REVIEW

### TEST-XXX: [Function/Feature Name]
- **Status:** `PENDING - MANUAL REVIEW`
- **File:** `[path/to/file.ts]`
- **Gap ID:** GAP-XXX
- **Importance:** [HIGH | CRITICAL]
- **Testability:** HARD
- **Reason for Review:** [Why human judgment needed]
- **Recommended Approach:** [Suggestions for testing]

---

## WON'T DO

### TEST-XXX: [Function/Feature Name]
- **Status:** `WON'T DO`
- **File:** `[path/to/file.ts]`
- **Gap ID:** GAP-XXX
- **Importance:** [level]
- **Testability:** [VERY HARD | N/A]
- **Reason:** [Why we're skipping this]

---

## Implementation Order

Recommended sequence based on coverage impact and dependencies:

1. **TEST-001** - [name] (+X.X% coverage)
2. **TEST-002** - [name] (+X.X% coverage)
3. ...

## Dependencies

Tests that share setup or mocking infrastructure:

- **Group A:** TEST-001, TEST-003, TEST-007 - All need [mock/fixture]
- **Group B:** TEST-002, TEST-005 - All test [module]
```

## Guidelines

- **Maximize coverage per test**: Prioritize tests that cover more lines
- **Group related tests**: Tests sharing mocks can be implemented together
- **Balance risk and reward**: CRITICAL importance trumps easy testability
- **Be realistic about VERY HARD**: Some code needs refactoring before testing
- **Track estimates**: We need to know when we'll hit 80%
