# Market Research Playbook

A systematic Auto Run playbook for building a **queryable knowledge corpus** about
any market using web research.

## Overview

This playbook creates an automated pipeline that:

1. **Configures** and validates the target market, and establishes a scope boundary
2. **Initializes** the vault with folder structure, agents, commands and a validator
3. **Analyzes** the market to fix the schema and author the taxonomy spine
4. **Discovers** entities, applying the scope test before any candidate is recorded
5. **Evaluates** each entity on two independent axes: membership and priority
6. **Researches** entities, alternating between depth and breadth
7. **Loops** until the work is done, the budget is spent, or the corpus needs repair

The output is an **Obsidian-compatible vault** where YAML frontmatter is the
database and the markdown body is the argument for what the frontmatter asserts.

## What makes this different from a folder of research documents

Two design choices do most of the work:

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

## Requirements

### Custom Agent Prompt Required

**This playbook requires a custom agent prompt.** Configure `Agent-Prompt.md` and
set your Maestro agent to use its contents.

`0_CONFIGURE.md` refuses to run while `MARKET_TOPIC` is still at its `<UNSET>`
default, so a forgotten configuration costs you nothing rather than thirty loops
of research into the wrong subject.

### Web Search Access

This playbook relies heavily on web search. Ensure your agent has it enabled.

### Python 3 with PyYAML

Needed by `Tools/health_check.py`. If it is missing the research still runs; it
just runs unvalidated, and `0_CONFIGURE` records that as a degradation.

```bash
pip install pyyaml
```

## Configuration

Everything the playbook needs is set in `Agent-Prompt.md`:

| Value | Required | Purpose |
|-------|----------|---------|
| `MARKET_TOPIC` | **yes** | The market to research. Narrow beats broad. |
| `SCOPE_IN` | recommended | One sentence: what belongs in the vault |
| `SCOPE_OUT` | recommended | One sentence: the adjacent market that does not |
| `DOMAIN_ENTITY` | optional | The market-specific entity type, if it has one |
| `SEED_SOURCE` | optional | A curated artifact to start from |
| `OUTPUT_FOLDER` | yes | Where the vault is written |
| `MAX_ENTITIES` | yes | Run budget. Defaults to 60 |
| `DEPTH_SWITCH_AT` | yes | Loop at which breadth starts. Defaults to 25 |

Leaving `SCOPE_IN` and `SCOPE_OUT` unset is allowed: `0_CONFIGURE` proposes a
pair from its own market survey, writes it to `SCOPE.md` marked
`status: agent-proposed`, and tells you it did so. Setting them yourself is
better, because the boundary is a judgment about what you want to know.

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

## Document Chain

| Document | Purpose | Reset on Completion? |
|----------|---------|---------------------|
| `Agent-Prompt.md` | Configuration | N/A |
| `0_CONFIGURE.md` | Validate config, establish scope, install tooling | No |
| `0_INITIALIZE.md` | Create vault structure, agents, commands | No |
| `1_ANALYZE.md` | Survey market, fix schema, author Categories | No |
| `2_DISCOVER.md` | Find entities, apply the scope test | No |
| `3_EVALUATE.md` | Score relevance, importance and effort | No |
| `4_RESEARCH.md` | Advance the vault: one entity, or one column sweep | No |
| `5_PROGRESS.md` | Gate: continue, repair, or exit | **Yes** |

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
├── Resources/                   # Reports, trends, technologies
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

## Generated Agents

| Agent | Purpose |
|-------|---------|
| `company-researcher` | Company profiles |
| `product-researcher` | Product and service profiles |
| `category-researcher` | The taxonomy spine |
| `person-researcher` | Key people |
| `capital-researcher` | Investors, in-scope portfolio only |
| `scope-validator` | Audit the corpus against the boundary and re-score |
| `trend-researcher` | Market trend analyzes |

## Assets

The `assets/` folder bundles two files that `0_CONFIGURE` copies into the vault:

| Asset | Purpose |
|-------|---------|
| `assets/health_check.py` | Config-driven corpus validator. No market-specific logic |
| `assets/kb.yaml` | Schema template. `1_ANALYZE` fills it in for the market |

`health_check.py` enforces fifteen rules: required and universal fields, relevance
type and range, enum membership, date format and future dates, integer currency,
typed-relation resolution, bidirectional mirror agreement, event-state
consistency, funding consistency, orphan detection, normalized duplicate-name
detection, and staleness. It reports a **relevance distribution** (the scope-drift
signal) and a **field-coverage table** (the sweep queue).

```bash
python3 Tools/health_check.py                 # summary
python3 Tools/health_check.py --report Resources/
python3 Tools/health_check.py --json
python3 Tools/health_check.py --dedup         # near-duplicate names only
python3 Tools/health_check.py --fail-on critical   # non-zero exit
```

## The Two Scores

| Score | Question | Lives | Range |
|-------|----------|-------|-------|
| `relevance` | Does this **belong**? | On the card, permanently | 0-100 |
| `importance` | Spend effort here **next**? | In the run plan, discarded after | CRITICAL..LOW |

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

## Depth and Breadth

`4_RESEARCH` alternates between two modes, and the alternation is the point.

A vault built only by researching one entity at a time ends up with the first
twenty cards excellent, the next fifty adequate, and the rest stubs. You cannot
compare across a corpus shaped like that.

| | Depth | Breadth |
|---|-------|---------|
| Unit | One entity, all fields | One field, all entities |
| Produces | A new card | Uniform coverage |
| Gaps after | Invisible | Countable empty fields |

`DEPTH_SWITCH_AT` sets when breadth starts. After that, `4_RESEARCH` reads the
field-coverage table from `health_check.py` and sweeps the lowest-coverage field.

## Loop Control

`5_PROGRESS` gates on three things rather than one:

```text
IF health_check reports CRITICAL issues      -> CONTINUE (repair before growing)
ELSE IF researched >= MAX_ENTITIES           -> EXIT (budget spent)
ELSE IF PENDING CRITICAL/HIGH entities       -> CONTINUE (research)
ELSE IF any field below 90% coverage         -> CONTINUE (sweep)
ELSE IF categories not all covered           -> CONTINUE (discover)
ELSE                                         -> EXIT (done)
```

**Why a budget.** Market research has no natural completion state - discovery
always surfaces one more medium-importance company. Without a ceiling the
priority ranking never actually constrains anything and the run ends wherever
Max Loops happens to stop it.

**Why integrity gates first.** A vault with broken typed relations is not a
smaller vault, it is a vault that returns wrong answers. Repair outranks growth,
and it outranks the budget.

## Recommended Setup

### In Maestro Batch Runner

```text
Loop Mode: ON
Max Loops: 20-30
Documents:
  0_CONFIGURE.md  [Reset: OFF]  <- validates config, halts if unconfigured
  0_INITIALIZE.md [Reset: OFF]  <- runs once
  1_ANALYZE.md    [Reset: OFF]
  2_DISCOVER.md   [Reset: OFF]
  3_EVALUATE.md   [Reset: OFF]
  4_RESEARCH.md   [Reset: OFF]
  5_PROGRESS.md   [Reset: ON]   <- resets 1-4 only
```

### Agent Prompt Configuration

**Critical**: set your Maestro agent to use the contents of `Agent-Prompt.md` as
its system prompt, after configuring the values in it.

## Working Documents (per loop)

- `MARKET_CONFIG.md` - resolved configuration, written once by `0_CONFIGURE`
- `LOOP_N_MARKET_ANALYSIS.md` - market overview and schema decisions
- `LOOP_N_ENTITIES.md` - discovered entities, and declined candidates with reasons
- `LOOP_N_PLAN.md` - scored research targets
- `SWEEP_GAPS.md` - entities surfaced mid-sweep that need cards
- `RESEARCH_LOG_{{AGENT_NAME}}_{{DATE}}.md` - cumulative log

## Entity Status Values

| Status | Meaning |
|--------|---------|
| `PENDING` | In scope, awaiting research |
| `RESEARCHED` | Full profile created |
| `SKIP` | In scope but not worth the effort |
| `DUPLICATE` | Covered under another entity |

Out-of-scope is **not** a status. Those candidates never enter the list - they go
in the `Declined` section of `LOOP_N_ENTITIES.md` with a reason, and once three
share a reason they become a cluster entry in `REJECTIONS.md`.

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
2. **Give it a seed source.** Starting from a curated artifact beats starting cold.
3. **Review after `0_CONFIGURE`.** It prints the boundary before any card exists.
   That is the cheap moment to correct it.
4. **Check `LOOP_1_MARKET_ANALYSIS.md`** before letting the loop run long.
5. **Watch the mean relevance** across loops. Falling means the boundary is eroding.
6. **Run `/health-check` yourself** at any point. The field-coverage table tells
   you what the vault does not yet know.
7. **Low scores are a queue, not a verdict.** Cards below 30 are an agenda item.

## Customization

### Changing entity types

Edit the `entities` block in `assets/kb.yaml`. The validator has no hardcoded
types, so adding one there is enough for it to be checked.

### Changing the event ledger

Set the `ledger` block in `kb.yaml` to the event class that drives your market:
approvals, licenses, contract awards, certifications. Delete the block if none
applies.

### Adjusting coverage targets

Set target counts in the market analysis output, and `MAX_ENTITIES` in the agent
prompt.

### Adding custom agents

Add files to `Agents/` - they are discoverable via the `.claude/agents` symlink.
