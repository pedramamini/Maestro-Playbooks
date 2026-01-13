# Claude Cognitive Infrastructure Setup

Deploys the complete Claude Cognitive Infrastructure to any agent directory, enabling persistent memory, modular skills, context management, and event-driven hooks.

## What This Playbook Does

This playbook creates the foundational `.claude/` directory structure that gives Claude-based agents their cognitive capabilities:

- **Hook System** - Event-driven automation with security validation, session management, and event logging
- **Memory System** - Three-tier persistent knowledge (hot/warm/cold) for session history, learnings, and state
- **Skills Framework** - Modular domain expertise with tiered loading and USE WHEN activation
- **Configuration** - Settings and config files for customization

## Infrastructure Structure

After running this playbook, the agent will have:

```
Agent Directory/
├── CLAUDE.md                    # Agent identity (single source of truth)
└── .claude/
    ├── settings.json            # Hook configuration
    ├── VERSION                  # Infrastructure version tracking
    ├── config/
    │   └── config.yaml          # Runtime settings
    ├── skills/
    │   ├── CORE/
    │   │   ├── SKILL.md         # Core identity skill
    │   │   ├── SYSTEM/          # System documentation
    │   │   │   ├── SKILLSYSTEM.md
    │   │   │   ├── MEMORYSYSTEM.md
    │   │   │   └── HOOKSYSTEM.md
    │   │   ├── USER/            # Personal configuration
    │   │   └── Workflows/       # Core workflows
    │   └── CreateSkill/
    │       └── SKILL.md         # Skill creation skill
    ├── MEMORY/
    │   ├── README.md            # Memory system docs
    │   ├── State/               # Operational state
    │   ├── Signals/             # Pattern detection
    │   ├── Work/                # Per-task memory
    │   ├── Learning/            # Phase-based learnings
    │   │   ├── OBSERVE/
    │   │   ├── THINK/
    │   │   ├── PLAN/
    │   │   ├── BUILD/
    │   │   ├── EXECUTE/
    │   │   └── VERIFY/
    │   ├── research/            # Research outputs
    │   ├── sessions/            # Session summaries
    │   ├── learnings/           # Learning moments
    │   ├── decisions/           # ADRs
    │   ├── execution/           # Task logs
    │   ├── security/            # Security events
    │   ├── recovery/            # Recovery snapshots
    │   ├── raw-outputs/         # JSONL event streams
    │   └── backups/             # Pre-change backups
    ├── hooks/
    │   ├── security-validator.ts   # 10-tier attack pattern blocking
    │   ├── initialize-session.ts   # Session start handler
    │   ├── load-core-context.ts    # Context loader
    │   ├── event-logger.ts         # PostToolUse logger
    │   └── session-summary.ts      # Session end handler
    ├── agents/                  # Orchestration worker definitions
    ├── scripts/                 # Utility scripts
    └── examples/                # Reference examples
```

## Hook System Features

The playbook installs a complete hook system with:

| Hook | Event | Purpose |
|------|-------|---------|
| `security-validator.ts` | PreToolUse (Bash) | 10-tier attack pattern blocking |
| `initialize-session.ts` | SessionStart | Session state initialization |
| `load-core-context.ts` | SessionStart | Load CORE skill context |
| `event-logger.ts` | PostToolUse | Log tool executions to MEMORY |
| `session-summary.ts` | Stop | Capture session summary |

### Security Validator Tiers

1. **Catastrophic** - `rm -rf /`, disk destruction (BLOCK)
2. **Reverse Shells** - Bash/netcat/socket shells (BLOCK)
3. **Credential Theft** - curl|sh, wget|sh patterns (BLOCK)
4. **Prompt Injection** - "ignore previous instructions" (BLOCK)
5. **Environment Manipulation** - API key exposure (WARN)
6. **Git Dangerous** - force push, hard reset (WARN)
7. **System Modification** - chmod 777, sudo (LOG)
8. **Network Operations** - ssh, scp, rsync (LOG)
9. **Data Exfiltration** - upload patterns (BLOCK)
10. **Infrastructure Protection** - rm .claude (BLOCK)

## Memory System Features

Three-tier memory architecture:

| Tier | Temperature | Purpose | Location |
|------|-------------|---------|----------|
| **CAPTURE** | Hot | Active work items | `MEMORY/Work/` |
| **SYNTHESIS** | Warm | Phase-based learnings | `MEMORY/Learning/` |
| **APPLICATION** | Cold | Historical archive | `MEMORY/sessions/`, etc. |

## Skills System Features

- **YAML Frontmatter** with `USE WHEN` activation triggers
- **TitleCase naming** convention
- **Tiered loading** - frontmatter at startup, full body on invocation
- **Workflow routing** tables for multi-step procedures
- **CreateSkill** skill for generating new skills

## Prerequisites

- An agent directory where you want to install the infrastructure
- The agent should have a clear purpose/role (used to generate identity)
- **Bun runtime** (for TypeScript hooks) - https://bun.sh

## Usage

Run this playbook in the target agent's directory. The playbook will:

1. Analyze the agent's purpose from directory name and any existing files
2. Generate appropriate agent identity (name, mission, role)
3. Create the complete `.claude/` directory structure
4. Install the Hook System with security validator
5. Initialize the Memory System with three-tier architecture
6. Create the Skills Framework with CORE and CreateSkill
7. Verify the installation

## After Installation

Once the infrastructure is installed, you can:

1. Run **Knowledge Pack** playbooks to add domain expertise
2. Customize the CLAUDE.md with additional instructions
3. Add custom hooks for automation
4. Create new skills using the CreateSkill skill
5. Start using the agent with full cognitive capabilities

## Git Configuration

### What to Commit

| Directory | Commit? | Reason |
|-----------|---------|--------|
| `.claude/settings.json` | Yes | Hook configuration |
| `.claude/VERSION` | Yes | Infrastructure version |
| `.claude/config/` | Yes | Runtime settings |
| `.claude/skills/` | Yes | Skill definitions |
| `.claude/skills/CORE/USER/` | No | Personal configuration |
| `.claude/MEMORY/State/` | No | Session state |
| `.claude/MEMORY/Signals/` | No | Pattern detection |
| `.claude/MEMORY/Work/` | No | Active work items |
| `.claude/MEMORY/raw-outputs/` | No | Event logs |
| `.claude/MEMORY/sessions/` | No | Session history |
| `.claude/MEMORY/security/` | No | Security events |
| `.claude/hooks/` | Yes | Event hooks |
| `CLAUDE.md` | Yes | Agent identity |

### Recommended .gitignore

```gitignore
# Claude Cognitive Infrastructure - Private Data
.claude/MEMORY/raw-outputs/
.claude/MEMORY/sessions/
.claude/MEMORY/security/
.claude/MEMORY/State/
.claude/MEMORY/Signals/
.claude/MEMORY/Work/
.claude/skills/CORE/USER/

# Keep structure but ignore contents
!.claude/MEMORY/.gitkeep
!.claude/MEMORY/State/.gitkeep
```

## Version Migration

### Upgrading Infrastructure

1. **Check current version**: Read `.claude/VERSION`
2. **Backup existing**: `cp -r .claude .claude.backup`
3. **Run upgrade playbook**: Future versions will include migration scripts
4. **Verify**: Run the 5_VERIFY phase to confirm upgrade success

### Version History

| Version | Changes |
|---------|---------|
| 1.1.0 | Initial release with hook system, memory system, skills framework |

## Version

Current infrastructure version: **1.1.0**

## Assets

This playbook includes the following assets in the `assets/` folder:

| Asset | Purpose |
|-------|---------|
| `settings.schema.json` | JSON schema for validating `.claude/settings.json` |

Reference assets using `{{AUTORUN_FOLDER}}/assets/` in playbook documents.

## Credits

The Claude Cognitive Infrastructure was influenced by [Daniel Miessler's](https://danielmiessler.com/) [Personal AI Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure) project, which pioneered many of the concepts around persistent memory, modular skills, and structured context for AI assistants.

---

*Claude Cognitive Infrastructure Setup Playbook*
