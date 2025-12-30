# Research Progress Gate

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Purpose

This document is the **progress gate** for the market research pipeline. It checks whether there are still entities to research and whether coverage targets have been met. **This is the only document with Reset ON** - it controls loop continuation by resetting tasks in documents 1-4 when more work is needed.

## Instructions

1. **Read the research plan** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. **Count entities by status** (PENDING vs RESEARCHED)
3. **Check coverage** against targets from market analysis
4. **Decide whether to continue or exit**
5. **If continuing**: Reset all tasks in documents 1-4
6. **If exiting**: Do NOT reset - finalize the vault

## Progress Check

- [ ] **Check progress and decide**: Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` and `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_ENTITIES.md`. The loop should CONTINUE (reset docs 1-4) if EITHER: (1) there are PENDING entities with CRITICAL or HIGH importance, OR (2) ENTITIES.md does NOT contain `## ALL_CATEGORIES_COVERED`. The loop should EXIT (do NOT reset) only when BOTH conditions are false: no PENDING CRITICAL/HIGH entities AND all categories are covered.

## Reset Tasks (Only if more research needed)

If the progress check determines we need to continue, reset all tasks in the following documents:

- [ ] **Reset 1_ANALYZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md`
- [ ] **Reset 2_DISCOVER.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_DISCOVER.md`
- [ ] **Reset 3_EVALUATE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md`
- [ ] **Reset 4_RESEARCH.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_RESEARCH.md`

**IMPORTANT**: Only reset documents 1-4 if there is work remaining (PENDING CRITICAL/HIGH entities OR unexplored categories). If all categories are covered AND all CRITICAL/HIGH entities are RESEARCHED, leave these reset tasks unchecked to allow the pipeline to exit.

## Decision Logic

```
IF LOOP_{{LOOP_NUMBER}}_PLAN.md doesn't exist:
    → Do NOT reset anything (PIPELINE JUST STARTED - LET IT RUN)

ELSE IF PENDING entities with CRITICAL or HIGH importance exist:
    → Reset documents 1-4 (CONTINUE TO RESEARCH PENDING ENTITIES)

ELSE IF LOOP_{{LOOP_NUMBER}}_ENTITIES.md does NOT contain "ALL_CATEGORIES_COVERED":
    → Reset documents 1-4 (CONTINUE TO DISCOVER MORE ENTITIES)

ELSE:
    → Do NOT reset anything (ALL CATEGORIES COVERED AND NO PENDING CRITICAL/HIGH - EXIT)
    → Finalize the vault (update INDEX.md, create summary)
```

**Key insight:** The loop should continue if EITHER:
1. There are PENDING entities with CRITICAL/HIGH importance to research, OR
2. There are still entity categories to discover (no `ALL_CATEGORIES_COVERED` marker)

## How This Works

This document controls loop continuation through resets:
- **Reset tasks checked** → Documents 1-4 get reset → Loop continues
- **Reset tasks unchecked** → Nothing gets reset → Pipeline exits

### Exit Conditions (Do NOT Reset)

Exit when ALL of these are true:
1. **Categories covered**: `LOOP_{{LOOP_NUMBER}}_ENTITIES.md` contains `## ALL_CATEGORIES_COVERED`
2. **No PENDING CRITICAL/HIGH**: All CRITICAL and HIGH importance entities are RESEARCHED or SKIP

Also exit if:
3. **Max Loops**: Hit the loop limit in Batch Runner

### Continue Conditions (Reset Documents 1-4)

Continue if EITHER is true:
1. There are PENDING entities with CRITICAL or HIGH importance in LOOP_{{LOOP_NUMBER}}_PLAN.md
2. `LOOP_{{LOOP_NUMBER}}_ENTITIES.md` does NOT contain `## ALL_CATEGORIES_COVERED` (more categories to discover)

## Current Status

Before making a decision, assess the vault:

| Metric | Value |
|--------|-------|
| **Total Entities Discovered** | ___ |
| **Entities Researched** | ___ |
| **PENDING (CRITICAL/HIGH)** | ___ |
| **PENDING (MEDIUM/LOW)** | ___ |
| **SKIP** | ___ |

### Coverage by Category

| Category | Target | Researched | Status |
|----------|--------|------------|--------|
| Companies | [X] | [Y] | [MET/BELOW] |
| Products | [X] | [Y] | [MET/BELOW] |
| People | [X] | [Y] | [MET/BELOW] |
| Technologies | [X] | [Y] | [MET/BELOW] |
| Trends | [X] | [Y] | [MET/BELOW] |

## Research History

Track progress across loops:

| Loop | Entities Researched | Total in Vault | Decision |
|------|---------------------|----------------|----------|
| 1 | ___ | ___ | [CONTINUE / EXIT] |
| 2 | ___ | ___ | [CONTINUE / EXIT] |
| ... | ... | ... | ... |

## Finalization Tasks (On Exit Only)

If exiting, perform these finalization tasks:

- [ ] **Update INDEX.md**: Ensure all researched entities are linked
- [ ] **Create vault summary**: Add research statistics to INDEX.md
- [ ] **Review connections**: Check that inter-page links are working
- [ ] **Note gaps**: Document any entities that couldn't be researched

## Vault Summary Template

Add to INDEX.md on exit:

```markdown
## Research Summary

**Research Period:** [Start Date] - {{DATE}}
**Total Loops:** {{LOOP_NUMBER}}
**Agent:** {{AGENT_NAME}}

### Coverage Statistics
| Category | Count |
|----------|-------|
| Companies | [X] |
| Products | [X] |
| People | [X] |
| Technologies | [X] |
| Trends | [X] |
| **Total Entities** | [X] |

### Research Notes
[Any important notes about coverage gaps or limitations]
```

## Manual Override

**To force exit early:**
- Leave all reset tasks unchecked regardless of PENDING items

**To continue despite meeting targets:**
- Check the reset tasks to keep researching

**To pause for review:**
- Leave unchecked
- Review the vault contents
- Restart when ready

## Notes

- This playbook focuses on building breadth first, then depth
- CRITICAL/HIGH entities should be researched before expanding to MEDIUM/LOW
- Quality of research matters more than hitting exact coverage numbers
- The vault should be useful and navigable, not exhaustive
