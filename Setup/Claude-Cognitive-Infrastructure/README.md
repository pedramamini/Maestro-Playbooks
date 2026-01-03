# Claude Cognitive Infrastructure Setup Playbook

A Maestro Auto Run playbook that deploys complete Claude Cognitive Infrastructure to any agent directory, including hooks, security validation, automatic history capture, and skills framework.

## Overview

This playbook creates an automated pipeline that:
1. **Initializes** - Validates prerequisites and target directory
2. **Analyzes** - Derives agent configuration from directory name
3. **Plans** - Generates customized infrastructure plan
4. **Evaluates** - Reviews plan before implementation
5. **Implements** - Creates all directories, hooks, skills, and configuration
6. **Verifies** - Runs testable verification procedures

**Fully Autonomous**: No user prompting required. The playbook derives agent name from the target directory and uses sensible defaults.

## Requirements

**Agent Prompt**: This playbook works with Maestro's **default agent prompt**. No custom configuration required.

**Prerequisites**:
- Target agent directory must exist
- Bun or Node.js installed (for TypeScript hooks)

## What Gets Deployed

### Core Infrastructure

| Component | Purpose |
|-----------|---------|
| `CLAUDE.md` | Agent identity and responsibilities |
| `.claude/settings.json` | Hook configuration |
| `.claude/hooks/` | Event-driven automation (7 hooks) |
| `.claude/skills/CORE/` | Agent skill definition |
| `.claude/context/memory/` | Persistent memory files |
| `.claude/context/history/` | Auto-populated session history |

### Hooks Included

| Hook | Event | Purpose |
|------|-------|---------|
| `security-validator.ts` | PreToolUse | 10-tier attack pattern blocking |
| `initialize-session.ts` | SessionStart | Session setup, tab titles |
| `load-core-context.ts` | SessionStart | CORE skill injection |
| `update-tab-titles.ts` | UserPromptSubmit | Dynamic tab titles |
| `capture-all-events.ts` | PostToolUse | Automatic event logging |
| `capture-session-summary.ts` | Stop | Auto session summaries |
| `stop-hook.ts` | Stop | Work capture on stop |

### Key Features

- **Fully Autonomous**: No user input required - derives configuration from directory
- **Automatic History Capture**: No manual work_status.md updates - hooks capture everything
- **Security Validation**: Blocks dangerous commands before execution
- **Progressive Skill Loading**: 4-tier context disclosure for token efficiency
- **Fail-Safe Design**: Hooks never crash Claude Code

## Document Chain

| Document | Purpose | Reset? |
|----------|---------|--------|
| `0_INITIALIZE.md` | Validate prerequisites | No |
| `1_ANALYZE.md` | Derive agent config from directory | No |
| `2_PLAN_STRUCTURE.md` | Plan customized infrastructure | No |
| `3_EVALUATE.md` | Review plan before implementation | No |
| `4_IMPLEMENT.md` | Create all files and directories | No |
| `5_VERIFY.md` | Testable verification procedures | No |

**Note**: This is a one-shot playbook (no looping). It either completes successfully or fails with clear error messages.

## Generated Files

- `AGENT_CONFIG.md` - Derived agent configuration
- `INFRASTRUCTURE_PLAN.md` - Generated implementation plan
- `SETUP_LOG.md` - Deployment log with timestamps
- `VERIFICATION_REPORT.md` - Results of verification tests

## Configuration (Auto-Derived)

The playbook automatically derives configuration:

| Field | Source | Default |
|-------|--------|---------|
| Agent Name | Directory name | e.g., "Research Assistant Agent" |
| Agent Persona | Generated | "Sam Riley" |
| Responsibilities | Derived from agent name | Generic assistant responsibilities |
| Organization | None | (blank) |

### Customization After Deployment

To customize the agent identity after deployment, edit:
- `{{AGENT_PATH}}/CLAUDE.md` - Update name, persona, responsibilities
- `{{AGENT_PATH}}/.claude/skills/CORE/SKILL.md` - Update skill definition

## Recommended Setup

```
Loop Mode: OFF (one-shot playbook)
Max Loops: 1
Documents:
  0_INITIALIZE.md   [Reset: OFF]
  1_ANALYZE.md      [Reset: OFF]
  2_PLAN_STRUCTURE.md [Reset: OFF]
  3_EVALUATE.md     [Reset: OFF]
  4_IMPLEMENT.md    [Reset: OFF]
  5_VERIFY.md       [Reset: OFF]
```

## Template Variables Used

| Variable | Description |
|----------|-------------|
| `{{AGENT_NAME}}` | Name of the Maestro agent |
| `{{AGENT_PATH}}` | Root path of the target project |
| `{{AUTORUN_FOLDER}}` | Path to this Auto Run folder |
| `{{DATE}}` | Today's date (YYYY-MM-DD) |

## After Deployment

Once the infrastructure is deployed, the agent can:

1. **Start a session**: `cd /path/to/agent && claude`
2. **Security is active**: Dangerous commands are blocked automatically
3. **History captures automatically**: Sessions, learnings, and work are recorded
4. **Skills load automatically**: CORE skill injects at session start

## Verification

The playbook includes testable verification:

- Directory structure validation
- Hook executability check
- Security validator test
- CLAUDE.md content verification
- Settings.json validation

## Credits & Inspiration

This playbook is inspired by and adapts code from **[Personal AI Infrastructure (PAI)](https://github.com/danielmiessler/PAI)** by **Daniel Miessler**.

PAI is a comprehensive framework for building personal AI systems with modular, battle-tested capabilities. The following components are adapted from PAI:

- **Hook System** (`kai-hook-system`): Event-driven automation framework
- **Security Validator**: 10-tier attack pattern detection and blocking
- **History System** (`kai-history-system`): Automatic session and event capture
- **Observability Library**: Dashboard integration utilities

Special thanks to Daniel Miessler for open-sourcing PAI and demonstrating how to build robust, production-ready AI infrastructure.

## Changelog

### 1.0.0 - 2025-01-02
- Initial release
- Core infrastructure deployment
- 7 hooks included
- Automatic history capture
- Security validation
- Testable verification
- Fully autonomous execution
