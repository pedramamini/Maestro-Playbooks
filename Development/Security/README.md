# Security Audit Playbook

A systematic Auto Run playbook for finding and remediating security vulnerabilities in your codebase.

## Overview

This playbook creates an automated pipeline that:
1. **Analyzes** your codebase for security-sensitive areas and runs vulnerability scans
2. **Finds** specific vulnerabilities: injection flaws, secrets, auth issues, dependencies
3. **Evaluates** each finding by severity and remediability
4. **Implements** fixes for HIGH and CRITICAL vulnerabilities
5. **Loops** until no CRITICAL or HIGH severity issues with EASY/MEDIUM remediability remain

## Document Chain

| Document | Purpose | Reset on Completion? |
|----------|---------|---------------------|
| `1_ANALYZE.md` | Run security scans, identify attack surface | No |
| `2_FIND_ISSUES.md` | Find specific vulnerabilities in code | No |
| `3_EVALUATE.md` | Rate severity and ease of remediation | No |
| `4_IMPLEMENT.md` | Fix CRITICAL and HIGH severity issues | No |
| `5_PROGRESS.md` | Security gate - resets 1-4 if CRITICAL/HIGH remain, exits if clear | **Yes** |

## Generated Files

Each loop iteration creates working documents with the loop number:

- `LOOP_1_ATTACK_SURFACE.md` - Security-sensitive areas identified
- `LOOP_1_VULNERABILITIES.md` - Specific issues found
- `LOOP_1_PLAN.md` - Evaluated findings with severity ratings
- `SECURITY_LOG_{{AGENT_NAME}}_{{DATE}}.md` - Cumulative log of all remediations

## Vulnerability Categories

### OWASP Top 10

| Category | What to Look For |
|----------|------------------|
| **Injection** | SQL injection, command injection, LDAP injection, XPath injection |
| **Broken Auth** | Weak passwords, missing MFA, session fixation, credential exposure |
| **Sensitive Data** | Unencrypted data, weak crypto, PII exposure, missing HTTPS |
| **XXE** | XML external entity processing, DTD attacks |
| **Broken Access** | IDOR, privilege escalation, missing function-level access control |
| **Misconfig** | Default credentials, verbose errors, unnecessary features enabled |
| **XSS** | Reflected, stored, DOM-based cross-site scripting |
| **Insecure Deserialization** | Untrusted data deserialization, object injection |
| **Vulnerable Components** | Outdated dependencies, known CVEs |
| **Logging Failures** | Missing audit logs, sensitive data in logs |

### Additional Categories

| Category | What to Look For |
|----------|------------------|
| **Hardcoded Secrets** | API keys, passwords, tokens, private keys in code |
| **Path Traversal** | `../` in file paths, unvalidated file access |
| **SSRF** | Server-side request forgery, internal network access |
| **Race Conditions** | TOCTOU bugs, non-atomic operations on shared state |
| **Crypto Issues** | Weak algorithms (MD5, SHA1), predictable random, ECB mode |

## Severity Levels

| Level | Description | Auto-Fix? |
|-------|-------------|-----------|
| **CRITICAL** | Actively exploitable, immediate risk, data breach potential | Yes |
| **HIGH** | Significant risk, requires specific conditions to exploit | Yes |
| **MEDIUM** | Moderate risk, defense-in-depth issue | Manual Review |
| **LOW** | Minor issue, best practice violation | Won't Do |
| **INFO** | Informational finding, no direct risk | Won't Do |

## How It Works

### The Loop Control Mechanism

The key to understanding this playbook is how `5_PROGRESS.md` controls the loop:

- **Documents 1-4** have `Reset: OFF` - they don't auto-reset
- **Document 5** has `Reset: ON` - it's the only one that resets, and it manually resets 1-4

When `5_PROGRESS.md` runs:
1. It reads `LOOP_{{LOOP_NUMBER}}_PLAN.md` to check for PENDING items with CRITICAL/HIGH severity and EASY/MEDIUM remediability
2. **If such PENDING items exist**: It resets all tasks in documents 1-4
   - This triggers a fresh pass through the pipeline
   - The loop continues
3. **If NO such PENDING items**: It does NOT reset documents 1-4
   - Documents 1-4 remain completed
   - The pipeline exits (all critical/high issues remediated)

### Single Pass (No Loop)
1. Documents execute in order: 1 → 2 → 3 → 4 → 5
2. Each document reads outputs from previous steps
3. `5_PROGRESS.md` evaluates whether CRITICAL/HIGH PENDING items exist
4. If such items exist, it resets tasks in docs 1-4 → loop continues
5. If no such items remain, it does NOT reset → pipeline exits

### Loop Mode Flow
1. Enable loop mode in Batch Runner settings
2. First pass: Analyze → Find Issues → Evaluate → Implement → Check Progress
3. `5_PROGRESS.md` checks for auto-remediable vulnerabilities:
   - CRITICAL/HIGH with EASY/MEDIUM remediability? Reset docs 1-4 → continue
   - No such items? Don't reset → exit
4. Each new loop creates `LOOP_N_*` files with incremented loop number
5. Loop exits when no CRITICAL/HIGH issues with EASY/MEDIUM remediability remain

## Recommended Setup

### For Automated Remediation
```
Loop Mode: ON
Max Loops: 5 (security fixes should converge quickly)
Documents:
  1_ANALYZE.md      [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  2_FIND_ISSUES.md  [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  3_EVALUATE.md     [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  4_IMPLEMENT.md    [Reset: OFF] ← Gets reset manually by 5_PROGRESS
  5_PROGRESS.md     [Reset: ON]  ← Controls loop: resets 1-4 if CRITICAL/HIGH remain, exits if clear
```

### For Review-First Approach
```
Loop Mode: OFF (run once)
Review LOOP_1_PLAN.md carefully
Verify findings are true positives
Then run again with loop mode on
```

## Security Scanning

Use the security tools available for your project's language/ecosystem:

### Finding Security Tools
1. **Check project dependencies** - Look for existing security scanning setup
2. **Check CI/CD pipelines** - May already run security scans
3. **Look for config files** - `.snyk`, `.trivyignore`, security linter configs
4. **Check package manager** - Most have built-in audit commands

### Common Scan Types
- **Dependency vulnerabilities** - Check for known CVEs in dependencies
- **Secret scanning** - Find hardcoded credentials in code
- **Static analysis** - Find code patterns that indicate vulnerabilities
- **License compliance** - Identify problematic dependency licenses

## Template Variables Used

These variables are automatically substituted:

- `{{AGENT_NAME}}` - Name of your Maestro agent
- `{{AGENT_PATH}}` - Root path of the project
- `{{AUTORUN_FOLDER}}` - Path to this Auto Run folder
- `{{LOOP_NUMBER}}` - Current loop iteration (1, 2, 3...)
- `{{DATE}}` - Today's date (YYYY-MM-DD)

## Safety Guidelines

1. **Never commit secrets** - Even to fix them, rotate first
2. **Test fixes thoroughly** - Security fixes can break functionality
3. **Verify before closing** - Re-run scans to confirm remediation
4. **Document exceptions** - Some findings may be false positives
5. **Rotate exposed credentials** - Assume any found secret is compromised

## False Positive Handling

Mark findings as `FALSE POSITIVE` in the plan with justification:
- Test/mock data that looks like secrets
- Intentionally weak crypto for legacy compatibility
- Dead code paths that can't be reached

## Tips

1. **Run scans before starting** - Know your baseline
2. **Fix secrets first** - Rotate any exposed credentials immediately
3. **Check dependencies** - Often the quickest wins
4. **Review auth flows** - Common source of critical issues
5. **Update the SECURITY_LOG** - Document all changes for audit trail
