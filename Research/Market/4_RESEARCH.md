# Entity Research - Build the Knowledge Vault

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Advance the vault by one unit of work. That unit is either a **new entity**
(depth) or a **column sweep** across every existing card (breadth), and picking
correctly between them is what determines whether the finished vault can answer
a comparative question.

## The Two Modes

A vault built only by researching one entity at a time ends up with the first
twenty cards excellent, the next fifty adequate, and the rest stubs. You cannot
compare across a corpus shaped like that, which was the point of building it.

| | **Depth** (new entity) | **Breadth** (column sweep) |
|---|---|---|
| Unit of work | One entity, all fields | One field, all entities |
| Produces | A new card | Uniform coverage of a field |
| Gaps afterwards | Invisible | Literal empty fields you can count |
| Cost per fact | Higher - context rebuilt per card | Lower - one context for N cards |

### Choosing the mode this loop

```text
IF loop number <= [DEPTH_SWITCH_AT] AND PENDING CRITICAL/HIGH entities exist:
    -> DEPTH. Research one new entity.

ELSE IF health_check.py reports a field below 70% coverage:
    -> BREADTH. Sweep that field across every card.

ELSE IF PENDING CRITICAL/HIGH entities exist:
    -> DEPTH.

ELSE:
    -> BREADTH on the lowest-coverage field, or mark complete if all are above 90%.
```

Run this to see the coverage table, which is also the sweep queue:

```bash
cd [OUTPUT_FOLDER] && python3 Tools/health_check.py
```

## Research Checklist

- [ ] **Advance the vault by one unit (or skip if nothing to do)**: Determine
      the mode using the rule above. In DEPTH mode, read
      `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`, pick ONE PENDING entity
      with CRITICAL or HIGH importance, research it, create the card with full
      frontmatter, add typed relations, update `INDEX.md`, mark it RESEARCHED,
      and log the work. In BREADTH mode, pick the lowest-coverage field, sweep
      it across every card that lacks it, and report filled/unknown/gap counts.
      If the plan does not exist or has no PENDING CRITICAL/HIGH entities and
      every field is above 90% coverage, mark this task complete without changes.

---

## DEPTH Mode: Research One Entity

### Step 1 - Gather

Work these sources in order. Later sources annotate earlier ones on a conflict;
they do not override them.

1. Official website - about, products, pricing, docs, careers
2. Developer portal and public repositories
3. Regulatory filings where applicable
4. Funding announcements: the company's own first, then the lead investor's
5. Structured databases (registries, funding trackers)
6. Reputable press and analyst coverage
7. Conference talks, podcasts, long-form interviews

**Go deep on products.** Companies routinely ship two to five times more than
the homepage suggests. Check the product menu, docs, developer portal,
marketplace listings and public repositories. An incomplete product list
corrupts every category comparison downstream.

**Job postings are signal.** What a company hires for reveals roadmap and true
headcount better than any marketing page.

### Step 2 - Validate

- Cross-reference every fact across at least two independent sources
- Where sources disagree on a figure, record the **lower** value and note the
  discrepancy in the body with both sources
- Any quantitative claim tracing only to the company's own marketing goes into
  `unverified_claims:`. Never assert it in prose
- Check dates and amounts twice. A wrong funding figure propagates into every
  rollup that touches it

### Step 3 - Write the card

**Frontmatter is the database. The body is the argument for what the frontmatter
asserts.** This is the rule that makes the vault queryable rather than merely
readable: a field in frontmatter can be counted, rolled up, validated and
graphed; the same fact in a body table can only be re-read.

Relations must use canonical names matching existing card filenames. Check with
Glob before writing one. Any entity you reference that has no card goes to
`{{AUTORUN_FOLDER}}/SWEEP_GAPS.md` - **do not create a stub card for it.** A
stub satisfies the validator while lying about coverage, which is worse than a
missing card, because a missing card is visible.

### Company Card

```markdown
---
company: [Name]
status: active                 # active | acquired | inactive | rebranded
founded: [YYYY]
headquarters: [City]
country: [Full country name]
employee_count: 11-50          # use the bands in kb.yaml
website: https://...

total_funding: 30000000        # plain integer, no symbols, commas or M/B
latest_round_size: 20000000
latest_round_date: 2024-07-24
latest_round_type: Series A
lead_investors: [Fund One]
all_investors: [Fund One, Fund Two]

products: [Product A, Product B]
founders: [Person Name]
board_members: [Person Name]

specialization: "One line on what they actually do."
relevance: 95
relevance_notes: "[From the plan, verbatim.]"
last_updated: {{DATE}}
---

# [Company Name]

> [One-line description]

## Overview
[2-3 paragraphs: what they do and their position in the market.]

## Products
- **[[Product A]]** - [what it does]

## Leadership
- **CEO**: [[Person]] - [background]

## Funding History
| Date | Round | Amount | Lead |
|------|-------|--------|------|
| [date] | [round] | $[amount] | [[Fund]] |

## Recent Developments
- **[YYYY-MM]**: [development]

## Competitive Position
[Where they stand. Name competitors as [[wikilinks]].]

## Sources
1. [Title](URL) - accessed [date]
```

**Acquisition state.** If the market tracks consolidation, the distinction
between a closed deal and a reported one is not pedantry - getting it wrong
inflates every consolidation figure the vault ever reports, and nobody notices
until someone checks one specific row.

```yaml
# Deal CLOSED
status: acquired
acquired_by: [Acquirer]
acquisition_announced: 2025-09-16
acquisition_date: 2025-12-31        # the CLOSE date
acquisition_amount: 300000000
acquisition_status: closed

# Reported or announced but NOT closed
status: active                      # NOT acquired. Never, until close.
acquisition_status: rumored         # or pending_close
acquisition_suitor: [Acquirer]      # NOT acquired_by
acquisition_reported_price: 300000000
acquisition_reported_date: 2026-08-02
```

`acquired_by` means the deal closed. `health_check.py` enforces this.

### Product Card

```markdown
---
product: [Name]
company: [Company]             # must resolve to a Companies/ card
category: [Category]           # must resolve to a Categories/ card
description: "One line, factual, no adjectives."
launch_date: 2023-04-01
pricing_model: Subscription    # see kb.yaml enum
cost_range: "Free tier; Pro from $X/mo; Enterprise contact sales"
deployment: [SaaS, Self-hosted]
product_link: https://...
relevance: 98
relevance_notes: "..."
last_updated: {{DATE}}
---

# [Product Name]

## What It Does
## Key Capabilities
## Pricing
## Target Buyer
## Competing Products
## Sources
```

`Not disclosed` is a correct and common answer for pricing. An empty field is
not - it means nobody looked, which is a different thing and should stay
distinguishable.

### Person Card

```markdown
---
name: [Full Name]
role: [Current role]
company: [Company]             # must resolve to a Companies/ card
previous_roles:
  - "VP Engineering at Prior Co (2019-2023)"
specialization: "Short phrase."
relevance: 85
relevance_notes: "..."
last_updated: {{DATE}}
---
```

The value is the **talent-flow edge**, not the biography. Prior roles with dates
and company names matter; education rarely does. Public professional information
only - never personal contact details or home location.

### Capital Card

```markdown
---
name: [Fund Name]
type: Venture Capital          # see kb.yaml enum
aum: 850000000
stage: "Seed to Series B"
check_size: "500000-15000000"
sector_focus: [...]
portfolio: [Company A, Company B]    # IN-SCOPE SUBSET ONLY
relevance: 70
relevance_notes: "..."
last_updated: {{DATE}}
---
```

`portfolio` holds the in-scope subset only. A generalist fund has hundreds of
positions and almost none are this market; recording them all destroys the
co-investment signal the field exists to provide.

### Unverified Claims

```yaml
unverified_claims:
  - claim: "10,000+ enterprise customers"
    risk_level: Medium         # Low | Medium | High
    reason: "Marketing claim. Counting methodology not stated."
```

`High` means the claim materially affects how the entity is positioned and must
not be repeated in any report without a caveat.

### Step 4 - Connect

Typed relations in frontmatter carry direction and meaning. Body `[[wikilinks]]`
are untyped mentions. Keep them separate - collapse them and "acquired by"
becomes indistinguishable from "named in the same paragraph as", and every
precise question about the graph stops being answerable.

Update the mirror side where one exists: `products` on a company mirrors
`company` on the product; `all_investors` mirrors `portfolio`.

### Step 5 - Update and validate

```bash
cd [OUTPUT_FOLDER] && python3 Tools/health_check.py
```

Fix anything CRITICAL before finishing the loop. Work the output in this order:
broken relations, then orphans, then missing required fields, then enum and
format, then event state, then duplicates. Fixing relations first prevents false
orphan reports.

---

## BREADTH Mode: Sweep One Column

Pick the lowest-coverage field from the health check table and fill it across
every card that lacks it.

### Anatomy of a sweep

```text
For each [entity type] in [folder]/*.md:

  1. Determine [field] from [named source priority].
  2. If it cannot be determined from those sources, write "[explicit unknown]".
     Do not guess and do not infer from adjacent facts.
  3. Record it in frontmatter as `[field]:`.
  4. Add a prose paragraph to the body explaining what you found and where.
  5. If this reveals a relation to an entity with no card, note it in
     SWEEP_GAPS.md rather than creating the card inline.

Process every file. Report counts: filled, explicitly-unknown, gaps logged.
```

Five properties make a sweep work, and dropping any one of them degrades it into
an ordinary research pass:

1. **Named source priority** - otherwise you get whichever page ranked first
2. **An explicit unknown value** - "nobody looked" and "not public" are
   different facts and both are useful
3. **Frontmatter and body both** - the field is queryable, the reasoning readable
4. **Gaps logged, not fixed inline** - creating cards mid-sweep destroys the
   uniformity you are buying
5. **A count at the end** - it is how you know the sweep processed everything
   rather than the first thirty files before context filled

### Sweep order

Each makes the next cheaper, because the vault knows more.

| # | Sweep | Why here |
|---|-------|----------|
| 1 | **Product completeness** - all products per company, not just the headline one | Everything downstream is wrong if the product set is wrong |
| 2 | **Category assignment** - every product to a category; author new ones as needed | The comparison spine must precede any analysis |
| 3 | **Relevance scoring** - score and justify every card | Set the boundary before the corpus outgrows review |
| 4 | **Relations** - founders, investors, parent companies | Turns the folder into a graph |
| 5 | **Funding** - rounds, dates, leads, totals | High value, well sourced, mostly public |
| 6 | **Pricing** - model and range | Highest value and hardest. Expect 40-60% `Not disclosed` - that is a finding |
| 7 | **People** - cards for founders surfaced in sweep 4 | Depends on relations existing |
| 8 | **Capital** - cards for investors surfaced in sweep 4 | Same |
| 9 | **Links** - website, docs, repo | Cheap and mechanical, do it last |

Sweeps 1 and 2 are the ones most often skipped, and skipping them is why a
market vault ends up unable to answer a comparative question.

### Log the sweep

Append to `{{AUTORUN_FOLDER}}/RESEARCH_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
## Sweep: [field] - {{DATE}}
- **Scope:** [N] cards in [folder]
- **Filled:** [N]   **Explicit unknown:** [N]   **Gaps logged:** [N]
- **Source priority used:** [...]
- **Notable:** [anything the sweep revealed about the market]
```

---

## Guidelines

- **One unit of work per loop** - one entity, or one field
- **Frontmatter first** - if a fact belongs in a rollup, it belongs in frontmatter
- **Never stub** - log to `SWEEP_GAPS.md` instead
- **Validate before finishing** - a loop that ends with broken relations has
  produced a vault that fails its next query
- **Date every claim** - markets move

## How to Know You're Done

**DEPTH:** one entity researched, card created with full frontmatter and
resolving typed relations, `INDEX.md` updated, status set to RESEARCHED, health
check clean of CRITICAL issues.

**BREADTH:** one field swept across every card that lacked it, counts reported,
gaps logged, health check clean of CRITICAL issues.

**Nothing to do:** no PENDING CRITICAL/HIGH entities and every field above 90%
coverage. Mark complete without changes.
