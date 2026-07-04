# Best PR Comparison Playbook

A Maestro Auto Run playbook that objectively compares two competing pull requests implementing the same feature, determines a winner, and extracts valuable insights from the runner-up.

## What This Playbook Does

When two developers create different implementations for the same feature, this playbook provides an objective, criteria-based comparison to determine which PR should be merged—and what good ideas from the other PR should be incorporated.

### Key Features

- **Objective Scoring**: Weighted rubric with qualitative labels (Excellent/Good/Fair/Poor) backed by numeric values
- **Weighted Categories**: Security and correctness matter more than code style
- **Cross-Pollination**: Extracts "gems" from the runner-up PR
- **Actionable Output**: Provides next steps to improve the winning PR

### Prerequisites

This Playbook works best if you have the `gh` CLI installed and authenticated.

## Scoring System

### Scale

| Rating | Score | Meaning |
|--------|-------|---------|
| Excellent | 5 | Exceeds expectations, exemplary |
| Good | 4 | Meets expectations, solid |
| Fair | 3 | Acceptable, room for improvement |
| Poor | 2 | Below expectations, needs work |
| N/A | 0 | Not applicable to this PR |

### Weighted Categories

| Category | Weight | Rationale |
|----------|--------|-----------|
| Security | 3x | Critical—vulnerabilities are blockers |
| Correctness | 3x | Must work correctly |
| Performance | 2x | Important for user experience |
| Test Coverage | 2x | Ensures maintainability |
| Code Quality | 1x | Readability, patterns, DRY |
| Documentation | 1x | Helpful but not critical |
| PR Size/Simplicity | 1x | Smaller is easier to review |

**Maximum Possible Score**: 65 points (if all categories score Excellent)

## Playbook Structure

This playbook follows a **linear 5-document pattern** (no looping):

```
1_ESTABLISH_CONTEXT.md  - Understand feature, fetch PR diffs, set up rubric
2_EVALUATE_PR_A.md      - Score PR-A against all weighted criteria
3_EVALUATE_PR_B.md      - Score PR-B against same criteria
4_COMPARE.md            - Side-by-side matrix, determine winner
5_SYNTHESIZE.md         - Final recommendation + cross-pollination insights
```

## Prerequisites

- Maestro installed and configured
- `gh` CLI installed and authenticated (`gh auth login`)
- Access to both PR repositories
- Agent with network access to fetch PR data

## Setup in Maestro

1. Place this folder in your Maestro Auto Run directory
2. In the Auto Run agent prompt panel, set `PR_A_URL` and `PR_B_URL` to the GitHub URLs of the two competing PRs. Optionally tune the category weights and `TIE_THRESHOLD_PCT`.
3. Configure Auto Run settings:
   - **Loop Mode**: OFF (sequential execution)
   - **Max Loops**: N/A (no looping)
4. Run the playbook

## Working Files Generated

| File | Purpose |
|------|---------|
| `EVALUATION_CRITERIA.md` | The rubric with weights and scoring guide |
| `PR_A_EVALUATION.md` | Detailed scores and notes for PR-A |
| `PR_B_EVALUATION.md` | Detailed scores and notes for PR-B |
| `COMPARISON_MATRIX.md` | Side-by-side scoring table |
| `BEST_PR_SUMMARY.md` | Final recommendation with next steps |

## Output: BEST_PR_SUMMARY.md

The final summary includes:

1. **Winner Declaration**: PR-A, PR-B, or "Too Close to Call"
2. **Score Summary**: Side-by-side weighted scores
3. **Key Differentiators**: Why the winner won
4. **Gems from the Runner-Up**: Good ideas worth incorporating
5. **Next Recommended Steps**: Improvements before merge

## Customization

### Adjusting Weights

Tune `WEIGHT_SECURITY`, `WEIGHT_CORRECTNESS`, `WEIGHT_PERFORMANCE`, `WEIGHT_TESTS`, `WEIGHT_QUALITY`, `WEIGHT_DOCS`, and `WEIGHT_SIZE` in the agent prompt to match your project's priorities. For example:
- Increase `WEIGHT_DOCS` for public APIs
- Increase `WEIGHT_PERFORMANCE` for hot paths
- Decrease `WEIGHT_SIZE` for complex features

### Adding Criteria

Add custom criteria in Document 1's rubric section. Ensure you apply the same criteria in Documents 2 and 3.

## Exit Conditions

Playbook completes when all 5 documents report `COMPLETED` status.

## Possible Outcomes

| Outcome | Meaning | Next Action |
|---------|---------|-------------|
| **PR-A Wins** | PR-A scored higher | Merge PR-A, consider runner-up gems |
| **PR-B Wins** | PR-B scored higher | Merge PR-B, consider runner-up gems |
| **Too Close to Call** | Scores within 5% | Human decision needed, focus on synthesis |

## Support

For issues or questions, refer to the Maestro documentation at <https://github.com/pedramamini/Maestro>.
