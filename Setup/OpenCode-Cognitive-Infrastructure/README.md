# OpenCode Cognitive Infrastructure Setup

Deploys the complete OpenCode Cognitive Infrastructure to any agent directory, enabling persistent memory, modular skills, context management, and event-driven plugins.

## What This Playbook Does

This playbook creates the foundational `.opencode/` directory structure that gives OpenCode-based agents their cognitive capabilities:

- **Plugin System** - Event-driven automation with security validation, session management, and event logging
- **Memory System** - Three-tier persistent knowledge (hot/warm/cold) for session history, learnings, and state
- **Skills Framework** - Modular domain expertise with on-demand loading and USE WHEN activation
- **Configuration** - opencode.json and config files for customization

## Infrastructure Structure

After running this playbook, the agent will have:

```
Agent Directory/
├── AGENTS.md                    # Agent identity (single source of truth)
├── opencode.json                # Main configuration
└── .opencode/
    ├── VERSION                  # Infrastructure version tracking
    ├── config/
    │   └── config.yaml          # Runtime settings
    ├── skill/
    │   ├── core/
    │   │   └── SKILL.md         # Core identity skill
    │   └── create-skill/
    │       └── SKILL.md         # Skill creation skill
    ├── plugin/
    │   ├── security-validator.ts   # 10-tier attack pattern blocking
    │   ├── session-manager.ts      # Session lifecycle handling
    │   ├── event-logger.ts         # Tool execution logging
    │   └── context-loader.ts       # Context initialization
    ├── memory/
    │   ├── README.md            # Memory system docs
    │   ├── state/               # Operational state
    │   ├── signals/             # Pattern detection
    │   ├── work/                # Per-task memory
    │   ├── learning/            # Phase-based learnings
    │   │   ├── observe/
    │   │   ├── think/
    │   │   ├── plan/
    │   │   ├── build/
    │   │   ├── execute/
    │   │   └── verify/
    │   ├── research/            # Research outputs
    │   ├── sessions/            # Session summaries
    │   ├── learnings/           # Learning moments
    │   ├── decisions/           # ADRs
    │   ├── execution/           # Task logs
    │   ├── security/            # Security events
    │   ├── recovery/            # Recovery snapshots
    │   ├── raw-outputs/         # JSONL event streams
    │   └── backups/             # Pre-change backups
    ├── command/                 # Custom commands
    ├── agents/                  # Custom agent definitions
    └── docs/
        ├── SKILLSYSTEM.md       # Skill system docs
        ├── MEMORYSYSTEM.md      # Memory system docs
        └── PLUGINSYSTEM.md      # Plugin system docs
```

## Plugin System Features

The playbook installs a complete plugin system with:

| Plugin | Event | Purpose |
|--------|-------|---------|
| `security-validator.ts` | tool.execute.before | 10-tier attack pattern blocking |
| `session-manager.ts` | lifecycle | Session state management |
| `event-logger.ts` | tool.execute.after | Log tool executions to memory |
| `context-loader.ts` | startup | Load CORE skill context |

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
10. **Infrastructure Protection** - rm .opencode (BLOCK)

## Memory System Features

Three-tier memory architecture:

| Tier | Temperature | Purpose | Location |
|------|-------------|---------|----------|
| **CAPTURE** | Hot | Active work items | `memory/work/` |
| **SYNTHESIS** | Warm | Phase-based learnings | `memory/learning/` |
| **APPLICATION** | Cold | Historical archive | `memory/sessions/`, etc. |

## Skills System Features

- **YAML Frontmatter** with `USE WHEN` activation triggers
- **Lowercase naming** convention with hyphens (e.g., `code-review`)
- **On-demand loading** - metadata at startup, full body on invocation
- **Claude-compatible** - works with `.claude/skills/` locations too
- **create-skill** skill for generating new skills

## Comparison: Claude Code vs OpenCode

| Feature | Claude Code | OpenCode |
|---------|-------------|----------|
| Config directory | `.claude/` | `.opencode/` |
| Main config | `.claude/settings.json` | `opencode.json` |
| Identity file | `CLAUDE.md` | `AGENTS.md` |
| Hooks/Plugins | Shell command hooks | TypeScript plugins |
| Skills location | `.claude/skills/` | `.opencode/skill/` |
| Skill naming | TitleCase | lowercase-with-hyphens |
| Memory | `.claude/MEMORY/` | `.opencode/memory/` |

## Prerequisites

- An agent directory where you want to install the infrastructure
- The agent should have a clear purpose/role (used to generate identity)
- **Node.js** (v18+) or **Bun** runtime for TypeScript plugins
- **OpenCode CLI** installed - https://opencode.ai

## Usage

Run this playbook in the target agent's directory. The playbook will:

1. Analyze the agent's purpose from directory name and any existing files
2. Generate appropriate agent identity (name, mission, role)
3. Create the complete `.opencode/` directory structure
4. Install the Plugin System with security validator
5. Initialize the Memory System with three-tier architecture
6. Create the Skills Framework with core and create-skill
7. Verify the installation

## After Installation

Once the infrastructure is installed, you can:

1. Configure **MCP servers** for external tool integrations
2. Add **custom skills** for domain expertise
3. Customize the AGENTS.md with additional instructions
4. Add custom **plugins** for automation
5. Create **custom commands** for reusable prompts
6. Start using the agent with full cognitive capabilities

## Git Configuration

### What to Commit

| Directory | Commit? | Reason |
|-----------|---------|--------|
| `opencode.json` | Yes | Main configuration |
| `.opencode/VERSION` | Yes | Infrastructure version |
| `.opencode/config/` | Yes | Runtime settings |
| `.opencode/skill/` | Yes | Skill definitions |
| `.opencode/plugin/` | Yes | Plugin code |
| `.opencode/docs/` | Yes | Documentation |
| `.opencode/memory/state/` | No | Session state |
| `.opencode/memory/signals/` | No | Pattern detection |
| `.opencode/memory/work/` | No | Active work items |
| `.opencode/memory/raw-outputs/` | No | Event logs |
| `.opencode/memory/sessions/` | No | Session history |
| `.opencode/memory/security/` | No | Security events |
| `AGENTS.md` | Yes | Agent identity |

### Recommended .gitignore

```gitignore
# OpenCode Cognitive Infrastructure - Private Data
.opencode/memory/raw-outputs/
.opencode/memory/sessions/
.opencode/memory/security/
.opencode/memory/state/
.opencode/memory/signals/
.opencode/memory/work/

# Keep structure but ignore contents
!.opencode/memory/.gitkeep
!.opencode/memory/state/.gitkeep
```

## MCP Server Integration

OpenCode supports MCP (Model Context Protocol) servers for external tools. Add to `opencode.json`:

```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com",
      "enabled": true
    }
  }
}
```

## Version Migration

### Upgrading Infrastructure

1. **Check current version**: Read `.opencode/VERSION`
2. **Backup existing**: `cp -r .opencode .opencode.backup`
3. **Run upgrade playbook**: Future versions will include migration scripts
4. **Verify**: Run the 5_VERIFY phase to confirm upgrade success

### Version History

| Version | Changes |
|---------|---------|
| 1.0.0 | Initial release with plugin system, memory system, skills framework |

## Version

Current infrastructure version: **1.0.0**

## Credits

The OpenCode Cognitive Infrastructure is adapted from the Claude Cognitive Infrastructure, which was influenced by [Daniel Miessler's](https://danielmiessler.com/) [Personal AI Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure) project.

OpenCode documentation and plugin system based on the official [OpenCode documentation](https://opencode.ai/docs/).

---

*OpenCode Cognitive Infrastructure Setup Playbook*
