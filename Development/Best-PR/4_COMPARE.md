# Document 4: Compare PRs

## Context

- **Playbook**: Best PR Comparison
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Create a side-by-side comparison matrix and determine the winner based on weighted scores.

## Prerequisites

- `{{AUTORUN_FOLDER}}/EVALUATION_CRITERIA.md` exists from Document 1
- `{{AUTORUN_FOLDER}}/PR_A_EVALUATION.md` exists from Document 2
- `{{AUTORUN_FOLDER}}/PR_B_EVALUATION.md` exists from Document 3

## Tasks

### Task 1: Load All Evaluations

- [ ] **Read PR-A evaluation**: Load `{{AUTORUN_FOLDER}}/PR_A_EVALUATION.md` and extract all scores.

- [ ] **Read PR-B evaluation**: Load `{{AUTORUN_FOLDER}}/PR_B_EVALUATION.md` and extract all scores.

### Task 2: Build Comparison Matrix

- [ ] **Calculate weighted scores**: Read the agent prompt for the configured category weights. For each category, multiply the raw score by the configured weight:
  - Security: score × [WEIGHT_SECURITY]
  - Correctness: score × [WEIGHT_CORRECTNESS]
  - Performance: score × [WEIGHT_PERFORMANCE]
  - Test Coverage: score × [WEIGHT_TESTS]
  - Code Quality: score × [WEIGHT_QUALITY]
  - Documentation: score × [WEIGHT_DOCS]
  - PR Size: score × [WEIGHT_SIZE]

- [ ] **Calculate totals**: Sum all weighted scores for each PR.

- [ ] **Calculate percentages**: (Total / max possible) × 100, where max = 5 × ([WEIGHT_SECURITY] + [WEIGHT_CORRECTNESS] + [WEIGHT_PERFORMANCE] + [WEIGHT_TESTS] + [WEIGHT_QUALITY] + [WEIGHT_DOCS] + [WEIGHT_SIZE]).

### Task 3: Determine Winner

- [ ] **Apply decision logic**: Read `[TIE_THRESHOLD_PCT]` from the agent prompt.
  - If percentage difference > [TIE_THRESHOLD_PCT]%: Clear winner
  - If percentage difference ≤ [TIE_THRESHOLD_PCT]%: "Too Close to Call"
  - Note: A tie on points still needs examination of critical categories

- [ ] **Check for disqualifiers**: Regardless of total score:
  - Security score of 2 (Poor) = potential blocker
  - Correctness score of 2 (Poor) = potential blocker
  - Flag these for human review

### Task 4: Analyze Category-by-Category

- [ ] **Identify winning categories**: For each category, note which PR scored higher.

- [ ] **Calculate category differentials**: Where are the biggest gaps?

- [ ] **Identify patterns**: Does one PR consistently win in certain areas?

### Task 5: Create Comparison Matrix Document

- [ ] **Write COMPARISON_MATRIX.md**: Create `{{AUTORUN_FOLDER}}/COMPARISON_MATRIX.md`:

```markdown
# PR Comparison Matrix

**Comparison Date**: {{DATE}}

## Side-by-Side Scores

| Category | Weight | PR-A Score | PR-A Weighted | PR-B Score | PR-B Weighted | Winner |
|----------|--------|------------|---------------|------------|---------------|--------|
| Security | 3x | X | XX | Y | YY | PR-? |
| Correctness | 3x | X | XX | Y | YY | PR-? |
| Performance | 2x | X | XX | Y | YY | PR-? |
| Test Coverage | 2x | X | XX | Y | YY | PR-? |
| Code Quality | 1x | X | XX | Y | YY | PR-? |
| Documentation | 1x | X | XX | Y | YY | PR-? |
| PR Size | 1x | X | XX | Y | YY | PR-? |
| **TOTAL** | **13x** | | **XX/65** | | **YY/65** | **PR-?** |

## Score Summary

| Metric | PR-A | PR-B |
|--------|------|------|
| Weighted Total | XX | YY |
| Percentage | XX% | YY% |
| Categories Won | X/7 | Y/7 |

## Winner Determination

**Result**: [PR-A / PR-B / Too Close to Call]

**Point Differential**: X points (Y%)

**Reasoning**: [Brief explanation of why this PR is the winner or why it's too close]

## Category Analysis

### Where PR-A Excels
[Categories where PR-A scored higher and why]

### Where PR-B Excels
[Categories where PR-B scored higher and why]

### Tied Categories
[Categories with equal scores, if any]

## Critical Category Check

### Security Status
- PR-A: [Score] - [OK / CONCERN / BLOCKER]
- PR-B: [Score] - [OK / CONCERN / BLOCKER]

### Correctness Status
- PR-A: [Score] - [OK / CONCERN / BLOCKER]
- PR-B: [Score] - [OK / CONCERN / BLOCKER]

## Disqualifiers or Blockers
[Any critical issues that should override the point-based decision]
```

## Success Criteria

- ✅ Both evaluations loaded and compared
- ✅ Weighted scores calculated correctly
- ✅ Winner determined (or declared too close)
- ✅ Category-by-category analysis completed
- ✅ Critical category check performed
- ✅ COMPARISON_MATRIX.md created

## Status

Mark complete when comparison matrix is created.

---

**Next**: Document 5 will synthesize the final recommendation with cross-pollination insights.
