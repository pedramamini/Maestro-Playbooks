# Security Audit Gate - CRITICAL/HIGH Remediation Target

## Context
- **Playbook:** Security
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Purpose

This document is the **security gate** for the audit pipeline. It checks whether all CRITICAL and HIGH severity vulnerabilities have been remediated. **This is the only document with Reset ON** - it controls loop continuation by resetting tasks in documents 1-4 when more work is needed.

## Instructions

1. **Read the plan** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. **Check for remaining CRITICAL or HIGH severity items** that are still `PENDING` with EASY/MEDIUM remediability
3. **If such PENDING items exist**: Reset all tasks in documents 1-4 to continue the loop
4. **If NO such items exist**: Do NOT reset - pipeline exits

## Security Gate Check

- [ ] **Check for remaining vulnerabilities**: Read LOOP_{{LOOP_NUMBER}}_PLAN.md and check if there are any items with status `PENDING` that have CRITICAL or HIGH severity AND EASY or MEDIUM remediability. If such items exist, reset documents 1-4 to continue the loop. If no auto-remediable CRITICAL/HIGH items remain, do NOT reset anything - allow the pipeline to exit.

## Reset Tasks (Only if PENDING CRITICAL/HIGH items with EASY/MEDIUM remediability exist)

If the security gate check above determines we need to continue, reset all tasks in the following documents:

- [ ] **Reset 1_ANALYZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md`
- [ ] **Reset 2_FIND_ISSUES.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_FIND_ISSUES.md`
- [ ] **Reset 3_EVALUATE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md`
- [ ] **Reset 4_IMPLEMENT.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_IMPLEMENT.md`

**IMPORTANT**: Only reset documents 1-4 if there are PENDING items with CRITICAL/HIGH severity and EASY/MEDIUM remediability. If all such items are IMPLEMENTED, or only HARD remediability items remain, leave these reset tasks unchecked to allow the pipeline to exit.

## Decision Logic

```
IF LOOP_{{LOOP_NUMBER}}_PLAN.md doesn't exist:
    → Do NOT reset anything (PIPELINE JUST STARTED - LET IT RUN)

ELSE IF no PENDING items with (CRITICAL|HIGH severity) AND (EASY|MEDIUM remediability):
    → Do NOT reset anything (ALL CRITICAL/HIGH FIXED - EXIT)

ELSE:
    → Reset documents 1-4 (CONTINUE TO NEXT LOOP)
```

## How This Works

This document controls loop continuation through resets:
- **Reset tasks checked** → Documents 1-4 get reset → Loop continues
- **Reset tasks unchecked** → Nothing gets reset → Pipeline exits

### Exit Conditions (Do NOT Reset)

1. **All Clear**: No CRITICAL or HIGH severity findings remain
2. **All Fixed**: All CRITICAL/HIGH items are `IMPLEMENTED`
3. **Only Hard Items**: Remaining CRITICAL/HIGH need `MANUAL REVIEW` (HARD remediability)
4. **Only Low Severity**: Remaining items are MEDIUM/LOW/INFO
5. **Max Loops**: Hit the loop limit in Batch Runner

### Continue Conditions (Reset Documents 1-4)

1. There are PENDING items with CRITICAL or HIGH severity
2. Those items have EASY or MEDIUM remediability
3. We haven't hit max loops

## Current Status

Before making a decision, tally the current state:

| Category | Count |
|----------|-------|
| **CRITICAL - PENDING (EASY/MEDIUM)** | ___ |
| **CRITICAL - IMPLEMENTED** | ___ |
| **HIGH - PENDING (EASY/MEDIUM)** | ___ |
| **HIGH - IMPLEMENTED** | ___ |
| **MANUAL REVIEW (HARD)** | ___ |
| **WON'T DO / FALSE POSITIVE** | ___ |

## Security Posture History

Track progress across loops:

| Loop | Critical (Start) | Critical (End) | High (Start) | High (End) | Decision |
|------|------------------|----------------|--------------|------------|----------|
| 1 | ___ | ___ | ___ | ___ | [CONTINUE / EXIT] |
| 2 | ___ | ___ | ___ | ___ | [CONTINUE / EXIT] |
| ... | ... | ... | ... | ... | ... |

## Manual Override

**To force exit early:**
- Leave all reset tasks unchecked regardless of remaining issues
- Document justification in SECURITY_LOG

**To continue fixing MEDIUM severity:**
- Check the reset tasks even when no CRITICAL/HIGH remain
- Will find and fix MEDIUM issues next loop

**To pause for manual review:**
- Leave unchecked
- Review SECURITY_LOG and plan
- Address MANUAL REVIEW items
- Restart when ready

## Remaining Work Summary

Items that still need attention after this loop:

### Needs Manual Review
- [ ] SEC-XXX: [description] - [why manual review needed]

### Accepted Risks
- [ ] SEC-XXX: [description] - [risk acceptance justification]

### Blocked / Waiting
- [ ] SEC-XXX: [description] - [what it's waiting for]

## Notes

- The goal is **zero CRITICAL and HIGH** findings
- MEDIUM severity items are defense-in-depth improvements
- Some findings may be false positives - verify before dismissing
- Document all risk acceptances for audit purposes
- Rotate any exposed credentials even after removing from code
