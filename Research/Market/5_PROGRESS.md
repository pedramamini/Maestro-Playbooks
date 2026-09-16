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

1. **Integrity** - is the corpus actually queryable, or is it broken?
2. **Work remaining** - are there entities still worth researching, names still
   dangling, categories still uncovered, columns still thin?
3. **Budget** - has this run hit its ceiling?

Gating on coverage alone lets a run exit having produced a vault that fails its
next query, and lets a run with no natural stopping point continue until the max
loop count stops it arbitrarily.

## Instructions

1. **Read the agent prompt** for `[OUTPUT_FOLDER]`, `[MAX_ENTITIES]`, `[COVERAGE_TARGET]`
2. **Run the validator** and record the result
3. **Read `{{AUTORUN_FOLDER}}/BACKLOG.md`** and `{{AUTORUN_FOLDER}}/SWEEP_GAPS.md`
4. **Apply the decision logic** and append a row to `PROGRESS_LOG.md`
5. **If continuing**: check the four reset tasks
6. **If exiting**: leave them unchecked and run the finalization tasks

## Progress Check

- [ ] **Measure**: Run
      `cd [OUTPUT_FOLDER] && python3 Tools/health_check.py --json > /tmp/hc.json; echo exit=$?`
      then read `critical`, `budget_cards`, `lowest_coverage`, `relevance.mean`
      and the `0-29` band from the JSON. Also write the markdown report:
      `python3 Tools/health_check.py --report Resources/`. If the exit code is
      2, integrity is **unknown** (config error or missing PyYAML) - record
      that and treat it as continue-with-repair, never as clean. Subtract any
      CRITICAL issues whose exact text appears under `## KNOWN_ISSUES` in
      `RESEARCH_LOG.md`. Then count in `BACKLOG.md`: entries with `Status:
      PENDING`, entries with `Status: DISCOVERED`, whether
      `## ALL_CATEGORIES_COVERED` is present; and in `SWEEP_GAPS.md`: unchecked
      lines not marked `queued`. Append a row to
      `{{AUTORUN_FOLDER}}/PROGRESS_LOG.md` (create it with the header below if
      absent).

- [ ] **Decide**: Apply the decision logic below to the numbers you just
      recorded, write the decision and its reason in the `PROGRESS_LOG.md`
      row, and then either check the four reset tasks (CONTINUE) or leave
      them unchecked and work the finalization tasks (EXIT).

## Reset Tasks (only if continuing)

- [ ] **Reset 1_ANALYZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_ANALYZE.md`
- [ ] **Reset 2_DISCOVER.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_DISCOVER.md`
- [ ] **Reset 3_EVALUATE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_EVALUATE.md`
- [ ] **Reset 4_RESEARCH.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_RESEARCH.md`

**IMPORTANT**: Do not reset `0_CONFIGURE.md` or `0_INITIALIZE.md`. They run once.

## Decision Logic

```text
effective_critical = critical - (issues listed under KNOWN_ISSUES)
budget_left        = budget_cards < [MAX_ENTITIES]
work_waiting       = PENDING > 0  OR  DISCOVERED > 0  OR  unqueued gaps > 0
                     OR  ALL_CATEGORIES_COVERED absent
coverage_met       = lowest_coverage pct >= [COVERAGE_TARGET]
                     (or the vault has no cards yet)

IF validator exit code == 2:
    -> CONTINUE (REPAIR CONFIG - 4_RESEARCH fixes kb.yaml next loop)

ELSE IF effective_critical > 0:
    -> CONTINUE (REPAIR - fix the corpus before adding to it)

ELSE IF budget_left AND work_waiting:
    -> CONTINUE (RESEARCH)

ELSE IF NOT coverage_met:
    -> CONTINUE (SWEEP - budget is spent or backlog is empty; every remaining
                 loop is a breadth sweep until columns are filled)

ELSE:
    -> EXIT (DONE - finalize the vault)
```

Two guards against spinning:

- **Stalled repair.** If `effective_critical` has been greater than zero for
  three consecutive rows of `PROGRESS_LOG.md`, the repair is not converging.
  Copy the remaining CRITICAL issue texts under `## KNOWN_ISSUES` in
  `RESEARCH_LOG.md`, note it in the decision reason, and re-evaluate the logic
  without them.
- **Stalled coverage.** If `lowest_coverage` names the same field with the same
  percentage for three consecutive rows, the field cannot be filled from
  public sources. Add it to `coverage_exclude` for that type in `kb.yaml`, note
  it in the decision reason, and re-run the validator.

### Why the budget clause

Market research has no natural completion state. Discovery always surfaces one
more medium-importance company, so without an explicit ceiling the priority
ranking in `3_EVALUATE` never actually constrains anything and the run continues
until Max Loops stops it at a place determined by nothing in particular.

`MAX_ENTITIES` is counted from the vault - the validator's `budget_cards`
figure, which excludes categories - not from the plan. When the budget is
finite, the matrix decides what gets researched rather than merely what gets
researched first.

### Why integrity gates before budget

A vault with broken typed relations is not a smaller vault, it is a vault that
returns wrong answers. Fixing the corpus takes priority over growing it, and it
takes priority over the budget, because a clean small vault is useful and a
broken large one is not.

## PROGRESS_LOG.md Format

```markdown
# Progress Log

One row per loop. The mean relevance column is the drift signal: if it falls
loop over loop, the boundary is eroding and the run is quietly broadening into
the adjacent market.

| Loop | Date | Mode ran | Cards (budget) | PENDING | DISCOVERED | Gaps | Covered? | CRITICAL | Lowest coverage | Mean rel. | Below 30 | Decision | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-01-01 | DEPTH | 3 | 4 | 0 | 5 | no | 0 | company.employee_count 0% | 88.3 | 0 | CONTINUE | research |
```

`Mode ran` is read from the latest `RESEARCH_LOG.md` entry.

## Finalization Tasks (on exit only)

- [ ] **Final integrity check**: `cd [OUTPUT_FOLDER] && python3 Tools/health_check.py --fail-on critical`.
      If it exits 1 and the issues are not all under `KNOWN_ISSUES`, the vault
      is not finished - do not proceed to the remaining finalization tasks;
      uncheck this task's siblings and let the next loop repair.
- [ ] **Update INDEX.md**: every card in every entity folder linked under its
      section, counts in the statistics table, and the vault summary below
      appended
- [ ] **Build the event ledger**: if `kb.yaml` declares a `ledger` block,
      generate `Resources/[Event Class] Ledger.md` - a time-ordered table of
      every card carrying the ledger's state field, with state, date,
      counterparty and amount, terminal events separated from open ones
- [ ] **Write the market map**: `Resources/Market Map.md` - one section per
      Category card listing its products (from `Products/*.md` where
      `category:` matches) with their companies, so the comparison spine is
      readable in one page
- [ ] **Review the relevance queue**: list every card scoring below 30 in
      `Resources/Relevance Review.md` with its notes, so a human can decide
      whether it comes up or comes out
- [ ] **Note the gaps**: append to the vault summary the entities in
      `BACKLOG.md` still `PENDING` or `SKIP - MANUAL REVIEW`, the unqueued
      lines in `SWEEP_GAPS.md`, and any field that never reached coverage

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
| [DomainEntity] | [X] |
| **Total** | [X] |

### Corpus Health
- CRITICAL issues at exit: [X] ([N] known and documented)
- Mean relevance: [X] (loop 1: [X])
- Cards below 30 (review queue): [X] - see [[Relevance Review]]
- Lowest field coverage: [X]% ([type].[field])

### Where to start
- [[Market Map]] - every category and what sits in it
- [[SCOPE]] - the boundary this vault was built on
- [[REJECTIONS]] - what was deliberately left out, and why

### Known Gaps
[Entities that could not be researched, fields that stayed thin, and any
category where the target count was not met.]
```

## Manual Override

- **Force exit early:** leave all reset tasks unchecked
- **Continue past the budget:** raise `MAX_ENTITIES` in the agent prompt
- **Pause for review:** leave unchecked, inspect the vault, restart when ready

## Notes

- Depth builds cards, breadth connects them; the alternation is set by
  `SWEEP_EVERY` and becomes all-breadth once the budget is spent
- CRITICAL/HIGH entities before MEDIUM/LOW
- A clean small vault beats a broken large one
- The vault should be useful and navigable, not exhaustive
