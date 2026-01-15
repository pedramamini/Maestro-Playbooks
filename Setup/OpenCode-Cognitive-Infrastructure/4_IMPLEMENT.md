# Phase 4: Implement Installation

## Objective

Execute the complete OpenCode Cognitive Infrastructure installation including the Plugin System, Memory System, and Skills System.

---

## Part 1: Directory Structure

### Step 1.1: Create Base Directory Tree

```bash
mkdir -p .opencode/{config,command,agents,docs}
mkdir -p .opencode/skill/{core,create-skill}
mkdir -p .opencode/plugin
mkdir -p .opencode/memory/{state,signals,work,learning/{observe,think,plan,build,execute,verify}}
mkdir -p .opencode/memory/{research,sessions,learnings,decisions,execution,security,recovery,raw-outputs,backups}
```

### Step 1.2: Create VERSION File

```bash
echo "1.0.0" > .opencode/VERSION
```

---

## Part 2: Plugin System

The Plugin System provides event-driven automation through TypeScript plugins that intercept tool executions and lifecycle events.

### Step 2.1: Create opencode.json

Create `opencode.json` in the agent root:

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

### Step 2.2: Create Security Validator Plugin

Create `.opencode/plugin/security-validator.ts`:

```typescript
import type { Plugin } from "@opencode-ai/plugin";

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
    action: "block",
    message: "BLOCKED: Catastrophic deletion/destruction detected",
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
    action: "block",
    message: "BLOCKED: Reverse shell pattern detected",
  },

  // Tier 3: Credential theft - Always block
  credentialTheft: {
    patterns: [
      /curl.*\|\s*(ba)?sh/i,
      /wget.*\|\s*(ba)?sh/i,
      /curl.*(-o|--output).*&&.*chmod.*\+x/i,
      /base64\s+-d.*\|\s*(ba)?sh/i,
    ],
    action: "block",
    message: "BLOCKED: Remote code execution pattern detected",
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
    action: "block",
    message: "BLOCKED: Prompt injection pattern detected",
  },

  // Tier 5: Environment manipulation - Warn
  envManipulation: {
    patterns: [
      /export\s+(ANTHROPIC|OPENAI|AWS|AZURE)_/i,
      /echo\s+\$\{?(ANTHROPIC|OPENAI)_/i,
      /env\s*\|.*KEY/i,
      /printenv.*KEY/i,
    ],
    action: "warn",
    message: "WARNING: Environment/credential access detected",
  },

  // Tier 6: Git dangerous operations - Require confirmation
  gitDangerous: {
    patterns: [
      /git\s+push.*(-f|--force)/i,
      /git\s+reset\s+--hard/i,
      /git\s+clean\s+-fd/i,
      /git\s+checkout\s+--\s+\./i,
    ],
    action: "warn",
    message: "WARNING: Potentially destructive git operation",
  },

  // Tier 7: System modification - Log
  systemMod: {
    patterns: [
      /chmod\s+777/i,
      /chown\s+root/i,
      /sudo\s+/i,
      /systemctl\s+(stop|disable)/i,
    ],
    action: "log",
    message: "LOGGED: System modification command",
  },

  // Tier 8: Network operations - Log
  network: {
    patterns: [/ssh\s+/i, /scp\s+/i, /rsync.*:/i, /curl\s+(-X\s+POST|--data)/i],
    action: "log",
    message: "LOGGED: Network operation",
  },

  // Tier 9: Data exfiltration patterns - Block
  exfiltration: {
    patterns: [/curl.*(@|--upload-file)/i, /tar.*\|.*curl/i, /zip.*\|.*nc/i],
    action: "block",
    message: "BLOCKED: Data exfiltration pattern detected",
  },

  // Tier 10: Infrastructure protection - Block
  infraProtection: {
    patterns: [/rm.*\.opencode/i, /rm.*\.config/i],
    action: "block",
    message: "BLOCKED: Infrastructure protection triggered",
  },
};

function validateCommand(command: string): {
  allowed: boolean;
  message?: string;
  action?: string;
} {
  if (!command || command.length < 3) {
    return { allowed: true };
  }

  for (const [tierName, tier] of Object.entries(ATTACK_PATTERNS)) {
    for (const pattern of tier.patterns) {
      if (pattern.test(command)) {
        console.error(`[Security] ${tierName}: ${tier.message}`);
        console.error(`[Security] Command: ${command.substring(0, 100)}...`);
        return {
          allowed: tier.action !== "block",
          message: tier.message,
          action: tier.action,
        };
      }
    }
  }

  return { allowed: true };
}

export const SecurityValidator: Plugin = async ({ client, $ }) => {
  return {
    tool: {
      execute: {
        before: async (input, output) => {
          // Check if this is a shell/bash command
          if (input.name === "shell" || input.name === "bash") {
            const command = input.input?.command || input.input?.cmd || "";
            const validation = validateCommand(command);

            if (!validation.allowed) {
              throw new Error(validation.message);
            }

            if (validation.action === "warn") {
              console.warn(validation.message);
            }
          }
        },
      },
    },
  };
};

export default SecurityValidator;
```

### Step 2.3: Create Session Manager Plugin

Create `.opencode/plugin/session-manager.ts`:

```typescript
import type { Plugin } from "@opencode-ai/plugin";
import { writeFileSync, existsSync, mkdirSync, readFileSync } from "fs";

const MEMORY_DIR = ".opencode/memory";
const STATE_DIR = `${MEMORY_DIR}/state`;
const SESSIONS_DIR = `${MEMORY_DIR}/sessions`;

export const SessionManager: Plugin = async ({ client, $ }) => {
  // Initialize session on plugin load
  const sessionId = `session_${Date.now()}`;
  const startedAt = new Date().toISOString();

  // Ensure directories exist
  if (!existsSync(STATE_DIR)) {
    mkdirSync(STATE_DIR, { recursive: true });
  }
  if (!existsSync(SESSIONS_DIR)) {
    mkdirSync(SESSIONS_DIR, { recursive: true });
  }

  // Write initial session state
  const sessionState = {
    session_id: sessionId,
    started_at: startedAt,
    status: "active",
  };

  writeFileSync(
    `${STATE_DIR}/active-session.json`,
    JSON.stringify(sessionState, null, 2)
  );

  console.log(`[Session] Initialized: ${sessionId}`);

  return {
    event: async ({ event }) => {
      // Handle session end
      if (event.type === "session.idle") {
        const summary = {
          session_id: sessionId,
          started_at: startedAt,
          ended_at: new Date().toISOString(),
          status: "completed",
        };

        writeFileSync(
          `${SESSIONS_DIR}/${sessionId}.json`,
          JSON.stringify(summary, null, 2)
        );

        console.log(`[Session] Summary saved: ${sessionId}`);
      }
    },
  };
};

export default SessionManager;
```

### Step 2.4: Create Event Logger Plugin

Create `.opencode/plugin/event-logger.ts`:

```typescript
import type { Plugin } from "@opencode-ai/plugin";
import { appendFileSync, existsSync, mkdirSync } from "fs";

const RAW_OUTPUT_DIR = ".opencode/memory/raw-outputs";

export const EventLogger: Plugin = async ({ client, $ }) => {
  // Ensure directory exists
  if (!existsSync(RAW_OUTPUT_DIR)) {
    mkdirSync(RAW_OUTPUT_DIR, { recursive: true });
  }

  return {
    tool: {
      execute: {
        after: async (input, output) => {
          try {
            const logEntry = {
              timestamp: new Date().toISOString(),
              tool_name: input.name,
              tool_input: input.input,
              success: !output.error,
            };

            // Append to daily log file
            const today = new Date().toISOString().split("T")[0];
            const logFile = `${RAW_OUTPUT_DIR}/${today}.jsonl`;

            appendFileSync(logFile, JSON.stringify(logEntry) + "\n");
          } catch (error) {
            // Silent fail - logging should never break execution
          }
        },
      },
    },
  };
};

export default EventLogger;
```

### Step 2.5: Create Context Loader Plugin

Create `.opencode/plugin/context-loader.ts`:

```typescript
import type { Plugin } from "@opencode-ai/plugin";
import { readFileSync, existsSync } from "fs";

const CORE_SKILL_PATH = ".opencode/skill/core/SKILL.md";
const AGENTS_PATH = "AGENTS.md";

export const ContextLoader: Plugin = async ({ client, $ }) => {
  // Load core context at startup
  let coreContext = "";
  let agentIdentity = "";

  if (existsSync(CORE_SKILL_PATH)) {
    coreContext = readFileSync(CORE_SKILL_PATH, "utf-8");
    console.log("[Context] Core skill loaded");
  }

  if (existsSync(AGENTS_PATH)) {
    agentIdentity = readFileSync(AGENTS_PATH, "utf-8");
    console.log("[Context] Agent identity loaded");
  }

  return {
    // Context is loaded at plugin initialization
    // Available for reference throughout the session
  };
};

export default ContextLoader;
```

---

## Part 3: Memory System

The Memory System provides persistent knowledge across sessions using a three-tier architecture.

### Step 3.1: Create Memory README

Create `.opencode/memory/README.md`:

```markdown
# Memory System

Persistent memory architecture for session history, learnings, and operational state.

## Directory Structure

| Directory      | Purpose                      | Retention       |
| -------------- | ---------------------------- | --------------- |
| `research/`    | Deep research outputs        | Permanent       |
| `sessions/`    | Session summaries            | Rolling 90 days |
| `learnings/`   | Learning moments             | Permanent       |
| `decisions/`   | Architectural Decision Records | Permanent     |
| `execution/`   | Task execution logs          | Rolling 30 days |
| `security/`    | Security event logs          | Permanent       |
| `recovery/`    | Recovery snapshots           | Rolling 7 days  |
| `raw-outputs/` | JSONL event streams          | Rolling 7 days  |
| `backups/`     | Pre-refactoring backups      | As needed       |
| `state/`       | Current operational state    | Active          |
| `signals/`     | Pattern detection            | Active          |
| `work/`        | Per-task memory              | Active          |
| `learning/`    | Phase-based learnings        | Permanent       |

## Three-Tier Memory Model

### 1. CAPTURE (Hot) - Per-Task Work

Current work items in `work/[task-name_timestamp]/`:

- `work.md` - Goal, result, signal tracking
- `trace.jsonl` - Decision trace
- `output/` - Deliverables produced

### 2. SYNTHESIS (Warm) - Aggregated Learning

Learnings organized by phase in `learning/`:

- `observe/` - Context gathering learnings
- `think/` - Hypothesis generation learnings
- `plan/` - Execution planning learnings
- `build/` - Success criteria learnings
- `execute/` - Implementation learnings
- `verify/` - Verification learnings

### 3. APPLICATION (Cold) - Archived History

Historical data organized by date in main directories.

## Privacy

Add to .gitignore:

```
.opencode/memory/raw-outputs/
.opencode/memory/sessions/
.opencode/memory/security/
```
```

### Step 3.2: Initialize State Files

Create `.opencode/memory/state/active-work.json`:

```json
{
  "current_task": null,
  "started_at": null,
  "status": "idle"
}
```

### Step 3.3: Initialize Signal Files

Create `.opencode/memory/signals/README.md`:

```markdown
# Signals

Real-time pattern detection and anomaly tracking.

## Signal Files

| File              | Purpose                     |
| ----------------- | --------------------------- |
| `failures.jsonl`  | VERIFY failures with context |
| `loopbacks.jsonl` | Phase loopback events        |
| `patterns.jsonl`  | Weekly aggregated patterns   |

## Format

Each file uses JSONL (JSON Lines) format - one JSON object per line.
```

---

## Part 4: Skills System

The Skills System provides modular domain expertise with on-demand loading.

### Step 4.1: Create Core Skill

Create `.opencode/skill/core/SKILL.md`:

```markdown
---
name: core
description: Core identity and configuration. Provides agent identity, capabilities overview, and operating principles. USE WHEN session begins OR user asks about identity, capabilities, or how the agent works.
---

# Core - Agent Identity

**Auto-loads at session start.** This skill defines agent identity and core operating principles.

## Examples

**Example: Identity query**

```
User: "Who are you?"
-> Reads core skill
-> Returns identity information
```

**Example: Capability check**

```
User: "What can you do?"
-> Lists available capabilities
-> References other skills if installed
```

---

## Identity

**Agent:** <Agent Name>
**Role:** <Agent Role>
**Organization:** <Organization>

---

## Available Capabilities

- **Memory System**: Persistent knowledge across sessions
- **Skills Framework**: Modular domain expertise
- **Plugin System**: Event-driven automation
- **MCP Integration**: External tool access

---

## Quick Reference

- Skills directory: `.opencode/skill/`
- Memory directory: `.opencode/memory/`
- Configuration: `opencode.json`
```

### Step 4.2: Create Skill System Documentation

Create `.opencode/docs/SKILLSYSTEM.md`:

```markdown
# OpenCode Skill System

The configuration system for all skills.

## Skill Structure

Every skill follows this structure:

```
skill-name/
├── SKILL.md           # Main skill file (required)
├── context.md         # Additional context (optional)
├── tools/             # CLI tools
│   └── tool-name.ts
└── workflows/         # Execution workflows
    └── workflow-name.md
```

## SKILL.md Format

### YAML Frontmatter

```yaml
---
name: skill-name
description: [What it does]. USE WHEN [intent triggers]. [Additional capabilities].
---
```

**Rules:**

- `name` must be lowercase alphanumeric with hyphens
- `name` pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
- `name` length: 1-64 characters
- `description` is a single line, max 1024 characters
- `USE WHEN` keyword is recommended for activation

### Markdown Body

```markdown
# skill-name

[Brief description]

## Workflow Routing

| Workflow   | Trigger      | File                    |
| ---------- | ------------ | ----------------------- |
| **Create** | "create new" | `workflows/create.md` |

## Examples

**Example 1:**

User: "[Request]"
-> [Action taken]
-> [Result]
```

## Skill Loading

1. **Discovery**: OpenCode scans skill directories at startup
2. **Metadata**: Only YAML frontmatter loads initially
3. **Invocation**: Full SKILL.md body loads when agent calls skill
4. **Workflow Execution**: Additional files load on-demand

## Skill Locations

OpenCode searches these locations (in order):

1. `.opencode/skill/<name>/SKILL.md` (project)
2. `~/.config/opencode/skill/<name>/SKILL.md` (global)
3. `.claude/skills/<name>/SKILL.md` (Claude-compatible)
4. `~/.claude/skills/<name>/SKILL.md` (Claude-compatible global)

## Permission Control

In `opencode.json`:

```json
{
  "skill": {
    "allow": ["*"],
    "deny": ["internal-*"]
  }
}
```

- `allow` - immediate access
- `deny` - hidden from agents
- Patterns support wildcards
```

### Step 4.3: Create CreateSkill Skill

Create `.opencode/skill/create-skill/SKILL.md`:

```markdown
---
name: create-skill
description: Creates new skills following the standard structure. USE WHEN user wants to create a new skill OR add new capability OR needs a custom workflow.
---

# create-skill

Creates properly structured skills following the OpenCode Skills System specification.

## Workflow Routing

| Workflow   | Trigger                    | File                    |
| ---------- | -------------------------- | ----------------------- |
| **Create** | "create skill", "new skill" | `workflows/create.md` |

## Examples

**Example: Create a research skill**

```
User: "Create a skill for code review"
-> Creates .opencode/skill/code-review/SKILL.md
-> Adds proper YAML frontmatter with USE WHEN
-> Creates workflows/ and tools/ directories
-> Returns confirmation with skill path
```

## Skill Template

When creating a skill, use this template:

```markdown
---
name: skill-name
description: [Purpose]. USE WHEN [triggers].
---

# skill-name

[Description]

## Workflow Routing

| Workflow | Trigger | File |
| -------- | ------- | ---- |

## Examples

**Example:**

User: "[Request]"
-> [Process]
-> [Result]
```

## Naming Rules

- Lowercase alphanumeric only
- Hyphens allowed (not at start/end)
- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Length: 1-64 characters

**Valid:** `code-review`, `my-skill`, `api-client`
**Invalid:** `Code-Review`, `my_skill`, `--skill`
```

---

## Part 5: Documentation

### Step 5.1: Create Memory System Documentation

Create `.opencode/docs/MEMORYSYSTEM.md`:

```markdown
# OpenCode Memory System

Persistent memory architecture for maintaining context across sessions.

## Architecture

### Three-Tier Model

| Tier            | Temperature | Purpose                | Location          |
| --------------- | ----------- | ---------------------- | ----------------- |
| **CAPTURE**     | Hot         | Active work items      | `memory/work/`    |
| **SYNTHESIS**   | Warm        | Phase-based learnings  | `memory/learning/`|
| **APPLICATION** | Cold        | Historical archive     | `memory/sessions/`|

### CAPTURE (Hot)

Per-task memory stored in `work/[task-name_timestamp]/`:

- `work.md` - Goal, result, signal tracking
- `trace.jsonl` - Decision trace
- `output/` - Deliverables produced

### SYNTHESIS (Warm)

Learnings organized by cognitive phase:

- `observe/` - Context gathering insights
- `think/` - Hypothesis and analysis
- `plan/` - Execution planning
- `build/` - Construction learnings
- `execute/` - Implementation notes
- `verify/` - Validation results

### APPLICATION (Cold)

Long-term storage organized by date/category:

- `sessions/` - Session summaries
- `decisions/` - Architectural Decision Records
- `research/` - Research outputs
- `learnings/` - Permanent learning moments

## State Management

Active state tracked in `memory/state/`:

- `active-work.json` - Current task state
- `active-session.json` - Session info

## Signal Detection

Pattern detection in `memory/signals/`:

- `failures.jsonl` - Failure patterns
- `loopbacks.jsonl` - Retry patterns
- `patterns.jsonl` - Aggregated patterns

## Retention Policy

| Directory      | Retention       |
| -------------- | --------------- |
| `raw-outputs/` | 7 days          |
| `recovery/`    | 7 days          |
| `execution/`   | 30 days         |
| `sessions/`    | 90 days         |
| Others         | Permanent       |
```

### Step 5.2: Create Plugin System Documentation

Create `.opencode/docs/PLUGINSYSTEM.md`:

```markdown
# OpenCode Plugin System

Event-driven automation through TypeScript plugins.

## Plugin Structure

```typescript
import type { Plugin } from "@opencode-ai/plugin";

export const MyPlugin: Plugin = async ({ client, $ }) => {
  return {
    tool: {
      execute: {
        before: async (input, output) => {
          // Before tool execution
        },
        after: async (input, output) => {
          // After tool execution
        },
      },
    },
    event: async ({ event }) => {
      // Handle lifecycle events
    },
  };
};

export default MyPlugin;
```

## Available Hooks

### Tool Execution

- `before` - Execute before any tool runs
- `after` - Execute after tool completion

### Lifecycle Events

- `session.idle` - Session completed

## Configuration

In `opencode.json`:

```json
{
  "plugins": {
    "plugin-name": {
      "enabled": true
    }
  }
}
```

## Plugin Contexts

| Context  | Purpose                    |
| -------- | -------------------------- |
| `client` | OpenCode API access        |
| `$`      | Shell command execution    |
| `app`    | Application instance       |
| `event`  | Event stream data          |

## Installed Plugins

| Plugin               | Purpose                     |
| -------------------- | --------------------------- |
| `security-validator` | 10-tier command validation  |
| `session-manager`    | Session lifecycle handling  |
| `event-logger`       | Tool execution logging      |
| `context-loader`     | Context initialization      |

## Security Validator Tiers

1. Catastrophic (BLOCK) - rm -rf, disk destruction
2. Reverse Shells (BLOCK) - bash -i, netcat shells
3. Credential Theft (BLOCK) - curl|sh patterns
4. Prompt Injection (BLOCK) - instruction manipulation
5. Environment Manipulation (WARN) - API key access
6. Git Dangerous (WARN) - force push, hard reset
7. System Modification (LOG) - chmod, sudo
8. Network Operations (LOG) - ssh, scp
9. Data Exfiltration (BLOCK) - upload patterns
10. Infrastructure Protection (BLOCK) - rm .opencode
```

---

## Part 6: Agent Identity

### Step 6.1: Create config.yaml

Create `.opencode/config/config.yaml`:

```yaml
version: "1.0.0"
infrastructure:
  name: "OpenCode Cognitive Infrastructure"
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
  plugins: true
  mcp: true
```

### Step 6.2: Create Root AGENTS.md

Create `AGENTS.md` in agent root directory:

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

You operate within the OpenCode Cognitive Infrastructure:

- **Skills Framework** (`.opencode/skill/`): Modular domain expertise
- **Memory System** (`.opencode/memory/`): Persistent knowledge
- **Plugin System** (`.opencode/plugin/`): Event-driven automation
- **Configuration** (`opencode.json`): Runtime settings

## Memory Management

**CRITICAL:** Update work status after EVERY conversation turn to maintain continuity.

- Read relevant memories before starting work
- Update memories after significant interactions
- Keep work status current at `.opencode/memory/state/`

## Organization Context

<Organization description and relevant context>

---

_OpenCode Cognitive Infrastructure v1.0.0_
```

---

## Part 7: Gitignore Configuration

### Step 7.1: Create/Update .gitignore

Add to `.gitignore` in agent root:

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

### Step 7.2: Create .gitkeep Files

```bash
touch .opencode/memory/.gitkeep
touch .opencode/memory/state/.gitkeep
touch .opencode/memory/signals/.gitkeep
touch .opencode/memory/work/.gitkeep
touch .opencode/memory/learning/.gitkeep
```

---

## Part 8: Plugin Dependencies

### Step 8.1: Initialize Package.json (Optional)

If using npm for plugin dependencies:

```bash
cd .opencode/plugin
npm init -y
npm install @opencode-ai/plugin --save-dev
```

Or with bun:

```bash
cd .opencode/plugin
bun init -y
bun add @opencode-ai/plugin --dev
```

---

## Post-Implementation Checklist

After all files are created:

- [ ] Verify all directories exist
- [ ] Validate JSON syntax in opencode.json
- [ ] Validate YAML syntax in config.yaml
- [ ] Ensure plugin files have valid TypeScript syntax
- [ ] Verify skill names follow naming convention
- [ ] Verify AGENTS.md has been customized with agent identity
- [ ] Confirm .gitignore excludes sensitive data
- [ ] Test OpenCode can start in directory: `opencode`

---

## Next Phase

Proceed to **5_VERIFY.md** to verify the installation.
