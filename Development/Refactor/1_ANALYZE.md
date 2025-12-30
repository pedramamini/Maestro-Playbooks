# Refactoring Analysis - Codebase Survey

## Context
- **Playbook:** Refactor
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Analyze the codebase to identify **categories of refactoring opportunities** and create a game plan for systematic improvement. This document drives the discovery phase - finding WHERE to look for code that needs simplification.

## Instructions

1. **Survey the codebase structure** - Identify main directories, file sizes, and organization patterns
2. **Identify refactoring-sensitive areas** based on:
   - Large files (500+ LOC)
   - Complex functions (50+ LOC, deep nesting)
   - Code duplication patterns
   - Inconsistent organization
   - Dead or unused code
3. **Output a tactical game plan** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md`

## Analysis Checklist

- [ ] **Survey codebase (if needed)**: First check if `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md` already exists with at least one tactic defined. If it does, skip the survey and mark this task complete—the game plan is already in place. If it doesn't exist, examine project structure, find largest files, identify patterns. Note file size distribution and any obvious organizational issues.

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAME_PLAN.md` with the following structure:

```markdown
# Refactoring Game Plan

## Codebase Profile
- **Total Files:** [Approximate count]
- **Largest Files:** [List top 5-10 by LOC]
- **Key Directories:** [Main source directories]
- **Existing Patterns:** [Any abstractions, utilities, or patterns already in use]

## Investigation Tactics

Each tactic is a specific, actionable search pattern for finding refactoring opportunities.

### Tactic 1: [Name]
- **Target:** [What type of issue this finds]
- **Search Pattern:** [Specific grep/glob patterns or metrics to look for]
- **Files to Check:** [Specific files or glob patterns]
- **Why It Matters:** [Brief explanation of maintainability impact]

### Tactic 2: [Name]
...
```

## Tactic Categories to Consider

When creating tactics, consider these common refactoring opportunity categories:

### File Size Issues
- Files over 500 lines of code
- Components with multiple unrelated functions
- "God" modules that do too many things
- Files that should be split by feature/concern

### Code Duplication
- Similar functions in different files
- Copy-pasted code blocks with minor variations
- Repeated patterns that could be utility functions
- Similar components that could share a base

### Function Complexity
- Functions over 50 lines
- Deeply nested conditionals (3+ levels of if/else/switch)
- Functions with 5+ parameters
- Complex boolean expressions that should be extracted
- Long chains of method calls

### Dead Code
- Unused exports
- Commented-out code blocks
- Functions that are never called
- Unused variables and imports
- Deprecated code without removal timeline

### Organization Issues
- Utilities scattered across the codebase
- Inconsistent file naming conventions
- Missing module re-exports or entry points
- Cross-cutting concerns mixed into components

## Guidelines

- **Be specific**: Each tactic should have concrete search patterns
- **Prioritize**: Order tactics by likely impact (biggest maintenance wins first)
- **Be realistic**: Focus on issues that can be safely refactored
- **No implementation**: This phase is discovery only - find WHERE to look, not WHAT to change
