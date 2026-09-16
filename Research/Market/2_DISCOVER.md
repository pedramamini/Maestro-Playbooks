# Entity Discovery - Find Research Targets

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Discover specific entities worth researching. Every candidate passes the scope
boundary **before** it enters the list, so that out-of-scope entities are
declined once rather than researched and then regretted.

## Instructions

1. **Read `[OUTPUT_FOLDER]/SCOPE.md`** - the boundary
2. **Read `[OUTPUT_FOLDER]/REJECTIONS.md`** - clusters already declined
3. **Read the market analysis** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MARKET_ANALYSIS.md`
4. **Read existing entities** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_ENTITIES.md`
5. **Focus on ONE entity category** that needs more discovery
6. **Apply the scope test to each candidate** before recording it
7. **Document discoveries** in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_ENTITIES.md`

## Discovery Checklist

- [ ] **Discover entities (or mark all covered)**: Read `SCOPE.md` and
      `REJECTIONS.md` first. Read the market analysis for priority categories
      and the existing entity list. If ALL priority categories already have 3+
      entities discovered, append `## ALL_CATEGORIES_COVERED` to
      `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_ENTITIES.md` and mark this task
      complete. Otherwise pick ONE category needing more entities, use web
      search to find 3-5 candidates, apply the scope test to each, and append
      the survivors with their basic info and discovery source. Record declined
      candidates too, with the reason.

## The Scope Test

Run this on every candidate, before it goes in the list. It costs one line and
it is the difference between a sharp corpus and a generic industry list.

1. **Check `REJECTIONS.md` first.** If the candidate belongs to a cluster that
   was already evaluated and declined, note it and move on. Do not re-litigate -
   that file exists precisely so this decision is free the second time.

2. **Apply the antonym pair from `SCOPE.md`.** The operative question is which
   party is the beneficiary, or which asset is the one being served. It is never
   which words appear on the homepage.

3. **Record the verdict:**
   - **Passes clearly** - add with `Scope: in`
   - **Straddles the line** - add with `Scope: borderline` and one line on which
     part of the business is in and which is out. `3_EVALUATE` will score it
     50-69. Borderline entities belong in the vault; that is what the score is for.
   - **Fails** - add to the `Declined` section with the reason. Do not create a
     card.

4. **Watch for a cluster.** If three or more candidates fail for the *same*
   reason, that is a cluster, not three coincidences. Append an entry to
   `REJECTIONS.md` covering it so later loops decline it for free.

### Three traps

These recur in every market and each one has produced bad entries:

- **Overloaded vocabulary.** Every market has a word both sides use. The word is
  not evidence. If you are accepting a candidate because of a phrase in their
  tagline, stop and read the product page.
- **Founder pedigree.** A well-known operator from this market, launching in the
  adjacent market, has launched in the adjacent market. This trap is seductive
  because pedigree correlates with funding and press, which is exactly what
  discovery surfaces loudest.
- **Award shortlists.** Innovation awards and analyst "ones to watch" lists
  optimize for novelty, not for this boundary. In any given year they skew
  heavily toward one side and it will not reliably be yours. Default to decline
  and make the candidate earn it on the product.

## Search Strategies by Entity Type

### Companies
- Search: "[market] companies", "[market] startups", "[market] market leaders"
- Check: company registries, professional networks, industry reports, news
- Look for: funding announcements, product launches, partnerships

### Products/Services
- Search: "[market] products", "[market] platforms", "[category] comparison"
- Check: review sites, marketplace listings, company websites, docs sites
- Look for: comparisons, feature lists, pricing pages

### Categories
- Search: "[market] landscape", "[market] buyer's guide", "[market] segments"
- Look for: how *buyers* name the segments, which rarely matches vendor marketing

### People
- Search: "[market] CEO", "[market] founder", conference speaker lists
- Look for: founders, repeat operators, people who move between tracked companies

### Capital
- Search: "[market] investors", "[market] funding round"
- Look for: funds with two or more in-scope positions - one is a coincidence

### [DOMAIN_ENTITY]
- Search strategy depends on the type resolved in `0_CONFIGURE`; use the
  authoritative registry for that object where one exists

## Output Format

Append to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_ENTITIES.md`:

```markdown
---

## [Category Name] - Discovered [YYYY-MM-DD]

### [Entity Name 1]
- **Type:** [Company | Product | Category | Person | Capital | DomainEntity]
- **Brief:** [one sentence]
- **Why Notable:** [why it matters in this market]
- **Scope:** in | borderline
- **Scope Note:** [required when borderline: which part is in, which is out]
- **Discovery Source:** [URL]
- **Status:** PENDING

### Declined

#### [Candidate Name]
- **Reason:** [which side of the antonym pair, and why]
- **Cluster:** [name, if this is the 3rd+ of a pattern - then log it in REJECTIONS.md]

### Discovery Summary
- **Category:** [category researched]
- **Found:** [count]   **Declined:** [count]
- **Search Queries Used:**
  - "[query 1]"
- **New rejection clusters logged:** [names, or none]
```

## Entity Status Values

| Status | Meaning |
|--------|---------|
| `PENDING` | Discovered and in scope, not yet researched |
| `RESEARCHED` | Full profile created in the vault |
| `SKIP` | In scope but not worth the research effort |
| `DUPLICATE` | Already covered under another entity |

Note that **out of scope is not a status.** Those candidates never enter the
list; they go in the `Declined` section. Status is about research effort, scope
is about membership, and keeping them separate is what stops the vault drifting.

## Guidelines

- **One category per run** - focused discovery beats scattered discovery
- **Quality over quantity** - 3-5 well-chosen entities beat 20 marginal ones
- **Record the declines** - a decline with a reason is reusable; a silent skip
  gets rediscovered next loop
- **Include the discovery source** - enables verification later
- **Check for duplicates** - including near-duplicate names of existing cards
- **Diversify within the category** - leaders, challengers and emerging players

## How to Know You're Done

**Option A - Discovered entities:** you picked one category, searched it, applied
the scope test to each candidate, and appended survivors and declines.

**Option B - All categories covered:** every priority category has 3+ entities,
and you appended `## ALL_CATEGORIES_COVERED`.
