# Usage Documentation Gap Evaluation

## Context
- **Playbook:** Usage
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Evaluate each documentation gap from the discovery phase and assign importance and effort ratings. This prioritization ensures we fix the most impactful gaps first - the ones that would confuse or frustrate users the most.

## Instructions

1. **Read the gaps list** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`
2. **Rate each gap** for user importance and fix effort
3. **Assign status** based on ratings
4. **Output prioritized plan** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`

## Evaluation Checklist

- [ ] **Evaluate gaps (or skip if empty)**: Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`. If it contains no gaps OR all gaps have already been evaluated in `LOOP_{{LOOP_NUMBER}}_PLAN.md`, mark this task complete without changes. Otherwise, rate each gap by USER IMPORTANCE (CRITICAL/HIGH/MEDIUM/LOW) and FIX EFFORT (EASY/MEDIUM/HARD). Mark gaps with HIGH/CRITICAL importance and EASY/MEDIUM effort as PENDING for auto-fix. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`.

## Rating Criteria

### User Importance Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **CRITICAL** | Blocks users from basic usage, causes confusion or errors | Missing installation steps, wrong command syntax, stale getting-started |
| **HIGH** | Affects common workflows, users will definitely encounter | Missing major feature docs, incorrect configuration, stale common commands |
| **MEDIUM** | Affects regular usage, users may encounter | Missing secondary features, incomplete examples, minor inaccuracies |
| **LOW** | Affects advanced/edge cases, few users will notice | Missing advanced options, incomplete edge case docs, cosmetic issues |

### Fix Effort Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **EASY** | Simple text addition or removal, clear what to write | Add one-liner feature mention, remove stale section, fix typo |
| **MEDIUM** | Requires some investigation, moderate text changes | Add feature description with examples, rewrite outdated section |
| **HARD** | Extensive rewrite, requires deep understanding | Major section restructure, comprehensive feature documentation |

### Auto-Fix Criteria

Gaps will be auto-fixed if:
- **User Importance:** CRITICAL or HIGH
- **Fix Effort:** EASY or MEDIUM

Gaps marked `PENDING - NEEDS REVIEW` if:
- Complex changes that need maintainer input
- Unclear what the correct documentation should be

Gaps marked `WON'T DO` if:
- **User Importance:** LOW with HARD effort
- Internal features that don't need user docs
- Intentionally undocumented (internal use only)

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` with:

```markdown
# Documentation Fix Plan - Loop {{LOOP_NUMBER}}

## Summary
- **Total Gaps:** [count]
- **Auto-Fix (PENDING):** [count]
- **Needs Review:** [count]
- **Won't Do:** [count]

## Current README Accuracy: [estimate]%
## Target README Accuracy: 90%

---

## PENDING - Ready for Auto-Fix

### DOC-001: [Feature/Gap Name]
- **Status:** `PENDING`
- **Gap ID:** GAP-XXX
- **Type:** [MISSING | STALE | INACCURATE | INCOMPLETE]
- **User Importance:** [CRITICAL | HIGH]
- **Fix Effort:** [EASY | MEDIUM]
- **README Section:** [where to add/update]
- **Fix Description:**
  [What needs to be written/changed]
- **Proposed Content:**
  ```markdown
  [Draft of the README content to add/change]
  ```

### DOC-002: [Feature/Gap Name]
- **Status:** `PENDING`
...

---

## PENDING - NEEDS REVIEW

### DOC-XXX: [Feature/Gap Name]
- **Status:** `PENDING - NEEDS REVIEW`
- **Gap ID:** GAP-XXX
- **User Importance:** [level]
- **Fix Effort:** [level]
- **Questions:**
  - [What needs clarification?]
  - [What's unclear about the feature?]

---

## WON'T DO

### DOC-XXX: [Feature/Gap Name]
- **Status:** `WON'T DO`
- **Gap ID:** GAP-XXX
- **Reason:** [Why skipping - low impact, internal only, intentionally undocumented, etc.]

---

## Fix Order

Recommended sequence based on importance and dependencies:

1. **DOC-001** - [name] (CRITICAL, blocks getting started)
2. **DOC-002** - [name] (HIGH, common workflow)
3. **DOC-003** - [name] (HIGH, related to DOC-002)
...

## README Section Updates Needed

| Section | Gaps to Fix | Action Needed |
|---------|-------------|---------------|
| Getting Started | DOC-001, DOC-003 | Add missing steps |
| Features | DOC-002, DOC-005 | Add new features |
| Configuration | DOC-004 | Update outdated info |
| [removed section] | DOC-006 | Remove stale content |
```

## Guidelines

- **Prioritize user-facing impact** - What would frustrate a new user?
- **Consider the README audience** - New users, not internal devs
- **Group related fixes** - Features that should be documented together
- **Draft actual content** - Include proposed README text where possible
- **Note dependencies** - Some fixes may depend on others

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Evaluated gaps:**
1. You've read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_GAPS.md`
2. You've evaluated gaps with importance and effort ratings
3. You've output the prioritized plan to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
4. Each gap has a status (PENDING, PENDING - NEEDS REVIEW, or WON'T DO)

**Option B - No gaps to evaluate:**
1. `LOOP_{{LOOP_NUMBER}}_GAPS.md` contains no gaps, OR
2. All gaps have already been evaluated in `LOOP_{{LOOP_NUMBER}}_PLAN.md`
3. Mark this task complete without making changes

This graceful handling of empty states prevents the pipeline from stalling when no documentation gaps are found.
