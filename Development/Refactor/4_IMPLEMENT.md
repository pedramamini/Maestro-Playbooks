# Refactoring Implementation - Execute Safe Refactors

## Context
- **Playbook:** Refactor
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Implement refactoring candidates that are **LOW risk** AND **HIGH or VERY HIGH benefit** marked as `PENDING`. Update statuses and log all changes made.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`** to get evaluated candidates
2. **For each `PENDING` candidate with LOW risk AND HIGH/VERY HIGH benefit:**
   - Implement the refactoring as described
   - Verify the change doesn't break anything obvious
   - Update status to `IMPLEMENTED`
3. **Skip candidates that are:**
   - `WON'T DO` - Not worth implementing
   - `PENDING - MANUAL REVIEW` - Needs human verification
   - `IMPLEMENTED` - Already done
   - MEDIUM or HIGH risk - Too risky for auto-implementation
   - LOW or MEDIUM benefit - Not enough payoff for auto-implementation
4. **Log all changes** to `{{AUTORUN_FOLDER}}/REFACTOR_LOG_{{AGENT_NAME}}_{{DATE}}.md`
5. **Update the plan** with new statuses

## Implementation Checklist

- [ ] **Implement LOW risk + HIGH benefit PENDING refactors**: Go through each PENDING candidate with LOW risk AND HIGH/VERY HIGH benefit rating, implement the refactoring, and update its status to IMPLEMENTED. Log all changes made.

## Implementation Guidelines

### Before Each Refactor
1. Read the current file content
2. Understand the proposed change
3. Verify the change is still applicable
4. Check for any obvious issues

### During Refactor
1. Make the smallest change that achieves the goal
2. Preserve existing behavior exactly
3. Maintain code style consistency
4. Update imports if moving code

### After Each Refactor
1. Update status to `IMPLEMENTED` in the plan
2. Add entry to the refactor log
3. Note any follow-up work needed

## What to Implement (By Category)

### File Size Refactors (LOW Risk)
- Extract clearly separable functions to new files
- Move utilities from component files to utils/
- Split large files along clear boundaries

### Duplication Refactors (LOW Risk)
- Extract repeated code blocks to shared functions
- Parameterize nearly-identical functions
- Create shared utilities for common patterns

### Complexity Refactors (LOW Risk)
- Extract deeply nested logic to helper functions
- Break long functions into smaller named steps
- Extract complex conditionals to named predicates

### Dead Code Refactors (LOW Risk)
- Remove unused imports
- Remove commented-out code
- Remove unused private functions (after verification)

### Organization Refactors (LOW Risk)
- Add module re-exports or entry point files for cleaner imports
- Move misplaced utilities to appropriate directories
- Consolidate scattered constants

## Log Format

Append to `{{AUTORUN_FOLDER}}/REFACTOR_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
## Loop {{LOOP_NUMBER}} - [Timestamp]

### Implemented Refactors

#### 1. [Candidate Name]
- **File(s):** `path/to/file`
- **Category:** [File Size / Duplication / Complexity / etc.]
- **Change:** [Brief description of what was done]
- **Lines Changed:** [Approximate +/- lines]
- **New Files:** [Any new files created, if applicable]
- **Notes:** [Any relevant observations]

#### 2. [Candidate Name]
...

### Skipped (This Loop)
- [Candidate X] - PENDING - MANUAL REVIEW
- [Candidate Y] - WON'T DO: [brief reason]
- [Candidate Z] - MEDIUM risk, needs review

### Statistics
- **Candidates Evaluated:** [Total in plan]
- **Implemented:** [Count]
- **Skipped (Manual Review):** [Count]
- **Skipped (Won't Do):** [Count]
- **Remaining PENDING:** [Count]
```

## Safety Checks

Before implementing each refactor:

1. **Scope Check**: Is this change confined to the expected files?
2. **Import Check**: Will this break any imports?
3. **Export Check**: Are we changing any public interfaces?
4. **Style Check**: Does the refactored code match project style?

## Guidelines

- **One at a time**: Implement refactors individually, not in batches
- **Verify each**: Check for obvious issues after each change
- **Log everything**: Document what was done and why
- **Preserve behavior**: Refactoring must not change functionality
- **Update plan**: Mark items as IMPLEMENTED after completion
