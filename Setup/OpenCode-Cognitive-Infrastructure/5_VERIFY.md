# Phase 5: Verify Installation

## Objective

Verify the OpenCode Cognitive Infrastructure is correctly installed and functional.

## Verification Checklist

### 1. Directory Structure

Verify all directories exist:

- [ ] `.opencode/` directory exists
- [ ] `.opencode/config/` exists
- [ ] `.opencode/skill/core/` exists
- [ ] `.opencode/skill/create-skill/` exists
- [ ] `.opencode/plugin/` exists
- [ ] `.opencode/memory/` exists
- [ ] `.opencode/memory/state/` exists
- [ ] `.opencode/memory/signals/` exists
- [ ] `.opencode/memory/learning/` exists
- [ ] `.opencode/command/` exists
- [ ] `.opencode/agents/` exists
- [ ] `.opencode/docs/` exists

### 2. Core Files

Verify essential files are in place:

- [ ] `AGENTS.md` exists in agent root
- [ ] `opencode.json` exists in agent root
- [ ] `.opencode/VERSION` contains "1.0.0"
- [ ] `.opencode/config/config.yaml` exists and is valid YAML
- [ ] `.opencode/skill/core/SKILL.md` exists
- [ ] `.opencode/skill/create-skill/SKILL.md` exists

### 3. Plugin System

Verify plugins are properly configured:

- [ ] `.opencode/plugin/security-validator.ts` exists
- [ ] `.opencode/plugin/session-manager.ts` exists
- [ ] `.opencode/plugin/event-logger.ts` exists
- [ ] `.opencode/plugin/context-loader.ts` exists
- [ ] `opencode.json` references all plugins
- [ ] Plugin files have valid TypeScript syntax

### 4. Memory System

Verify memory files:

- [ ] `.opencode/memory/README.md` exists
- [ ] `.opencode/memory/state/active-work.json` exists
- [ ] `.opencode/memory/signals/README.md` exists
- [ ] Learning phase directories exist (observe, think, plan, build, execute, verify)

### 5. Skills System

Verify skill configuration:

- [ ] Skill names are lowercase with hyphens
- [ ] SKILL.md files have valid YAML frontmatter
- [ ] Core skill has `USE WHEN` in description
- [ ] `opencode.json` has skill permissions configured

### 6. Content Validation

#### AGENTS.md
- [ ] Contains agent name
- [ ] Contains persona name
- [ ] Contains mission statement
- [ ] Contains role description
- [ ] Contains memory management instructions

#### opencode.json
- [ ] Valid JSON syntax
- [ ] Has `$schema` reference
- [ ] Contains plugins configuration
- [ ] Contains skill permissions

#### core/SKILL.md
- [ ] Valid YAML frontmatter
- [ ] Name is lowercase (`core`)
- [ ] Description under 1024 characters
- [ ] Contains `USE WHEN` trigger

## Functional Testing

### Test 1: OpenCode Startup

```bash
opencode
```

**Expected**: OpenCode starts without errors and loads the agent context.

### Test 2: Skill Discovery

In OpenCode, ask: "What skills are available?"

**Expected**: OpenCode should list the core and create-skill skills.

### Test 3: Identity Check

Ask the agent: "Who are you?"

**Expected**: Agent should respond with its persona name, role, and purpose from AGENTS.md.

### Test 4: Memory Access

Ask the agent: "What's your current work status?"

**Expected**: Agent should read and report from `.opencode/memory/state/`.

### Test 5: Skill Invocation

Ask: "Use the core skill"

**Expected**: Agent should invoke the core skill and display identity information.

### Test 6: Plugin Verification

Run a safe shell command and check logs:

```bash
# After running a command in OpenCode, check:
cat .opencode/memory/raw-outputs/$(date +%Y-%m-%d).jsonl
```

**Expected**: Event logger should have recorded the command execution.

### Test 7: Security Validator

In OpenCode, attempt: "Run `rm -rf /`"

**Expected**: Security validator should BLOCK the command.

## Validation Commands

### Check Directory Structure

```bash
find .opencode -type d | head -20
```

### Validate JSON Files

```bash
# opencode.json
python3 -c "import json; json.load(open('opencode.json'))" && echo "Valid JSON"

# active-work.json
python3 -c "import json; json.load(open('.opencode/memory/state/active-work.json'))" && echo "Valid JSON"
```

### Check Skill Names

```bash
# Should all be lowercase with hyphens
ls -1 .opencode/skill/
```

### Verify Plugin Syntax

```bash
# If using TypeScript compiler
npx tsc --noEmit .opencode/plugin/*.ts

# Or with bun
bun check .opencode/plugin/*.ts
```

## Success Criteria

Installation is successful when:

1. All directories exist
2. All core files are present
3. Files contain valid content
4. OpenCode starts without errors
5. Agent responds correctly to identity queries
6. Skills are discoverable and invokable
7. Plugins are loaded and functional
8. Memory read/write operations work
9. Security validator blocks dangerous commands

## Troubleshooting

### OpenCode Won't Start

- Check `opencode.json` is valid JSON
- Verify plugin files have no syntax errors
- Check for conflicting configurations

### Skills Not Found

- Verify skill names are lowercase with hyphens
- Check SKILL.md has valid YAML frontmatter
- Ensure skill directories are in `.opencode/skill/`

### Plugins Not Loading

- Verify plugin exports default function
- Check plugin is enabled in `opencode.json`
- Look for TypeScript compilation errors

### Memory Not Updating

- Verify memory directory exists
- Check file permissions
- Ensure state files are valid JSON

### Identity Not Loading

- Verify AGENTS.md is in agent root (not in .opencode/)
- Check file permissions
- Ensure no syntax errors in markdown

## Post-Verification

Once verification passes:

1. **Document completion** - Note installation date in config.yaml
2. **Test knowledge packs** - Ready to install additional skills
3. **Customize as needed** - Add agent-specific context and skills
4. **Configure MCP servers** - Add external tool integrations

## Installation Complete

The OpenCode Cognitive Infrastructure is now installed and operational.

The agent has:

- Persistent memory across sessions
- Modular skill system with discovery
- Event-driven plugin automation
- Security validation on shell commands
- Complete identity configuration
- MCP integration capability

### Next Steps

1. Add **custom skills** for domain expertise
2. Configure **MCP servers** for external tools
3. Customize AGENTS.md with additional instructions
4. Add custom **plugins** for automation
5. Begin using the agent with full cognitive capabilities

---

_OpenCode Cognitive Infrastructure v1.0.0_
