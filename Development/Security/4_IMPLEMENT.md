# Security Remediation - Fix Vulnerabilities

## Context
- **Playbook:** Security
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Implement fixes for `PENDING` security vulnerabilities from the evaluation phase. Apply secure coding practices and verify each fix.

## Instructions

1. **Read the plan** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. **Find all `PENDING` items** (not `IMPLEMENTED`, `WON'T DO`, or `PENDING - MANUAL REVIEW`)
3. **Implement the fix** following the fix strategy
4. **Verify the fix** works and doesn't break functionality
5. **Update status** to `IMPLEMENTED` in the plan file
6. **Log changes** to `{{AUTORUN_FOLDER}}/SECURITY_LOG_{{AGENT_NAME}}_{{DATE}}.md`

## Task

- [ ] **Read configured values**: Read the agent prompt for `AUTO_FIX_SEVERITY` and `AUTO_FIX_REMEDIABILITY`. These define which findings are eligible for auto-remediation. Use these values throughout this document wherever you see `[AUTO_FIX_SEVERITY]` or `[AUTO_FIX_REMEDIABILITY]` placeholders.

- [ ] **Fix one vulnerability (or skip if none)**: Read {{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md. If the file doesn't exist OR contains no items with status exactly `PENDING` that have `[AUTO_FIX_SEVERITY]` severity AND `[AUTO_FIX_REMEDIABILITY]` remediability, mark this task complete without changes. Otherwise, find ONE such item, implement the fix following secure coding practices, verify the fix, log to {{AUTORUN_FOLDER}}/SECURITY_LOG_{{AGENT_NAME}}_{{DATE}}.md, and update status to `IMPLEMENTED` in the plan file.

## Implementation Checklist

Before implementing, verify:
- [ ] The status is exactly `PENDING` (not `PENDING - MANUAL REVIEW` or `WON'T DO`)
- [ ] The severity matches `[AUTO_FIX_SEVERITY]`
- [ ] The remediability matches `[AUTO_FIX_REMEDIABILITY]`
- [ ] The fix strategy is clearly specified
- [ ] No other changes are required (no dependencies)

## Remediation Patterns

### SQL Injection Fix
- Replace string concatenation with parameterized queries
- Use ORM methods that auto-escape
- Validate and sanitize input types

### Command Injection Fix
- Use array-based command execution without shell
- Validate input against allowlist
- Escape special characters if shell is required

### Path Traversal Fix
- Resolve paths and verify they're within allowed directory
- Use basename to strip directory components
- Reject paths containing `..`

### Hardcoded Secrets Fix
- Move secrets to environment variables
- Use secrets management (Vault, AWS Secrets Manager)
- Rotate any exposed credentials immediately
- Add to .gitignore if config files

### XSS Fix
- Use framework's auto-escaping (React, Vue, etc.)
- Sanitize HTML with DOMPurify or similar
- Use Content-Security-Policy headers
- Validate and encode output context-appropriately

### Authentication Fix
- Use bcrypt/argon2 for password hashing
- Implement constant-time comparison for tokens
- Add secure and httpOnly flags to cookies
- Regenerate session after login

### Cryptography Fix
- Replace MD5/SHA1 with SHA-256 or better
- Use authenticated encryption (AES-GCM)
- Generate random IVs for each encryption
- Use crypto.randomBytes() for tokens

### Dependency Fix
- Update to patched version
- If no patch, evaluate alternatives
- Document if accepting risk temporarily

## Verification Steps

After each fix:

1. **Code Review**: Does the fix address the root cause?
2. **Regression Test**: Does existing functionality still work?
3. **Security Test**: Is the vulnerability actually fixed?
4. **Scan Again**: Do automated tools still flag it?

## Update Plan Status

After implementing each fix, update `LOOP_{{LOOP_NUMBER}}_PLAN.md`:

```markdown
### SEC-001: [Vulnerability Name]
- **Status:** `IMPLEMENTED`  ← Changed from PENDING
- **Implemented In:** Loop {{LOOP_NUMBER}}
- **Fix Applied:** [Brief description of what was changed]
- **Files Modified:** `[list of files]`
- **Verified:** [How you verified it works]
```

## Log Format

Append to `{{AUTORUN_FOLDER}}/SECURITY_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
## Loop {{LOOP_NUMBER}} - [Timestamp]

### Vulnerabilities Remediated

#### SEC-001: [Vulnerability Name]
- **Status:** IMPLEMENTED
- **Severity:** [CRITICAL | HIGH]
- **Type:** [SQL Injection | XSS | etc.]
- **File:** `[path/to/file.ts]`
- **Fix Description:**
  [What was changed and why]
- **Before:** [Brief description or code reference]
- **After:** [Brief description of the fix]
- **Verification:**
  - [x] Code review passed
  - [x] Functionality tested
  - [x] Vulnerability no longer exploitable
  - [x] Automated scan clean

---
```

## Special Handling

### Exposed Credentials
If you find hardcoded credentials:
1. **DO NOT COMMIT** the secret, even to remove it
2. **Assume compromised** - credential must be rotated
3. **Note in log** that rotation is required
4. **Replace with** environment variable reference

### Breaking Changes
If a fix might break functionality:
1. **Document the risk** in the plan
2. **Mark as PENDING - MANUAL REVIEW** if uncertain
3. **Add migration notes** if API changes

### Dependencies with No Patch
If a vulnerable dependency has no fix:
1. **Check for alternatives** - can we switch libraries?
2. **Assess exploitability** - is our usage actually vulnerable?
3. **Document accepted risk** if keeping temporarily
4. **Set reminder** to check for patch

## Guidelines

- **One fix at a time**: Easier to verify and rollback
- **Test after each fix**: Don't batch untested changes
- **Rotate secrets immediately**: Don't wait for the fix to merge
- **Keep the log detailed**: Audit trail is important
- **When in doubt, ask**: Mark for manual review

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Implemented a fix:**
1. You've implemented exactly ONE fix from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. You've appended the change details to `{{AUTORUN_FOLDER}}/SECURITY_LOG_{{AGENT_NAME}}_{{DATE}}.md`
3. You've updated the item status in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` to `IMPLEMENTED`

**Option B - No PENDING fixes available:**
1. `LOOP_{{LOOP_NUMBER}}_PLAN.md` doesn't exist, OR
2. It contains no items with status exactly `PENDING` that have `[AUTO_FIX_SEVERITY]` severity AND `[AUTO_FIX_REMEDIABILITY]` remediability
3. Mark this task complete without making changes

This graceful handling allows the pipeline to continue when a loop iteration produces no actionable fixes.

## When No Fixes Are Available

If there are no qualifying `PENDING` items in the plan file, append to `{{AUTORUN_FOLDER}}/SECURITY_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
---

## [YYYY-MM-DD HH:MM] - Loop {{LOOP_NUMBER}} Complete

**Agent:** {{AGENT_NAME}}
**Project:** {{AGENT_PATH}}
**Loop:** {{LOOP_NUMBER}}
**Status:** No PENDING fixes available (`[AUTO_FIX_SEVERITY]` severity with `[AUTO_FIX_REMEDIABILITY]` remediability)

**Summary:**
- Items IMPLEMENTED: [count]
- Items WON'T DO: [count]
- Items PENDING - MANUAL REVIEW: [count]
- Items PENDING (LOW severity or HARD remediability): [count]

**Recommendation:** [Either "All automatable security fixes implemented" or "Remaining items need manual review or have lower priority"]
```

This signals to the pipeline that this loop iteration is complete.
