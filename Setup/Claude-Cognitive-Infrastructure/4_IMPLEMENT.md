# Phase 4: Implement Installation

## Objective

Execute the complete Claude Cognitive Infrastructure installation including the Hook System, Memory System, and Skills System.

---

## Part 1: Directory Structure

### Step 1.1: Create Base Directory Tree

```bash
mkdir -p .claude/{config,hooks/lib,agents,scripts,examples}
mkdir -p .claude/skills/{CORE/{SYSTEM,USER,Workflows},CreateSkill}
mkdir -p .claude/MEMORY/{State,Signals,Work,Learning/{OBSERVE,THINK,PLAN,BUILD,EXECUTE,VERIFY}}
mkdir -p .claude/MEMORY/{research,sessions,learnings,decisions,execution,security,recovery,raw-outputs,backups}
```

### Step 1.2: Create VERSION File

```bash
echo "1.1.0" > .claude/VERSION
```

---

## Part 2: Hook System

The Hook System provides event-driven automation that fires at key lifecycle points.

### Step 2.1: Create settings.json

Create `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bun run .claude/hooks/initialize-session.ts"
          },
          {
            "type": "command",
            "command": "bun run .claude/hooks/load-core-context.ts"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bun run .claude/hooks/security-validator.ts"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bun run .claude/hooks/event-logger.ts"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bun run .claude/hooks/session-summary.ts"
          }
        ]
      }
    ]
  },
  "permissions": {
    "tools": ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebFetch", "WebSearch", "Task"]
  }
}
```

### Step 2.2: Create Security Validator Hook

Create `.claude/hooks/security-validator.ts`:

```typescript
#!/usr/bin/env bun
// Security validator - PreToolUse hook for Bash commands
// Validates commands and blocks dangerous operations

interface PreToolUsePayload {
  session_id: string;
  tool_name: string;
  tool_input: Record<string, any>;
}

// Attack pattern categories - 10 tiers of protection
const ATTACK_PATTERNS = {
  // Tier 1: Catastrophic - Always block
  catastrophic: {
    patterns: [
      /rm\s+(-rf?|--recursive)\s+[\/~]/i,
      /rm\s+(-rf?|--recursive)\s+\*/i,
      />\s*\/dev\/sd[a-z]/i,
      /mkfs\./i,
      /dd\s+if=.*of=\/dev/i,
    ],
    action: 'block',
    message: 'BLOCKED: Catastrophic deletion/destruction detected'
  },

  // Tier 2: Reverse shells - Always block
  reverseShell: {
    patterns: [
      /bash\s+-i\s+>&\s*\/dev\/tcp/i,
      /nc\s+(-e|--exec)\s+\/bin\/(ba)?sh/i,
      /python.*socket.*connect/i,
      /perl.*socket.*connect/i,
      /ruby.*TCPSocket/i,
      /php.*fsockopen/i,
      /socat.*exec/i,
      /\|\s*\/bin\/(ba)?sh/i,
    ],
    action: 'block',
    message: 'BLOCKED: Reverse shell pattern detected'
  },

  // Tier 3: Credential theft - Always block
  credentialTheft: {
    patterns: [
      /curl.*\|\s*(ba)?sh/i,
      /wget.*\|\s*(ba)?sh/i,
      /curl.*(-o|--output).*&&.*chmod.*\+x/i,
      /base64\s+-d.*\|\s*(ba)?sh/i,
    ],
    action: 'block',
    message: 'BLOCKED: Remote code execution pattern detected'
  },

  // Tier 4: Prompt injection indicators - Block and log
  promptInjection: {
    patterns: [
      /ignore\s+(all\s+)?previous\s+instructions/i,
      /disregard\s+(all\s+)?prior\s+instructions/i,
      /you\s+are\s+now\s+(in\s+)?[a-z]+\s+mode/i,
      /new\s+instruction[s]?:/i,
      /system\s+prompt:/i,
      /\[INST\]/i,
      /<\|im_start\|>/i,
    ],
    action: 'block',
    message: 'BLOCKED: Prompt injection pattern detected'
  },

  // Tier 5: Environment manipulation - Warn
  envManipulation: {
    patterns: [
      /export\s+(ANTHROPIC|OPENAI|AWS|AZURE)_/i,
      /echo\s+\$\{?(ANTHROPIC|OPENAI)_/i,
      /env\s*\|.*KEY/i,
      /printenv.*KEY/i,
    ],
    action: 'warn',
    message: 'WARNING: Environment/credential access detected'
  },

  // Tier 6: Git dangerous operations - Require confirmation
  gitDangerous: {
    patterns: [
      /git\s+push.*(-f|--force)/i,
      /git\s+reset\s+--hard/i,
      /git\s+clean\s+-fd/i,
      /git\s+checkout\s+--\s+\./i,
    ],
    action: 'warn',
    message: 'WARNING: Potentially destructive git operation'
  },

  // Tier 7: System modification - Log
  systemMod: {
    patterns: [
      /chmod\s+777/i,
      /chown\s+root/i,
      /sudo\s+/i,
      /systemctl\s+(stop|disable)/i,
    ],
    action: 'log',
    message: 'LOGGED: System modification command'
  },

  // Tier 8: Network operations - Log
  network: {
    patterns: [
      /ssh\s+/i,
      /scp\s+/i,
      /rsync.*:/i,
      /curl\s+(-X\s+POST|--data)/i,
    ],
    action: 'log',
    message: 'LOGGED: Network operation'
  },

  // Tier 9: Data exfiltration patterns - Block
  exfiltration: {
    patterns: [
      /curl.*(@|--upload-file)/i,
      /tar.*\|.*curl/i,
      /zip.*\|.*nc/i,
    ],
    action: 'block',
    message: 'BLOCKED: Data exfiltration pattern detected'
  },

  // Tier 10: Infrastructure protection - Block
  infraProtection: {
    patterns: [
      /rm.*\.claude/i,
      /rm.*\.config/i,
    ],
    action: 'block',
    message: 'BLOCKED: Infrastructure protection triggered'
  }
};

function validateCommand(command: string): { allowed: boolean; message?: string; action?: string } {
  if (!command || command.length < 3) {
    return { allowed: true };
  }

  for (const [tierName, tier] of Object.entries(ATTACK_PATTERNS)) {
    for (const pattern of tier.patterns) {
      if (pattern.test(command)) {
        console.error(`[Security] ${tierName}: ${tier.message}`);
        console.error(`[Security] Command: ${command.substring(0, 100)}...`);
        return {
          allowed: tier.action !== 'block',
          message: tier.message,
          action: tier.action
        };
      }
    }
  }

  return { allowed: true };
}

async function main() {
  try {
    const stdinData = await Bun.stdin.text();
    if (!stdinData.trim()) {
      process.exit(0);
    }

    const payload: PreToolUsePayload = JSON.parse(stdinData);

    if (payload.tool_name !== 'Bash') {
      process.exit(0);
    }

    const command = payload.tool_input?.command;
    if (!command) {
      process.exit(0);
    }

    const validation = validateCommand(command);

    if (!validation.allowed) {
      console.log(validation.message);
      console.log(`Command blocked: ${command.substring(0, 100)}...`);
      process.exit(2); // Exit code 2 signals block to Claude Code
    }

    if (validation.action === 'warn') {
      console.log(validation.message);
    }

  } catch (error) {
    console.error('Security validator error:', error);
  }

  process.exit(0);
}

main();
```

### Step 2.3: Create Initialize Session Hook

Create `.claude/hooks/initialize-session.ts`:

```typescript
#!/usr/bin/env bun
// Initialize session - SessionStart hook
// Sets up session state and loads initial context

import { writeFileSync, existsSync, mkdirSync } from 'fs';

const MEMORY_DIR = '.claude/MEMORY';
const STATE_DIR = `${MEMORY_DIR}/State`;

async function main() {
  try {
    // Ensure directories exist
    if (!existsSync(STATE_DIR)) {
      mkdirSync(STATE_DIR, { recursive: true });
    }

    // Initialize or update session state
    const sessionState = {
      session_id: `session_${Date.now()}`,
      started_at: new Date().toISOString(),
      status: 'active'
    };

    writeFileSync(
      `${STATE_DIR}/active-session.json`,
      JSON.stringify(sessionState, null, 2)
    );

    console.log(`Session initialized: ${sessionState.session_id}`);

  } catch (error) {
    console.error('Session initialization error:', error);
  }
}

main();
```

### Step 2.4: Create Load Core Context Hook

Create `.claude/hooks/load-core-context.ts`:

```typescript
#!/usr/bin/env bun
// Load core context - SessionStart hook
// Loads CORE skill content at session start

import { readFileSync, existsSync } from 'fs';

const CORE_SKILL_PATH = '.claude/skills/CORE/SKILL.md';

async function main() {
  try {
    if (existsSync(CORE_SKILL_PATH)) {
      const content = readFileSync(CORE_SKILL_PATH, 'utf-8');
      // Output to stdout for context injection
      console.log('--- CORE CONTEXT LOADED ---');
      console.log(content);
      console.log('--- END CORE CONTEXT ---');
    }
  } catch (error) {
    console.error('Context loading error:', error);
  }
}

main();
```

### Step 2.5: Create Event Logger Hook

Create `.claude/hooks/event-logger.ts`:

```typescript
#!/usr/bin/env bun
// Event logger - PostToolUse hook
// Logs tool executions to MEMORY

import { appendFileSync, existsSync, mkdirSync } from 'fs';

const RAW_OUTPUT_DIR = '.claude/MEMORY/raw-outputs';

interface PostToolUsePayload {
  session_id: string;
  tool_name: string;
  tool_input: Record<string, any>;
  tool_output?: string;
}

async function main() {
  try {
    const stdinData = await Bun.stdin.text();
    if (!stdinData.trim()) {
      process.exit(0);
    }

    const payload: PostToolUsePayload = JSON.parse(stdinData);

    // Ensure directory exists
    if (!existsSync(RAW_OUTPUT_DIR)) {
      mkdirSync(RAW_OUTPUT_DIR, { recursive: true });
    }

    // Create log entry
    const logEntry = {
      timestamp: new Date().toISOString(),
      session_id: payload.session_id,
      tool_name: payload.tool_name,
      tool_input: payload.tool_input
    };

    // Append to daily log file
    const today = new Date().toISOString().split('T')[0];
    const logFile = `${RAW_OUTPUT_DIR}/${today}.jsonl`;

    appendFileSync(logFile, JSON.stringify(logEntry) + '\n');

  } catch (error) {
    // Silent fail - logging should never break execution
  }
}

main();
```

### Step 2.6: Create Session Summary Hook

Create `.claude/hooks/session-summary.ts`:

```typescript
#!/usr/bin/env bun
// Session summary - Stop hook
// Captures session summary when session ends

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';

const SESSIONS_DIR = '.claude/MEMORY/sessions';
const STATE_DIR = '.claude/MEMORY/State';

async function main() {
  try {
    // Ensure directory exists
    if (!existsSync(SESSIONS_DIR)) {
      mkdirSync(SESSIONS_DIR, { recursive: true });
    }

    // Read active session state
    const sessionFile = `${STATE_DIR}/active-session.json`;
    let sessionId = 'unknown';
    let startedAt = new Date().toISOString();

    if (existsSync(sessionFile)) {
      const state = JSON.parse(readFileSync(sessionFile, 'utf-8'));
      sessionId = state.session_id || sessionId;
      startedAt = state.started_at || startedAt;
    }

    // Create session summary
    const summary = {
      session_id: sessionId,
      started_at: startedAt,
      ended_at: new Date().toISOString(),
      status: 'completed'
    };

    // Save to sessions directory
    const filename = `${SESSIONS_DIR}/${sessionId}.json`;
    writeFileSync(filename, JSON.stringify(summary, null, 2));

    console.log(`Session summary saved: ${filename}`);

  } catch (error) {
    console.error('Session summary error:', error);
  }
}

main();
```

---

## Part 3: Memory System

The Memory System provides persistent knowledge across sessions using a three-tier architecture.

### Step 3.1: Create MEMORY README

Create `.claude/MEMORY/README.md`:

```markdown
# MEMORY System

Persistent memory architecture for session history, learnings, and operational state.

## Directory Structure

| Directory | Purpose | Retention |
|-----------|---------|-----------|
| `research/` | Deep research outputs | Permanent |
| `sessions/` | Session summaries (auto-captured) | Rolling 90 days |
| `learnings/` | Learning moments | Permanent |
| `decisions/` | Architectural Decision Records | Permanent |
| `execution/` | Task execution logs | Rolling 30 days |
| `security/` | Security event logs | Permanent |
| `recovery/` | Recovery snapshots | Rolling 7 days |
| `raw-outputs/` | JSONL event streams | Rolling 7 days |
| `backups/` | Pre-refactoring backups | As needed |
| `State/` | Current operational state | Active |
| `Signals/` | Pattern detection | Active |
| `Work/` | Per-task memory | Active |
| `Learning/` | Phase-based learnings | Permanent |

## Three-Tier Memory Model

### 1. CAPTURE (Hot) - Per-Task Work

Current work items in `Work/[Task-Name_TIMESTAMP]/`:
- `Work.md` - Goal, result, signal tracking
- `TRACE.jsonl` - Decision trace
- `Output/` - Deliverables produced

### 2. SYNTHESIS (Warm) - Aggregated Learning

Learnings organized by phase in `Learning/`:
- `OBSERVE/` - Context gathering learnings
- `THINK/` - Hypothesis generation learnings
- `PLAN/` - Execution planning learnings
- `BUILD/` - Success criteria learnings
- `EXECUTE/` - Implementation learnings
- `VERIFY/` - Verification learnings

### 3. APPLICATION (Cold) - Archived History

Historical data organized by date in main directories.

## Privacy

Add to .gitignore:
\`\`\`
.claude/MEMORY/raw-outputs/
.claude/MEMORY/sessions/
.claude/MEMORY/security/
\`\`\`
```

### Step 3.2: Initialize State Files

Create `.claude/MEMORY/State/active-work.json`:

```json
{
  "current_task": null,
  "started_at": null,
  "status": "idle"
}
```

### Step 3.3: Initialize Signal Files

Create `.claude/MEMORY/Signals/README.md`:

```markdown
# Signals

Real-time pattern detection and anomaly tracking.

## Signal Files

| File | Purpose |
|------|---------|
| `failures.jsonl` | VERIFY failures with context |
| `loopbacks.jsonl` | Phase loopback events |
| `patterns.jsonl` | Weekly aggregated patterns |

## Format

Each file uses JSONL (JSON Lines) format - one JSON object per line.
```

---

## Part 4: Skills System

The Skills System provides modular domain expertise with tiered loading.

### Step 4.1: Create CORE Skill

Create `.claude/skills/CORE/SKILL.md`:

```markdown
---
name: CORE
description: Core identity and configuration. AUTO-LOADS at session start. USE WHEN session begins OR user asks about identity, capabilities, or how the agent works.
---

# CORE - Agent Identity

**Auto-loads at session start.** This skill defines agent identity and core operating principles.

## Examples

**Example: Identity query**
\`\`\`
User: "Who are you?"
-> Reads CORE skill
-> Returns identity information
\`\`\`

**Example: Capability check**
\`\`\`
User: "What can you do?"
-> Lists available capabilities
-> References other skills if installed
\`\`\`

---

## Identity

**Agent:** <Agent Name>
**Role:** <Agent Role>
**Organization:** <Organization>

---

## Available Capabilities

- **Memory System**: Persistent knowledge across sessions
- **Skills Framework**: Modular domain expertise
- **Hook System**: Event-driven automation
- **Context System**: Structured knowledge by domain

---

## Quick Reference

- Skills directory: `.claude/skills/`
- Memory directory: `.claude/MEMORY/`
- Configuration: `.claude/settings.json`
```

### Step 4.2: Create Skill System Documentation

Create `.claude/skills/CORE/SYSTEM/SKILLSYSTEM.md`:

```markdown
# Custom Skill System

The configuration system for all skills.

## Skill Structure

Every skill follows this structure:

\`\`\`
SkillName/
├── SKILL.md           # Main skill file (required)
├── Context.md         # Additional context (optional)
├── Tools/             # CLI tools
│   └── ToolName.ts
└── Workflows/         # Execution workflows
    └── WorkflowName.md
\`\`\`

## SKILL.md Format

### YAML Frontmatter

\`\`\`yaml
---
name: SkillName
description: [What it does]. USE WHEN [intent triggers]. [Additional capabilities].
---
\`\`\`

**Rules:**
- `name` uses TitleCase
- `description` is a single line
- `USE WHEN` keyword is mandatory for activation
- Max 1024 characters

### Markdown Body

\`\`\`markdown
# SkillName

[Brief description]

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Create** | "create new" | \`Workflows/Create.md\` |

## Examples

**Example 1:**
\`\`\`
User: "[Request]"
-> [Action taken]
-> [Result]
\`\`\`
\`\`\`

## Skill Loading

1. **Session Start**: Only YAML frontmatter loads for routing
2. **Skill Invocation**: Full SKILL.md body loads
3. **Workflow Execution**: Additional files load on-demand

## Creating New Skills

Use the CreateSkill skill or manually create following this structure.
```

### Step 4.3: Create CreateSkill Skill

Create `.claude/skills/CreateSkill/SKILL.md`:

```markdown
---
name: CreateSkill
description: Creates new skills following the standard structure. USE WHEN user wants to create a new skill OR add new capability OR needs a custom workflow.
---

# CreateSkill

Creates properly structured skills following the Skills System specification.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Create** | "create skill", "new skill" | `Workflows/Create.md` |

## Examples

**Example: Create a research skill**
\`\`\`
User: "Create a skill for code review"
-> Creates .claude/skills/CodeReview/SKILL.md
-> Adds proper YAML frontmatter with USE WHEN
-> Creates Workflows/ and Tools/ directories
-> Returns confirmation with skill path
\`\`\`

## Skill Template

When creating a skill, use this template:

\`\`\`markdown
---
name: SkillName
description: [Purpose]. USE WHEN [triggers].
---

# SkillName

[Description]

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|

## Examples

**Example:**
\`\`\`
User: "[Request]"
-> [Process]
-> [Result]
\`\`\`
\`\`\`
```

### Step 4.4: Create USER Configuration Directory

Create `.claude/skills/CORE/USER/README.md`:

```markdown
# USER Configuration

Personal configuration that customizes agent behavior.

## Files

| File | Purpose |
|------|---------|
| `ABOUTME.md` | User background and context |
| `PREFERENCES.md` | Working style preferences |
| `CONTACTS.md` | Contact information |

## Privacy

This directory contains personal information. Add to .gitignore if version controlling:

\`\`\`
.claude/skills/CORE/USER/
\`\`\`

## Customization

Create files as needed to personalize the agent's knowledge about you and your preferences.
```

### Step 4.5: Create SYSTEM Documentation Directory

Create `.claude/skills/CORE/SYSTEM/README.md`:

```markdown
# SYSTEM Documentation

System-level documentation for the Claude Cognitive Infrastructure.

## Files

| File | Purpose |
|------|---------|
| `SKILLSYSTEM.md` | Skill creation and structure |
| `MEMORYSYSTEM.md` | Memory architecture |
| `HOOKSYSTEM.md` | Event-driven automation |

## Usage

These files provide reference documentation. They are loaded on-demand when relevant context is needed.
```

---

## Part 5: Agent Identity

### Step 5.1: Create config.yaml

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

### Step 5.2: Create Root CLAUDE.md

Create `CLAUDE.md` in agent root directory:

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

## System Architecture

You operate within the Claude Cognitive Infrastructure:

- **Skills Framework** (`.claude/skills/`): Modular domain expertise
- **Memory System** (`.claude/MEMORY/`): Persistent knowledge
- **Hook System** (`.claude/hooks/`): Event-driven automation
- **Configuration** (`.claude/config/`): Runtime settings

## Memory Management

**CRITICAL:** Update work status after EVERY conversation turn to maintain continuity.

- Read relevant memories before starting work
- Update memories after significant interactions
- Keep work status current at `.claude/MEMORY/State/`

## Organization Context

<Organization description and relevant context>

---

*Claude Cognitive Infrastructure v1.1.0*
```

---

## Part 6: Gitignore Configuration

### Step 6.1: Create/Update .gitignore

Add to `.gitignore` in agent root:

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

### Step 6.2: Create .gitkeep Files

```bash
touch .claude/MEMORY/.gitkeep
touch .claude/MEMORY/State/.gitkeep
touch .claude/MEMORY/Signals/.gitkeep
touch .claude/MEMORY/Work/.gitkeep
touch .claude/MEMORY/Learning/.gitkeep
```

---

## Post-Implementation Checklist

After all files are created:

- [ ] Verify all directories exist
- [ ] Validate JSON syntax in settings.json
- [ ] Validate YAML syntax in config.yaml
- [ ] Ensure hook files are executable (`chmod +x .claude/hooks/*.ts`)
- [ ] Test security validator: `echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | bun run .claude/hooks/security-validator.ts`
- [ ] Verify CLAUDE.md has been customized with agent identity
- [ ] Confirm .gitignore excludes sensitive data

---

## Next Phase

Proceed to **5_VERIFY.md** to verify the installation.
