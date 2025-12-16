# Security Issue Discovery - Find Vulnerabilities

## Context
- **Playbook:** Security
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Using the attack surface map, systematically search for specific security vulnerabilities. This document identifies WHAT security issues exist in the codebase.

## Instructions

1. **Read the attack surface** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_ATTACK_SURFACE.md`
2. **Search for vulnerabilities** using the investigation tactics
3. **Document each finding** with location, type, and evidence
4. **Output findings** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_VULNERABILITIES.md`

## Discovery Checklist

- [ ] **Find vulnerabilities**: Using the attack surface map and tactics, search for injection flaws, hardcoded secrets, auth issues, XSS, and insecure dependencies. Document each finding with file path, line number, vulnerability type, and evidence. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_VULNERABILITIES.md`.

## Vulnerability Search Patterns

### Injection Flaws

#### SQL Injection
Look for string concatenation or template literals in database queries instead of parameterized queries with placeholders.

#### Command Injection
Look for user input passed to shell commands via string interpolation. Safe patterns use array arguments without shell interpretation.

#### Path Traversal
Look for unvalidated file paths where user input is used directly. Safe patterns resolve and validate that paths stay within allowed directories.

### Hardcoded Secrets

Search for patterns like:
- Variables named API_KEY, SECRET, PASSWORD with string literal values
- AWS access keys matching pattern: AKIA followed by 16 alphanumeric chars
- GitHub tokens matching pattern: ghp_ followed by 36 alphanumeric chars
- Private key headers in source code
- Long base64-like strings assigned to variables

### Authentication Issues

Look for:
- Plain text password comparison instead of hash comparison
- Weak hashing algorithms (MD5, SHA1) for passwords
- Cookies missing secure or httpOnly flags
- Missing session regeneration after login
- Non-constant-time token comparison (timing attacks)

### Cross-Site Scripting (XSS)

Look for:
- Setting innerHTML directly from user input
- React's dangerous HTML prop with unsanitized content
- DOM methods that write raw HTML from user data
- Dynamic code evaluation with user input
- User-controlled href attributes allowing javascript: protocol

### Insecure Cryptography

Look for:
- Weak hash algorithms: MD5, SHA1 for security purposes
- Weak ciphers: DES, RC4
- ECB mode encryption
- Hardcoded initialization vectors (IVs)
- Math.random() used for security tokens

### Access Control Issues

Look for:
- API endpoints without authentication middleware
- Direct object references without ownership validation (IDOR)
- Mass assignment vulnerabilities (user-controlled role fields)
- Missing function-level access control

## Output Format

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_VULNERABILITIES.md` with:

```markdown
# Security Vulnerabilities - Loop {{LOOP_NUMBER}}

## Summary
- **Total Findings:** [count]
- **Critical:** [count]
- **High:** [count]
- **Medium:** [count]
- **Low/Info:** [count]

---

## VULN-001: [Vulnerability Name]
- **Type:** [SQL Injection | XSS | Hardcoded Secret | etc.]
- **File:** `[path/to/file]`
- **Line:** [XX]
- **Severity:** [CRITICAL | HIGH | MEDIUM | LOW]
- **Evidence:** [Description or code snippet of the vulnerable pattern]
- **Attack Scenario:** [How this could be exploited]
- **Remediation:** [How to fix it]

---

## VULN-002: [Vulnerability Name]
- **Type:** [Type]
- **File:** `[path/to/file]`
- **Line:** [XX]
- **Severity:** [Level]
- **Evidence:** [Description or code snippet]
- **Attack Scenario:** [How exploited]
- **Remediation:** [How to fix]

---

## Findings by Category

| Category | Count | Critical | High |
|----------|-------|----------|------|
| Injection | X | X | X |
| Secrets | X | X | X |
| Auth | X | X | X |
| XSS | X | X | X |
| Crypto | X | X | X |
| Access Control | X | X | X |
| Dependencies | X | X | X |

## Dependency Vulnerabilities

From automated dependency scans:

| Package | Version | Vulnerability | Severity | Fix Version |
|---------|---------|---------------|----------|-------------|
| [pkg] | [ver] | [CVE-XXXX-XXXX] | [sev] | [fix ver] |

## Potential False Positives

Findings that may not be actual vulnerabilities:

- **VULN-XXX** - [Why it might be false positive]
```

## Guidelines

- **Search systematically**: Use the patterns above as starting points
- **Verify findings**: Confirm vulnerabilities are actually exploitable
- **Note context**: Some patterns are safe in certain contexts
- **Check dependencies**: Don't forget third-party vulnerabilities
- **Document evidence**: Include actual code snippets
