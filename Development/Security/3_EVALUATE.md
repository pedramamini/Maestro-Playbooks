# Security Finding Evaluation - Severity and Remediation Assessment

## Context
- **Playbook:** Security
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Evaluate each security finding from the discovery phase and assign severity and remediability ratings. This prioritization ensures we fix the most critical and easily-remediated issues first.

## Instructions

1. **Read the vulnerabilities** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_VULNERABILITIES.md`
2. **Rate each finding** for severity and ease of remediation
3. **Assign status** based on ratings
4. **Output prioritized plan** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`

## Evaluation Checklist

- [ ] **Evaluate findings**: Read LOOP_{{LOOP_NUMBER}}_VULNERABILITIES.md, rate each finding by SEVERITY (CRITICAL/HIGH/MEDIUM/LOW) and REMEDIABILITY (EASY/MEDIUM/HARD). Mark CRITICAL or HIGH severity with EASY/MEDIUM remediation as PENDING for auto-fix. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`.

## Rating Criteria

### Severity Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **CRITICAL** | Actively exploitable, immediate data breach risk, no authentication required | SQL injection in public endpoint, hardcoded production credentials, RCE vulnerability |
| **HIGH** | Significant risk, requires some conditions to exploit | XSS in authenticated area, IDOR vulnerabilities, weak crypto for sensitive data |
| **MEDIUM** | Moderate risk, defense-in-depth issue | Missing security headers, verbose error messages, session timeout too long |
| **LOW** | Minor issue, best practice violation | Informational disclosure, missing HSTS on internal app |
| **INFO** | No direct risk, observation only | Deprecated library (no known CVE), suboptimal configuration |

### Remediability Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **EASY** | Simple code change, no architectural impact, low risk of regression | Adding parameterized query, removing hardcoded secret, updating dependency |
| **MEDIUM** | Moderate changes, some testing needed, localized impact | Refactoring auth flow, adding input validation across multiple files |
| **HARD** | Significant changes, architectural impact, high regression risk | Redesigning session management, migrating crypto implementation |
| **VERY HARD** | Major overhaul required, breaking changes likely | Complete auth system replacement, database schema changes |

### Auto-Remediation Criteria

Vulnerabilities will be auto-remediated if:
- **Severity:** CRITICAL or HIGH
- **Remediability:** EASY or MEDIUM

Vulnerabilities marked `PENDING - MANUAL REVIEW` if:
- **Severity:** CRITICAL/HIGH but **Remediability:** HARD
- Complex fixes that need human judgment
- Potential for breaking changes

Vulnerabilities marked `WON'T DO` if:
- **Severity:** LOW or INFO
- **Remediability:** VERY HARD with only MEDIUM severity
- False positives after verification
- Accepted risks with documented justification

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` with:

```markdown
# Security Remediation Plan - Loop {{LOOP_NUMBER}}

## Summary
- **Total Findings:** [count]
- **Auto-Remediate (PENDING):** [count]
- **Manual Review:** [count]
- **Won't Do / False Positive:** [count]

## Risk Summary

| Severity | Count | Auto-Fix | Manual | Won't Do |
|----------|-------|----------|--------|----------|
| CRITICAL | X | X | X | X |
| HIGH | X | X | X | X |
| MEDIUM | X | X | X | X |
| LOW/INFO | X | X | X | X |

---

## PENDING - Ready for Auto-Remediation

### SEC-001: [Vulnerability Name]
- **Status:** `PENDING`
- **Vuln ID:** VULN-XXX
- **Severity:** [CRITICAL | HIGH]
- **Remediability:** [EASY | MEDIUM]
- **File:** `[path/to/file.ts]`
- **Line:** [XX]
- **Issue:** [Brief description]
- **Fix Strategy:**
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Verification:** [How to verify the fix works]

### SEC-002: [Vulnerability Name]
- **Status:** `PENDING`
...

---

## PENDING - MANUAL REVIEW

### SEC-XXX: [Vulnerability Name]
- **Status:** `PENDING - MANUAL REVIEW`
- **Vuln ID:** VULN-XXX
- **Severity:** [CRITICAL | HIGH]
- **Remediability:** HARD
- **File:** `[path/to/file.ts]`
- **Reason for Review:** [Why human judgment needed]
- **Recommended Approach:** [Suggestions]
- **Breaking Change Risk:** [Assessment]

---

## WON'T DO / FALSE POSITIVE

### SEC-XXX: [Finding Name]
- **Status:** `WON'T DO` | `FALSE POSITIVE`
- **Vuln ID:** VULN-XXX
- **Severity:** [level]
- **Reason:** [Justification - accepted risk, false positive, etc.]
- **Risk Acceptance:** [If applicable, who accepted and when]

---

## Remediation Order

Recommended sequence based on severity and dependencies:

1. **SEC-001** - [name] (CRITICAL, blocks other fixes)
2. **SEC-002** - [name] (CRITICAL)
3. **SEC-003** - [name] (HIGH, depends on SEC-001)
...

## Dependencies

Fixes that should be done together:

- **Group A:** SEC-001, SEC-003 - Both involve auth module
- **Group B:** SEC-002, SEC-005 - Both are dependency updates
```

## Guidelines

- **Fix CRITICAL first**: These are actively dangerous
- **Verify before closing**: Re-test after each fix
- **Document accepted risks**: If skipping, explain why
- **Group related fixes**: Some vulnerabilities share root causes
- **Consider dependencies**: Some fixes enable or require others
