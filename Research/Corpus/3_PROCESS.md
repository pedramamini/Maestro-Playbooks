# Document 3: Fan Out — Process the Batch

## Context

- **Playbook**: Corpus Synthesis
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}
- **Loop**: {{LOOP_NUMBER}}

## Purpose

Run one subagent per item in this loop's batch, concurrently, each with
**identical instructions** and one transcript.

This is the throughput step. Nothing here requires cross-item reasoning — that
is document 4's job — so nothing here should be serialized, and nothing here
needs your most expensive model.

## Tasks

### Task 1: Read the batch brief

- [ ] **Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_BATCH.md`.** This is the
      only file you need. Do not re-read the manifest or the agent prompt.

- [ ] **Handle the empty batch**: if the brief contains `## BATCH_EMPTY`, there
      is nothing to process. Mark every remaining task in this document complete
      without doing anything and stop. Do not treat this as a failure and do not
      report it as one.

### Task 2: Fan out

- [ ] **Dispatch one subagent per item in the batch, in a single parallel
      dispatch.** Each subagent gets:

      - the path to its **one** raw transcript,
      - the **verbatim** analytical lens from the brief,
      - the **verbatim** synopsis contract from the brief,
      - its assigned output filename.

      Each subagent does not get: the other items, the manifest, the corpus
      config, or this document. Isolation is the feature — it keeps every
      worker's context small and stops one long transcript from crowding out
      another's.

      **Model choice:** this is extraction, not reasoning. Send the workers to a
      fast model. Keep the expensive model for document 4, where the
      cross-cutting work happens.

      Instruct each worker to **read its transcript in full** before writing.
      A synopsis derived from the first two thousand words of a thirty-minute
      talk is the specific failure this playbook exists to avoid.

### Task 3: Verify the output exists

- [ ] **Confirm each expected file landed**: list `[OUTPUT_FOLDER]` and check
      for every filename the brief assigned. Check the bytes, not just the name —
      a zero-byte or stub file is a failure, not a success.

      Do not take a worker's word for it. A subagent reporting "done" is not
      evidence that a file exists; the file existing is the evidence.

### Task 4: Update the manifest

- [ ] **Write the results back to `{{AUTORUN_FOLDER}}/CORPUS_MANIFEST.md`**:
      for each item in the batch set the status to `PROCESSED` and fill the
      `Synopsis` column with the output filename. For any item whose file is
      missing or empty, set `FAILED` with a one-line reason.

      An item that fails twice across loops should be set to `SKIP` with the
      reason — retrying a transcript that does not parse forever is how a loop
      stops converging.

### Task 5: Report

- [ ] **One line**: items processed this loop, items failed, items remaining
      `PENDING`.
