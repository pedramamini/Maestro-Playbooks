# Entity Evaluation - Score Membership, Then Priority

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Score every `DISCOVERED` entity in the backlog on **two independent axes** and
promote it to `PENDING` or `SKIP`.

| Axis | Question | Where it lives |
|---|---|---|
| **Relevance** (0-100) | Does this **belong** in the vault? | On the card, permanently |
| **Importance** (CRITICAL..LOW) | Should effort go here **next**? | In `BACKLOG.md`, discarded after |

These are orthogonal and conflating them is the most common way a research vault
goes wrong. An out-of-scope company can be genuinely CRITICAL to its own market;
without a separate membership score, nothing prevents it being researched into
your vault with a HIGH rating attached and never questioned again.

Scoring is cheap compared to research - a couple of searches per entity, no
card written - so this document scores **everything that is waiting**, not one
entity. Discovery adds three to eight names per loop and the seed feed may add
dozens; a one-per-loop evaluator would leave most of them unscored forever.

## Instructions

1. **Read the agent prompt** for `[OUTPUT_FOLDER]`
2. **Read `[OUTPUT_FOLDER]/SCOPE.md`** - the boundary
3. **Read `{{AUTORUN_FOLDER}}/BACKLOG.md`** and collect every entry with `Status: DISCOVERED`
4. **Score each one: relevance, then importance, then effort**
5. **Rewrite each entry in place** with the scores and the new status

## Evaluation Checklist

- [ ] **Evaluate all DISCOVERED entities (or skip if none)**: Read
      `{{AUTORUN_FOLDER}}/BACKLOG.md`. If no entry has `Status: DISCOVERED`,
      mark this task complete without changes. Otherwise, for each such entry
      (cap at 25 per loop; leave the rest `DISCOVERED` for next loop): score
      relevance against `SCOPE.md` with a written justification, assess
      importance and research effort, apply the decision matrix, and edit the
      entry in place to add the `Evaluation` block and set the status to
      `PENDING` or `SKIP`. Keep the entry's original discovery fields intact.

## Axis 1: Relevance (scope membership)

Score every entity 0-100 against the antonym pair in `SCOPE.md`, and write a
justification naming the specific evidence and the specific doubt.

| Band | Classification | Meaning |
|------|---------------|---------|
| **90-100** | Core | Unambiguously the in-scope side. Primary business, whole product line. |
| **70-89** | Strong | Clearly in scope with minor ambiguity. May carry an adjacent line alongside. |
| **50-69** | Mixed | Straddles the line. Real business on both sides, or positioning genuinely unclear. |
| **30-49** | Adjacent | Primarily the out-of-scope side; in-scope claims read as feature or marketing. |
| **0-29** | Out | Not in scope. Keep only as market context, and flag for removal. |

### Why this matters

- The boundary becomes **auditable** - sort by score and the edge is visible
- Borderline entities can **stay in** at 50-69 instead of forcing keep-or-kill
- A **review queue** falls out for free: everything under 30
- **Drift becomes measurable** - a falling mean across loops is a number, not a
  feeling. `health_check.py` reports the distribution for exactly this reason

### Writing the justification

`relevance_notes` is not optional and not a formality. A bare score is worthless
three weeks later, when nobody can reconstruct whether 65 meant "borderline but
leaning in" or "we had no information".

```yaml
relevance: 95
relevance_notes: "Entire product line addresses the in-scope problem. No
  adjacent business. Founded specifically for this."

relevance: 62
relevance_notes: "Established vendor from the adjacent market that added an
  in-scope line in 2024, roughly one of five product families. Retained because
  it is the largest incumbent crossing the boundary and its pricing sets the
  ceiling for the category."

relevance: 25
relevance_notes: "Uses in-scope vocabulary in marketing but the product serves
  the out-of-scope beneficiary. Candidate for removal; kept one cycle because
  two tracked companies name it as a competitor."
```

### Scoring discipline

- Score at evaluation, never later. An unscored card is an unreviewed card.
- **Do not cluster at 80.** If most scores land 78-85 you are not using the
  scale, you are using a binary with extra steps.
- A score below 30 is an agenda item, not a verdict. It comes up with evidence,
  or the card comes out.

## Axis 2: Importance (research priority)

| Level | Description |
|-------|-------------|
| **CRITICAL** | Defines the space. Every conversation about this market names them. |
| **HIGH** | Significant player. Materially changes the picture. |
| **MEDIUM** | Adds depth. |
| **LOW** | Completeness only. |

Factors: market share or influence, innovation leadership, growth trajectory,
analyst attention, interconnectedness with other entities. **An entity that
arrived via `SWEEP_GAPS.md` is already connected** - it is named by a card in
the vault - so it starts at MEDIUM and goes up from there, never down to LOW.

## Axis 3: Research Effort

| Level | Description |
|-------|-------------|
| **EASY** | Public company or well documented. Abundant sources. |
| **MEDIUM** | Decent coverage, needs synthesis across several sources. |
| **HARD** | Private, thin coverage, requires digging. |
| **VERY HARD** | Stealth or near-silent. May not be researchable at all. |

Factors: availability of public information, quality of the company's own site
and docs, press coverage, executive visibility, complexity of the entity.

## Output Format

Edit the entity's existing entry in `{{AUTORUN_FOLDER}}/BACKLOG.md`: change the
`Status` line and append this block beneath the discovery fields.

```markdown
- **Status:** PENDING

#### Evaluation - [YYYY-MM-DD], loop [N]
- **Relevance:** [0-100]
- **Relevance Notes:** [the justification that will go on the card verbatim]
- **Importance:** [CRITICAL | HIGH | MEDIUM | LOW] - [one line why]
- **Effort:** [EASY | MEDIUM | HARD | VERY HARD] - [one line why]
- **Key Questions:**
  1. [question the research should answer]
  2. [question]
- **Expected Relations:** `[field]:` [[Entity A]]; `[field]:` [[Entity B]]
- **Decision:** [matrix row, e.g. ">= 50 / HIGH / MEDIUM -> PENDING"]
```

For `SKIP`, the same block with `- **Status:** SKIP - [reason]`.

## Status Decision Matrix

Relevance gates first. An entity that does not belong is not researched however
important it is to somebody else's market.

| Relevance | Importance | Effort | Status |
|-----------|------------|--------|--------|
| **< 30** | any | any | `SKIP - out of scope` (log the cluster if it is the 3rd) |
| 30-49 | CRITICAL/HIGH | EASY | `PENDING` - context only, keep it brief |
| 30-49 | anything else | any | `SKIP - adjacent, effort exceeds value` |
| >= 50 | CRITICAL | any | `PENDING` - must research |
| >= 50 | HIGH | EASY/MEDIUM/HARD | `PENDING` - worth the effort |
| >= 50 | HIGH | VERY HARD | `PENDING - MANUAL REVIEW` - may need human help |
| >= 50 | MEDIUM | EASY/MEDIUM | `PENDING` - good value |
| >= 50 | MEDIUM | HARD/VERY HARD | `SKIP - effort exceeds value` |
| >= 50 | LOW | EASY | `PENDING` - if budget permits |
| >= 50 | LOW | MEDIUM+ | `SKIP - low priority` |

`4_RESEARCH` works `PENDING` entries in importance order, so a LOW entity is
only researched once nothing above it is waiting.

## Guidelines

- **Score relevance first** - it gates everything else
- **Be honest about effort** - do not underestimate research difficulty
- **Think about connections** - highly connected entities add more value
- **Note key questions** - they guide the research phase
- **Identify sources upfront** - saves time later
- **Do not research** - two or three searches to score is the ceiling. The card
  is written in `4_RESEARCH`

## How to Know You're Done

**Option A - Evaluated:** every `DISCOVERED` entry (up to the cap) now reads
`PENDING` or `SKIP` with an `Evaluation` block.

**Option B - Nothing to evaluate:** `BACKLOG.md` has no `DISCOVERED` entries.
Mark complete without changes.
