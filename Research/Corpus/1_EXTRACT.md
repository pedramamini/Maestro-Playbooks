# Document 1: Bulk Extraction

## Context

- **Playbook**: Corpus Synthesis
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}
- **Loop**: {{LOOP_NUMBER}}

## Purpose

Get **every** item into plain text, once, up front. Then write the manifest that
every later document reads.

This is the cheap, boring, mechanical half of the pipeline. It is deliberately
separated from analysis: extraction is I/O-bound and dumb, synopsis writing is
token-bound and smart, and mixing them means re-downloading things you already
have every time a loop resets.

**This document is a no-op on every loop after the first.** Extraction happens
once per corpus.

## Tasks

### Task 1: Skip if extraction is already done

- [ ] **Check the manifest**: If `{{AUTORUN_FOLDER}}/CORPUS_MANIFEST.md` exists
      and contains the marker `## EXTRACTION_COMPLETE`, extraction has already
      run. Mark every remaining task in this document complete without doing
      anything and stop.

      If the manifest exists **without** that marker, extraction was interrupted.
      Resume it: read the manifest, and extract only the items whose status is
      `NOT_EXTRACTED`.

### Task 2: Read the configuration

- [ ] **Read `{{AUTORUN_FOLDER}}/CORPUS_CONFIG.md`** for the resolved corpus
      kind, `[CORPUS_SOURCE]`, `[OUTPUT_FOLDER]`, `[MAX_ITEMS]`, and any recorded
      toolchain degradations.

### Task 3: Extract to plain text

- [ ] **Run the extraction for the resolved kind** into
      `{{AUTORUN_FOLDER}}/raw/`. Use one file per item, named
      `NNN-slug.txt` with a zero-padded ordinal so the natural sort is stable.

      **`youtube-playlist`** — pull auto-generated subtitles for the whole
      playlist in one command, then strip VTT timing to clean text:

      ```bash
      mkdir -p "{{AUTORUN_FOLDER}}/raw"
      yt-dlp --skip-download --write-auto-sub --write-sub --sub-lang en \
             --sub-format vtt --write-info-json --ignore-errors \
             -o "{{AUTORUN_FOLDER}}/raw/%(playlist_index)03d-%(title)s.%(ext)s" \
             "<CORPUS_SOURCE>"
      ```

      Then convert each `.vtt` to `.txt`: drop the `WEBVTT` header, timing lines,
      and cue settings; collapse the duplicate rolling-caption lines that
      auto-subs emit; keep sentence flow. Retain each `.info.json` — it carries
      the title, duration, uploader, and canonical URL you need for front matter.

      **`url-list` / `single-url` / `opml`** — read the URLs, fetch each page,
      convert to markdown/text. For `opml`, parse the `xmlUrl` attributes, fetch
      each feed, and treat every entry as an item. Fetch politely: sequential,
      not a burst.

      **`local-files`** — walk the directory. `.md`/`.txt` copy through;
      `.pdf` via `pdftotext -layout`; `.docx` via `pandoc -t plain`. If a
      converter was recorded as missing in `CORPUS_CONFIG.md`, mark those items
      `SKIP` with the reason rather than failing.

      Honour `[MAX_ITEMS]`: if it is a number, stop after that many items and
      record how many were left untouched. **Say the number out loud** — a
      silent cap reads as full coverage when it is not.

### Task 4: Handle the empty corpus

- [ ] **Refuse to continue on an empty extraction**: If zero items were
      extracted, do not write an `EXTRACTION_COMPLETE` manifest and do not let
      the pipeline loop on nothing.

      Write a **halt marker** into this document, directly below this
      task: an HTML comment whose entire body is

      ```text
      maestro:halt: Extraction produced zero items. Check CORPUS_SOURCE.
      ```

      The marker is described rather than shown, because a literal one sitting
      in this file would halt the playbook the moment the document is read.

      Leave this task unchecked, and in your final message state exactly what was
      attempted (the command run, the source string, the error output) and the
      two likeliest causes: a private/region-locked playlist, or a path that
      resolved to an empty directory. Remind the user to delete the halt marker
      before re-running.

### Task 5: Write the manifest

- [ ] **Write `{{AUTORUN_FOLDER}}/CORPUS_MANIFEST.md`** as the single source of
      truth for the rest of the run. One row per item:

      ```markdown
      # Corpus Manifest

      **Source:** <CORPUS_SOURCE>
      **Kind:** <resolved kind>
      **Extracted:** {{DATE}}
      **Items:** <n extracted> of <n discovered>  <!-- state the cap if one applied -->

      | # | Title | Raw file | Bytes | Status | Synopsis |
      |---|-------|----------|-------|--------|----------|
      | 001 | ... | raw/001-....txt | 48213 | PENDING | |
      | 002 | ... | raw/002-....txt | 0 | SKIP (no transcript) | |
      ```

      Status values: `PENDING`, `PROCESSED`, `FAILED`, `SKIP`. Anything that
      extracted to zero bytes starts as `SKIP` with the reason inline — a
      transcript that does not exist is not a failure to retry forever.

- [ ] **Append the completion marker**: add a final line reading exactly
      `## EXTRACTION_COMPLETE` to the manifest. Document 5 reads this marker to
      decide whether discovery is exhausted, so it must be present and exact.

- [ ] **Report the extraction**: one line — items discovered, items extracted,
      items skipped and why, total bytes. Not a table, not a preamble.
