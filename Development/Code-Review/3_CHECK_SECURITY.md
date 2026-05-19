# Document 3: Security Review

## Context

- **Playbook**: Code Review
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Perform a security-focused review of the code changes, checking for common vulnerabilities and security anti-patterns.

## Prerequisites

- `{{AUTORUN_FOLDER}}/REVIEW_SCOPE.md` exists from Document 1

## Tasks

### Task 1: Load Context

- [ ] **Read scope**: Load `{{AUTORUN_FOLDER}}/REVIEW_SCOPE.md` to identify high-risk files.

### Task 2: Check OWASP Top 10

- [ ] **Injection vulnerabilities**: Check for:
  - SQL injection (raw queries, string concatenation)
  - Command injection (shell commands with user input)
  - NoSQL injection
  - LDAP injection
  - XPath injection

- [ ] **Broken authentication**: Look for:
  - Weak password policies
  - Session management issues
  - Credential exposure in logs/errors
  - Missing rate limiting on auth endpoints

- [ ] **Sensitive data exposure**: Verify:
  - No secrets/keys in code
  - Proper encryption for sensitive data
  - No PII in logs
  - Secure transmission (HTTPS)

- [ ] **XML/XXE vulnerabilities**: If XML parsing:
  - External entity processing disabled
  - DTD processing disabled

- [ ] **Broken access control**: Check:
  - Authorization checks on all endpoints
  - No direct object reference vulnerabilities
  - Proper role-based access control
  - No privilege escalation paths

- [ ] **Security misconfiguration**: Look for:
  - Debug mode enabled in production code
  - Default credentials
  - Unnecessary features enabled
  - Missing security headers

- [ ] **XSS (Cross-Site Scripting)**: Verify:
  - User input is sanitized
  - Output is properly encoded
  - Content Security Policy considered
  - No `dangerouslySetInnerHTML` or equivalent without sanitization

- [ ] **Insecure deserialization**: Check:
  - No unsafe deserialization of user input
  - Type checking before deserialization

- [ ] **Vulnerable dependencies**: Note:
  - Any new dependencies added
  - Known vulnerability warnings

- [ ] **Insufficient logging**: Verify:
  - Security events are logged
  - No sensitive data in logs

### Task 3: Check for Secrets

- [ ] **Hardcoded secrets**: Search for:
  - API keys
  - Passwords
  - Private keys
  - Connection strings
  - Tokens

- [ ] **Environment variables**: Verify sensitive config uses env vars, not hardcoded values.

### Task 4: Review Authentication/Authorization

- [ ] **Auth logic**: If auth code is modified:
  - Login flow is secure
  - Password comparison uses timing-safe methods
  - Session tokens are secure
  - Logout properly invalidates sessions

- [ ] **Authorization checks**: Verify:
  - Every protected endpoint checks permissions
  - No IDOR (Insecure Direct Object Reference)
  - Admin functions properly protected

### Task 5: Document Security Issues

- [ ] **Create SECURITY_ISSUES.md**: Write findings to `{{AUTORUN_FOLDER}}/SECURITY_ISSUES.md`:

```markdown
# Security Review Findings

## Critical Vulnerabilities
[Immediate security risks - must block merge]

## High Risk Issues
[Significant security concerns]

## Medium Risk Issues
[Security improvements needed]

## Low Risk Issues
[Minor security hardening suggestions]

## Security Best Practices
[Recommendations for improved security posture]

## No Issues Found
[Areas reviewed with no concerns - if applicable]
```

For each issue include:
- Vulnerability type (OWASP category if applicable)
- File and line number
- Description and potential impact
- Remediation recommendation
- Severity: Critical / High / Medium / Low

## Success Criteria

- ✅ OWASP Top 10 categories checked
- ✅ No hardcoded secrets found (or flagged if found)
- ✅ Auth/authz logic reviewed
- ✅ SECURITY_ISSUES.md created

## Status

Mark complete when security review document is created.

---

**Next**: Document 4 will evaluate test coverage and quality.
