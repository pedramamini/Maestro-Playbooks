# Phase 2: Plan Structure

## Objective

Plan the complete Claude Cognitive Infrastructure directory structure for the agent.

## Core Directory Structure

```
<Agent Directory>/
├── CLAUDE.md                        # Agent identity file
└── .claude/
    ├── VERSION                      # Infrastructure version (1.1.0)
    ├── settings.json                # Hook and behavior settings
    ├── config/
    │   └── config.yaml              # Runtime configuration
    ├── skills/
    │   └── CORE/
    │       └── SKILL.md             # Core agent skill
    ├── context/
    │   ├── CLAUDE.md                # Context system documentation
    │   ├── memory/
    │   │   ├── learnings.md         # Accumulated knowledge
    │   │   ├── user_preferences.md  # User working style
    │   │   └── work_status.md       # Current task tracking
    │   ├── architecture/
    │   │   └── CLAUDE.md            # Architecture context
    │   ├── design/
    │   │   └── CLAUDE.md            # Design principles
    │   ├── development/
    │   │   └── CLAUDE.md            # Development context
    │   ├── projects/
    │   │   └── CLAUDE.md            # Project configs
    │   ├── testing/
    │   │   └── CLAUDE.md            # Testing guidelines
    │   ├── tools/
    │   │   └── CLAUDE.md            # Tool documentation
    │   └── working/
    │       └── CLAUDE.md            # Working context
    ├── hooks/
    │   └── CLAUDE.md                # Hooks documentation
    ├── agents/
    │   └── CLAUDE.md                # Agent definitions
    ├── scripts/
    │   └── CLAUDE.md                # Utility scripts
    └── examples/
        └── CLAUDE.md                # Reference examples
```

## File Contents Plan

### CLAUDE.md (Root Identity)

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
**CRITICAL:** Update work_status.md after EVERY conversation turn.

## Organization Context
<Organization details>
```

### settings.json

```json
{
  "hooks": {
    "preToolCall": [],
    "postToolCall": [],
    "notification": []
  },
  "permissions": {
    "tools": ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
  }
}
```

### VERSION

```
1.1.0
```

### config/config.yaml

```yaml
version: "1.1.0"
agent:
  name: "<Agent Name>"
  persona: "<Persona>"
  type: "<Agent Type>"
settings:
  memory_update_frequency: "every_turn"
  context_loading: "progressive"
```

### CORE/SKILL.md

```markdown
---
name: CORE
version: 1.0.0
priority: 100
triggers:
  - identity
  - who are you
  - what do you do
context_budget: 5000
---

# <Persona>: Core Identity

## Overview
<Agent description and capabilities>

## Primary Functions
<Key responsibilities>

## Working Style
<How the agent operates>
```

### Memory Files

**learnings.md:**
```markdown
# Learnings

Facts and knowledge accumulated about users, organization, and domain.

## Users

## Organization

## Domain Knowledge
```

**user_preferences.md:**
```markdown
# User Preferences

Working style and preferences for interactions.

## Communication Style

## Working Hours

## Preferences
```

**work_status.md:**
```markdown
# Work Status

Current tasks and progress tracking.

## Active Tasks

## Pending Items

## Recently Completed

---
*Last updated: <date>*
```

## Context Placeholder Files

Each context subdirectory gets a CLAUDE.md placeholder:

```markdown
# <Context Name> Context

This directory contains <context type> information.

## Contents

<Description of what goes here>

## Usage

<How the agent should use this context>
```

## Next Phase

Proceed to **3_EVALUATE.md** to evaluate the planned structure.
