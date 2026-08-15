# Document 5: Progress Gate

## Context

- **Playbook**: Corpus Synthesis
- **Agent**: {{AGENT_NAME}}
- **Working Folder**: {{AUTORUN_FOLDER}}
- **Loop**: {{LOOP_NUMBER}}

## Purpose

Decide whether to run another batch. **This is the only document with Reset ON**
— it controls loop continuation by resetting documents 0-4 when work remains.

## Decision Logic

```
IF CORPUS_MANIFEST.md does not exist:
    → Do NOT reset (pipeline just started, or it halted in document 0/1 — let
      the halt stand rather than looping on a broken config)

ELSE IF items with status PENDING exist:
    → Reset documents 0-4 (MORE BATCHES TO PROCESS)

ELSE IF CORPUS_MANIFEST.md does NOT contain "## EXTRACTION_COMPLETE":
    → Reset documents 0-4 (EXTRACTION WAS INTERRUPTED — RESUME IT)

ELSE IF SYNTHESIS.md does not exist in the output folder:
    → Reset documents 0-4 (ITEMS ARE DONE BUT THE FAN-IN NEVER RAN)

ELSE:
    → Do NOT reset (CORPUS COMPLETE — EXIT)
```

The middle two conditions are the ones that matter. A gate that only checks for
`PENDING` items exits the moment a batch empties — even if extraction never
finished, or the synthesis never ran. Both are silent failures that look
identical to success.

## Progress Check

- [ ] **Check progress and decide**: Read `{{AUTORUN_FOLDER}}/CORPUS_MANIFEST.md`
      and list `[OUTPUT_FOLDER]`. Apply the decision logic above. The loop
      CONTINUES if ANY of: `PENDING` items exist, the manifest lacks
      `## EXTRACTION_COMPLETE`, or `SYNTHESIS.md` is absent. The loop EXITS only
      when all three are satisfied: nothing pending, extraction complete,
      synthesis written.

## Reset Tasks (only if work remains)

- [ ] **Reset 0_CONFIGURE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/0_CONFIGURE.md`
- [ ] **Reset 1_EXTRACT.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/1_EXTRACT.md`
- [ ] **Reset 2_PLAN.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/2_PLAN.md`
- [ ] **Reset 3_PROCESS.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/3_PROCESS.md`
- [ ] **Reset 4_SYNTHESIZE.md**: Uncheck all tasks in `{{AUTORUN_FOLDER}}/4_SYNTHESIZE.md`

**IMPORTANT**: Only check these reset tasks if the progress check says CONTINUE.
Documents 0 and 1 both skip themselves on re-entry (0 sees `STATUS: READY`,
1 sees `## EXTRACTION_COMPLETE`), so resetting them is cheap — they cost one
file read each, not a re-run.

If the progress check says EXIT, leave every reset task unchecked.

## Status Table

Fill this in each loop so the run has a readable history:

| Loop | Processed this loop | Total processed | Pending | Decision |
|------|---------------------|-----------------|---------|----------|
| 1 | ___ | ___ | ___ | [CONTINUE / EXIT] |
| 2 | ___ | ___ | ___ | [CONTINUE / EXIT] |

## On Exit

- [ ] **Report the finished corpus (exit only)**: If the decision is EXIT, give
      the user a four-line close — items processed, items skipped or failed and
      why, the absolute path to `SYNTHESIS.md`, and the absolute path to
      `INDEX.md`. If anything was capped by `[MAX_ITEMS]`, say the number that
      was left unprocessed. A silent cap reads as full coverage.

## Manual Override

- **Force exit early**: leave all reset tasks unchecked. The synopses already
  written stay valid; re-running the playbook later resumes from the manifest.
- **Reprocess an item**: set its status back to `PENDING` in
  `CORPUS_MANIFEST.md`, delete `SYNTHESIS.md`, and re-run.
- **Start a fresh corpus over the same source**: delete `CORPUS_MANIFEST.md`,
  `CORPUS_CONFIG.md`, and `raw/`.
