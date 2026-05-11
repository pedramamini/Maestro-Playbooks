# Document 1: Establish Context

## Context

- **Playbook**: Best PR Comparison
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Understand the feature both PRs implement, fetch their diffs, and establish the evaluation criteria.

## Pull Request Information

PR URLs and category weights are configured in the agent prompt. The agent should read them before starting.

## Tasks

### Task 0: Read Configured Values

- [ ] **Read configured values**: Read the agent prompt for `[PR_A_URL]`, `[PR_B_URL]`, the category weights (`[WEIGHT_SECURITY]`, `[WEIGHT_CORRECTNESS]`, `[WEIGHT_PERFORMANCE]`, `[WEIGHT_TESTS]`, `[WEIGHT_QUALITY]`, `[WEIGHT_DOCS]`, `[WEIGHT_SIZE]`), and `[TIE_THRESHOLD_PCT]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

### Task 1: Fetch PR-A Details

- [ ] **Get PR-A information**: Run `gh pr view [PR_A_URL] --json title,body,additions,deletions,changedFiles,author` to get PR metadata.

- [ ] **Get PR-A diff**: Run `gh pr diff [PR_A_URL]` to get the full diff. Save key observations.

- [ ] **Note PR-A files changed**: List the files modified by PR-A.

### Task 2: Fetch PR-B Details

- [ ] **Get PR-B information**: Run `gh pr view [PR_B_URL] --json title,body,additions,deletions,changedFiles,author` to get PR metadata.

- [ ] **Get PR-B diff**: Run `gh pr diff [PR_B_URL]` to get the full diff. Save key observations.

- [ ] **Note PR-B files changed**: List the files modified by PR-B.

### Task 3: Understand the Feature

- [ ] **Identify the shared goal**: Based on both PR descriptions and diffs, describe what feature both PRs are implementing in 2-3 sentences.

- [ ] **Note any scope differences**: Do the PRs have exactly the same scope, or does one do more/less?

### Task 4: Create Evaluation Criteria Document

- [ ] **Write EVALUATION_CRITERIA.md**: Create `{{AUTORUN_FOLDER}}/EVALUATION_CRITERIA.md`:

```markdown
# Evaluation Criteria for PR Comparison

## Feature Being Implemented
[Description of the shared feature goal]

## PR Information

### PR-A
- **URL**: [PR-A URL]
- **Title**: [Title]
- **Author**: [Author]
- **Size**: +X / -Y lines, Z files

### PR-B
- **URL**: [PR-B URL]
- **Title**: [Title]
- **Author**: [Author]
- **Size**: +X / -Y lines, Z files

## Scoring Scale

| Rating | Score | Meaning |
|--------|-------|---------|
| Excellent | 5 | Exceeds expectations, exemplary |
| Good | 4 | Meets expectations, solid |
| Fair | 3 | Acceptable, room for improvement |
| Poor | 2 | Below expectations, needs work |
| N/A | 0 | Not applicable to this PR |

## Weighted Evaluation Categories

### 1. Security (Weight: [WEIGHT_SECURITY]x)
- Input validation present and correct
- No injection vulnerabilities (SQL, command, XSS)
- Proper authentication/authorization checks
- No secrets or credentials exposed
- Secure data handling

### 2. Correctness (Weight: [WEIGHT_CORRECTNESS]x)
- Feature completeness (does it fully solve the problem?)
- Edge case handling
- Error handling robustness
- Null/undefined safety
- Logic correctness

### 3. Performance (Weight: [WEIGHT_PERFORMANCE]x)
- Algorithm efficiency
- No N+1 queries or unnecessary loops
- Memory usage considerations
- Caching where appropriate
- Async/concurrent handling

### 4. Test Coverage (Weight: [WEIGHT_TESTS]x)
- Unit test coverage for new code
- Integration tests where needed
- Edge case tests
- Test quality and clarity
- Mocking appropriateness

### 5. Code Quality (Weight: [WEIGHT_QUALITY]x)
- Readability and clarity
- Follows existing codebase patterns
- DRY principle adherence
- Appropriate abstraction level
- Naming conventions

### 6. Documentation (Weight: [WEIGHT_DOCS]x)
- Code comments where needed
- README/docs updated if applicable
- API documentation
- Clear commit messages

### 7. PR Size/Simplicity (Weight: [WEIGHT_SIZE]x)
- Lines of code changed (smaller often better)
- Number of files touched
- Complexity introduced
- Focused scope (no unrelated changes)

## Maximum Possible Score

For each category, max contribution = 5 × (configured weight).
Total max = 5 × ([WEIGHT_SECURITY] + [WEIGHT_CORRECTNESS] + [WEIGHT_PERFORMANCE] + [WEIGHT_TESTS] + [WEIGHT_QUALITY] + [WEIGHT_DOCS] + [WEIGHT_SIZE]).

With default weights (3, 3, 2, 2, 1, 1, 1) the total is 65 points.
```

## Success Criteria

- ✅ Both PRs fetched and analyzed
- ✅ Feature goal clearly understood
- ✅ Scope differences noted
- ✅ EVALUATION_CRITERIA.md created with complete rubric

## Status

Mark complete when criteria document is created.

---

**Next**: Document 2 will evaluate PR-A against these criteria.
