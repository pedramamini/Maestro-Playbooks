# Phase 3: Evaluate Plan

## Objective

Evaluate the infrastructure plan for completeness, correctness, and safety.

## Evaluation Checklist

### 1. Identity Completeness

- [ ] Agent name is clear and descriptive
- [ ] Persona name is short and memorable
- [ ] Mission statement is concise (one sentence)
- [ ] Role description explains purpose (2-3 sentences)
- [ ] Responsibilities are specific and actionable

### 2. Structure Completeness

- [ ] All required directories planned
- [ ] All required files identified
- [ ] Memory files initialized with proper structure
- [ ] CORE skill has appropriate triggers

### 3. Configuration Validity

- [ ] settings.json is valid JSON
- [ ] config.yaml is valid YAML
- [ ] VERSION file contains valid semver
- [ ] File paths are correct

### 4. Content Quality

- [ ] CLAUDE.md follows standard template
- [ ] SKILL.md has valid frontmatter
- [ ] Memory update instruction is present
- [ ] Organization context is included

### 5. Safety Checks

- [ ] No existing files will be overwritten without backup
- [ ] No sensitive data in templates
- [ ] Permissions are appropriate
- [ ] No destructive operations planned

## Validation Matrix

| Component | Required | Planned | Valid |
|-----------|----------|---------|-------|
| CLAUDE.md | Yes | | |
| .claude/ | Yes | | |
| settings.json | Yes | | |
| VERSION | Yes | | |
| config/config.yaml | Yes | | |
| skills/CORE/SKILL.md | Yes | | |
| context/memory/ | Yes | | |
| context/CLAUDE.md | Yes | | |
| hooks/ | Yes | | |

## Risk Assessment

### Low Risk
- Creating new directories
- Creating new files in empty locations
- Adding placeholder CLAUDE.md files

### Medium Risk
- Overwriting existing CLAUDE.md
- Modifying existing settings.json

### High Risk (Require Confirmation)
- Overwriting existing memory files
- Deleting existing content
- Modifying existing skills

## Pre-Implementation Checklist

Before proceeding to implementation:

- [ ] All directories identified
- [ ] All file contents drafted
- [ ] Agent identity finalized
- [ ] Backup plan for existing files (if applicable)
- [ ] No blocking issues identified

## Approval Gate

Implementation can proceed when:
1. All required components are planned
2. All content passes validation
3. No high-risk operations without mitigation
4. Structure matches infrastructure specification

## Next Phase

If evaluation passes, proceed to **4_IMPLEMENT.md** to execute the installation.
