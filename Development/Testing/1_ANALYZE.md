# Test Coverage Analysis - Baseline Measurement

## Context
- **Playbook:** Testing
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Measure current test coverage and identify the testing landscape. This document establishes the baseline metrics that drive the test generation pipeline.

## Instructions

1. **Identify the test framework** - Detect what testing tools the project uses
2. **Run coverage analysis** - Execute test suite with coverage enabled
3. **Document current metrics** - Line, branch, and function coverage
4. **Identify testing patterns** - How existing tests are organized
5. **Output a coverage report** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_COVERAGE_REPORT.md`

## Analysis Checklist

- [ ] **Measure coverage (if needed)**: First check if `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_COVERAGE_REPORT.md` already exists with coverage data (look for "Overall Line Coverage:" with a percentage). If it does, skip the analysis and mark this task complete—the coverage report is already in place. If it doesn't exist, identify the project's test framework and run the test suite with coverage enabled. Document line coverage percentage and identify lowest-covered modules. Output results to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_COVERAGE_REPORT.md`.

## How to Find Coverage Commands

1. **Check project configuration files** for test scripts:
   - `package.json` scripts section
   - `Makefile` or `justfile` targets
   - `pyproject.toml` or `setup.py`
   - `Cargo.toml` for Rust
   - Build tool configs (Maven, Gradle, etc.)

2. **Look for existing coverage configuration**:
   - Coverage config files in project root
   - CI/CD pipeline definitions
   - README documentation

3. **Run with coverage flag** - Most test frameworks support a `--coverage` or similar flag

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_COVERAGE_REPORT.md` with:

```markdown
# Coverage Report - Loop {{LOOP_NUMBER}}

## Summary
- **Overall Line Coverage:** [XX.X%]
- **Target:** 80%
- **Gap to Target:** [XX.X%]
- **Test Framework:** [name and version]
- **Coverage Command Used:** [the command that was run]
- **Total Test Files:** [count]
- **Total Test Cases:** [count]

## Coverage by Module

| Module | Lines | Branches | Functions | Status |
|--------|-------|----------|-----------|--------|
| [module1] | XX% | XX% | XX% | [NEEDS WORK / OK] |
| [module2] | XX% | XX% | XX% | [NEEDS WORK / OK] |
| ... | ... | ... | ... | ... |

## Lowest Coverage Files

Files with coverage below 50% that are good testing candidates:

1. **[filename]** - [XX%] line coverage
   - [Brief description of what this file does]
   - [Why it's important to test]

2. **[filename]** - [XX%] line coverage
   - ...

## Existing Test Patterns

### Test Location
- [ ] Tests alongside source files
- [ ] Tests in dedicated test directories
- [ ] Tests follow naming convention: [describe pattern]
- [ ] Other: [describe]

### Mocking Patterns
- [How the project handles mocks and test doubles]

### Fixture Patterns
- [How test data is organized - factories, fixtures, inline data]

## Recommendations

### Quick Wins (Easy to test, high impact)
1. [Module/file] - [why it's a quick win]

### Requires Setup (Need mocking infrastructure)
1. [Module/file] - [what setup is needed]

### Skip for Now (Low priority or too complex)
1. [Module/file] - [reason to skip]
```

## Guidelines

- **Be accurate**: Run actual coverage commands, don't estimate
- **Note patterns**: Understanding existing tests helps write consistent new ones
- **Identify blockers**: Some code may need refactoring before it's testable
- **Focus on gaps**: We care most about untested critical code
