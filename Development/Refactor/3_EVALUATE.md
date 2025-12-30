# Refactoring Evaluation - Risk & Benefit Assessment

## Context
- **Playbook:** Refactor
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Evaluate each refactoring candidate with **risk and benefit ratings** to determine which should be auto-implemented, which need manual review, and which should be skipped.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`** to get the list of candidates
2. **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`** (if it exists) to see which candidates have already been evaluated
3. **Select ONE unevaluated candidate** (one that doesn't appear in the plan yet)
4. **Evaluate it** for risk and benefit
5. **Assign a status** based on the evaluation matrix
6. **Append to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`**

## Evaluation Checklist

- [ ] **Evaluate one candidate (or skip if empty)**: Read {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md. If it contains no findings OR all findings have already been evaluated in LOOP_{{LOOP_NUMBER}}_PLAN.md, mark this task complete without changes. Otherwise, pick one unevaluated candidate, assess risk/benefit, and append to {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md.

## Risk Assessment Criteria

| Risk Level | Criteria |
|------------|----------|
| **LOW** | Internal-only change, no API changes, single file, easy to verify, no side effects |
| **MEDIUM** | May affect callers, multiple files, requires testing, some external dependencies |
| **HIGH** | Breaking changes, public API modification, many dependents, complex migration |

### Risk Factors to Consider
- Does it change exported interfaces?
- How many files import/use this code?
- Is there test coverage for this code?
- Does it affect data flow or state?
- Could it introduce subtle behavioral changes?

## Benefit Assessment Criteria

| Benefit Level | Criteria |
|---------------|----------|
| **LOW** | Minor cleanup, cosmetic improvement, slightly better naming |
| **MEDIUM** | Improved readability, reduced cognitive load, easier maintenance |
| **HIGH** | Significant duplication removal, major complexity reduction, much easier to modify |
| **VERY HIGH** | Architectural improvement, enables future work, fixes structural problem |

### Benefit Factors to Consider
- How much duplicate code is removed?
- How much is complexity reduced?
- How much easier will future changes be?
- Does it improve test coverage or testability?
- Does it align with architectural goals?

## Status Assignment Matrix

| Risk ↓ / Benefit → | LOW | MEDIUM | HIGH | VERY HIGH |
|-------------------|-----|--------|------|-----------|
| **LOW** | `WON'T DO` | `PENDING` | `PENDING` | `PENDING` |
| **MEDIUM** | `WON'T DO` | `PENDING - MANUAL REVIEW` | `PENDING` | `PENDING` |
| **HIGH** | `WON'T DO` | `WON'T DO` | `PENDING - MANUAL REVIEW` | `PENDING - MANUAL REVIEW` |

## Output Format

Append to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` using this structure (create file with header if it doesn't exist):

```markdown
# Refactoring Plan - Loop {{LOOP_NUMBER}}

## Summary
- **Total Candidates:** [Number]
- **PENDING (auto-implement):** [Count]
- **PENDING - MANUAL REVIEW:** [Count]
- **WON'T DO:** [Count]

## Status Matrix

| # | Candidate | Risk | Benefit | Status |
|---|-----------|------|---------|--------|
| 1 | [Brief name] | LOW | HIGH | PENDING |
| 2 | [Brief name] | MEDIUM | MEDIUM | PENDING - MANUAL REVIEW |
| 3 | [Brief name] | HIGH | LOW | WON'T DO |

## Detailed Evaluations

### 1. [Candidate Name]
- **Location:** `path/to/file:LINE-LINE`
- **Category:** [File Size / Duplication / Complexity / etc.]
- **Risk:** [LOW/MEDIUM/HIGH]
- **Benefit:** [LOW/MEDIUM/HIGH/VERY HIGH]
- **Status:** [PENDING / PENDING - MANUAL REVIEW / WON'T DO]
- **Risk Rationale:** [Why this risk level]
- **Benefit Rationale:** [Why this benefit level]
- **Refactoring Approach:** [How to implement this refactor]

### 2. [Candidate Name]
...
```

## Status Definitions

| Status | Meaning | Next Step |
|--------|---------|-----------|
| `PENDING` | Safe to auto-implement | Will be refactored in step 4 |
| `PENDING - MANUAL REVIEW` | Needs human verification | Skipped in auto-mode |
| `WON'T DO` | Not worth the risk | Skipped permanently |
| `IMPLEMENTED` | Completed | (Set by step 4) |

## Guidelines

- **One candidate per run**: Only evaluate ONE candidate, then stop. This allows incremental progress.
- **Be conservative with risk**: When in doubt, rate risk higher
- **Consider dependencies**: Check what imports/uses the code
- **Think about tests**: Untested code = higher risk
- **Document rationale**: Future you will thank present you
- **Include approach**: Describe HOW to do the refactor, not just WHAT

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Evaluated a candidate:**
1. You've evaluated exactly ONE candidate from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_CANDIDATES.md`
2. You've appended a complete evaluation to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
3. The evaluation includes both risk and benefit ratings
4. The status is set according to the matrix above

**Option B - No candidates to evaluate:**
1. `LOOP_{{LOOP_NUMBER}}_CANDIDATES.md` contains no findings, OR
2. All findings have already been evaluated in `LOOP_{{LOOP_NUMBER}}_PLAN.md`
3. Mark this task complete without making changes

This graceful handling of empty states prevents the pipeline from stalling when a tactic yields no candidates.
