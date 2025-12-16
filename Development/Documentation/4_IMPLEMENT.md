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

- [ ] **Write documentation**: Read LOOP_{{LOOP_NUMBER}}_PLAN.md, write documentation for ONE `PENDING` item with PUBLIC/INTERNAL visibility and HIGH/CRITICAL importance. Follow project documentation conventions. Update status to `IMPLEMENTED` in the plan. Log to DOC_LOG. Only document ONE export per task.

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
