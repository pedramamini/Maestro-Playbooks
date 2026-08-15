# Corpus Synthesis Playbook

Turns a pile of source material — a YouTube playlist, a folder of PDFs, a list
of URLs, an OPML file — into a navigable, interlinked knowledge base with a
cross-cutting synthesis on top.

The pattern is **bulk extract → fan out → fan in**. Extraction happens once and
is dumb. Analysis happens in parallel batches, one subagent per item, each
reading exactly one document. Synthesis happens once at the end, reading only
the synopses.

## Overview

| | |
|---|---|
| **Category** | Research |
| **Loops** | Yes, one batch per loop |
| **Needs** | Web access; `yt-dlp` for playlists, `pdftotext`/`pandoc` for local docs |
| **Writes** | `[OUTPUT_FOLDER]` (synopses + `INDEX.md` + `SYNTHESIS.md`), working files in the Auto Run folder |
| **Permissions** | None beyond ordinary file and network access |

## What it produces

```
<OUTPUT_FOLDER>/
├── INDEX.md            # every item, one key point each, coverage line at top
├── SYNTHESIS.md        # themes, numbers, disagreements, what to read first
├── 001-first-item.md   # one synopsis per item, YAML front matter, wiki-links
├── 002-second-item.md
└── ...
```

Each synopsis carries front matter and `[[wiki-links]]`, so the result browses
in Maestro's DocGraph and drops straight into an Obsidian vault.

## Document chain

| # | Document | Does | Cost |
|---|----------|------|------|
| 0 | `0_CONFIGURE` | Validates config, probes the toolchain, **halts on unedited defaults** | Trivial |
| 1 | `1_EXTRACT` | Pulls every item to plain text, writes `CORPUS_MANIFEST.md` | I/O-bound |
| 2 | `2_PLAN` | Selects the next `BATCH_SIZE` items, writes a self-contained brief | Cheap |
| 3 | `3_PROCESS` | One parallel subagent per item, one synopsis each | The bulk |
| 4 | `4_SYNTHESIZE` | Updates `INDEX.md`; writes `SYNTHESIS.md` **only when exhausted** | Spiky |
| 5 | `5_PROGRESS` | Gate — continue or exit | Trivial |

Documents 0 and 1 skip themselves on re-entry, so a loop reset costs two file
reads, not a re-extraction.

## Configuration

Configure in the Auto Run prompt before the first run:

| Variable | Default | What it does |
|---|---|---|
| `CORPUS_SOURCE` | `<UNSET>` | Playlist URL, folder, URL-list file, or OPML |
| `CORPUS_KIND` | `auto` | Override detection if it guesses wrong |
| `ANALYTICAL_LENS` | thesis/claims/metrics/quotes | Steers both synopsis and synthesis |
| `OUTPUT_FOLDER` | `{{AUTORUN_FOLDER}}/corpus` | Where the knowledge base is built |
| `BATCH_SIZE` | `8` | Items per loop, one subagent each |
| `MAX_ITEMS` | `all` | Cap for sampling a large source |

`ANALYTICAL_LENS` is the variable worth spending a minute on. It is inlined
verbatim into every worker's instructions, so it is the single highest-leverage
knob in the playbook — "extract every pricing figure with its source sentence"
and "identify the argument and the unaddressed objections" produce completely
different corpora from the same input.

`CORPUS_SOURCE` deliberately ships as `<UNSET>` rather than a plausible example.
The playbook **halts on document 0** if you leave it — a run against someone
else's example value is a silent waste, and a stopped run with a reason in the
History panel is not.

## Recommended settings

| Setting | Value |
|---|---|
| Loop | On |
| Max loops | `ceil(items / BATCH_SIZE) + 2` — e.g. 10 for a 60-item playlist at batch 8 |
| Reset on completion | Off for 0-4, **On for 5** |

## How the loop terminates

The gate continues if **any** of these is true:

1. Items are still `PENDING`
2. `CORPUS_MANIFEST.md` lacks `## EXTRACTION_COMPLETE` (extraction was cut short)
3. `SYNTHESIS.md` does not exist (the fan-in never ran)

It exits only when all three are resolved. A gate that checks only condition 1
exits the moment a batch empties, which is exactly how a corpus ends up with no
synthesis and every light green.

## Failure handling

- **Zero items extracted** → halts with the attempted command and the two
  likeliest causes. Does not loop on an empty corpus.
- **Missing hard dependency** (`yt-dlp` for a playlist) → halts on document 0
  with the install command, before any extraction is attempted.
- **An item with no transcript** → `SKIP` with the reason in the manifest.
  Counted and reported, never retried forever.
- **An item that fails twice** → promoted to `SKIP`, so the loop still converges.
- **A capped run** → the number of unprocessed items is stated explicitly in the
  exit report.

## Generalizes to

The shape is "N documents that need the same analytical treatment, then a
synthesis layer." That covers conference playlists, due diligence across a set
of companies, literature reviews, competitive analysis, a backlog of meeting
transcripts, and reading an entire documentation site.

## Origin

Derived from [60 Talks, One Afternoon](https://pedsidian.pedramamini.com/Claude/Blog/2026-03-26-unprompted-2026-60-talks-one-afternoon),
which processed a 60-talk conference playlist into a browsable vault in about
twenty minutes.
