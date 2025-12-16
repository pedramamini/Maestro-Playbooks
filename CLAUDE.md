# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains **playbooks for [Maestro](https://github.com/pedramamini/Maestro) Auto Run**. Playbooks automate multi-step code improvement workflows through looping document chains processed by AI agents.

## What is Maestro Auto Run?

Auto Run is Maestro's file-system-based task automation system that batch-processes markdown checklists through AI agents. Key characteristics:

- **Document-driven**: Each markdown file contains task checkboxes (`- [ ]`) that agents complete
- **Session isolation**: Each task executes in a fresh AI session with clean context
- **Loop support**: Playbooks can cycle back to the first document after completion
- **Reset on Completion**: Documents can auto-uncheck their tasks for repeatable execution

For more information, see the [Maestro documentation](https://github.com/pedramamini/Maestro).

## How Auto Run Playbooks Work

### Execution Flow

1. Maestro processes documents in order (1 -> 2 -> 3 -> 4 -> 5)
2. Each document's tasks run in isolated AI sessions
3. Document 5 (progress gate) evaluates exit conditions
4. If work remains, document 5 resets documents 1-4 and the loop continues
5. If exit conditions are met, document 5 does NOT reset, and the pipeline exits

### The Reset Mechanism

The loop control relies on selective resetting:
- **Documents 1-4**: `Reset: OFF` - They stay completed unless explicitly reset
- **Document 5**: `Reset: ON` - Always resets itself, conditionally resets 1-4

When document 5 checks its reset tasks:
- If reset tasks are checked -> Documents 1-4 get reset -> Loop continues
- If reset tasks are unchecked -> Nothing resets -> Pipeline exits

### Template Variables

Maestro substitutes these at runtime:

| Variable | Description |
|----------|-------------|
| `{{AGENT_NAME}}` | Name of the Maestro agent |
| `{{AGENT_PATH}}` | Root path of the target project |
| `{{AUTORUN_FOLDER}}` | Path to the Auto Run folder |
| `{{LOOP_NUMBER}}` | Current loop iteration (1, 2, 3...) |
| `{{DATE}}` | Today's date (YYYY-MM-DD) |
| `{{CWD}}` | Current working directory |
| `{{GIT_BRANCH}}` | Current git branch |

## Working with Playbooks

When editing playbooks:
- Preserve the markdown task checkbox format (`- [ ]`) as it drives automation
- Keep the Context section with `{{VARIABLE}}` placeholders intact
- Maintain document chain references (e.g., `LOOP_{{LOOP_NUMBER}}_PLAN.md`)
- Each playbook's README.md contains specific configuration details

### Critical Design Considerations

1. **One task per document step**: Each document should do ONE thing, then stop. This allows proper loop iteration.

2. **Session isolation awareness**: Each task runs in a fresh session. Don't rely on information from previous tasks being "remembered" - read it from generated files instead.

3. **Exit condition clarity**: Document 5 must have unambiguous logic for when to reset vs. when to exit.

4. **Incremental progress**: Playbooks should make small, verifiable changes per loop iteration rather than large batch changes.

See README.md for available playbooks and usage instructions.
