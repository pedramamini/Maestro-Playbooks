# Claude Cognitive Infrastructure Setup

Deploys the complete Claude Cognitive Infrastructure to any agent directory, enabling persistent memory, modular skills, context management, and event-driven hooks.

## What This Playbook Does

This playbook creates the foundational `.claude/` directory structure that gives Claude-based agents their cognitive capabilities:

- **Memory System** - Persistent knowledge across sessions (learnings, preferences, work status)
- **Skills Framework** - Modular domain expertise that activates based on intent
- **Context Management** - Structured knowledge organized by domain
- **Hooks System** - Event-driven automation for observability
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
    │   └── CORE/
    │       └── SKILL.md         # Core skill with agent identity
    ├── context/
    │   ├── CLAUDE.md            # Context system documentation
    │   ├── memory/              # Persistent memory
    │   │   ├── learnings.md     # Facts about users/org
    │   │   ├── user_preferences.md  # Working style
    │   │   └── work_status.md   # Current tasks
    │   ├── architecture/        # System design patterns
    │   ├── design/              # Design principles
    │   ├── development/         # Development context
    │   ├── projects/            # Project-specific configs
    │   ├── testing/             # Testing guidelines
    │   ├── tools/               # Tool documentation
    │   └── working/             # Working context
    ├── hooks/                   # TypeScript event hooks
    ├── agents/                  # Orchestration worker definitions
    ├── scripts/                 # Utility scripts
    └── examples/                # Reference examples
```

## Prerequisites

- An agent directory where you want to install the infrastructure
- The agent should have a clear purpose/role (used to generate identity)

## Usage

Run this playbook in the target agent's directory. The playbook will:

1. Analyze the agent's purpose from directory name and any existing files
2. Generate appropriate agent identity (name, mission, role)
3. Create the complete `.claude/` directory structure
4. Initialize memory files
5. Create the CORE skill with agent identity
6. Verify the installation

## After Installation

Once the infrastructure is installed, you can:

1. Run **Knowledge Pack** playbooks to add domain expertise
2. Customize the CLAUDE.md with additional instructions
3. Add custom hooks for automation
4. Start using the agent with full cognitive capabilities

## Version

Current infrastructure version: **1.1.0**

## Credits

The Claude Cognitive Infrastructure was influenced by [Daniel Miessler's](https://danielmiessler.com/) [Personal AI Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure) project, which pioneered many of the concepts around persistent memory, modular skills, and structured context for AI assistants.

---

*Claude Cognitive Infrastructure Setup Playbook*
