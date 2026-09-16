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
6. **Output the analysis** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MARKET_ANALYSIS.md`

## Analysis Checklist

- [ ] **Analyze the market and fix the schema (if not already done)**: First
      check whether `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MARKET_ANALYSIS.md`
      already exists with at least one entity category defined. If it does, skip
      the analysis and mark this task complete. Otherwise: read
      `MARKET_CONFIG.md` and `SCOPE.md`, survey the market with web search,
      write the analysis file, fill in `kb.yaml`, and initialize the vault
      folders with `INDEX.md` as the launch page.

- [ ] **Author the Category cards**: Categories are the comparison spine and the
      most commonly skipped entity type. Without them the vault is a list of
      companies; with them it is a market map. Create 8-15 Category cards in
      `[OUTPUT_FOLDER]/Categories/` following the schema below. If fewer than
      three products would sit in a proposed category, it is not a category -
      fold it into a broader one. Expect to add two or three more during later
      loops: when a product fits nowhere, that is a signal to author a new
      category rather than to force-fit it.

## Filling in kb.yaml

`0_CONFIGURE` copied a template to `[OUTPUT_FOLDER]/kb.yaml`. Now make it
specific to this market:

1. **Prune the enumerations** to the values this market actually uses, and add
   any it needs that are missing. An unused enum value is noise; a missing enum
   means that field goes unvalidated.
2. **Set `enums.segment`** to the primary non-category split in this market, or
   delete it and every `segment:` field if the market has no such split.
3. **Write the `DOMAIN_ENTITY` block** using the type resolved in
   `0_CONFIGURE`, or delete the commented block if it was `none`.
4. **Set the `ledger` block** to the event class that drives this market - M&A
   for enterprise software, approvals for pharma, licenses for regulated
   finance, contract awards for public sector, certifications for industrial.
   Delete the block if no event class matters here.

Then confirm it parses:

```bash
cd [OUTPUT_FOLDER] && python3 Tools/health_check.py
```

On an empty vault this reports missing folders and nothing else. That is the
expected first run, and it proves the schema is loadable.

## Output Format

Create `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MARKET_ANALYSIS.md`:

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

### Priority Categories (research first)
| Category | Relevance | Target Count |
|----------|-----------|--------------|
| Companies | [why relevant] | [15-30] |
| Products | [why relevant] | [25-50] |
| Categories | taxonomy spine | [8-15] |
| ... | ... | ... |

### Secondary Categories (if budget permits)
| Category | Relevance | Target Count |
|----------|-----------|--------------|
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

## Vault Structure

Create in `[OUTPUT_FOLDER]`:

```text
vault/
├── INDEX.md           # Launch page
├── SCOPE.md           # The boundary (from 0_CONFIGURE)
├── REJECTIONS.md      # Rejection log (from 0_CONFIGURE)
├── kb.yaml            # Schema driving the validator
├── Tools/             # health_check.py
├── Companies/
├── Products/
├── Categories/        # The taxonomy spine
├── People/
├── Capital/
├── [DomainEntity]/    # If resolved
└── Resources/         # Reports, data sources, references
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

## INDEX.md Template

```markdown
# [MARKET_TOPIC] Research Vault

> Last updated: {{DATE}}
> Research by: {{AGENT_NAME}}

## Scope
- **IN:**  [SCOPE_IN]
- **OUT:** [SCOPE_OUT]

See [[SCOPE]] for edge rules and [[REJECTIONS]] for clusters already declined.

## Overview
[2-3 sentence summary of the market]

## Quick Navigation

### Categories
- [[Category 1]]

### Companies
- [[Company 1]]

### Products
- [[Product 1]]

### People
- [[Person 1]]

### Capital
- [[Fund 1]]

## Market Stats
| Metric | Value | Source |
|--------|-------|--------|
| Market Size | $X | [source] |

## Recent Developments
- [Date]: [development]

---
*Built with the Maestro Market Research Playbook*
```

## Guidelines

- **Use web search extensively** - get current market data
- **Be market-specific** - tailor the schema to the actual market, do not accept
  the template's defaults unexamined
- **Categories before entities** - the spine has to exist before things hang off it
- **Prioritize ruthlessly** - not every entity type matters in every market
- **Respect the boundary** - if the survey keeps surfacing the out-of-scope side,
  that is a signal the boundary is working, not that it is too narrow
