# Market Analysis - Landscape Survey

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Survey the target market, fix the schema that every later card will follow, and
author the **Categories** that make comparison possible. This document turns the
scope boundary from `0_CONFIGURE` into a working research framework.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/MARKET_CONFIG.md`** for the resolved configuration
2. **Read `[OUTPUT_FOLDER]/SCOPE.md`** for the boundary
3. **Research the market broadly** using web search
4. **Fill in `kb.yaml`** with the entity types and enumerations this market needs
5. **Author Category cards** - the taxonomy spine
6. **Output the analysis** to `{{AUTORUN_FOLDER}}/MARKET_ANALYSIS.md`

This document does its real work **once**. `MARKET_ANALYSIS.md` is a static
file, not a per-loop one: the market does not change between loops, and
re-surveying it thirty times would be the single largest waste in the run.
On every loop after the first, both tasks below are two file checks and a
completion mark.

## Analysis Checklist

- [ ] **Analyze the market and fix the schema (once)**: If
      `{{AUTORUN_FOLDER}}/MARKET_ANALYSIS.md` already exists with a
      `## Schema Decisions` section, mark this task complete without changes.
      Otherwise: read `MARKET_CONFIG.md` and `SCOPE.md`, survey the market
      with web search, write `MARKET_ANALYSIS.md` in the format below, fill in
      `[OUTPUT_FOLDER]/kb.yaml` as described under "Filling in kb.yaml", and
      confirm the validator accepts it (exit 0).

- [ ] **Author the Category cards (once)**: If `[OUTPUT_FOLDER]/Categories/`
      already holds 8 or more cards, mark this task complete without changes.
      Otherwise: Categories are the comparison spine and the most commonly
      skipped entity type. Without them the vault is a list of companies; with
      them it is a market map. Create 8-15 Category cards in
      `[OUTPUT_FOLDER]/Categories/` following the schema below. If fewer than
      three products would sit in a proposed category, it is not a category -
      fold it into a broader one. Then **seed the backlog**: every company
      named in any card's `leaders:` or `emerging:` goes into
      `{{AUTORUN_FOLDER}}/SWEEP_GAPS.md` as `- [ ] [Name] - Company - named by
      [[Category]] in leaders`, unless already present. Those names are the
      first thing `2_DISCOVER` picks up. Expect to add two or three more
      categories during later loops: when a product fits nowhere, that is a
      signal to author a new category rather than to force-fit it.

## Filling in kb.yaml

`0_CONFIGURE` copied a template to `[OUTPUT_FOLDER]/kb.yaml`. Now make it
specific to this market:

1. **Prune the enumerations** to the values this market actually uses, and add
   any it needs that are missing. An unused enum value is noise; a missing enum
   means that field goes unvalidated.
2. **Decide on `segment`**: if the market has a primary non-category split
   (SMB / Enterprise, Hardware / Software), uncomment `enums.segment` with the
   real values and uncomment the `segment: segment` lines under `company` and
   `product`. Otherwise leave all three commented.
3. **Write the `DOMAIN_ENTITY` block** using the type resolved in
   `0_CONFIGURE`, or delete the commented block if it was `none`. Also create
   its folder in the vault.
4. **Set the `ledger` block** to the event class that drives this market - M&A
   for enterprise software, approvals for pharma, licenses for regulated
   finance, contract awards for public sector, certifications for industrial.
   Every field name in the block is configurable; the comment above it shows a
   pharma example. Delete the block if no event class matters here.
5. **If you remove an entity type**, also remove every relation that targets
   it (for example, dropping `capital` means dropping `company.all_investors`
   and `company.lead_investors`). The validator refuses to run otherwise.

Then confirm it parses:

```bash
cd [OUTPUT_FOLDER] && python3 Tools/health_check.py; echo "exit=$?"
```

Exit 0 and a `0 cards` summary is the expected result on an empty vault. Exit 2
prints `CONFIG ERROR` with the exact problem - fix it before moving on. The
schema has to be loadable before any research depends on it.

## Output Format

Create `{{AUTORUN_FOLDER}}/MARKET_ANALYSIS.md`:

```markdown
# Market Analysis: [MARKET_TOPIC]

## Scope
- **IN:**  [from SCOPE.md]
- **OUT:** [from SCOPE.md]

## Market Overview
- **Market Size:** [current size, projected growth]
- **Growth Rate:** [CAGR or annual growth]
- **Key Drivers:** [what is driving growth]
- **Key Challenges:** [barriers, headwinds]

## Market Segments
1. [Segment 1] - [brief description]
2. [Segment 2] - [brief description]

## Competitive Landscape
- **Market Leaders:** [top 3-5 companies]
- **Emerging Players:** [notable challengers]
- **Recent Consolidation:** [notable events]

## Entity Categories for Research

These are the buckets `2_DISCOVER` fills and `5_PROGRESS` checks. Targets
must sum to roughly `MAX_ENTITIES`; Categories do not count against it.

### Priority Categories (research first)
| Category | Why relevant | Target Count |
|----------|--------------|--------------|
| Companies | [why] | [20-30] |
| Products | [why] | [15-25] |
| People | founders and repeat operators | [8-12] |
| Capital | funds with 2+ in-scope positions | [5-8] |
| [DomainEntity] | [why] | [N] |

### Secondary Categories (if budget permits)
| Category | Why relevant | Target Count |
|----------|--------------|--------------|
| ... | ... | ... |

## Schema Decisions
- **Domain entity type:** [resolved type, or `none` and why]
- **Segment axis:** [the split, or `none`]
- **Event ledger:** [event class, or `none`]
- **Enumerations pruned:** [what was removed or added and why]

## Overloaded Terms
Vocabulary used by both sides of the scope boundary. Validate per candidate.

| Term | In-scope meaning | Out-of-scope meaning |
|---|---|---|
| [term] | [meaning] | [meaning] |

## Research Priorities
1. [first priority area]
2. [second priority area]

## Sources Consulted
- [URL 1]
- [URL 2]
```

## Category Card Schema

Categories get real frontmatter, not just prose. `evaluation_criteria` is the
highest-value field on the card: it is what buyers actually compare on, and it
is what makes two products in the same category comparable at all.

```markdown
---
category: [Name]
definition: "One sentence a buyer would recognize."
maturity: emerging | growth | mature | consolidating | declining
buyer: "Who holds the budget line."
leaders: [Company A, Company B]
emerging: [Company C]
evaluation_criteria:
  - [What buyers compare on]
  - [Second criterion]
adjacent_categories: [Other Category]
relevance: 100
relevance_notes: "Core segment of the tracked market."
last_updated: {{DATE}}
---

# [Category Name]

## Definition
[What this category is, in buyers' words rather than vendors' words.]

## What Buyers Evaluate On
[The criteria above, explained.]

## Current Shape
[Who leads, who is emerging, who is exiting, and why.]

## How It Is Shifting
[Direction of travel.]

## Adjacent Categories
[Where it blurs into neighbors, and where exactly the seam is.]
```

## INDEX.md

`0_INITIALIZE` created `INDEX.md`. After authoring the categories, replace the
`_No categories defined yet._` line under `### Categories` with one
`- [[Category Name]]` line per card, and add a two-sentence `## Overview` of
the market beneath the scope block.

## Guidelines

- **Use web search extensively** - get current market data
- **Be market-specific** - tailor the schema to the actual market, do not accept
  the template's defaults unexamined
- **Categories before entities** - the spine has to exist before things hang off it
- **Prioritize ruthlessly** - not every entity type matters in every market
- **Respect the boundary** - if the survey keeps surfacing the out-of-scope side,
  that is a signal the boundary is working, not that it is too narrow
