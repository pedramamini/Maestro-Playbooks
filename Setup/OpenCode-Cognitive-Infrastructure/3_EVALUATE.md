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
- [ ] Core skill has appropriate description
- [ ] Skill names follow OpenCode naming convention (lowercase with hyphens)

### 3. Configuration Validity

- [ ] opencode.json is valid JSON
- [ ] opencode.json has correct schema reference
- [ ] config.yaml is valid YAML
- [ ] VERSION file contains valid semver
- [ ] File paths are correct

### 4. Content Quality

- [ ] AGENTS.md follows standard template
- [ ] SKILL.md files have valid frontmatter
- [ ] Memory update instruction is present
- [ ] Organization context is included

### 5. OpenCode-Specific Validation

- [ ] Skill names are lowercase alphanumeric with hyphens
- [ ] Skill descriptions are under 1024 characters
- [ ] Plugin files export proper Plugin type
- [ ] opencode.json plugin references match file names

### 6. Safety Checks

- [ ] No existing files will be overwritten without backup
- [ ] No sensitive data in templates
- [ ] Permissions are appropriate
- [ ] No destructive operations planned

## Validation Matrix

| Component | Required | Planned | Valid |
|-----------|----------|---------|-------|
| AGENTS.md | Yes | | |
| opencode.json | Yes | | |
| .opencode/ | Yes | | |
| VERSION | Yes | | |
| config/config.yaml | Yes | | |
| skill/core/SKILL.md | Yes | | |
| memory/ | Yes | | |
| plugin/ | Yes | | |

## OpenCode Naming Rules

### Skill Names
- Must be 1-64 characters
- Lowercase alphanumeric only
- Single hyphens allowed (not at start/end)
- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`

**Valid:** `core`, `create-skill`, `code-review`, `my-custom-skill`
**Invalid:** `Core`, `create_skill`, `my--skill`, `-skill`

### Plugin Names
- Should match directory/file naming
- Use kebab-case for consistency
- Export matches file name

## Risk Assessment

### Low Risk
- Creating new directories
- Creating new files in empty locations
- Adding README.md placeholder files

### Medium Risk
- Overwriting existing AGENTS.md
- Modifying existing opencode.json
- Adding new plugins

### High Risk (Require Confirmation)
- Overwriting existing memory files
- Deleting existing content
- Modifying existing skills
- Changing plugin configurations

## Pre-Implementation Checklist

Before proceeding to implementation:

- [ ] All directories identified
- [ ] All file contents drafted
- [ ] Agent identity finalized
- [ ] Skill names validated against naming rules
- [ ] Plugin structure matches OpenCode Plugin type
- [ ] Backup plan for existing files (if applicable)
- [ ] No blocking issues identified

## Approval Gate

Implementation can proceed when:
1. All required components are planned
2. All content passes validation
3. No high-risk operations without mitigation
4. Structure matches OpenCode infrastructure specification
5. All naming conventions are followed

## Next Phase

If evaluation passes, proceed to **4_IMPLEMENT.md** to execute the installation.
