# Phase 0: Initialize

## Objective

Validate prerequisites and prepare for Claude Cognitive Infrastructure deployment.

## Prerequisites Checklist

### 1. Target Directory

Verify the target agent directory:

- [ ] Agent directory exists and is writable
- [ ] Directory has a clear name indicating agent purpose
- [ ] No critical files will be overwritten (or backup is acceptable)

### 2. Existing Infrastructure Check

Check for existing `.claude/` directory:

- [ ] If `.claude/` exists, determine upgrade vs fresh install
- [ ] If upgrading, backup existing memory files
- [ ] Note any custom configurations to preserve

### 3. Agent Context

Gather information about the agent:

- [ ] Agent name (from directory name)
- [ ] Organization (from parent directory, if applicable)
- [ ] Agent type/role (inferred from name or existing files)

## Agent Type Detection

Based on directory name, detect agent type for customization:

| Keywords in Name | Agent Type | Persona Suggestion |
|------------------|------------|-------------------|
| Sales, Lead, Pipeline | Sales | Scout |
| Engineer, Architect, Developer | Technical | Archon |
| Research, Analysis | Research | Sage |
| Marketing, Content | Marketing | Maven |
| Fundraising, Investor | Finance | Catalyst |
| Operations, Admin | Operations | Atlas |
| People, Recruiting, HR | People | Harbor |
| Executive, Chief | Executive | Aria |
| Brand, Communications | Communications | Echo |
| Strategy, Planning | Strategy | Compass |
| Customer, Success | Customer | Bridge |
| UX, Design | Design | Pixel |

## Validation Steps

1. Confirm agent directory path
2. Check write permissions
3. Detect agent type from name
4. Check for existing infrastructure
5. Determine installation mode (fresh/upgrade)

## Installation Modes

### Fresh Install
- Create complete `.claude/` structure
- Generate new CLAUDE.md identity
- Initialize empty memory files

### Upgrade Install
- Preserve existing memory files
- Update structure to latest version
- Add new capabilities (hooks, skills)

## Next Phase

Once prerequisites are validated, proceed to **1_ANALYZE.md** to analyze the agent context.
