# Analyze Agent Configuration

## Context
- **Playbook:** Claude Cognitive Infrastructure Setup
- **Agent:** Test Cognitive Infrastructure Agent
- **Target:** /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent
- **Auto Run Folder:** /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/autorun
- **Date:** 2026-01-03

## Purpose

Derive agent configuration from the target directory. This step automatically extracts the agent name from the directory path and generates appropriate defaults. No user prompting required.

## Configuration Checklist

- [x] **Derive agent configuration**: Extract configuration from the target directory path `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent`:

> **Completed 2026-01-02 19:26:** Configuration derived successfully. Agent name "Test Cognitive Infrastructure Agent" extracted from directory path. Default persona "Sam Riley" applied. Responsibilities derived from "Test" and "Infrastructure" keywords. AGENT_CONFIG.md created at `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/autorun/AGENT_CONFIG.md`.

      **Agent Name:**
      - Extract the directory name from `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent`
      - Use the last component of the path as the agent name
      - Example: `/Users/me/Agents/Research Assistant Agent` → "Research Assistant Agent"

      **Agent Persona:**
      - Use default: "Sam Riley"
      - This is a generic, forgettable office-type name

      **Responsibilities:**
      - Derive from agent name if it contains keywords:
        - "Research" → "Conduct research, analyze findings, synthesize information"
        - "Assistant" → "Assist with tasks, provide guidance, maintain context"
        - "Development" or "Engineer" → "Support development workflows, code review, documentation"
        - "Operations" → "Track processes, coordinate activities, maintain documentation"
      - Default: "A general-purpose assistant that helps with tasks, research, and coordination."

      **Organization:**
      - Default: (blank - no organization specified)

      Save all derived information to `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/autorun/AGENT_CONFIG.md`

## Agent Configuration Template

Create `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/autorun/AGENT_CONFIG.md` with:

```markdown
# Agent Configuration

**Derived:** 2026-01-03 [current time]
**Target Directory:** /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent

## Identity

**Agent Name:** [extracted from directory name]
**Agent Persona:** Sam Riley
**Organization:** (none specified)

## Responsibilities

[derived from agent name keywords, or default generic responsibilities]

## Derivation Notes

- Agent name extracted from: [last path component]
- Persona: Default (Sam Riley)
- Responsibilities: [Derived from keywords / Default]
- Organization: Not specified

## Configuration Status

- [x] Agent name derived
- [x] Persona set (default)
- [x] Responsibilities derived
- [x] Organization set (blank)

---

*Configuration ready for infrastructure planning*
```

## How to Know You're Done

This task is complete when:
1. Agent name has been extracted from the directory path
2. Default persona "Sam Riley" has been set
3. Responsibilities have been derived or defaulted
4. AGENT_CONFIG.md exists with all fields populated

## Update Setup Log

Append to `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/autorun/SETUP_LOG.md`:

```markdown
- [x] 1_ANALYZE - Agent configuration derived
  - Name: [agent name from directory]
  - Persona: Sam Riley (default)
  - Organization: none
```
