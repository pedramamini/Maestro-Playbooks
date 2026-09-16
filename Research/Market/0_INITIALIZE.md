# Initialize Research Vault

## Context
- **Playbook:** Market Research
- **Agent:** {{AGENT_NAME}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Purpose

This document initializes the research vault with the proper folder structure, creates entity-specific agents, and sets up Claude Code integration via `.claude/` with symlinks. **This runs once at the start before the main research loop begins.**

`0_CONFIGURE.md` has already run and validated the configuration, established the scope boundary in `SCOPE.md`, and installed the validator in `Tools/`. This document builds the rest of the vault around them.

## Instructions

1. **Read `{{AUTORUN_FOLDER}}/MARKET_CONFIG.md`** for the resolved configuration
2. **Create the vault folder structure** with visible Agents/ and Commands/ folders
3. **Set up .claude/ with symlinks** so Claude Code can discover agents and commands
4. **Generate entity-type agents** customized for the market topic
5. **Create the commands** for easy invocation
6. **Initialize INDEX.md** as the vault launch page

## Initialization Checklist

- [ ] **Initialize vault structure**: Read `MARKET_CONFIG.md` for the resolved MARKET_TOPIC, OUTPUT_FOLDER and DOMAIN_ENTITY. Create the vault folder structure including Agents/, Commands/, .claude/ with symlinks, and entity subfolders (including the DOMAIN_ENTITY folder if one was resolved). Generate entity-specific agents based on the market. Create initial INDEX.md and CLAUDE.md for the vault.

## Vault Structure to Create

```
[OUTPUT_FOLDER]/
├── .claude/
│   ├── agents -> ../Agents      # Symlink to Agents folder
│   └── commands -> ../Commands  # Symlink to Commands folder
├── Agents/                      # Visible in Obsidian, holds agent definitions
│   ├── company-researcher.md
│   ├── product-researcher.md
│   ├── category-researcher.md
│   ├── person-researcher.md
│   ├── capital-researcher.md
│   ├── scope-validator.md
│   └── trend-researcher.md
├── Commands/                    # Visible in Obsidian, holds slash commands
│   ├── research.md
│   ├── health-check.md
│   └── scope-audit.md
├── Tools/                       # From 0_CONFIGURE
│   └── health_check.py          # Corpus validator
├── Companies/                   # Company profiles
├── Products/                    # Product profiles
├── Categories/                  # Taxonomy spine - what makes comparison possible
├── People/                      # Key people profiles
├── Capital/                     # Investor profiles
├── [DomainEntity]/              # The market-specific type, if one was resolved
├── Resources/                   # Reports, data sources
├── SCOPE.md                     # The boundary (from 0_CONFIGURE)
├── REJECTIONS.md                # Declined clusters (from 0_CONFIGURE)
├── kb.yaml                      # Schema driving the validator
├── INDEX.md                     # Launch page
└── CLAUDE.md                    # Vault-specific Claude instructions
```

**On Technologies/ and Trends/**: earlier versions of this playbook created these as first-class entity folders. They are better served as documents in `Resources/` - a trend is an analysis with a date, not an entity with relations and a lifecycle, and treating it as one puts untyped nodes in the graph. `Categories/` and `Capital/` take their place as entity types, because a taxonomy bucket and an investor both have stable identity, typed relations and a reason to be compared against their peers.

## Create .claude/ with Symlinks

```bash
# Create .claude directory
mkdir -p [OUTPUT_FOLDER]/.claude

# Create symlinks (relative paths so they work if vault is moved)
cd [OUTPUT_FOLDER]/.claude
ln -s ../Agents agents
ln -s ../Commands commands
```

## Entity Agent Template

Create agents in `[OUTPUT_FOLDER]/Agents/` for each entity type:

### company-researcher.md
```markdown
---
name: company-researcher
description: Researches a company and creates a structured profile for the [MARKET_TOPIC] knowledge vault.
model: inherit
---

# Company Researcher Agent

**Purpose:** Research a specific company in the [MARKET_TOPIC] market and create a comprehensive profile.

## Input
- Company name to research
- Any known information (website, description, etc.)

## Process
1. **Web Search** - Gather information about the company:
   - Official website and about page
   - Crunchbase/LinkedIn profiles
   - Recent news and press releases
   - Funding announcements
   - Product information

2. **Create Profile** - Write markdown file in `Companies/[Company-Name].md`:
   - Use the company template from market analysis
   - Include all discoverable facts with sources
   - Add [[wiki-links]] to related entities
   - Note any information gaps

3. **Update INDEX.md** - Add link to new company under Companies section

## Output
- Company markdown file in `Companies/`
- Updated INDEX.md
- Research notes in log file

## Quality Standards
- Cross-reference facts from multiple sources
- Include source URLs for all claims
- Note when information is uncertain
- Prioritize recent information (last 2 years)
```

### product-researcher.md
```markdown
---
name: product-researcher
description: Researches a product/service and creates a structured profile for the [MARKET_TOPIC] knowledge vault.
model: inherit
---

# Product Researcher Agent

**Purpose:** Research a specific product/service in the [MARKET_TOPIC] market and create a comprehensive profile.

## Input
- Product name to research
- Company that makes it (if known)

## Process
1. **Web Search** - Gather information about the product:
   - Official product page
   - Feature lists and documentation
   - Pricing information
   - Reviews and comparisons (G2, Capterra, etc.)
   - Case studies and customer testimonials

2. **Create Profile** - Write markdown file in `Products/[Product-Name].md`:
   - Use the product template from market analysis
   - Include features, pricing, target customers
   - Add [[wiki-links]] to company and competitors
   - Note any information gaps

3. **Update INDEX.md** - Add link to new product under Products section

## Output
- Product markdown file in `Products/`
- Updated INDEX.md
- Research notes in log file
```

### person-researcher.md
```markdown
---
name: person-researcher
description: Researches a key person and creates a structured profile for the [MARKET_TOPIC] knowledge vault.
model: inherit
---

# Person Researcher Agent

**Purpose:** Research a key person in the [MARKET_TOPIC] market and create a comprehensive profile.

## Input
- Person's name
- Known role/company (if available)

## Process
1. **Web Search** - Gather information about the person:
   - LinkedIn profile
   - Company bio page
   - Conference talks and interviews
   - Published articles or thought leadership
   - Career history

2. **Create Profile** - Write markdown file in `People/[Person-Name].md`:
   - Use the person template from market analysis
   - Include career history, achievements, thought leadership
   - Add [[wiki-links]] to companies and other people
   - Note any information gaps

3. **Update INDEX.md** - Add link to new person under People section

## Output
- Person markdown file in `People/`
- Updated INDEX.md
- Research notes in log file
```

### category-researcher.md

```markdown
---
name: category-researcher
description: Defines or refreshes a market category card for the [MARKET_TOPIC] knowledge vault. Categories are the taxonomy spine.
model: inherit
---

# Category Researcher Agent

**Purpose:** Define a market category in [MARKET_TOPIC]. Categories are what make
comparison possible - without them the vault is a list of companies rather than a
market map.

## Before authoring a new category

1. Check `Categories/` for an existing card that covers it. Prefer widening an
   existing definition over creating a near-duplicate.
2. Check `REJECTIONS.md` - this cluster may already have been declined.
3. Confirm at least three products would sit in it. Fewer than three is not a
   category, it is a product with ambitions.
4. Confirm it passes the antonym pair in `SCOPE.md`.

## Process

1. **Research** - how do *buyers* name this segment? Use their words, not vendor
   marketing words. What do they actually evaluate on? Who holds the budget?
   Who leads, who is emerging, who is exiting? Which adjacent categories does it
   blur into, and where exactly is the seam?
2. **Write** the card in `Categories/[Name].md` with full frontmatter:
   `definition`, `maturity`, `buyer`, `leaders`, `emerging`,
   `evaluation_criteria`, `adjacent_categories`, plus `relevance`,
   `relevance_notes` and `last_updated`.
3. **Update INDEX.md**

`evaluation_criteria` is the highest-value field on the card. It is what makes
two products in this category comparable at all.

## Output

    Created|Updated: [Category]
    - Products assigned: [N]
    - Maturity: [stage]
    - Leaders: [names]
    - Adjacent: [names]
```

### capital-researcher.md

```markdown
---
name: capital-researcher
description: Researches an investor and creates a profile for the [MARKET_TOPIC] knowledge vault, focused on the in-scope portfolio subset.
model: inherit
---

# Capital Researcher Agent

**Purpose:** Profile an investor active in [MARKET_TOPIC].

## The critical constraint

`portfolio:` holds the **in-scope subset only**. A generalist fund has hundreds
of positions and almost none of them are this market. Recording them all
destroys the co-investment signal the field exists to provide.

To build it: grep `Companies/*.md` for this fund in `all_investors` and
`lead_investors`. That set, plus any in-scope position you find that has no card
yet (log those to `SWEEP_GAPS.md`), is the portfolio.

## Process

1. **Research** - fund site, portfolio page, published thesis, partner bios,
   recent announcements, filings where fund size is disclosed. Capture stage
   focus and check range: they predict where this fund shows up next, which is
   the forward-looking value of the card.
2. **Write** the card in `Capital/[Name].md` with `type`, `aum`, `stage`,
   `check_size`, `sector_focus`, `portfolio`, plus the universal fields.
3. **Update INDEX.md**

## Output

    Created|Updated: [Fund]
    - Type: [type]   AUM: [amount or unknown]
    - In-scope portfolio: [N] ([names])
    - Stage: [range]   Check: [range]
```

### scope-validator.md

```markdown
---
name: scope-validator
description: Audits existing cards against the scope boundary and re-scores relevance. Run when a company's positioning changes, or as a periodic corpus audit.
model: inherit
---

# Scope Validator Agent

**Purpose:** Audit vault membership. You do not add entities; you decide whether
the ones present still belong.

This agent exists because companies reposition. A card scored 85 two months ago
may describe a company that has since moved across the boundary, and nothing
else in the pipeline would ever notice.

## Process

1. Read `SCOPE.md` and `REJECTIONS.md`.
2. For each assigned card, re-apply the antonym pair against the entity's
   **current** positioning, not the positioning recorded on the card.
3. Re-score `relevance` and rewrite `relevance_notes`. When the score changes,
   say so in the notes with the date and the reason:
   "Lowered from 85 to 58 on [date]: the 2026 relaunch repositioned the platform
   toward the out-of-scope beneficiary; one of four product lines remains in scope."
4. For anything below 30, recommend removal or retention-as-context with a reason.
5. Where three or more cards fall out for the same reason, propose a
   `REJECTIONS.md` entry covering the cluster.

## Guardrails

- **Never delete a card.** Recommend; a human decides.
- A score moving is information. Never silently overwrite the old value.
- Whole-corpus drift is itself a finding. Report the distribution and the mean.

## Output

    Scope audit - [N] cards reviewed
    - Unchanged: [N]   Raised: [N]   Lowered: [N]
    - Below 30 (recommend removal): [names]
    - Proposed rejection clusters: [names]
    - Distribution: 90-100:[n] 70-89:[n] 50-69:[n] 30-49:[n] 0-29:[n]
    - Mean relevance: [N] (previous audit: [N])
```

### trend-researcher.md
```markdown
---
name: trend-researcher
description: Researches a market trend and writes a dated analysis into Resources/Trends/ for the [MARKET_TOPIC] knowledge vault. Trends are documents, not entities.
model: inherit
---

# Trend Researcher Agent

**Purpose:** Research and analyze a specific trend in the [MARKET_TOPIC] market.

A trend is a dated analysis, not an entity: it has no lifecycle and no typed
relations, so it lives in `Resources/Trends/` and is excluded from the
validator. Link to the entity cards it discusses with `[[wikilinks]]`.

## Input
- Trend name/description
- Timeframe to focus on

## Process
1. **Web Search** - Gather information about the trend:
   - Industry reports and analyzes
   - News coverage
   - Expert commentary
   - Data and statistics
   - Companies driving or affected by trend

2. **Write the analysis** - `Resources/Trends/[YYYY-MM] [Trend Name].md` with
   frontmatter `type: trend`, `date`, `entities: [names discussed]`:
   - Drivers, implications, timeline
   - `[[wikilinks]]` to every company, product and category discussed
   - Quantitative data with sources where available

3. **Update INDEX.md** - Add link under a `### Trends` heading in Resources

## Output
- Trend document in `Resources/Trends/`
- Updated INDEX.md
```

## Research Command Template

Create in `[OUTPUT_FOLDER]/Commands/research.md`:

```markdown
# Research Entity

Research a specific entity and add it to the [MARKET_TOPIC] knowledge vault.

## Usage
Provide the entity type and name to research.

## Process
1. Read `SCOPE.md` and confirm the entity passes the boundary. If it does
   not, say so and stop - do not create a card for context.

2. Identify the appropriate agent for the entity type:
   - Company → company-researcher
   - Product → product-researcher
   - Category → category-researcher
   - Person → person-researcher
   - Capital / investor → capital-researcher
   - Trend → trend-researcher (writes a document, not a card)

3. Spawn the agent with the Task tool to research the entity

4. Run `python3 Tools/health_check.py` and fix anything CRITICAL the new card
   introduced. Verify INDEX.md was updated.

## Example
"Research the company Acme Corp"
→ Spawns company-researcher agent
→ Creates Companies/Acme-Corp.md
→ Updates INDEX.md
```

## Health Check Command Template

Create in `[OUTPUT_FOLDER]/Commands/health-check.md`:

```markdown
# Health Check

Validate the vault and work the queue it prints.

## Process
1. Run `python3 Tools/health_check.py --report Resources/` from the vault root.
2. Read the report it wrote. Work issues in this order: broken relations,
   duplicates, missing required fields, enum and date format, ledger state,
   orphans, then the relevance review queue.
3. Never create a stub card to satisfy a relation. Fix the name or remove the
   relation and note the missing entity.
4. Re-run until CRITICAL is zero. Report the before/after counts and the
   lowest-coverage field, which is the next column worth sweeping.

## Flags
- `--json` for machine-readable output
- `--dedup` for near-duplicate names only
- `--fail-on critical` for a non-zero exit in scripts
```

## Scope Audit Command Template

Create in `[OUTPUT_FOLDER]/Commands/scope-audit.md`:

```markdown
# Scope Audit

Re-score the corpus against the boundary. Run this periodically after the
playbook finishes - companies reposition, and nothing else notices.

## Usage
Optionally name a folder or a list of cards. Default: every card whose
`last_updated` is older than 90 days, plus every card scoring below 50.

## Process
1. Spawn the scope-validator agent with the card list.
2. It re-applies the antonym pair in `SCOPE.md` to each card's current
   positioning, re-scores `relevance`, and rewrites `relevance_notes` with the
   date and reason whenever a score moves.
3. It never deletes. Cards below 30 are listed for a human decision.
4. Report the distribution, the mean, and how the mean compares to the last
   entry in `Resources/health_check_*.md`.
```

## Vault CLAUDE.md Template

Create in `[OUTPUT_FOLDER]/CLAUDE.md`:

```markdown
# [MARKET_TOPIC] Research Vault

## Purpose

This vault contains structured research about the [MARKET_TOPIC] market, organized as interlinked markdown files compatible with Obsidian.

**YAML frontmatter is the database. The body is the argument for what the frontmatter asserts.** A fact in frontmatter can be counted, rolled up, validated and graphed; the same fact in a body table can only be re-read.

## Scope

- **IN:** [SCOPE_IN]
- **OUT:** [SCOPE_OUT]

Read `SCOPE.md` before creating or scoring anything, and check `REJECTIONS.md` before adding a candidate - a cluster declined once should cost nothing to decline again.

## Structure

- **Companies/** - Company profiles
- **Products/** - Product/service profiles
- **Categories/** - The taxonomy spine
- **People/** - Key people in the market
- **Capital/** - Investor profiles
- **Resources/** - Reports, `Trends/`, data sources, health check reports
- **Tools/** - `health_check.py`, the corpus validator
- **Agents/** - Research agents for each entity type
- **Commands/** - Slash commands for common operations

## Rules that do not bend

1. **Every card carries `relevance` (0-100), `relevance_notes` and `last_updated`.** Score at creation. An unscored card is an unreviewed card.
2. **`relevance` is scope membership, not research priority.** Priority lives in the run plan and dies with the run.
3. **Filename is the canonical name.** Every typed relation uses exactly that string.
4. **Typed relations must resolve.** Create the target, fix the name, or remove the relation - never leave one dangling. A dangling `[[mention]]` in the body is fine.
5. **Never stub a card to satisfy a relation.** It passes the validator while lying about coverage. Log to `SWEEP_GAPS.md` instead.
6. **Marketing numbers are not facts.** Quarantine them in `unverified_claims:` and attribute them in prose.

## Before finishing any task

```bash
python3 Tools/health_check.py
```

Work the output in order: broken relations, orphans, missing required fields, enum and format, event state, duplicates, relevance review queue.

## Agents

Located in `Agents/` (also accessible via `.claude/agents`):

| Agent | Purpose |
|-------|---------|
| company-researcher | Research and profile companies |
| product-researcher | Research and profile products |
| category-researcher | Define the taxonomy spine |
| person-researcher | Research and profile key people |
| capital-researcher | Profile investors, in-scope portfolio only |
| scope-validator | Audit the corpus against the boundary and re-score |
| trend-researcher | Research and analyze market trends |

## Commands

Located in `Commands/` (also accessible via `.claude/commands`):

| Command | Purpose |
|---------|---------|
| /research | Research a specific entity |
| /health-check | Validate corpus integrity and print the work queue |
| /scope-audit | Re-score the corpus against the boundary |

## Conventions

- Use `[[Entity Name]]` for inter-page links
- Keep profiles factual with source citations
- Update INDEX.md when adding new entities
- Use consistent naming: `Entity-Name.md` (kebab-case)

## Working in This Vault

1. Use the research agents to add new entities
2. Manually edit profiles to add context or corrections
3. Check INDEX.md for navigation
4. Use the graph view in Obsidian to explore connections
```

## INDEX.md Template

Create initial launch page in `[OUTPUT_FOLDER]/INDEX.md`:

```markdown
# [MARKET_TOPIC] Research Vault

> Research initiated: {{DATE}}
> Agent: {{AGENT_NAME}}

## Overview

This vault contains structured research about the **[MARKET_TOPIC]** market.

## Quick Navigation

### Categories
_No categories defined yet._

### Companies
_No companies researched yet._

### Products & Services
_No products researched yet._

### Key People
_No people researched yet._

### Capital
_No investors researched yet._

## Scope

- **IN:** [SCOPE_IN]
- **OUT:** [SCOPE_OUT]

See [[SCOPE]] for edge rules and [[REJECTIONS]] for clusters already declined.

## Research Tools

### Agents
- [[Agents/company-researcher|Company Researcher]]
- [[Agents/product-researcher|Product Researcher]]
- [[Agents/category-researcher|Category Researcher]]
- [[Agents/person-researcher|Person Researcher]]
- [[Agents/capital-researcher|Capital Researcher]]
- [[Agents/scope-validator|Scope Validator]]
- [[Agents/trend-researcher|Trend Researcher]]

### Commands
- `/research` - Research a specific entity
- `/health-check` - Validate corpus integrity
- `/scope-audit` - Re-score the corpus against the boundary

## Statistics

| Category | Count |
|----------|-------|
| Companies | 0 |
| Products | 0 |
| Categories | 0 |
| People | 0 |
| Capital | 0 |
| **Total Entities** | 0 |

---
*This vault was initialized by the Maestro Market Research Playbook*
```

## How to Know You're Done

This task is complete when:
1. All folders exist (Companies/, Products/, Categories/, People/, Capital/, Resources/, Tools/, Agents/, Commands/, plus the DomainEntity folder if one was resolved)
2. `.claude/` folder exists with working symlinks to Agents/ and Commands/
3. All seven agents are created in Agents/ (company, product, category,
   person, capital, scope-validator, trend)
4. All three commands are created in Commands/ (research, health-check,
   scope-audit)
5. INDEX.md exists with the market topic and the scope pair
6. CLAUDE.md exists with vault documentation
7. `cd [OUTPUT_FOLDER] && python3 Tools/health_check.py` exits 0 with a
   `0 cards` summary (or exits 2 naming PyYAML, if `0_CONFIGURE` recorded that
   degradation)

Step 7 matters: it proves the schema in `kb.yaml` is loadable before any research
depends on it. A traceback is a defect; exit 2 with a `CONFIG ERROR` line is a
kb.yaml problem to fix now.

## Notes

- The symlinks allow Claude Code to discover agents/commands via `.claude/`
- Agents/ and Commands/ folders are visible in Obsidian for easy reference
- Entity agents are customized with the MARKET_TOPIC from configuration
- Every research agent must read `SCOPE.md` before creating a card
- This only runs once - subsequent loops skip to 1_ANALYZE.md
