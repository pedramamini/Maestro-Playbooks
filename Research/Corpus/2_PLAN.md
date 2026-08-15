# Document 2: Select the Next Batch

## Context

- **Playbook**: Corpus Synthesis
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}
- **Loop**: {{LOOP_NUMBER}}

## Purpose

Pick the next `[BATCH_SIZE]` items off the manifest and write a **self-contained
brief** for them. Document 3 must be able to do its whole job from
`LOOP_{{LOOP_NUMBER}}_BATCH.md` alone, without re-reading the manifest, the
config, or the agent prompt.

That is the point of this document: it pays the context cost of orientation
once, so the eight parallel workers downstream each start with exactly what they
need and nothing else.

## Tasks

### Task 1: Read state

- [ ] **Read `{{AUTORUN_FOLDER}}/CORPUS_MANIFEST.md` and
      `{{AUTORUN_FOLDER}}/CORPUS_CONFIG.md`.** Count items by status. Record
      `[BATCH_SIZE]` and `[ANALYTICAL_LENS]` from the config.

### Task 2: Select the batch

- [ ] **Take the next `[BATCH_SIZE]` items with status `PENDING`**, in manifest
      order. Do not reorder, do not cherry-pick interesting-looking titles —
      manifest order keeps coverage predictable and makes an interrupted run
      resumable.

      If fewer than `[BATCH_SIZE]` items are `PENDING`, take all of them.

      **If zero items are `PENDING`**: write
      `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_BATCH.md` containing only the
      marker `## BATCH_EMPTY` and a one-line reason, mark the remaining tasks in
      this document complete, and stop. This is the normal, expected end state —
      not an error. Document 3 will no-op and document 4 will run the final
      synthesis.

### Task 3: Write the batch brief

- [ ] **Write `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_BATCH.md`** with
      everything a worker needs, inlined:

      ```markdown
      # Batch — Loop {{LOOP_NUMBER}}

      **Analytical lens:** <the full [ANALYTICAL_LENS] text, verbatim>
      **Output folder:** <[OUTPUT_FOLDER]>
      **Items in this batch:** <n>
      **Corpus position:** items <first>-<last> of <total>

      ## Synopsis contract

      Every worker writes exactly one file to <OUTPUT_FOLDER>/<NNN>-<slug>.md
      with this shape:

      ---
      type: synopsis
      title: "<item title>"
      source: "<canonical URL or file path>"
      author: "<speaker / author, or unknown>"
      duration: "<if known>"
      corpus: "<corpus name>"
      created: {{DATE}}
      tags: [<3-6 topical tags, lowercase-hyphenated>]
      ---

      # <title>

      ## Thesis
      One paragraph. The single claim this item is making.

      ## Key points
      3-7 bullets. Each is a claim, not a topic.

      ## Evidence and specifics
      Concrete numbers, methods, named systems, dates. Cite them as stated.

      ## Notable quotes
      1-3 verbatim lines worth repeating, each attributed.

      ## Connections
      Wiki-links to other items in this corpus: [[NNN-slug]]. Only link to
      items you can see in <OUTPUT_FOLDER>; do not invent filenames.

      ## Items

      | # | Title | Raw file | Output filename |
      |---|-------|----------|-----------------|
      ...
      ```

      Inline the lens text in full. A worker that has to go read the agent prompt
      to find out what it is looking for has already lost the benefit of this
      document.

### Task 4: Note the plan

- [ ] **Report the batch**: one line — how many items this batch, how many
      remain `PENDING` after it, and the estimated loops to finish
      (`ceil(remaining / [BATCH_SIZE])`). This is the progress signal the user
      watches; give it every loop.
