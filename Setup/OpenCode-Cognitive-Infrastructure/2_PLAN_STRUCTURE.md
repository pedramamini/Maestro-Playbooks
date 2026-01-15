# Phase 2: Plan Structure

## Objective

Plan the complete OpenCode Cognitive Infrastructure directory structure for the agent.

## Core Directory Structure

```
<Agent Directory>/
├── AGENTS.md                        # Agent identity file
├── opencode.json                    # Main configuration
└── .opencode/
    ├── VERSION                      # Infrastructure version (1.0.0)
    ├── config/
    │   └── config.yaml              # Runtime configuration
    ├── skill/
    │   ├── core/
    │   │   └── SKILL.md             # Core agent skill
    │   └── create-skill/
    │       └── SKILL.md             # Skill creation skill
    ├── plugin/
    │   ├── security-validator.ts    # Security hook
    │   ├── session-manager.ts       # Session lifecycle
    │   ├── event-logger.ts          # Event logging
    │   └── context-loader.ts        # Context loading
    ├── memory/
    │   ├── README.md                # Memory system docs
    │   ├── state/
    │   │   └── active-work.json     # Current work state
    │   ├── signals/
    │   │   └── README.md            # Signal detection
    │   ├── work/                    # Per-task memory
    │   ├── learning/
    │   │   ├── observe/
    │   │   ├── think/
    │   │   ├── plan/
    │   │   ├── build/
    │   │   ├── execute/
    │   │   └── verify/
    │   ├── research/                # Research outputs
    │   ├── sessions/                # Session summaries
    │   ├── learnings/               # Learning moments
    │   ├── decisions/               # ADRs
    │   ├── execution/               # Task logs
    │   ├── security/                # Security events
    │   ├── recovery/                # Recovery snapshots
    │   ├── raw-outputs/             # JSONL event streams
    │   └── backups/                 # Pre-change backups
    ├── command/
    │   └── README.md                # Custom commands
    ├── agents/
    │   └── README.md                # Custom agent definitions
    └── docs/
        ├── SKILLSYSTEM.md           # Skill system docs
        ├── MEMORYSYSTEM.md          # Memory system docs
        └── PLUGINSYSTEM.md          # Plugin system docs
```

## File Contents Plan

### AGENTS.md (Root Identity)

```markdown
# <Agent Name>: <Agent Type>

## Your Name
Your name is **<Persona>**. You are the <Agent Type> for <Organization>.

## Your Mission
<Mission statement>

## Your Role
<Role description>

## Core Responsibilities
<Grouped responsibilities>

## Memory Management
**CRITICAL:** Update work state after EVERY conversation turn.

## Organization Context
<Organization details>
```

### opencode.json

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": {
    "security-validator": {
      "enabled": true
    },
    "session-manager": {
      "enabled": true
    },
    "event-logger": {
      "enabled": true
    },
    "context-loader": {
      "enabled": true
    }
  },
  "skill": {
    "allow": ["*"],
    "deny": []
  },
  "agents": {
    "build": {
      "model": "anthropic:claude-sonnet-4-20250514"
    },
    "plan": {
      "model": "anthropic:claude-sonnet-4-20250514"
    }
  }
}
```

### VERSION

```
1.0.0
```

### config/config.yaml

```yaml
version: "1.0.0"
agent:
  name: "<Agent Name>"
  persona: "<Persona>"
  type: "<Agent Type>"
settings:
  memory_update_frequency: "every_turn"
  context_loading: "progressive"
```

### skill/core/SKILL.md

```markdown
---
name: core
description: Core identity and configuration. Provides agent identity, capabilities overview, and operating principles. USE WHEN session begins OR user asks about identity, capabilities, or how the agent works.
---

# Core - Agent Identity

**Auto-loads at session start.** This skill defines agent identity and core operating principles.

## Identity

**Agent:** <Agent Name>
**Role:** <Agent Role>
**Organization:** <Organization>

## Available Capabilities

- **Memory System**: Persistent knowledge across sessions
- **Skills Framework**: Modular domain expertise
- **Plugin System**: Event-driven automation
- **MCP Integration**: External tool access

## Quick Reference

- Skills directory: `.opencode/skill/`
- Memory directory: `.opencode/memory/`
- Configuration: `opencode.json`
```

### Memory Files

**memory/README.md:**
```markdown
# Memory System

Persistent memory architecture for session history, learnings, and operational state.

## Directory Structure

| Directory | Purpose | Retention |
|-----------|---------|-----------|
| `research/` | Deep research outputs | Permanent |
| `sessions/` | Session summaries | Rolling 90 days |
| `learnings/` | Learning moments | Permanent |
| `decisions/` | Architectural Decision Records | Permanent |
| `execution/` | Task execution logs | Rolling 30 days |
| `security/` | Security event logs | Permanent |
| `recovery/` | Recovery snapshots | Rolling 7 days |
| `raw-outputs/` | JSONL event streams | Rolling 7 days |
| `backups/` | Pre-refactoring backups | As needed |
| `state/` | Current operational state | Active |
| `signals/` | Pattern detection | Active |
| `work/` | Per-task memory | Active |
| `learning/` | Phase-based learnings | Permanent |
```

**memory/state/active-work.json:**
```json
{
  "current_task": null,
  "started_at": null,
  "status": "idle"
}
```

## Context Placeholder Files

Each context subdirectory gets a README.md placeholder:

```markdown
# <Context Name>

This directory contains <context type> information.

## Contents

<Description of what goes here>

## Usage

<How the agent should use this context>
```

## Next Phase

Proceed to **3_EVALUATE.md** to evaluate the planned structure.
