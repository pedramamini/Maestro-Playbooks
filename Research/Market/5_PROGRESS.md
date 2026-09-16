# Research Progress Gate

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Purpose

The **progress gate**. It decides whether the pipeline continues or exits, and
it is the only document with Reset ON - it controls loop continuation by
resetting documents 1-4 when more work remains.

It gates on three things, not one:

1. **Work remaining** - are there entities still worth researching?
2. **Budget** - has this run hit its ceiling?
3. **Integrity** - is the corpus actually queryable, or is it broken?

Gating on coverage alone lets a run exit having produced a vault that fails its
next query, and lets a run with no natural stopping point continue until the max
loop count stops it arbitrarily.

## Instructions

1. **Read the research plan** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
2. **Read `{{AUTORUN_FOLDER}}/MARKET_CONFIG.md`** for `MAX_ENTITIES`
3. **Run the validator** and record the result
4. **Count entities and check coverage**
5. **Decide: continue or exit**
6. **If continuing**: reset documents 1-4
7. **If exiting**: do NOT reset - finalize the vault

## Progress Check

- [ ] **Run the integrity check**: Execute
      `cd [OUTPUT_FOLDER] && python3 Tools/health_check.py --report Resources/`
      and record the CRITICAL count, the relevance distribution and the mean
      relevance. If PyYAML is unavailable, note it and treat integrity as
      unknown rather than clean.

- [ ] **Check progress and decide**: Read
      `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md` and
      `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_ENTITIES.md`. Apply the decision
      logic below. The loop CONTINUES (reset docs 1-4) if there is work
      remaining AND the budget is not exhausted, OR if the corpus has CRITICAL
      integrity issues. The loop EXITS only when the work is done or the budget
      is spent AND the corpus is clean.

## Reset Tasks (only if continuing)

- [ ] **Reset 1_ANALYZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md`
- [ ] **Reset 2_DISCOVER.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_DISCOVER.md`
- [ ] **Reset 3_EVALUATE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md`
- [ ] **Reset 4_RESEARCH.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_RESEARCH.md`

**IMPORTANT**: Do not reset `0_CONFIGURE.md` or `0_INITIALIZE.md`. They run once.

## Decision Logic

```text
IF LOOP_{{LOOP_NUMBER}}_PLAN.md does not exist:
    -> Do NOT reset (PIPELINE JUST STARTED - LET IT RUN)

ELSE IF health_check.py reports CRITICAL issues:
    -> Reset documents 1-4 (FIX THE CORPUS BEFORE ADDING TO IT)
    -> Note the issues so 4_RESEARCH addresses them next loop

ELSE IF entities researched >= [MAX_ENTITIES]:
    -> Do NOT reset (BUDGET EXHAUSTED - EXIT AND FINALIZE)

ELSE IF PENDING entities with CRITICAL or HIGH importance exist:
    -> Reset documents 1-4 (CONTINUE RESEARCHING)

ELSE IF any tracked field is below 90% coverage:
    -> Reset documents 1-4 (CONTINUE SWEEPING)

ELSE IF LOOP_{{LOOP_NUMBER}}_ENTITIES.md lacks "ALL_CATEGORIES_COVERED":
    -> Reset documents 1-4 (CONTINUE DISCOVERING)

ELSE:
    -> Do NOT reset (DONE - FINALIZE THE VAULT)
```

### Why the budget clause

Market research has no natural completion state. Discovery always surfaces one
more medium-importance company, so without an explicit ceiling the priority
ranking in `3_EVALUATE` never actually constrains anything and the run continues
until Max Loops stops it at a place determined by nothing in particular.

`MAX_ENTITIES` makes the ranking do its job: when the budget is finite, the
matrix decides what gets researched rather than merely what gets researched
first.

### Why integrity gates before budget

A vault with broken typed relations is not a smaller vault, it is a vault that
returns wrong answers. Fixing the corpus takes priority over growing it, and it
takes priority over the budget, because a clean small vault is useful and a
broken large one is not.

## Current Status

| Metric | Value |
|--------|-------|
| **Total Entities Discovered** | ___ |
| **Entities Researched** | ___ / [MAX_ENTITIES] |
| **PENDING (CRITICAL/HIGH)** | ___ |
| **PENDING (MEDIUM/LOW)** | ___ |
| **SKIP** | ___ |
| **Declined as out of scope** | ___ |

### Corpus Integrity

| Check | Value |
|-------|-------|
| CRITICAL issues | ___ |
| MEDIUM issues | ___ |
| Lowest field coverage | ___ % (`field name`) |

### Scope Health

The mean relevance is the drift signal. If it falls loop over loop, the boundary
is eroding and the run is quietly broadening into the adjacent market. Say so
explicitly in the exit summary rather than letting it pass unremarked.

| Band | Cards |
|------|-------|
| 90-100 | ___ |
| 70-89 | ___ |
| 50-69 | ___ |
| 30-49 | ___ |
| 0-29 | ___ |
| **Mean this loop** | ___ |
| **Mean previous loop** | ___ |

### Coverage by Category

| Category | Target | Researched | Status |
|----------|--------|------------|--------|
| Companies | [X] | [Y] | [MET/BELOW] |
| Products | [X] | [Y] | [MET/BELOW] |
| Categories | [X] | [Y] | [MET/BELOW] |
| People | [X] | [Y] | [MET/BELOW] |
| Capital | [X] | [Y] | [MET/BELOW] |

## Research History

| Loop | Mode | Researched | Total | CRITICAL | Mean relevance | Decision |
|------|------|-----------|-------|----------|----------------|----------|
| 1 | ___ | ___ | ___ | ___ | ___ | [CONTINUE/EXIT] |

## Finalization Tasks (on exit only)

- [ ] **Final integrity check**: `python3 Tools/health_check.py --fail-on critical`.
      If it fails, the vault is not finished - do not proceed to the remaining
      finalization tasks.
- [ ] **Update INDEX.md**: every researched entity linked
- [ ] **Write the vault summary**: statistics into `INDEX.md`
- [ ] **Build the event ledger**: if `kb.yaml` declares a `ledger` block,
      generate the time-ordered rollup into `Resources/`
- [ ] **Review the relevance queue**: list every card scoring below 30 so a
      human can decide whether it comes up or comes out
- [ ] **Note the gaps**: entities that could not be researched, and fields that
      never reached coverage

## Vault Summary Template

Add to `INDEX.md` on exit:

```markdown
## Research Summary

**Period:** [start] - {{DATE}}
**Loops:** {{LOOP_NUMBER}}
**Agent:** {{AGENT_NAME}}

### Scope
- **IN:**  [SCOPE_IN]
- **OUT:** [SCOPE_OUT]
- Scope pair was: [user-configured | agent-proposed and unreviewed]

### Coverage
| Entity Type | Count |
|-------------|-------|
| Companies | [X] |
| Products | [X] |
| Categories | [X] |
| People | [X] |
| Capital | [X] |
| **Total** | [X] |

### Corpus Health
- CRITICAL issues at exit: [X]
- Mean relevance: [X]
- Cards below 30 (review queue): [X]
- Lowest field coverage: [X]% ([field])

### Known Gaps
[Entities that could not be researched, fields that stayed thin, and any
category where the target count was not met.]
```

## Manual Override

- **Force exit early:** leave all reset tasks unchecked
- **Continue past the budget:** raise `MAX_ENTITIES` in the agent prompt, or
  check the reset tasks manually
- **Pause for review:** leave unchecked, inspect the vault, restart when ready

## Notes

- Breadth first, then depth. `DEPTH_SWITCH_AT` controls the changeover
- CRITICAL/HIGH entities before MEDIUM/LOW
- A clean small vault beats a broken large one
- The vault should be useful and navigable, not exhaustive
