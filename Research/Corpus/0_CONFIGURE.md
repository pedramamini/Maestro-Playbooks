# Document 0: Validate Configuration and Preflight

## Context

- **Playbook**: Corpus Synthesis
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}
- **Loop**: {{LOOP_NUMBER}}

## Purpose

Fail fast and loudly **before** spending a single token on extraction.

The two ways this playbook wastes a user's afternoon are (1) running against an
unedited example value and (2) discovering on item 40 of 60 that the extraction
tool was never installed. Both are caught here.

This document runs once. If `CORPUS_CONFIG.md` already exists and records
`STATUS: READY`, every task below is a no-op — skip them and move on.

## Tasks

### Task 1: Skip if already validated

- [ ] **Check for prior validation**: If `{{AUTORUN_FOLDER}}/CORPUS_CONFIG.md`
      exists and contains `STATUS: READY`, this playbook has already passed
      preflight on an earlier loop. Mark every remaining task in this document
      complete without doing anything and stop. Otherwise continue.

### Task 2: Read the configuration

- [ ] **Read the agent prompt** and record the configured values for
      `[CORPUS_SOURCE]`, `[CORPUS_KIND]`, `[ANALYTICAL_LENS]`,
      `[OUTPUT_FOLDER]`, `[BATCH_SIZE]`, and `[MAX_ITEMS]`. Quote each value
      verbatim — do not normalize or interpret yet.

### Task 3: Halt on unconfigured placeholders

- [ ] **Refuse to run on defaults**: If `[CORPUS_SOURCE]` still contains the
      string `<UNSET` — or is empty, or is one of the commented-out example
      values — do **not** proceed.

      Write a **halt marker** into this document, directly below this
      task: an HTML comment whose entire body is

      ```text
      maestro:halt: CORPUS_SOURCE is unconfigured. Edit the Auto Run prompt and re-run.
      ```

      The marker is described rather than shown, because a literal one sitting
      in this file would halt the playbook the moment the document is read.

      Leave this task **unchecked** so the stopping point is visible, and make
      your final message exactly this:

      > **Nothing ran.** `CORPUS_SOURCE` is still at its `<UNSET>` default.
      > Open the Auto Run prompt, replace that line with your playlist URL /
      > folder path / URL-list file, then start the playbook again. Also remove
      > the `maestro:halt` marker from `0_CONFIGURE.md` — a stale marker blocks
      > the re-run.

      Do not attempt to guess a source. Do not proceed to document 1.

### Task 4: Resolve the corpus kind

- [ ] **Determine what you are actually pointed at**: If `[CORPUS_KIND]` is
      `auto`, classify `[CORPUS_SOURCE]`:

      | Source looks like | Kind |
      |---|---|
      | `youtube.com/playlist?list=` or `youtu.be` playlist | `youtube-playlist` |
      | A path to a `.txt`/`.md` file whose lines are URLs | `url-list` |
      | A path to a `.opml` file | `opml` |
      | A path to an existing directory | `local-files` |
      | Any other single `http(s)://` URL | `single-url` |

      If the source is a path, confirm it exists and is readable **now**. If it
      does not exist, halt exactly as in Task 3 with the reason
      `CORPUS_SOURCE path does not exist`. Record the resolved kind.

### Task 5: Probe the extraction toolchain

- [ ] **Check the tools this kind needs, before you need them**:

      ```bash
      for c in yt-dlp curl python3 pandoc pdftotext; do
        if command -v "$c" >/dev/null 2>&1; then echo "$c: $(command -v "$c")"; else echo "$c: MISSING"; fi
      done
      ```

      Map the result to the resolved kind:

      | Kind | Hard requirement | Soft (degrades) |
      |---|---|---|
      | `youtube-playlist` | `yt-dlp` | — |
      | `url-list` / `single-url` | web fetch capability | `curl` |
      | `local-files` | `python3` | `pdftotext` (PDFs), `pandoc` (docx) |
      | `opml` | `python3` + web fetch | `curl` |

      If a **hard** requirement is missing, halt as in Task 3 with the reason
      naming the missing tool and the one-line install command
      (`brew install yt-dlp`, `brew install poppler` for `pdftotext`,
      `brew install pandoc`). If only a **soft** requirement is missing, record
      it as a degradation — items in that format will be marked `SKIP` with a
      reason rather than failing the run.

### Task 6: Prepare the output tree

- [ ] **Create `[OUTPUT_FOLDER]`** if it does not exist. If it exists and
      already contains synopsis files, this is a **resumed** corpus, not a fresh
      one — note that fact; document 1 will reconcile against the existing
      manifest rather than re-extracting.

### Task 7: Write the config record

- [ ] **Write `{{AUTORUN_FOLDER}}/CORPUS_CONFIG.md`** containing: the resolved
      corpus kind, every configured value, the toolchain probe result, any
      degradations, whether this is a fresh or resumed corpus, and a final line
      reading exactly `STATUS: READY`.

- [ ] **Tell the user what is about to happen**: state, in two lines, the
      resolved kind, the output folder, and the batch size. This is the last
      cheap moment to catch a wrong source.
