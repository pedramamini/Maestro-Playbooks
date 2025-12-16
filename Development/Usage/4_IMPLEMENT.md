# Usage Documentation Implementation - Update README

## Context
- **Playbook:** Usage
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Implement ONE documentation fix from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` that has status `PENDING`. Update the project's README.md and log the change.

## Instructions

1. **Read the plan** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. **Find a `PENDING` item** with CRITICAL/HIGH importance and EASY/MEDIUM effort
3. **Implement the fix** in `{{AGENT_PATH}}/README.md`
4. **Update status** to `IMPLEMENTED` in the plan file
5. **Log the change** to `{{AUTORUN_FOLDER}}/USAGE_LOG_{{AGENT_NAME}}_{{DATE}}.md`

## Implementation Checklist

- [ ] **Fix one documentation gap**: Read LOOP_{{LOOP_NUMBER}}_PLAN.md, find an item with status exactly `PENDING`, implement the fix in the project's README.md, mark as IMPLEMENTED in the plan, and log to USAGE_LOG. Only fix ONE gap per task.

## Fix Types

### For MISSING Features
- Add a new section or bullet point describing the feature
- Include brief usage example if applicable
- Place in the appropriate section of the README

### For STALE Documentation
- Remove or update references to removed features
- Update command syntax or options that changed
- Remove outdated screenshots or links

### For INACCURATE Documentation
- Correct the description to match actual behavior
- Update examples to use correct syntax
- Fix default values, options, or parameters

### For INCOMPLETE Documentation
- Add missing details, options, or examples
- Expand brief mentions into useful descriptions
- Add links to more detailed docs if available

## Writing Guidelines

### Tone and Style
- **Match existing README style** - Follow the same formatting and voice
- **Be concise** - Users skim READMEs, keep it scannable
- **Use examples** - Show, don't just tell
- **Think like a new user** - What would they need to know?

### Formatting
- Use the same heading levels as existing sections
- Match bullet point and code block styles
- Keep line lengths consistent with the file
- Preserve any existing badges, links, or structure

### Content
- **Feature name** - Clear, recognizable name
- **What it does** - One sentence description
- **How to use it** - Brief example or syntax
- **Any caveats** - Important limitations or requirements

## Output Format

After implementing, append to `{{AUTORUN_FOLDER}}/USAGE_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
---

## [YYYY-MM-DD HH:MM] - [Brief Description]

**Agent:** {{AGENT_NAME}}
**Project:** {{AGENT_PATH}}
**Loop:** {{LOOP_NUMBER}}
**Doc ID:** DOC-XXX
**Gap ID:** GAP-XXX

### Change Type
[MISSING → Added | STALE → Removed | INACCURATE → Corrected | INCOMPLETE → Expanded]

### README Section
[Section name where change was made]

### What Was Changed
[1-2 sentence description of the change]

### Content Added/Changed
```markdown
[The actual text that was added or changed]
```

### Verification
- [ ] Change matches the proposed fix from LOOP_{{LOOP_NUMBER}}_PLAN.md
- [ ] Formatting matches existing README style
- [ ] No broken links or references introduced
- [ ] Content is accurate based on code review
```

## Update Plan Status

After implementing, update `LOOP_{{LOOP_NUMBER}}_PLAN.md`:

```markdown
### DOC-001: [Feature Name]
- **Status:** `IMPLEMENTED`  ← Changed from PENDING
- **Implemented In:** Loop {{LOOP_NUMBER}}
- **Changes Made:**
  - [x] Added feature description
  - [x] Added usage example
```

## Guidelines

- **One fix per run** - Implement exactly ONE fix, then stop
- **Follow the plan** - Implement what was proposed, don't improvise
- **Preserve structure** - Don't reorganize unrelated parts of README
- **Update both files** - Log the change AND update status in plan
- **Be conservative** - If unclear, skip and note why

## When No Fixes Are Available

If there are no items with status exactly `PENDING` in the plan file, append to the log:

```markdown
---

## [YYYY-MM-DD HH:MM] - Loop {{LOOP_NUMBER}} Complete

**Agent:** {{AGENT_NAME}}
**Project:** {{AGENT_PATH}}
**Loop:** {{LOOP_NUMBER}}
**Status:** No PENDING fixes available

**Summary:**
- Items IMPLEMENTED: [count]
- Items WON'T DO: [count]
- Items PENDING - NEEDS REVIEW: [count]

**README Accuracy:** [estimate]%
**Recommendation:** [All gaps fixed | Remaining items need maintainer review]
```
