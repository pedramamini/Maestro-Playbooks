# Usage Documentation Gap Discovery

## Context
- **Playbook:** Usage
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Compare the feature inventory against the README to identify specific documentation gaps. This includes features missing from the README, stale documentation for removed features, and inaccurate descriptions.

## Instructions

1. **Read the feature inventory** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_FEATURE_INVENTORY.md`
2. **Identify discrepancies** between code and README
3. **Classify each gap** by type (missing, stale, inaccurate)
4. **Output findings** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`

## Gap Discovery Checklist

- [ ] **Find documentation gaps**: Read LOOP_{{LOOP_NUMBER}}_FEATURE_INVENTORY.md, compare features in code vs README. Identify: (1) features in code but missing from README, (2) features in README but removed from code, (3) features documented inaccurately. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`.

## Gap Types

### MISSING - Feature exists in code but not in README
- New features added without documentation
- Major functionality users should know about
- Configuration options not explained
- Commands or shortcuts not listed

### STALE - Feature in README but not in code
- Features that were removed
- Deprecated functionality still documented
- Old command names or syntax
- References to removed files or options

### INACCURATE - Feature exists but description is wrong
- Changed behavior not reflected in docs
- Incorrect examples or syntax
- Wrong default values documented
- Outdated screenshots or demos referenced

### INCOMPLETE - Feature documented but lacking detail
- Missing important options or flags
- No examples for complex features
- Missing error handling guidance
- Unclear or ambiguous descriptions

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md` with:

```markdown
# Documentation Gaps - Loop {{LOOP_NUMBER}}

## Summary
- **Total Gaps Found:** [count]
- **MISSING (undocumented features):** [count]
- **STALE (removed features still documented):** [count]
- **INACCURATE (wrong descriptions):** [count]
- **INCOMPLETE (needs more detail):** [count]

---

## Gap List

### GAP-001: [Feature Name]
- **Type:** [MISSING | STALE | INACCURATE | INCOMPLETE]
- **Feature:** [name of the feature]
- **Code Location:** `[path/to/file]` (if applicable)
- **README Location:** [section name / line numbers] (if applicable)
- **Description:**
  [What the gap is - e.g., "Feature X allows users to do Y but is not mentioned in README"]
- **Evidence:**
  - Code: [what the code shows]
  - README: [what the README says, or "not mentioned"]
- **User Impact:** [Why a user would care about this gap]

### GAP-002: [Feature Name]
- **Type:** [MISSING | STALE | INACCURATE | INCOMPLETE]
...

---

## Gaps by Type

### MISSING Features
| Gap ID | Feature | Code Location | User Impact |
|--------|---------|---------------|-------------|
| GAP-XXX | [name] | [location] | [impact] |
| ... | ... | ... | ... |

### STALE Documentation
| Gap ID | Feature | README Section | What Changed |
|--------|---------|----------------|--------------|
| GAP-XXX | [name] | [section] | [removed/deprecated] |
| ... | ... | ... | ... |

### INACCURATE Documentation
| Gap ID | Feature | What's Wrong | Correct Behavior |
|--------|---------|--------------|------------------|
| GAP-XXX | [name] | [incorrect info] | [actual behavior] |
| ... | ... | ... | ... |

### INCOMPLETE Documentation
| Gap ID | Feature | What's Missing |
|--------|---------|----------------|
| GAP-XXX | [name] | [missing info] |
| ... | ... | ... |

---

## Priority Indicators

### High Priority Gaps
Features that new users would immediately encounter or need:
1. GAP-XXX: [feature] - [reason]
2. ...

### Medium Priority Gaps
Features that regular users would use:
1. GAP-XXX: [feature] - [reason]
2. ...

### Low Priority Gaps
Advanced features or edge cases:
1. GAP-XXX: [feature] - [reason]
2. ...
```

## Guidelines

- **Be specific** - Include file paths and line numbers where possible
- **Focus on user impact** - Why would a user care about this gap?
- **Check both directions** - Missing features AND stale docs
- **Note severity** - Some gaps matter more than others
- **Verify gaps** - Make sure it's actually a discrepancy, not a false positive
