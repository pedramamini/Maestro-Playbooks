# Entity Research - Build the Knowledge Vault

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Advance the vault by one unit of work. That unit is a **repair** (fix what the
validator flags), a **depth batch** (new entity cards), or a **column sweep**
(one field across every existing card). Picking correctly between them is what
determines whether the finished vault can answer a comparative question.

## The Three Modes

A vault built only by researching entities ends up with the first twenty cards
excellent, the next fifty adequate, and the rest stubs, with every founder and
investor a dangling name. You cannot compare across a corpus shaped like that,
which was the point of building it.

| | **Repair** | **Depth** (new cards) | **Breadth** (column sweep) |
|---|---|---|---|
| Unit of work | Every CRITICAL issue | Up to `[DEPTH_BATCH]` entities, all fields | One field, all entities |
| Produces | A vault that answers correctly | New cards | Uniform coverage of a field |
| Gaps afterwards | None at CRITICAL | Invisible | Literal empty fields you can count |

### Choosing the mode this loop

Read the agent prompt for `[DEPTH_BATCH]`, `[SWEEP_EVERY]`, `[MAX_ENTITIES]`,
`[COVERAGE_TARGET]` and `[OUTPUT_FOLDER]`, then run:

```bash
cd [OUTPUT_FOLDER] && python3 Tools/health_check.py --json > /tmp/hc.json && python3 -c "import json;d=json.load(open('/tmp/hc.json'));print('critical',d['critical'],'budget_cards',d['budget_cards'],'lowest',d['lowest_coverage'])"
```

```text
IF the validator exits 2:
    -> Fix kb.yaml (the message names the problem). That is this loop's work.

ELSE IF critical > 0:
    -> REPAIR. Fix every CRITICAL issue. Nothing else this loop.

ELSE IF {{LOOP_NUMBER}} is a multiple of [SWEEP_EVERY]:
    -> BREADTH on the lowest-coverage field.

ELSE IF budget_cards < [MAX_ENTITIES] AND BACKLOG.md has PENDING entries:
    -> DEPTH. Research up to [DEPTH_BATCH] PENDING entities, highest importance first.

ELSE IF lowest coverage < [COVERAGE_TARGET]:
    -> BREADTH on the lowest-coverage field.

ELSE:
    -> Nothing to do. Mark complete without changes.
```

## Research Checklist

- [ ] **Advance the vault by one unit (or skip if nothing to do)**: Run the
      health check and choose the mode with the rule above. In REPAIR mode,
      work the CRITICAL list to zero and log what you fixed. In DEPTH mode,
      read `{{AUTORUN_FOLDER}}/BACKLOG.md`, take up to `[DEPTH_BATCH]`
      `PENDING` entries in importance order (CRITICAL, HIGH, MEDIUM, LOW; ties
      by lower effort), and for each one: research it, write the card with
      full frontmatter, record typed relations, log unresolved names to
      `SWEEP_GAPS.md`, update `INDEX.md`, and set its backlog status to
      `RESEARCHED`. Run the health check after each card. In BREADTH mode,
      sweep the lowest-coverage field across every card that lacks it and
      report filled / explicitly-unknown / gaps-logged counts. In every mode,
      append an entry to `{{AUTORUN_FOLDER}}/RESEARCH_LOG.md`.

---

## REPAIR Mode: Fix What the Validator Flags

Work the CRITICAL list in this order. Fixing relations first prevents false
orphan reports.

1. `broken-relation` - a hard relation names a card that does not exist. Fix
   the name if it is a spelling or suffix mismatch (`Acme` vs `Acme Inc`),
   otherwise remove the relation and log the target in `SWEEP_GAPS.md`.
   **Never create a stub card to satisfy a relation.**
2. `duplicate-name` - two cards normalize to the same name. Merge into the one
   with more content, redirect relations, delete the other.
3. `missing-required`, `missing-key`, `no-frontmatter`, `yaml-parse` - complete
   or repair the frontmatter.
4. `ledger-state` - the event state machine is violated. Read the message; it
   says which field to clear or set.
5. `relevance-type`, `relevance-range` - fix the score.

If a CRITICAL issue is genuinely unfixable (the validator is wrong, or the fix
requires information that does not exist), record it under `## KNOWN_ISSUES`
in `RESEARCH_LOG.md` with the exact issue text. `5_PROGRESS` stops gating on
issues listed there, so the run cannot spin forever on one bad row.

---

## DEPTH Mode: Research Entities

Work one entity at a time, start to finish, before beginning the next.

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
corrupts every category comparison downstream. **Create the product cards in
the same pass** - a company card whose `products:` names cards that do not
exist is a CRITICAL broken relation.

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

**Filename is the canonical name.** `Companies/Acme.md` is the entity `Acme`,
and every relation that points at it writes exactly `Acme`. Check existing
filenames with `ls` before writing a relation.

Relations come in two strengths, declared in `kb.yaml`:

| | Hard | Soft |
|---|---|---|
| Examples | `product.company`, `product.category`, `person.company` | `founders`, `all_investors`, `leaders`, `acquired_by` |
| Target missing | CRITICAL - fix now | MEDIUM - queue it |
| What to do | Create the target in this pass (products) or fix the name | Write the name anyway, and add a line to `SWEEP_GAPS.md` |

Soft relations are how the graph grows: you name the founder on the company
card today, `2_DISCOVER` picks the name up from `SWEEP_GAPS.md`, and a later
depth loop cards them. **Do not create a stub card for a soft target.** A stub
satisfies the validator while lying about coverage, which is worse than a
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
relevance_notes: "[From the backlog evaluation, verbatim.]"
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

**Event state.** If `kb.yaml` declares a ledger, the distinction between a
final event and a reported one is not pedantry - getting it wrong inflates
every rollup the vault ever reports. For the shipped M&A ledger:

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

`health_check.py` enforces whichever state machine `kb.yaml` declares.

### Product Card

```markdown
---
product: [Name]
company: [Company]             # HARD - must resolve to a Companies/ card
category: [Category]           # HARD - must resolve to a Categories/ card
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
distinguishable. If a product fits no existing category, author the category
card in the same pass rather than forcing a fit.

### Person Card

```markdown
---
name: [Full Name]
role: [Current role]
company: [Company]             # HARD - must resolve to a Companies/ card
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
only - never personal contact details or home location. When you card a person,
confirm the company card's `founders:` or `board_members:` names them with the
exact filename.

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

`portfolio` holds the in-scope subset only. Build it by grepping
`Companies/*.md` for this fund in `all_investors` and `lead_investors`. A
generalist fund has hundreds of positions and almost none are this market;
recording them all destroys the co-investment signal the field exists to provide.

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

Log every soft target that has no card to `{{AUTORUN_FOLDER}}/SWEEP_GAPS.md`:

```markdown
- [ ] [Entity Name] - [Type] - named by [[Card]] in `[field]`
```

### Step 5 - Update and validate

After each card:

```bash
cd [OUTPUT_FOLDER] && python3 Tools/health_check.py
```

Fix anything CRITICAL before starting the next entity. Update `INDEX.md` and
set the backlog entry to `RESEARCHED` with the card path.

---

## BREADTH Mode: Sweep One Column

Pick the lowest-coverage field from the health check and fill it across every
card of that type that lacks it.

### Anatomy of a sweep

```text
For each [entity type] in [folder]/*.md:

  1. Determine [field] from [named source priority].
  2. If it cannot be determined from those sources, write the explicit
     unknown for that field ("Not disclosed", "unknown", or [] for a list).
     Do not guess and do not infer from adjacent facts.
  3. Record it in frontmatter as `[field]:`.
  4. Add a prose line to the body explaining what you found and where.
  5. If this reveals a soft relation to an entity with no card, write the
     name and add it to SWEEP_GAPS.md rather than creating the card inline.

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

### When the lowest field is a relation

If the lowest-coverage field is `founders`, `all_investors`, `leaders` or
another soft relation, the sweep is: for every card lacking it, find the names,
write them, and log each to `SWEEP_GAPS.md`. The **cards** for those people and
funds are created by later depth loops, fed by `2_DISCOVER`. That is the
intended two-step, not a shortcut.

### Log the sweep

Append to `{{AUTORUN_FOLDER}}/RESEARCH_LOG.md`:

```markdown
## Loop {{LOOP_NUMBER}} - BREADTH: [type].[field] - {{DATE}}
- **Scope:** [N] cards in [folder]
- **Filled:** [N]   **Explicit unknown:** [N]   **Gaps logged:** [N]
- **Source priority used:** [...]
- **Notable:** [anything the sweep revealed about the market]
```

---

## Log Format

Every mode appends to `{{AUTORUN_FOLDER}}/RESEARCH_LOG.md`. Depth entries:

```markdown
## Loop {{LOOP_NUMBER}} - DEPTH - {{DATE}}
- **Researched:** [[Entity A]] (Companies), [[Entity B]] (Companies), [[Product X]] (Products)
- **Products created alongside:** [N]
- **Gaps logged:** [N] ([names])
- **Health check after:** CRITICAL [N], MEDIUM [N]
- **Notable:** [one line]
```

## Guidelines

- **One unit of work per loop** - a repair pass, a depth batch, or one field
- **Frontmatter first** - if a fact belongs in a rollup, it belongs in frontmatter
- **Never stub** - log to `SWEEP_GAPS.md` instead
- **Validate before finishing** - a loop that ends with broken relations has
  produced a vault that fails its next query
- **Date every claim** - markets move

## How to Know You're Done

**REPAIR:** health check reports zero CRITICAL, or every remaining one is
recorded under `## KNOWN_ISSUES` with a reason.

**DEPTH:** up to `[DEPTH_BATCH]` entities researched, each with a card with
full frontmatter, hard relations resolving, soft targets logged, `INDEX.md`
updated, backlog status `RESEARCHED`, health check clean of CRITICAL.

**BREADTH:** one field swept across every card that lacked it, counts
reported, gaps logged, health check clean of CRITICAL.

**Nothing to do:** no CRITICAL, no PENDING entries (or budget spent), and every
field at or above `[COVERAGE_TARGET]`. Mark complete without changes.
