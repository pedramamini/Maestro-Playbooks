# Market Research Playbook

A systematic Auto Run playbook for building a **queryable knowledge corpus** about
any market using web research.

## Overview

This playbook creates an automated pipeline that:

1. **Configures** and validates the target market, and establishes a scope boundary
2. **Initializes** the vault with folder structure, agents, commands and a validator
3. **Analyzes** the market once, fixes the schema and authors the taxonomy spine
4. **Discovers** entities from three feeds, applying the scope test before any candidate is recorded
5. **Evaluates** every waiting entity on two independent axes: membership and priority
6. **Researches** in batches, alternating depth (new cards) with breadth (one field across all cards)
7. **Loops** until the work is done, the budget is spent, or the corpus needs repair

The output is an **Obsidian-compatible vault** where YAML frontmatter is the
database and the markdown body is the argument for what the frontmatter asserts.

## What makes this different from a folder of research documents

Three design choices do most of the work:

**A scope boundary, stated as an antonym pair.** Every market has a confusable
adjacent market that shares its vocabulary. Over twenty or thirty research loops,
a pipeline with no stated boundary absorbs that neighbor one individually
defensible entity at a time, until the vault is a generic industry list that
answers no question better than a web search does. The boundary is configured (or
proposed and flagged for review) before a single card exists.

**A relevance score, separate from research priority.** Importance answers
"should I spend effort here". Relevance answers "does this belong at all". They
are orthogonal: an out-of-scope company can be genuinely CRITICAL to its own
market. With only one axis, nothing stops it being researched into your vault
with a HIGH rating attached. With two, the boundary becomes auditable, borderline
entities can stay in at 50-69 rather than forcing a keep-or-kill decision, and
scope drift becomes a measurable number rather than a feeling.

**The graph grows from its own edges.** A company card names its founders and
investors before they have cards. Those names land in `SWEEP_GAPS.md`, discovery
drains that file before it searches the web, and the next depth loop cards them.
Every person and fund in the finished vault is there because something already
in the vault pointed at it. That is what makes it interconnected rather than
merely large.

## How to run it

### 1. Install

From the Playbook Exchange inside Maestro, or copy `Research/Market/` (including
`assets/`) into your agent's Auto Run folder.

### 2. Tell it the market

**All configuration lives in the Auto Run prompt** - the text box in the Auto
Run panel, which the Exchange pre-fills with `Agent-Prompt.md`. Nothing in the
numbered documents needs editing. Replace every `<UNSET ...>` value:

| Value | Required | Purpose |
|-------|----------|---------|
| `MARKET_TOPIC` | **yes** | The market to research. Narrow beats broad. |
| `SCOPE_IN` | recommended | One sentence: what belongs in the vault |
| `SCOPE_OUT` | recommended | One sentence: the adjacent market that does not |
| `DOMAIN_ENTITY` | optional | The market-specific entity type, if it has one |
| `SEED_SOURCE` | optional | A curated artifact to start from |
| `OUTPUT_FOLDER` | yes | Where the vault is written. Defaults into the Auto Run folder |
| `MAX_ENTITIES` | yes | Run budget, counted from the vault. Default 60 |
| `DEPTH_BATCH` | yes | Entities per depth loop. Default 3 |
| `SWEEP_EVERY` | yes | Every Nth loop is a breadth sweep. Default 4 |
| `COVERAGE_TARGET` | yes | Field coverage percentage required to exit. Default 90 |

If you are launching from the CLI instead of the panel, pass the edited prompt
with `--prompt "$(cat Agent-Prompt.md)"`.

`0_CONFIGURE.md` refuses to run while `MARKET_TOPIC` is still `<UNSET>`, so a
forgotten configuration costs you nothing rather than thirty loops of research
into the wrong subject.

Leaving `SCOPE_IN` and `SCOPE_OUT` unset is allowed: `0_CONFIGURE` proposes a
pair from a short market survey, writes it to `SCOPE.md` marked
`status: agent-proposed`, and tells you it did so. Setting them yourself is
better, because the boundary is a judgment about what you want to know.

### 3. Set the loop

```text
Loop Mode: ON
Max Loops: 30
Documents:
  0_CONFIGURE.md  [Reset: OFF]  <- validates config, halts if unconfigured
  0_INITIALIZE.md [Reset: OFF]  <- runs once
  1_ANALYZE.md    [Reset: OFF]  <- real work once, two file checks after
  2_DISCOVER.md   [Reset: OFF]
  3_EVALUATE.md   [Reset: OFF]
  4_RESEARCH.md   [Reset: OFF]
  5_PROGRESS.md   [Reset: ON]   <- resets 1-4 only
```

With the defaults, 30 loops is roughly 22 depth loops (up to 66 cards, capped
at 60) and 8 or more sweeps. The run exits on its own when the backlog is empty
or the budget is spent **and** every tracked field meets `COVERAGE_TARGET`
**and** the validator reports zero CRITICAL issues.

### 4. Review after the first loop

`0_CONFIGURE` prints the boundary before any card exists. That is the cheap
moment to correct it. `MARKET_ANALYSIS.md` and the first Category cards are the
second checkpoint.

### Writing a good antonym pair

State what is in, and the specific near-miss that is out. The out side should be
a real, well-funded market that sounds like yours.

| Market | IN | OUT |
|--------|----|----|
| Carbon technology | Carbon removal - net-negative | Carbon reduction - less-positive |
| Clinical software | Systems informing a diagnosis | Systems managing scheduling and billing |
| Robotics | General-purpose manipulation | Fixed-function industrial automation |
| Payments | Regulated money-movement infrastructure | Consumer apps built on top of it |

If your "out" sentence describes something obviously irrelevant, you have not
found the real boundary yet. The test is usually which party is the beneficiary,
or which asset is the one being served - never which words appear on the homepage.

## Requirements

- **Web search** enabled on the agent. The playbook is nothing without it.
- **Python 3 with PyYAML** for `Tools/health_check.py`. `0_CONFIGURE` tries
  `pip3 install pyyaml` once; if that fails the research still runs, unvalidated,
  and the degradation is recorded.

## Document Chain

| Document | Purpose | Runs | Reset on Completion? |
|----------|---------|------|---------------------|
| `Agent-Prompt.md` | Configuration (the Auto Run prompt) | - | N/A |
| `0_CONFIGURE.md` | Validate config, establish scope, install tooling | Once | No |
| `0_INITIALIZE.md` | Create vault structure, agents, commands | Once | No |
| `1_ANALYZE.md` | Survey market, fix schema, author Categories | Once (self-skips after) | No |
| `2_DISCOVER.md` | Drain gaps, mine the seed, or search one category | Every loop | No |
| `3_EVALUATE.md` | Score every waiting entity: relevance, importance, effort | Every loop | No |
| `4_RESEARCH.md` | Repair, depth batch, or column sweep | Every loop | No |
| `5_PROGRESS.md` | Gate: continue, repair, or exit | Every loop | **Yes** |

## Durable State

Nothing is carried in memory between tasks. Every document reads these first
and appends to them after. All live in the Auto Run folder unless noted.

| File | Holds |
|------|-------|
| `MARKET_CONFIG.md` | Resolved configuration, written once |
| `MARKET_ANALYSIS.md` | Market survey, targets per entity type, schema decisions |
| `BACKLOG.md` | Every entity ever discovered: `DISCOVERED` → `PENDING` / `SKIP` → `RESEARCHED` |
| `SWEEP_GAPS.md` | Names a card references that have no card yet. Discovery feed #1 |
| `RESEARCH_LOG.md` | What each loop did, plus `KNOWN_ISSUES` the validator cannot resolve |
| `PROGRESS_LOG.md` | One row per loop: counts, coverage, mean relevance, decision |
| `SCOPE.md` (vault) | The boundary |
| `REJECTIONS.md` (vault) | Clusters declined, with reasons, so they are declined for free next time |
| `kb.yaml` (vault) | Schema driving the validator |

## Generated Vault Structure

```text
vault/
├── .claude/
│   ├── agents -> ../Agents
│   └── commands -> ../Commands
├── Agents/                      # Seven research agents
├── Commands/                    # /research, /health-check, /scope-audit
├── Tools/
│   └── health_check.py          # Corpus validator
├── Companies/
├── Products/
├── Categories/                  # The taxonomy spine
├── People/
├── Capital/
├── [DomainEntity]/              # If the market has one
├── Resources/                   # Trends/, health check reports, Market Map, ledger
├── SCOPE.md                     # The boundary
├── REJECTIONS.md                # Declined clusters, with rationale
├── kb.yaml                      # Schema driving the validator
├── INDEX.md
└── CLAUDE.md
```

### Entity types

Five are generic to every market, plus one optional market-specific type:

| Type | Why it exists |
|------|---------------|
| **Companies** | The primary node |
| **Products** | One card each. Companies ship 2-5x more than their homepage shows |
| **Categories** | The comparison spine. Without it you have a list, not a map |
| **People** | The value is the talent-flow edge, not the biography |
| **Capital** | In-scope portfolio subset only, or the co-investment signal is lost |
| **[DomainEntity]** | Whatever this market cannot be described without |

Naming the domain entity is what separates a modeled market from a copied
template: a `Clearance` for medical devices, a `Charter` for regulated finance, a
`Trial` for pharma, a `Standard` for industrial, a `Contract Vehicle` for public
sector. `none` is a valid answer.

Trends are **documents**, not entities. They live in `Resources/Trends/` with
`[[wikilinks]]` to the cards they discuss, and the validator ignores them.

## Generated Agents

| Agent | Purpose |
|-------|---------|
| `company-researcher` | Company profiles |
| `product-researcher` | Product and service profiles |
| `category-researcher` | The taxonomy spine |
| `person-researcher` | Key people |
| `capital-researcher` | Investors, in-scope portfolio only |
| `scope-validator` | Audit the corpus against the boundary and re-score |
| `trend-researcher` | Dated trend analyses in `Resources/Trends/` |

## Assets

The `assets/` folder bundles two files that `0_CONFIGURE` copies into the vault:

| Asset | Purpose |
|-------|---------|
| `assets/health_check.py` | Config-driven corpus validator |
| `assets/kb.yaml` | Schema template. `1_ANALYZE` fills it in for the market |

`health_check.py` enforces: required and universal fields, relevance type and
range, enum membership, date format and future dates, integer currency,
typed-relation resolution (hard relations CRITICAL, soft relations MEDIUM),
bidirectional mirror agreement, event-state consistency for whatever ledger
`kb.yaml` declares, funding consistency, orphan detection, normalized
duplicate-name detection, and staleness. It reports a **relevance
distribution** (the scope-drift signal), a **field-coverage table** (the sweep
queue), and a **budget count** (cards that count against `MAX_ENTITIES`).

```bash
python3 Tools/health_check.py                      # summary
python3 Tools/health_check.py --report Resources/  # dated markdown report
python3 Tools/health_check.py --json               # machine-readable
python3 Tools/health_check.py --dedup              # near-duplicate names only
python3 Tools/health_check.py --fail-on critical   # non-zero exit
```

Exit codes: 0 clean, 1 issues at or above `--fail-on`, 2 configuration error
(missing PyYAML, invalid `kb.yaml`, a relation targeting a type you removed).
The validator has no market-specific logic; the ledger's field names and state
values all come from `kb.yaml`, so a pharma approvals ledger or a licensing
ledger validates the same way the shipped M&A one does.

### Hard and soft relations

| | Hard | Soft |
|---|---|---|
| Examples | product → company, product → category, person → company | founders, investors, category leaders, acquirer |
| Target has no card | CRITICAL, fixed this loop | MEDIUM, logged to `SWEEP_GAPS.md` |
| Why | The card is meaningless without it | The name is how the target gets discovered |

Soft relations are declared with `soft: true` in `kb.yaml`. They are the reason
the run can name a founder on loop 3 and card them on loop 7 without ever
writing a stub.

## The Two Scores

| Score | Question | Lives | Range |
|-------|----------|-------|-------|
| `relevance` | Does this **belong**? | On the card, permanently | 0-100 |
| `importance` | Spend effort here **next**? | In `BACKLOG.md`, discarded after | CRITICAL..LOW |

### Relevance bands

| Band | Meaning |
|------|---------|
| 90-100 | Core. Unambiguously the in-scope side |
| 70-89 | Strong. Minor ambiguity, may carry an adjacent line |
| 50-69 | Mixed. Straddles the line - and belongs in the vault |
| 30-49 | Adjacent. In-scope claims read as feature or marketing |
| 0-29 | Out. Keep only as context; flag for removal |

Every score requires a written justification in `relevance_notes`. A bare score
is worthless three weeks later, when nobody can reconstruct whether 65 meant
"borderline but leaning in" or "we had no information".

## Depth, Breadth and Repair

`4_RESEARCH` picks one of three modes each loop:

```text
IF validator reports CRITICAL           -> REPAIR  (fix everything flagged)
ELSE IF loop is a multiple of SWEEP_EVERY -> BREADTH (lowest-coverage field, all cards)
ELSE IF budget left AND backlog has PENDING -> DEPTH  (up to DEPTH_BATCH new cards)
ELSE IF coverage below target           -> BREADTH
ELSE                                    -> nothing to do
```

A vault built only by researching entities ends up with the first twenty cards
excellent, the next fifty adequate, and the rest stubs, with every founder a
dangling name. Sweeps fix the columns; the gap feed fixes the names.

| | Depth | Breadth |
|---|-------|---------|
| Unit | Up to `DEPTH_BATCH` entities, all fields | One field, all entities |
| Produces | New cards, and new names in `SWEEP_GAPS.md` | Uniform coverage |
| Gaps after | Invisible | Countable empty fields |

## Loop Control

`5_PROGRESS` gates on integrity, then work, then budget:

```text
IF validator exit 2 (config error)            -> CONTINUE (repair kb.yaml)
ELSE IF CRITICAL issues (minus KNOWN_ISSUES)  -> CONTINUE (repair)
ELSE IF budget left AND anything waiting      -> CONTINUE (research)
     (PENDING, DISCOVERED, unqueued gaps, or categories not yet covered)
ELSE IF any field below COVERAGE_TARGET       -> CONTINUE (sweep)
ELSE                                          -> EXIT (finalize)
```

Two guards stop it spinning: a CRITICAL issue that survives three repair loops
is recorded under `KNOWN_ISSUES` and no longer gates; a field stuck at the same
coverage for three loops is moved to `coverage_exclude`.

**Why a budget.** Market research has no natural completion state - discovery
always surfaces one more medium-importance company. Without a ceiling the
priority ranking never actually constrains anything and the run ends wherever
Max Loops happens to stop it.

**Why integrity gates first.** A vault with broken typed relations is not a
smaller vault, it is a vault that returns wrong answers. Repair outranks growth,
and it outranks the budget.

## What you get on exit

- `INDEX.md` with every card linked and a research summary
- `Resources/Market Map.md` - every category with its products and their companies
- `Resources/[Event] Ledger.md` - time-ordered events, final separated from reported
- `Resources/Relevance Review.md` - cards below 30, for a human decision
- `Resources/health_check_YYYY-MM-DD.md` - the final integrity report

## After the run

The vault is maintained, not just built. `/health-check` prints the work queue;
`/scope-audit` spawns the `scope-validator` agent to re-score cards against the
boundary, because companies reposition and nothing else notices. `/research
<entity>` adds one card by hand through the same agents the playbook used.

## Entity Status Values

| Status | Meaning |
|--------|---------|
| `DISCOVERED` | In scope, not yet scored |
| `PENDING` | Scored, worth researching, awaiting a depth loop |
| `RESEARCHED` | Card exists in the vault |
| `SKIP` | In scope but not worth the effort |
| `DUPLICATE` | Covered under another entity |

Out-of-scope is **not** a status. Those candidates never enter the backlog - they
go in the `Declined` section with a reason, and once three share a reason they
become a cluster entry in `REJECTIONS.md`.

## Example Markets

- **Technology**: "AI Code Assistants", "Kubernetes Platforms", "No-Code Tools"
- **Consumer**: "Plant-Based Foods", "Smart Home Devices", "Electric Vehicles"
- **B2B**: "Sales Enablement Software", "HR Tech", "Freight Brokerage"
- **Emerging**: "Carbon Capture", "Quantum Computing", "Synthetic Biology"
- **Regulated**: "Digital Health Records", "Insurance Claims Automation"

Narrow markets yield better vaults than broad ones. "Enterprise Kubernetes
Platforms" produces a sharper corpus than "Cloud Infrastructure".

## Tips

1. **Write the scope pair yourself.** It is the highest-leverage ten minutes in
   the whole run.
2. **Give it a seed source.** Starting from a curated artifact beats starting cold,
   and the seed loop is the one place a large discovery batch is correct.
3. **Review after `0_CONFIGURE`.** It prints the boundary before any card exists.
4. **Check `MARKET_ANALYSIS.md`** and the Category cards before letting the loop run long.
5. **Watch the mean relevance** in `PROGRESS_LOG.md`. Falling means the boundary is eroding.
6. **Run `/health-check` yourself** at any point. The field-coverage table tells
   you what the vault does not yet know.
7. **Low scores are a queue, not a verdict.** Cards below 30 are an agenda item.

## Customization

### Changing entity types

Edit the `entities` block in `kb.yaml`. The validator has no hardcoded types.
If you remove a type, remove the relations that target it too - the validator
tells you which ones.

### Changing the event ledger

Set the `ledger` block in `kb.yaml` to the event class that drives your market:
approvals, licenses, contract awards, certifications. Every field name and
state value is configurable; the comment above the block shows a pharma
example. Delete the block if none applies.

### Adjusting pace and budget

`MAX_ENTITIES`, `DEPTH_BATCH`, `SWEEP_EVERY` and `COVERAGE_TARGET` in the agent
prompt; target counts per entity type in `MARKET_ANALYSIS.md`.

### Adding custom agents

Add files to `Agents/` - they are discoverable via the `.claude/agents` symlink.
