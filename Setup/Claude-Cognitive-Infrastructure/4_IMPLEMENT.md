# Phase 4: Implement Installation

## Objective

Execute the Claude Cognitive Infrastructure installation.

## Implementation Steps

### Step 1: Create Directory Structure

Create the `.claude/` directory tree:

```bash
mkdir -p .claude/{config,skills/CORE,context/{memory,architecture,design,development,projects,testing,tools,working},hooks,agents,scripts,examples}
```

### Step 2: Create VERSION File

```bash
echo "1.1.0" > .claude/VERSION
```

### Step 3: Create settings.json

Create `.claude/settings.json`:

```json
{
  "hooks": {
    "preToolCall": [],
    "postToolCall": [],
    "notification": []
  },
  "permissions": {
    "tools": ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebFetch", "WebSearch"]
  },
  "memory": {
    "updateFrequency": "every_turn",
    "autoSave": true
  }
}
```

### Step 4: Create config.yaml

Create `.claude/config/config.yaml`:

```yaml
version: "1.1.0"
infrastructure:
  name: "Claude Cognitive Infrastructure"
  installed: "<current-date>"

agent:
  name: "<Agent Name>"
  persona: "<Persona>"
  type: "<Agent Type>"
  organization: "<Organization>"

settings:
  memory_update_frequency: "every_turn"
  context_loading: "progressive"
  skill_activation: "trigger_based"

capabilities:
  memory: true
  skills: true
  hooks: true
  context: true
```

### Step 5: Create CLAUDE.md (Root Identity)

Create `CLAUDE.md` in agent root:

```markdown
# <Agent Name>: <Agent Type>

## Your Name

Your name is **<Persona>**. You are the <Agent Type> for <Organization>.

## Your Mission

<Mission statement - one clear sentence describing purpose>

## Your Role

<Role description - 2-3 sentences on how this agent fits in the organization>

## Core Responsibilities

### Primary Functions
- <Key responsibility 1>
- <Key responsibility 2>
- <Key responsibility 3>

### Supporting Tasks
- <Supporting task 1>
- <Supporting task 2>

## Context System

You have access to a context system at `.claude/context/`:

- **Memory** (`.claude/context/memory/`): Persistent knowledge
  - `learnings.md` - Facts about users and organization
  - `user_preferences.md` - Working preferences and style
  - `work_status.md` - Current tasks and progress

## Memory Management

**CRITICAL:** Update `work_status.md` after EVERY conversation turn to maintain continuity.

- Read relevant memories before starting work
- Update memories after significant interactions
- Keep work status current

## Organization Context

<Organization description and relevant context>

---

*Claude Cognitive Infrastructure v1.1.0*
```

### Step 6: Create CORE Skill

Create `.claude/skills/CORE/SKILL.md`:

```markdown
---
name: CORE
version: 1.0.0
priority: 100
triggers:
  - identity
  - who are you
  - what do you do
  - help
  - capabilities
context_budget: 5000
---

# <Persona>: Core Identity

## Overview

I am **<Persona>**, the <Agent Type> for <Organization>. <Brief description of capabilities and purpose>.

## Primary Functions

<List of key responsibilities>

## Working Style

<Description of how the agent operates, communicates, and approaches tasks>

## Available Capabilities

- **Memory**: Persistent knowledge across sessions
- **Skills**: Modular domain expertise
- **Context**: Structured knowledge by domain
- **Hooks**: Event-driven automation

---

*Core Identity Skill v1.0.0*
```

### Step 7: Initialize Memory Files

Create `.claude/context/memory/learnings.md`:

```markdown
# Learnings

Facts and knowledge accumulated about users, organization, and domain.

## Users

<!-- Add user-specific learnings here -->

## Organization

<!-- Add organization learnings here -->

## Domain Knowledge

<!-- Add domain-specific learnings here -->

---
*Last updated: <date>*
```

Create `.claude/context/memory/user_preferences.md`:

```markdown
# User Preferences

Working style and preferences for interactions.

## Communication Style

<!-- Preferred communication approach -->

## Working Hours

<!-- Typical availability -->

## Preferences

<!-- Specific preferences noted -->

---
*Last updated: <date>*
```

Create `.claude/context/memory/work_status.md`:

```markdown
# Work Status

Current tasks and progress tracking.

## Active Tasks

<!-- Currently in-progress work -->

## Pending Items

<!-- Queued for future -->

## Recently Completed

<!-- Finished within last session -->

---
*Last updated: <date>*
```

### Step 8: Create Context Placeholders

Create CLAUDE.md in each context subdirectory with appropriate documentation for that context type.

### Step 9: Create Hooks Placeholder

Create `.claude/hooks/CLAUDE.md`:

```markdown
# Hooks

Event-driven automation hooks for the agent.

## Available Hook Points

- **preToolCall**: Before tool execution
- **postToolCall**: After tool execution
- **notification**: For alerts and updates

## Adding Hooks

Create TypeScript files in this directory to add hook functionality.
```

## Post-Implementation

After all files are created:

1. Verify file permissions
2. Validate JSON/YAML syntax
3. Confirm all directories exist
4. Test basic functionality

## Next Phase

Proceed to **5_VERIFY.md** to verify the installation.
