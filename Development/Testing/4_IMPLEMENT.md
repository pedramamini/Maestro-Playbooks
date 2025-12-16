# Test Implementation - Write the Tests

## Context
- **Playbook:** Testing
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Implement tests for `PENDING` candidates from the evaluation phase. Write high-quality tests that follow project conventions and maximize coverage gain.

## Instructions

1. **Read the plan** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. **Find all `PENDING` items** (not `IMPLEMENTED`, `WON'T DO`, or `PENDING - MANUAL REVIEW`)
3. **Write tests** for each PENDING item
4. **Run the tests** to verify they pass
5. **Update statuses** to `IMPLEMENTED` in the plan file
6. **Log changes** to `{{AUTORUN_FOLDER}}/TEST_LOG_{{AGENT_NAME}}_{{DATE}}.md`

## Implementation Checklist

- [ ] **Write tests**: Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`, implement tests for ONE `PENDING` item with EASY/MEDIUM testability and HIGH/CRITICAL importance. Follow project test conventions. Run tests to verify they pass. Update status to `IMPLEMENTED` in the plan. Log to `{{AUTORUN_FOLDER}}/TEST_LOG_{{AGENT_NAME}}_{{DATE}}.md`. Only implement ONE test per task execution.

## Test Writing Guidelines

### Before Writing

1. **Check existing test patterns** - Match project conventions
2. **Identify the test file location** - Follow project structure
3. **Review the function being tested** - Understand inputs, outputs, side effects
4. **Plan test cases** - Cover happy path, edge cases, error cases

### Universal Test Structure

Regardless of language or framework, tests should follow this pattern:

```
Test Suite: [Module or Class Name]
  Test Group: [Function or Method Name]

    Setup (if needed):
      - Initialize test fixtures
      - Create mocks/stubs

    Test Case: "should [expected behavior] when [condition]"
      - Arrange: Set up test data
      - Act: Call the function
      - Assert: Verify the result

    Teardown (if needed):
      - Clean up resources
      - Reset mocks
```

### Naming Conventions

| Pattern | Example |
|---------|---------|
| `should [action] when [condition]` | `should return empty array when input is null` |
| `should handle [edge case]` | `should handle unicode characters` |
| `should throw [error] when [condition]` | `should throw ValidationError when email is invalid` |

### Common Test Patterns

#### Testing Pure Functions
```
Test: "should add two numbers"
  Input: (2, 3)
  Expected: 5
  Assert: result equals expected
```

#### Testing Async Functions
```
Test: "should fetch user data"
  Input: user ID 123
  Expected: user object with name
  Assert: result.name equals expected name
```

#### Testing with Mocks
```
Test: "should call the API"
  Setup: Create mock API function
  Action: Call service with mock
  Assert: Mock was called with expected arguments
```

#### Testing Error Handling
```
Test: "should throw on invalid input"
  Input: null or invalid data
  Expected: Specific error type/message
  Assert: Function throws expected error
```

## Update Plan Status

After implementing each test, update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`:

```markdown
### TEST-001: [Function Name]
- **Status:** `IMPLEMENTED`  ← Changed from PENDING
- **Implemented In:** Loop {{LOOP_NUMBER}}
- **Test File:** `[path/to/test/file]`
- **Test Cases Added:** [count]
- **Coverage Gain:** +[X.X%] (verified)
```

## Log Format

Append to `{{AUTORUN_FOLDER}}/TEST_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
## Loop {{LOOP_NUMBER}} - [Timestamp]

### Tests Implemented

#### TEST-001: [Function Name]
- **Status:** IMPLEMENTED
- **Test File:** `[path/to/test/file]`
- **Test Cases:**
  1. [Test case description]
  2. [Test case description]
  3. [Test case description]
- **Coverage Before:** [XX.X%]
- **Coverage After:** [XX.X%]
- **Gain:** +[X.X%]

---
```

## Quality Checks

Before marking a test as IMPLEMENTED:

- [ ] Tests pass (run the project's test command)
- [ ] No skipped tests
- [ ] No debug statements left in code
- [ ] Assertions are meaningful (not just checking truthiness)
- [ ] Edge cases are covered
- [ ] Mocks/stubs are properly cleaned up
- [ ] Test names are descriptive

## Guidelines

- **One test file per source file** - Follow project conventions
- **Run tests frequently** - Catch failures early
- **Don't skip failures** - Fix or mark as PENDING - MANUAL REVIEW
- **Update coverage** - Re-run coverage after each implementation
- **Be thorough but efficient** - Good coverage, not 100% coverage
