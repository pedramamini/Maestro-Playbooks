# Corpus Synthesis Agent Prompt

**IMPORTANT: Configure the placeholders below before running this playbook.**

The playbook **halts on document 0** if you leave `CORPUS_SOURCE` at its
`<UNSET>` default. That is deliberate — a run against an example value wastes
tokens and produces a knowledge base about something you do not care about.

---

## Configuration

### The Corpus

<!-- CONFIGURE: What you want processed. One source, not a list. -->
**CORPUS_SOURCE:** `<UNSET — replace this line with your playlist URL, folder path, OPML file, or URL-list file>`

<!-- Examples:
- https://www.youtube.com/playlist?list=PLjmt1tu85IhAiVPugOjP-7Cy0Oemi3m7z
- ~/Downloads/due-diligence-pdfs
- {{AGENT_PATH}}/sources.txt        (one URL per line)
- ~/Documents/subscriptions.opml
- https://github.com/someorg/somerepo   (processes docs/ and *.md)
-->

<!-- CONFIGURE: Leave `auto` unless detection guesses wrong. -->
**CORPUS_KIND:** `auto`

<!-- Valid values:
- auto              detect from the source string
- youtube-playlist  yt-dlp --write-auto-sub, VTT to text
- url-list          a file with one URL per line
- local-files       a directory of pdf/md/txt/docx
- opml              an OPML subscription file
- single-url        one page, crawled one level deep
-->

### What You Want Out

<!-- CONFIGURE: One sentence. This steers both the per-item synopsis and the
     final synthesis. Be specific — "what did each speaker claim and what is
     the evidence" produces a different corpus than "extract every pricing
     number mentioned". -->
**ANALYTICAL_LENS:** `Extract the core thesis, the key claims with supporting evidence, notable metrics, and quotable lines.`

<!-- Examples:
- Score each vendor against our evaluation criteria and flag disqualifiers.
- For each paper: method, dataset, headline result, and stated limitations.
- Pull every pricing, headcount, and funding figure with its source sentence.
- Identify the argument, the counterargument it answers, and unaddressed objections.
-->

### Output

<!-- CONFIGURE: Where the knowledge base gets built. -->
**OUTPUT_FOLDER:** `{{AUTORUN_FOLDER}}/corpus`

<!-- CONFIGURE: How many items get processed per loop iteration. Each item in a
     batch is handled by its own parallel subagent. 6-10 is the sweet spot;
     above ~12 you are queuing, not parallelizing. -->
**BATCH_SIZE:** `8`

<!-- CONFIGURE: Stop after this many items even if the source has more.
     Use `all` for no cap. Useful when you are sampling a large playlist. -->
**MAX_ITEMS:** `all`

---

## Agent Instructions

You are building a navigable knowledge base from a corpus of source documents.

The pattern is **bulk extract → fan out → fan in**:

1. Get every item into plain text once, up front (document 1).
2. Process items in batches, one batch per loop iteration, with a parallel
   subagent per item and identical instructions to each (documents 2-3).
3. Maintain a running index each loop, then write the cross-cutting synthesis
   when the corpus is exhausted (document 4).

Every synopsis is a standalone markdown file with YAML front matter and
wiki-links, so the result is browsable in Maestro's DocGraph and in Obsidian.

Configured values are referenced in the task documents as `[CORPUS_SOURCE]`,
`[CORPUS_KIND]`, `[ANALYTICAL_LENS]`, `[OUTPUT_FOLDER]`, `[BATCH_SIZE]`, and
`[MAX_ITEMS]`. Read them from this prompt — do not guess.

Throughput work belongs on a fast model. The per-item synopsis agents are an
extraction task, not a reasoning task. The synthesis pass is the reasoning task
and stays with you.
