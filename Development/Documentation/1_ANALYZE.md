# Documentation Analysis - Coverage Measurement

## Context
- **Playbook:** Documentation
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Measure current documentation coverage and identify the documentation landscape. This document establishes the baseline metrics that drive the documentation pipeline.

## Instructions

1. **Identify the documentation style** - Detect the project's doc comment format
2. **Count documented vs undocumented exports** - Functions, classes, types
3. **Calculate coverage percentage** - Documented / Total exports
4. **Identify documentation patterns** - How existing docs are structured
5. **Output report** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_DOC_REPORT.md`

## Analysis Checklist

- [ ] **Measure documentation coverage**: Survey the codebase for exported/public functions, classes, and types. Count how many have doc comments vs how many are undocumented. Calculate the percentage. Identify the existing documentation style and conventions. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_DOC_REPORT.md`.

## What to Count

### Documented (Has Documentation)
- Functions with doc comments describing purpose
- Classes with class-level documentation
- Interfaces/types with description comments
- Modules with header comments or README
- Constants with explanatory comments (if not self-evident)

### Undocumented (Needs Documentation)
- Exported functions without any doc comment
- Public classes without class description
- Complex types without explanation
- Non-obvious constants without comments
- Modules without any overview documentation

### Excluded from Count
- Private/internal functions (not exported)
- Test files and test utilities
- Auto-generated code (marked as such)
- Third-party/vendor directories
- Configuration files

## Documentation Style Detection

Look for how the project documents code:

1. **Check existing documented functions** - What format do they use?
2. **Look for style guides** - CONTRIBUTING.md, docs/ folder
3. **Check linter configs** - May enforce doc comment rules
4. **Follow existing patterns** - Match what's already there

Common patterns to identify:
- Doc comment syntax (block comments, triple-quotes, etc.)
- Parameter documentation format
- Return value documentation format
- Whether examples are included
- Whether errors/exceptions are documented

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_DOC_REPORT.md` with:

```markdown
# Documentation Coverage Report - Loop {{LOOP_NUMBER}}

## Summary
- **Overall Coverage:** [XX.X%]
- **Target:** 90%
- **Gap to Target:** [XX.X%]
- **Documentation Style:** [describe the format used]

## Coverage by Category

| Category | Documented | Total | Coverage |
|----------|------------|-------|----------|
| Functions | XX | XX | XX% |
| Classes | XX | XX | XX% |
| Interfaces/Types | XX | XX | XX% |
| Modules | XX | XX | XX% |
| **Total** | **XX** | **XX** | **XX%** |

## Coverage by Module/Directory

| Module | Documented | Total | Coverage | Status |
|--------|------------|-------|----------|--------|
| [module1] | XX | XX | XX% | [NEEDS WORK / OK] |
| [module2] | XX | XX | XX% | [NEEDS WORK / OK] |
| ... | ... | ... | ... | ... |

## Lowest Coverage Areas

Modules with coverage below 70%:

1. **[module/path]** - [XX%] coverage
   - [XX] undocumented exports
   - Key exports: [list important undocumented items]

2. **[module/path]** - [XX%] coverage
   - ...

## Existing Documentation Patterns

### Style Guide Observations
- **Comment style:** [describe the doc comment format]
- **Parameter format:** [how params are documented]
- **Return format:** [how return values are documented]
- **Example usage:** [Present | Absent | Inconsistent]

### Common Patterns Found
- [Pattern 1 - e.g., "All API handlers are documented"]
- [Pattern 2 - e.g., "Utility functions often lack docs"]
- [Pattern 3 - e.g., "Types are well-documented"]

## High-Value Documentation Targets

### Quick Wins (Easy to document, high visibility)
1. [Export name] in [file] - [why it's a quick win]

### High Priority (Heavily used, undocumented)
1. [Export name] in [file] - [usage count or importance]

### Skip for Now (Low priority)
1. [Export name] in [file] - [reason to skip]
```

## Guidelines

- **Be accurate**: Actually count, don't estimate
- **Note style**: Match existing conventions
- **Identify patterns**: Some modules may be consistently documented
- **Focus on exports**: Internal functions are lower priority
