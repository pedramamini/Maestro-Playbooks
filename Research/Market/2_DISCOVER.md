# Entity Discovery - Find Research Targets

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Add entities worth researching to the durable backlog. Every candidate passes
the scope boundary **before** it enters the list, so that out-of-scope entities
are declined once rather than researched and then regretted.

Discovery has three feeds, worked in this order because each is a better
source than the one after it:

1. **`SWEEP_GAPS.md`** - entities that existing cards already name (a founder,
   an investor, a category leader, an acquirer). These are the highest-value
   candidates in the run: carding them turns a dangling name into an edge.
2. **`SEED_SOURCE`** - the curated artifact from the configuration, on the
   first loop it is available.
3. **Web search** on one under-covered category.

## Instructions

1. **Read the agent prompt** for `[SEED_SOURCE]` and `[OUTPUT_FOLDER]`
2. **Read `[OUTPUT_FOLDER]/SCOPE.md`** - the boundary
3. **Read `[OUTPUT_FOLDER]/REJECTIONS.md`** - clusters already declined
4. **Read `{{AUTORUN_FOLDER}}/MARKET_ANALYSIS.md`** - priority categories and targets
5. **Read `{{AUTORUN_FOLDER}}/BACKLOG.md`** - everything already discovered
6. **List existing cards**: `ls [OUTPUT_FOLDER]/Companies [OUTPUT_FOLDER]/Products [OUTPUT_FOLDER]/People [OUTPUT_FOLDER]/Capital`
7. **Work the feeds in order** and apply the scope test to each candidate
8. **Append survivors to `BACKLOG.md`** with `Status: DISCOVERED`

## Discovery Checklist

- [ ] **Discover entities (or mark all covered)**: Read the files above. Build
  the set of names already known: every entry in `BACKLOG.md` plus every
  card filename in the vault. Then:

  **Feed 1 - gaps.** If `{{AUTORUN_FOLDER}}/SWEEP_GAPS.md` has entries not
  marked `queued`, take up to 5 of them, apply the scope test, append the
  survivors to `BACKLOG.md` as `DISCOVERED`, and mark each gap line
  `queued` (or `declined - reason`). If this yields 3 or more survivors,
  you are done for this loop.

  **Feed 2 - seed.** If `[SEED_SOURCE]` is configured and `BACKLOG.md`
  does not yet contain the line `<!-- seed mined -->`, read or fetch the
  seed source, extract every entity name it contains, apply the scope test
  to each, append survivors (there may be many - that is fine, this is the
  one loop where a large batch is correct), and append `<!-- seed mined -->`
  to `BACKLOG.md`. You are done for this loop.

  **Feed 3 - search.** Read the priority categories and target counts from
  `MARKET_ANALYSIS.md`. Count how many `BACKLOG.md` entries (any status
  except declined) fall under each. If every priority category has reached
  its target, append `## ALL_CATEGORIES_COVERED` to `BACKLOG.md` if it is
  not already there and mark this task complete. Otherwise pick the ONE
  category furthest below target, use web search to find 5-8 candidates
  that are not already known, apply the scope test to each, and append
  survivors and declines.

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

Append to `{{AUTORUN_FOLDER}}/BACKLOG.md`. Create the file with the header
below if it does not exist.

```markdown
# Research Backlog

Every entity ever surfaced for this vault, with its current status. Entries are
never deleted; their status changes. One entry per entity, keyed on the
canonical name that will become the card filename.

<!-- status flow: DISCOVERED -> PENDING | SKIP -> RESEARCHED -->

---

## [Feed or Category] - Discovered [YYYY-MM-DD], loop [N]

### [Entity Name 1]
- **Type:** [Company | Product | Person | Capital | DomainEntity]
- **Category:** [category from MARKET_ANALYSIS.md, if known]
- **Brief:** [one sentence]
- **Why Notable:** [why it matters in this market]
- **Scope:** in | borderline
- **Scope Note:** [required when borderline: which part is in, which is out]
- **Discovery Source:** [URL, "seed", or "gap: named by [[Card]]"]
- **Status:** DISCOVERED

### Declined

#### [Candidate Name]
- **Reason:** [which side of the antonym pair, and why]
- **Cluster:** [name, if this is the 3rd+ of a pattern - then log it in REJECTIONS.md]

### Discovery Summary
- **Feed:** gaps | seed | search
- **Category:** [category researched, if search]
- **Found:** [count]   **Declined:** [count]
- **Search Queries Used:**
  - "[query 1]"
- **New rejection clusters logged:** [names, or none]
```

## Entity Status Values

| Status | Set by | Meaning |
|--------|--------|---------|
| `DISCOVERED` | 2_DISCOVER | In scope, not yet scored |
| `PENDING` | 3_EVALUATE | Scored, worth researching, awaiting a depth loop |
| `SKIP` | 3_EVALUATE | In scope but not worth the research effort |
| `RESEARCHED` | 4_RESEARCH | Card exists in the vault |
| `DUPLICATE` | any | Already covered under another entity |

Note that **out of scope is not a status.** Those candidates never enter the
list; they go in the `Declined` section. Status is about research effort, scope
is about membership, and keeping them separate is what stops the vault drifting.

## Guidelines

- **Gaps before search** - an entity an existing card already names is worth
  more than a new stranger, because carding it creates an edge
- **Never re-add a known name** - check the backlog and the vault filenames,
  including near-duplicates ("Acme" vs "Acme Inc")
- **Record the declines** - a decline with a reason is reusable; a silent skip
  gets rediscovered next loop
- **Include the discovery source** - enables verification later
- **Diversify within the category** - leaders, challengers and emerging players

## How to Know You're Done

**Option A - Discovered entities:** you worked the first feed that had
something in it, applied the scope test to each candidate, and appended
survivors and declines to `BACKLOG.md`.

**Option B - All categories covered:** the gap file is drained, the seed is
mined, every priority category has reached its target, and
`## ALL_CATEGORIES_COVERED` is present in `BACKLOG.md`.
