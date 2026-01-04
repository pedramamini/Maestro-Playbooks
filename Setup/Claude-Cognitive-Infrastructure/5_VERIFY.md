# Phase 5: Verify Installation

## Objective

Verify the Claude Cognitive Infrastructure is correctly installed and functional.

## Verification Checklist

### 1. Directory Structure

Verify all directories exist:

- [ ] `.claude/` directory exists
- [ ] `.claude/config/` exists
- [ ] `.claude/skills/CORE/` exists
- [ ] `.claude/context/` exists
- [ ] `.claude/context/memory/` exists
- [ ] `.claude/hooks/` exists
- [ ] `.claude/agents/` exists
- [ ] `.claude/scripts/` exists
- [ ] `.claude/examples/` exists

### 2. Core Files

Verify essential files are in place:

- [ ] `CLAUDE.md` exists in agent root
- [ ] `.claude/VERSION` contains "1.1.0"
- [ ] `.claude/settings.json` exists and is valid JSON
- [ ] `.claude/config/config.yaml` exists and is valid YAML
- [ ] `.claude/skills/CORE/SKILL.md` exists

### 3. Memory System

Verify memory files:

- [ ] `.claude/context/memory/learnings.md` exists
- [ ] `.claude/context/memory/user_preferences.md` exists
- [ ] `.claude/context/memory/work_status.md` exists

### 4. Content Validation

#### CLAUDE.md
- [ ] Contains agent name
- [ ] Contains persona name
- [ ] Contains mission statement
- [ ] Contains role description
- [ ] Contains memory management instructions
- [ ] Contains "Update work_status.md after EVERY conversation turn"

#### settings.json
- [ ] Valid JSON syntax
- [ ] Contains hooks configuration
- [ ] Contains permissions

#### CORE/SKILL.md
- [ ] Valid YAML frontmatter
- [ ] Contains triggers
- [ ] Has priority of 100
- [ ] Has context_budget defined

## Functional Testing

### Test 1: Identity Check
Ask the agent: "Who are you?"

**Expected**: Agent should respond with its persona name, role, and purpose.

### Test 2: Memory Access
Ask the agent: "What's in your work status?"

**Expected**: Agent should read and report from `.claude/context/memory/work_status.md`.

### Test 3: Memory Update
Ask the agent to add a task to work status.

**Expected**: Agent should update `.claude/context/memory/work_status.md`.

### Test 4: Skill Activation
Ask: "What can you do?"

**Expected**: Agent should describe its capabilities based on CORE skill.

## Success Criteria

Installation is successful when:

1. All directories exist
2. All core files are present
3. Files contain valid content
4. Agent responds correctly to identity queries
5. Memory read/write operations work

## Troubleshooting

### Missing Directories
Re-run the mkdir command from Step 1 of implementation.

### Invalid JSON/YAML
Check for syntax errors:
- Trailing commas in JSON
- Incorrect indentation in YAML
- Missing quotes around strings

### Identity Not Loading
- Verify CLAUDE.md is in agent root (not in .claude/)
- Check file permissions
- Ensure no syntax errors in markdown

### Memory Not Updating
- Verify memory directory exists
- Check file permissions
- Ensure files are not locked

## Post-Verification

Once verification passes:

1. **Document completion** - Note installation date in config.yaml
2. **Test knowledge packs** - Ready to install additional knowledge packs
3. **Customize as needed** - Add agent-specific context and skills

## Installation Complete

The Claude Cognitive Infrastructure is now installed and operational.

The agent has:
- Persistent memory across sessions
- Modular skill system
- Structured context management
- Event-driven hooks capability
- Complete identity configuration

### Next Steps

1. Run **Knowledge Pack** playbooks to add domain expertise
2. Customize CLAUDE.md with additional instructions
3. Add custom hooks for automation
4. Begin using the agent

---

*Claude Cognitive Infrastructure v1.1.0*
