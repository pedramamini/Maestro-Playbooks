# Entity Evaluation - Score Membership, Then Priority

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Score one entity on **two independent axes** and add it to the research plan.

| Axis | Question | Where it lives |
|---|---|---|
| **Relevance** (0-100) | Does this **belong** in the vault? | On the card, permanently |
| **Importance** (CRITICAL..LOW) | Should effort go here **next**? | In the run plan, discarded after |

These are orthogonal and conflating them is the most common way a research vault
goes wrong. An out-of-scope company can be genuinely CRITICAL to its own market;
without a separate membership score, nothing prevents it being researched into
your vault with a HIGH rating attached and never questioned again.

## Instructions

1. **Read `[OUTPUT_FOLDER]/SCOPE.md`** - the boundary
2. **Read discovered entities** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_ENTITIES.md`
3. **Read the research plan** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`
4. **Select ONE unevaluated entity**
5. **Score relevance, then importance, then effort**
6. **Append to the research plan**

## Evaluation Checklist

- [ ] **Evaluate one entity (or skip if empty)**: Read
      `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_ENTITIES.md` for PENDING
      entities. If the file has no entities, or all are already evaluated in
      `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`, mark this task complete
      without changes. Otherwise pick ONE unevaluated entity. Score its
      relevance against `SCOPE.md`, then assess importance and research effort.
      Append the evaluation to the plan with the status from the decision matrix.

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
analyst attention, interconnectedness with other entities.

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

Append to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_PLAN.md`:

```markdown
---

## [Entity Name] - Evaluated [YYYY-MM-DD]

**Source:** [reference to the ENTITIES.md entry]
**Type:** [Company | Product | Category | Person | Capital | DomainEntity]
**Category:** [which category from the market analysis]

### Quick Profile
[2-3 sentences on what this entity is and does]

### Relevance (scope membership)
- **Score:** [0-100]
- **Notes:** [the justification that will go on the card verbatim]

### Importance Assessment
- **Rating:** [CRITICAL | HIGH | MEDIUM | LOW]
- **Justification:** [why]
- **Key Questions to Answer:**
  1. [question the research should answer]
  2. [question]

### Research Effort Assessment
- **Rating:** [EASY | MEDIUM | HARD | VERY HARD]
- **Justification:** [why]
- **Primary Sources Available:**
  - [source 1]
  - [source 2]

### Expected Connections
Typed relations this card will carry:
- `[field]:` [[Entity A]] - [relation meaning]
- `[field]:` [[Entity B]] - [relation meaning]

### Status: [PENDING | SKIP - reason]
```

## Status Decision Matrix

Relevance gates first. An entity that does not belong is not researched however
important it is to somebody else's market.

| Relevance | Importance | Effort | Status |
|-----------|------------|--------|--------|
| **< 30** | any | any | `SKIP - out of scope` (log the cluster if it is the 3rd) |
| 30-49 | CRITICAL/HIGH | EASY | `PENDING` - context only, keep it brief |
| 30-49 | anything else | any | `SKIP - adjacent, effort exceeds value` |
| >= 50 | CRITICAL | any | `PENDING` - must research |
| >= 50 | HIGH | EASY/MEDIUM | `PENDING` - high value, reasonable effort |
| >= 50 | HIGH | HARD | `PENDING` - worth the effort |
| >= 50 | HIGH | VERY HARD | `PENDING - MANUAL REVIEW` - may need human help |
| >= 50 | MEDIUM | EASY | `PENDING` - quick win |
| >= 50 | MEDIUM | MEDIUM | `PENDING` - good value |
| >= 50 | MEDIUM | HARD/VERY HARD | `SKIP - effort exceeds value` |
| >= 50 | LOW | EASY | `PENDING` - if budget permits |
| >= 50 | LOW | MEDIUM+ | `SKIP - low priority` |

## Guidelines

- **One entity per run** - thorough evaluation beats rushed assessment
- **Score relevance first** - it gates everything else
- **Be honest about effort** - do not underestimate research difficulty
- **Think about connections** - highly connected entities add more value
- **Note key questions** - they guide the research phase
- **Identify sources upfront** - saves time later

## How to Know You're Done

**Option A - Evaluated an entity:** exactly one entity scored on all three axes,
appended to the plan, with a status from the matrix.

**Option B - Nothing to evaluate:** `LOOP_{{LOOP_NUMBER}}_ENTITIES.md` has no
entities, or all are already in the plan. Mark complete without changes.

This graceful handling of empty states prevents the pipeline stalling when
discovery yields nothing.
