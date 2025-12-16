# Documentation Gap Evaluation - Prioritize What to Document

## Context
- **Playbook:** Documentation
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Evaluate each documentation gap from the discovery phase and assign visibility and importance ratings. This prioritization ensures we document the most important and visible code first.

## Instructions

1. **Read the gaps list** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`
2. **Rate each gap** for visibility and importance
3. **Assign status** based on ratings
4. **Output prioritized plan** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`

## Evaluation Checklist

- [ ] **Evaluate gaps**: Read LOOP_{{LOOP_NUMBER}}_GAPS.md, rate each gap by VISIBILITY (PUBLIC/INTERNAL/UTILITY/IMPLEMENTATION) and IMPORTANCE (CRITICAL/HIGH/MEDIUM/LOW). Mark PUBLIC or INTERNAL visibility with HIGH or CRITICAL importance as PENDING for auto-documentation. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`.

## Rating Criteria

### Visibility Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **PUBLIC** | Exported for external consumers, part of public API | SDK functions, library exports, API handlers |
| **INTERNAL** | Used across modules within the project | Shared utilities, internal services |
| **UTILITY** | Helper functions, used in limited scope | Format helpers, validation utils |
| **IMPLEMENTATION** | Private/internal details | Internal state, private methods |

### Importance Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **CRITICAL** | Core functionality, widely used, error-prone | Main entry points, complex algorithms |
| **HIGH** | Frequently used, non-obvious behavior | Common utilities, configuration handlers |
| **MEDIUM** | Moderately used, mostly straightforward | Supporting functions, helpers |
| **LOW** | Rarely used, self-explanatory | One-off utilities, simple getters |

### Auto-Documentation Criteria

Gaps will be auto-documented if:
- **Visibility:** PUBLIC or INTERNAL
- **Importance:** CRITICAL or HIGH

Gaps marked `PENDING - NEEDS CONTEXT` if:
- Complex behavior that needs domain knowledge
- Unclear purpose without maintainer input

Gaps marked `WON'T DO` if:
- **Visibility:** IMPLEMENTATION (private/internal)
- **Importance:** LOW with simple, obvious behavior
- Deprecated code slated for removal
- Auto-generated code

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` with:

```markdown
# Documentation Plan - Loop {{LOOP_NUMBER}}

## Summary
- **Total Gaps:** [count]
- **Auto-Document (PENDING):** [count]
- **Needs Context:** [count]
- **Won't Do:** [count]

## Current Coverage: [XX.X%]
## Target Coverage: 90%
## Estimated Post-Loop Coverage: [XX.X%]

---

## PENDING - Ready for Auto-Documentation

### DOC-001: [Export Name]
- **Status:** `PENDING`
- **File:** `[path/to/file]`
- **Gap ID:** GAP-XXX
- **Type:** [Function | Class | Interface | etc.]
- **Visibility:** [PUBLIC | INTERNAL]
- **Importance:** [CRITICAL | HIGH]
- **Signature:**
  ```
  function name(params) -> ReturnType
  ```
- **Documentation Plan:**
  - [ ] Description: [What it does]
  - [ ] Parameters: [List params to document]
  - [ ] Returns: [Return value description]
  - [ ] Examples: [Yes/No - include example?]
  - [ ] Errors: [Throws to document]

### DOC-002: [Export Name]
- **Status:** `PENDING`
...

---

## PENDING - NEEDS CONTEXT

### DOC-XXX: [Export Name]
- **Status:** `PENDING - NEEDS CONTEXT`
- **File:** `[path/to/file]`
- **Gap ID:** GAP-XXX
- **Visibility:** [level]
- **Importance:** [level]
- **Questions:**
  - [What needs clarification?]
  - [What domain knowledge is needed?]

---

## WON'T DO

### DOC-XXX: [Export Name]
- **Status:** `WON'T DO`
- **File:** `[path/to/file]`
- **Gap ID:** GAP-XXX
- **Reason:** [Why skipping - private, deprecated, self-explanatory, etc.]

---

## Documentation Order

Recommended sequence based on visibility and dependencies:

1. **DOC-001** - [name] (PUBLIC, entry point)
2. **DOC-002** - [name] (PUBLIC, depends on DOC-001)
3. **DOC-003** - [name] (INTERNAL, widely used)
...

## Related Documentation

Exports that should be documented together for consistency:

- **Group A:** DOC-001, DOC-003, DOC-007 - All part of [feature] API
- **Group B:** DOC-002, DOC-005 - Related utilities
```

## Guidelines

- **Document public APIs first**: External consumers need docs most
- **Group related exports**: Document together for consistency
- **Consider dependencies**: Document base types before functions using them
- **Match existing style**: Be consistent with codebase conventions
- **Skip obvious code**: Not everything needs documentation
