# Refactoring Discovery - Find Specific Issues

## Context
- **Playbook:** Refactor
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Execute the tactics from the game plan to find **specific, actionable refactoring candidates**. Each candidate should be a concrete piece of code that can be improved.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md`** to get the investigation tactics
2. **Execute each tactic** using grep, glob, file reading, and code analysis
3. **Document specific findings** with file paths and line numbers
4. **Output candidates** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`

## Discovery Checklist

- [ ] **Execute tactics**: Run through each tactic from the game plan, searching for specific issues. Document each finding with enough detail to understand the refactoring opportunity.

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md` with the following structure:

```markdown
# Refactoring Candidates - Loop {{LOOP_NUMBER}}

## Summary
- **Total Candidates Found:** [Number]
- **By Category:**
  - File Size: [Count]
  - Duplication: [Count]
  - Complexity: [Count]
  - Dead Code: [Count]
  - Organization: [Count]

## Candidates

### Candidate 1: [Brief Description]
- **Category:** [File Size / Duplication / Complexity / Dead Code / Organization]
- **Location:** `path/to/file:LINE-LINE`
- **Current State:** [Describe what's wrong]
- **Proposed Change:** [Brief description of the refactoring]
- **Code Context:**
  ```
  // Relevant code snippet showing the issue
  ```

### Candidate 2: [Brief Description]
...
```

## What to Look For

### File Size Candidates
- Files over 500 LOC → Consider splitting by concern
- Single file with multiple unrelated exports → Extract to separate modules
- Component files with embedded utilities → Move utilities to shared location

### Duplication Candidates
- Two functions that differ only in variable names → Parameterize
- Repeated code blocks (3+ occurrences) → Extract to utility
- Similar components → Create shared base or composition

### Complexity Candidates
- Functions with 3+ levels of nesting → Extract to smaller functions
- Functions over 50 LOC → Break into logical steps
- Complex conditionals → Extract to named boolean functions
- Many parameters → Use options object pattern

### Dead Code Candidates
- Functions with no callers → Remove (verify first)
- Commented-out code → Remove (it's in git history)
- Unused imports → Remove
- Unused variables → Remove or investigate

### Organization Candidates
- Utilities in component files → Move to utils/
- Constants scattered → Consolidate to constants/
- Types in multiple files → Consolidate to types/

## Guidelines

- **Be specific**: Include exact file paths and line numbers
- **Show context**: Include code snippets that illustrate the issue
- **One issue per candidate**: Don't bundle unrelated issues
- **Skip trivials**: Focus on issues worth the refactoring effort
- **Note dependencies**: If a change might affect other files, note it
