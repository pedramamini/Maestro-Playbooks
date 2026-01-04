# Phase 1: Analyze Agent Context

## Objective

Analyze the target agent's context to determine appropriate identity, skills, and configuration.

## Analysis Tasks

### 1. Directory Analysis

Examine the agent directory:

- [ ] Read directory name for agent purpose
- [ ] Check parent directory for organization context
- [ ] Look for existing ROLE.md or similar documentation
- [ ] Identify any existing configuration files

### 2. Agent Identity Derivation

From the directory name, derive:

| Component | Source | Example |
|-----------|--------|---------|
| Agent Name | Directory name | "Sales Lead Agent" |
| Organization | Parent directory | "Wayward Guardian" |
| Persona Name | Generated from type | "Scout" |
| Agent Type | Keywords in name | "Sales" |

### 3. Role Detection

If ROLE.md exists, extract:

- Role description (first paragraph after title)
- Key responsibilities (bulleted lists)
- Domain expertise areas
- Integration points with other agents

### 4. Existing Files Inventory

Check for files that inform configuration:

| File | Purpose | Action |
|------|---------|--------|
| ROLE.md | Role definition | Extract responsibilities |
| README.md | Documentation | Extract context |
| .claude/ | Existing infrastructure | Plan upgrade |
| auto-run/ | Playbooks | Note for integration |

## Agent Profile Template

Based on analysis, build agent profile:

```yaml
agent:
  name: "<Agent Name>"
  persona: "<Short Persona Name>"
  organization: "<Organization Name>"
  type: "<Agent Type>"

identity:
  mission: "<One sentence mission>"
  role: "<2-3 sentence role description>"

capabilities:
  primary: []      # Core responsibilities
  secondary: []    # Supporting tasks

integrations:
  collaborates_with: []  # Other agents
  tools: []              # External tools
```

## Analysis Outputs

Document the following for use in later phases:

1. **Agent Profile** - Complete identity information
2. **Installation Mode** - Fresh or upgrade
3. **Customizations Needed** - Based on agent type
4. **Preservation List** - Files to keep if upgrading

## Type-Specific Considerations

### Technical Agents
- Include architecture context directories
- Add development and testing contexts
- Consider code-related hooks

### Business Agents
- Include projects context
- Add working context for active tasks
- Consider CRM/pipeline integrations

### Research Agents
- Emphasize knowledge context
- Add research methodology
- Consider web search capabilities

### Operations Agents
- Include process documentation
- Add tracking and reporting
- Consider scheduling integrations

## Next Phase

Proceed to **2_PLAN_STRUCTURE.md** to plan the infrastructure structure.
