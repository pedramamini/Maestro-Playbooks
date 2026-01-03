# Verify Infrastructure Installation

## Context
- **Playbook:** Claude Cognitive Infrastructure Setup
- **Agent:** Test Cognitive Infrastructure Agent
- **Target:** /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent
- **Auto Run Folder:** /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/autorun
- **Date:** 2026-01-03

## Purpose

Run testable verification procedures to confirm the Claude Cognitive Infrastructure was deployed correctly. This is the final quality gate before the playbook completes.

## Verification Checklist

- [x] **Verify directory structure**: Check that all required directories exist at `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent`:
      **Result:** All 11 directories exist - PASS
      ```
      Required directories:
      - .claude/
      - .claude/hooks/
      - .claude/hooks/lib/
      - .claude/skills/
      - .claude/skills/CORE/
      - .claude/context/
      - .claude/context/memory/
      - .claude/context/history/
      - .claude/context/history/sessions/
      - .claude/agents/
      - .claude/config/
      ```

      For each directory: EXISTS / MISSING

- [x] **Verify core files exist**: Check that all required files exist:
      **Result:** All 5 files exist - PASS
      ```
      Required files:
      - /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/CLAUDE.md
      - /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/.claude/settings.json
      - /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/.claude/skills/CORE/SKILL.md
      - /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/.claude/context/memory/learnings.md
      - /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/.claude/context/memory/user_preferences.md
      ```

      For each file: EXISTS / MISSING

- [x] **Verify hooks deployed**: Check that all hook files exist and are executable:
      **Result:** All 9 hooks exist, 7 main hooks are executable, 2 lib files exist - PASS
      ```
      Required hooks:
      - .claude/hooks/security-validator.ts
      - .claude/hooks/initialize-session.ts
      - .claude/hooks/load-core-context.ts
      - .claude/hooks/update-tab-titles.ts
      - .claude/hooks/capture-all-events.ts
      - .claude/hooks/capture-session-summary.ts
      - .claude/hooks/stop-hook.ts
      - .claude/hooks/lib/observability.ts
      - .claude/hooks/lib/metadata-extraction.ts
      ```

      For each hook: EXISTS + EXECUTABLE / MISSING / NOT EXECUTABLE

- [x] **Verify settings.json valid**: Parse `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/.claude/settings.json`:
      **Result:** Valid JSON with all required hook configurations - PASS
      - Is valid JSON? YES / NO
      - Has "hooks" key? YES / NO
      - Has PreToolUse configured? YES / NO
      - Has SessionStart configured? YES / NO
      - Has Stop configured? YES / NO

- [x] **Verify CLAUDE.md content**: Read `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/CLAUDE.md` and check:
      **Result:** Contains agent name, persona, responsibilities, system architecture, and memory management - PASS
      - Contains agent name? YES / NO
      - Contains persona? YES / NO
      - Contains responsibilities? YES / NO
      - Contains system architecture section? YES / NO
      - Contains memory management section? YES / NO

- [x] **Verify SKILL.md content**: Read `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/.claude/skills/CORE/SKILL.md` and check:
      **Result:** Has YAML frontmatter, USE WHEN directive, and core identity section - PASS
      - Has YAML frontmatter? YES / NO
      - Has "USE WHEN" in description? YES / NO
      - Has core identity section? YES / NO

- [x] **Test security validator (optional)**: If bun is available, test the security validator:
      **Result:** SKIPPED - Bun runtime not installed. Hooks use Bun-specific APIs.
      ```bash
      echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | bun /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/.claude/hooks/security-validator.ts
      ```
      Expected: Exit code 0 (command allowed)

      ```bash
      echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | bun /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/.claude/hooks/security-validator.ts
      ```
      Expected: Exit code 2 (command blocked)

- [x] **Create verification report**: Write `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/autorun/VERIFICATION_REPORT.md`:
      **Result:** Report created with detailed verification results - COMPLETE

      ```markdown
      # Verification Report

      **Completed:** 2026-01-03 [current time]
      **Target:** /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent
      **Agent:** [Agent Name]

      ## Summary

      | Category | Status |
      |----------|--------|
      | Directory Structure | PASS / FAIL |
      | Core Files | PASS / FAIL |
      | Hooks | PASS / FAIL |
      | settings.json | PASS / FAIL |
      | CLAUDE.md | PASS / FAIL |
      | SKILL.md | PASS / FAIL |
      | Security Test | PASS / FAIL / SKIPPED |

      ## Overall Status

      **INSTALLATION: SUCCESSFUL / FAILED**

      ## Details

      ### Directory Structure
      [List each directory and status]

      ### Core Files
      [List each file and status]

      ### Hooks
      [List each hook and status]

      ### Issues Found
      [None / List issues]

      ## Next Steps

      If SUCCESSFUL:
      1. Navigate to agent directory: `cd /Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent`
      2. Start Claude Code: `claude`
      3. Security validation and history capture are now active

      If FAILED:
      [List remediation steps]

      ---
      *Verification completed by Claude Cognitive Infrastructure Setup Playbook*
      ```

- [x] **Finalize setup log**: Append final status to `/Users/stephanchenette/Documents/Agents/Maestro/Test Cognitive Infrastructure Agent/autorun/SETUP_LOG.md`:
      **Result:** Setup log updated with completion status - COMPLETE

      ```markdown
      - [x] 5_VERIFY - Installation verified
        - Directories: [X/Y passed]
        - Files: [X/Y passed]
        - Hooks: [X/Y passed]
        - Overall: SUCCESSFUL / FAILED

      ## Completion

      **Finished:** 2026-01-03 [current time]
      **Status:** SUCCESSFUL / FAILED
      **Report:** VERIFICATION_REPORT.md

      ---
      *Claude Cognitive Infrastructure Setup Complete*
      ```

## How to Know You're Done

This task is complete when:
1. All verification checks have been run
2. VERIFICATION_REPORT.md has been created with results
3. SETUP_LOG.md has been finalized
4. Overall status is clearly reported (SUCCESSFUL or FAILED)

## Success Criteria

Installation is SUCCESSFUL if:
- All directories exist
- All core files exist
- All hooks exist and are executable
- settings.json is valid
- CLAUDE.md contains required content
- SKILL.md contains required content

Installation is FAILED if:
- Any required directory is missing
- Any required file is missing
- Hooks are not executable
- settings.json is invalid
- Critical content is missing from CLAUDE.md or SKILL.md
