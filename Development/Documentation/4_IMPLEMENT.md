# Documentation Implementation - Write the Docs

## Context
- **Playbook:** Documentation
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Write documentation for `PENDING` gaps from the evaluation phase. Create high-quality documentation that follows project conventions and helps users understand the code.

## Instructions

1. **Read the plan** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. **Find all `PENDING` items** (not `IMPLEMENTED`, `WON'T DO`, or `PENDING - NEEDS CONTEXT`)
3. **Write documentation** for each PENDING item
4. **Update status** to `IMPLEMENTED` in the plan file
5. **Log changes** to `{{AUTORUN_FOLDER}}/DOC_LOG_{{AGENT_NAME}}_{{DATE}}.md`

## Implementation Checklist

- [ ] **Read configured values**: Read the agent prompt for `COVERAGE_TARGET`, `AUTO_DOC_VISIBILITY`, and `AUTO_DOC_IMPORTANCE`. These define the documentation coverage threshold and which exports are eligible for auto-documentation. Use these values throughout this document wherever you see `[COVERAGE_TARGET]`, `[AUTO_DOC_VISIBILITY]`, or `[AUTO_DOC_IMPORTANCE]` placeholders.

- [ ] **Write documentation (or skip if none)**: Read {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md. If the file doesn't exist OR contains no items with status exactly `PENDING`, mark this task complete without changes. Otherwise, write documentation for ONE `PENDING` item with `[AUTO_DOC_VISIBILITY]` visibility and `[AUTO_DOC_IMPORTANCE]` importance. Follow project documentation conventions. Update status to `IMPLEMENTED` in the plan. Log to DOC_LOG. Only document ONE export per task.

## Documentation Structure

Use the documentation format already established in the project. All doc comments should include:

### For Functions/Methods
```
[Brief description - what does this function do?]

Parameters:
  - paramName: [type] - Description of what this parameter is for
  - optionalParam: [type] - Description (optional, default: X)

Returns:
  [type] - Description of what is returned and when

Errors/Exceptions:
  - [ErrorType]: When [condition that causes this error]

Example:
  [Show typical usage]
```

### For Classes
```
[Brief description - what is this class for?]

[Longer description explaining when to use this class,
its responsibilities, and lifecycle if relevant]

Constructor:
  - param1: [type] - Description
  - param2: [type] - Description

Example:
  [Show how to instantiate and use]
```

### For Types/Interfaces
```
[Brief description - what does this type represent?]

[When to use this type and any constraints]

Properties:
  - propertyName: [type] - Description
  - optionalProp: [type] - Description (optional)
```

## Documentation Quality Checklist

Before marking as IMPLEMENTED:

- [ ] **Description is clear**: Explains WHAT, not HOW
- [ ] **All parameters documented**: With types and descriptions
- [ ] **Return value documented**: What it returns and when
- [ ] **Errors documented**: What exceptions can be thrown
- [ ] **Examples included**: For complex functions
- [ ] **Matches project style**: Consistent with existing docs
- [ ] **No implementation details**: Focus on interface, not internals
- [ ] **Grammatically correct**: Clear, professional language

## What to Include

### Always Include
- **Description**: What does it do? (1-2 sentences)
- **Parameters**: Type, name, description for each
- **Returns**: What comes back, including edge cases

### Include When Relevant
- **Examples**: For complex or non-obvious usage
- **Throws/Raises**: Error conditions
- **See Also**: Related functions or types
- **Deprecated**: If being phased out
- **Since**: Version when added (if project tracks this)

### Avoid
- Implementation details that may change
- Obvious information ("param x: the x value")
- Duplicating the function name in description
- Overly long descriptions
- Outdated examples

## Update Plan Status

After documenting each export, update `LOOP_{{LOOP_NUMBER}}_PLAN.md`:

```markdown
### DOC-001: [Export Name]
- **Status:** `IMPLEMENTED`  ← Changed from PENDING
- **Implemented In:** Loop {{LOOP_NUMBER}}
- **Documentation Added:**
  - [x] Description
  - [x] Parameters (3)
  - [x] Returns
  - [x] Example
```

## Log Format

Append to `{{AUTORUN_FOLDER}}/DOC_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
## Loop {{LOOP_NUMBER}} - [Timestamp]

### Documentation Added

#### DOC-001: [Export Name]
- **Status:** IMPLEMENTED
- **File:** `[path/to/file]`
- **Type:** [Function | Class | Interface]
- **Documentation Summary:**
  - Description: [brief summary of what was written]
  - Parameters: [count] documented
  - Examples: [Yes/No]
- **Coverage Impact:** +[X.X%]

---
```

## Guidelines

- **One export at a time**: Focus on quality over quantity
- **Read the code first**: Understand before documenting
- **Match existing style**: Be consistent with project conventions
- **Think like a user**: What would someone need to know?
- **Examples matter**: Show, don't just tell

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Documented an export:**
1. You've written documentation for exactly ONE export from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. You've appended the change details to `{{AUTORUN_FOLDER}}/DOC_LOG_{{AGENT_NAME}}_{{DATE}}.md`
3. You've updated the item status in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` to `IMPLEMENTED`

**Option B - No PENDING items available:**
1. `LOOP_{{LOOP_NUMBER}}_PLAN.md` doesn't exist, OR
2. It contains no items with status exactly `PENDING`
3. Mark this task complete without making changes

This graceful handling allows the pipeline to continue when a loop iteration produces no actionable documentation gaps.

## When No Documentation Is Available

If there are no items with status exactly `PENDING` in the plan file, append to `{{AUTORUN_FOLDER}}/DOC_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
---

## [YYYY-MM-DD HH:MM] - Loop {{LOOP_NUMBER}} Complete

**Agent:** {{AGENT_NAME}}
**Project:** {{AGENT_NAME}}
**Loop:** {{LOOP_NUMBER}}
**Status:** No PENDING documentation gaps available

**Summary:**
- Items IMPLEMENTED: [count]
- Items WON'T DO: [count]
- Items PENDING - NEEDS CONTEXT: [count]

**Recommendation:** [Either "All automatable documentation complete" or "Remaining items need manual review"]
```

This signals to the pipeline that this loop iteration is complete.
