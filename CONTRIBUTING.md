# Contributing Playbooks

This repository powers the **Maestro in-app Playbook Exchange**. We welcome community contributions of new playbooks that automate useful workflows.

## Quick Start

1. Fork this repository
2. Create your playbook in `Category/Subcategory/` format
3. Add your playbook entry to `manifest.json`
4. Submit a pull request

## Playbook Structure

Each playbook lives in a folder following the `Category/Subcategory` pattern:

```
Category/
└── YourPlaybook/
    ├── README.md           # Required: Description shown in exchange
    ├── 1_ANALYZE.md        # Survey and identify targets
    ├── 2_FIND_*.md         # Find specific issues/gaps/entities
    ├── 3_EVALUATE.md       # Rate candidates by priority
    ├── 4_IMPLEMENT.md      # Execute one item per loop
    ├── 5_PROGRESS.md       # Loop gate: continue or exit
    ├── Agent-Prompt.md     # Optional: Custom prompt (if not using default)
    └── assets/             # Optional: Non-markdown assets (configs, scripts, etc.)
```

### Optional Initialization Document

If your playbook needs one-time setup (folder structure, agents, etc.), add:

```
0_INITIALIZE.md         # Runs once, never resets
```

### Assets Folder

> **Exchange-only feature.** The `assets/` folder is supported **only for playbooks submitted to this repository** (the Maestro in-app Playbook Exchange). User-shared playbooks distributed via direct links or copied between machines do not carry an `assets/` folder—Maestro's share/install flow only transports the markdown documents. If your playbook depends on bundled files, it must be PR'd here so the Exchange installer copies the full folder.

The `assets/` subfolder bundles non-markdown files with your playbook:

```
assets/
├── config.yaml         # Configuration templates
├── schema.json         # Schema definitions
├── Dockerfile          # Container files
└── helper.sh           # Utility scripts
```

**When to use assets:**
- Pre-configured templates that agents should read or copy
- Schema files for validation
- Docker/container configurations
- Helper scripts for complex operations
- Reference data (lookup tables, mappings)

**Referencing assets in documents:**

Use the `{{AUTORUN_FOLDER}}/assets/` path:

```markdown
- [ ] Read the API schema from `{{AUTORUN_FOLDER}}/assets/openapi.yaml`
- [ ] Copy `{{AUTORUN_FOLDER}}/assets/Dockerfile` to the project root
```

**Important notes:**
- Assets ship with the playbook **only when installed from the Exchange**—not when shared peer-to-peer via Maestro's direct-share links
- Keep assets small—large binary files slow down installation
- Document any assets in your playbook's README.md so users understand what's bundled

## Required Files

### README.md

Your README is displayed in the exchange preview. Include:

- **Title and description** - What does this playbook do?
- **Requirements** - Does it need a custom prompt? Special tools?
- **Document chain table** - Purpose of each document
- **Generated files** - What working files does it create?
- **How it works** - Explain the loop control logic
- **Recommended setup** - Loop mode, max loops, reset settings
- **Tips** - Best practices for using the playbook

See existing playbooks for examples.

### Document Files (1-5)

Each document must contain:

1. **Context block** - Template variables and playbook identity
2. **Task checkboxes** - `- [ ]` format for Auto Run to process
3. **Clear instructions** - What the agent should do

Example context block:

```markdown
# Context

- **Playbook:** Your Playbook Name
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Loop:** {{LOOP_NUMBER}}
- **Date:** {{DATE}}
- **Working Folder:** {{AUTORUN_FOLDER}}
```

### Template Variables

Use these Maestro-substituted variables:

| Variable | Description |
|----------|-------------|
| `{{AGENT_NAME}}` | Name of the Maestro agent |
| `{{AGENT_PATH}}` | Root path of the target project |
| `{{AUTORUN_FOLDER}}` | Path to the Auto Run folder |
| `{{LOOP_NUMBER}}` | Current loop iteration (1, 2, 3...) |
| `{{DATE}}` | Today's date (YYYY-MM-DD) |
| `{{CWD}}` | Current working directory |

## Adding to manifest.json

Add your playbook entry to the `playbooks` array in `manifest.json`:

```json
{
  "id": "category-subcategory",
  "title": "Your Playbook Title",
  "description": "One or two sentences describing what this playbook does.",
  "category": "Category",
  "subcategory": "Subcategory",
  "author": "Your Name",
  "authorLink": "https://your-website.com",
  "tags": ["relevant", "searchable", "keywords"],
  "lastUpdated": "YYYY-MM-DD",
  "path": "Category/Subcategory",
  "documents": [
    { "filename": "1_ANALYZE", "resetOnCompletion": false },
    { "filename": "2_FIND_ISSUES", "resetOnCompletion": false },
    { "filename": "3_EVALUATE", "resetOnCompletion": false },
    { "filename": "4_IMPLEMENT", "resetOnCompletion": false },
    { "filename": "5_PROGRESS", "resetOnCompletion": true }
  ],
  "loopEnabled": true,
  "maxLoops": null,
  "prompt": null
}
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique slug: `category-subcategory` (lowercase, hyphenated) |
| `title` | Yes | Display name in exchange |
| `description` | Yes | 1-2 sentence description for search/display |
| `category` | Yes | Top-level category (matches folder name) |
| `subcategory` | No | Nested category (matches subfolder name) |
| `author` | Yes | Your name |
| `authorLink` | No | URL to your website/profile |
| `tags` | No | Searchable keywords array |
| `lastUpdated` | Yes | Date in `YYYY-MM-DD` format |
| `minMaestroVersion` | No | Semver string (e.g. `0.16.17`, `0.16.17-RC`). Match the exact case of Maestro's released version tags — semver prerelease comparison is case-sensitive (`-RC` and `-rc` sort differently in ASCII order). Maestro versions older than this hide or disable the tile in the exchange and render a "Requires Maestro X.Y.Z+" badge. Omit if your playbook works on every shipped version. |
| `beta` | No | Boolean. Set `true` while the playbook is still maturing. The exchange renders a `BETA` badge on the tile but does not block install. Default: `false`. Remove the flag (or set `false`) once you have shipped a stable version. |
| `path` | Yes | Folder path relative to repo root |
| `documents` | Yes | Ordered array of `{ filename, resetOnCompletion }` |
| `loopEnabled` | Yes | `true` if playbook loops, `false` otherwise |
| `maxLoops` | No | Loop limit (`null` for unlimited) |
| `prompt` | Yes | Custom prompt string, or `null` for Maestro default |

### When to set `minMaestroVersion`

Set this **only** when your playbook depends on a Maestro capability that does not degrade gracefully on older versions. Examples:

- **A new Auto Run primitive that older versions cannot dispatch** — e.g. the `<!-- maestro:halt -->` marker (added in `0.16.17-RC`). If your playbook uses halt as a UX improvement on top of an already-correct fallback path, you can still pin the version so users on older builds see a clear "Requires Maestro 0.16.17+" badge instead of getting the slow-but-functional path.
- **A new template variable** — older Maestro will not substitute it, so the agent receives the literal `{{NEW_VAR}}` and behavior is undefined.
- **A new manifest field that affects safe execution** — e.g. permission flags, isolation settings — where running the playbook on a version that ignores the field would be unsafe.

Do **not** set this for ordinary code changes that work fine on the version you developed against. The field is a hard gate; an unnecessary version pin cuts off users who could otherwise run your playbook successfully.

Use the lowest version that actually contains the dependency. If a feature shipped in `0.16.17-RC`, pin to `0.16.17-RC` (exact case — see note above), not the date you wrote the playbook.

### When to set `beta`

Set `beta: true` while you are iterating publicly and want the exchange to flag the playbook as not-yet-stable. The badge tells users "expect rough edges" without blocking install. Common reasons to keep `beta` on:

- The playbook depends on a Maestro feature that itself is in RC / preview.
- You expect breaking changes to the document chain or generated-file names within the next few releases.
- Real-world testing has been narrow and you want explicit feedback before declaring stable.

Remove the flag once the playbook has had at least one full release cycle without breaking changes and you are comfortable defaulting it for users.

### Document Array

- `filename`: Without `.md` extension
- `resetOnCompletion`:
  - `false` for documents 0-4 (controlled by document 5)
  - `true` for document 5 (the progress gate)

### Prompt Field

- Use `null` if your playbook works with Maestro's default agent prompt
- Include full prompt text (with escaped newlines) if custom prompt required

## Design Guidelines

### Progressive Disclosure

Front-load discovery in documents 1-3, execute cheaply in document 4:

```
Phase 1: Discovery & Planning (token-heavy)
├── Documents 1-3: Explore, investigate, evaluate
└── Output: LOOP_N_PLAN.md with detailed steps

Phase 2: Execution (token-light)
├── Document 4: Execute ONE item from the plan
└── Document 5: Check progress, loop if needed
```

### One Task Per Loop

Document 4 should implement **one item** per loop iteration, not batch multiple items. This enables:
- Clean git commits per change
- Easy rollback if something breaks
- Progress visibility in the log

### Clear Exit Conditions

Document 5 must have unambiguous logic for when to:
- **Reset documents 1-4** and continue looping
- **Not reset** and exit the pipeline

Common exit conditions:
- Coverage target reached (80%, 90%)
- No PENDING items with required priority remain
- All high-priority work completed

### Status Values

Use consistent status values in `LOOP_N_PLAN.md`:

| Status | Meaning |
|--------|---------|
| `PENDING` | Ready for automated processing |
| `IMPLEMENTED` / `RESEARCHED` | Completed this loop |
| `WON'T DO` / `SKIP` | Intentionally skipped |
| `PENDING - MANUAL REVIEW` | Needs human decision |

## Categories

### Existing Categories

- **Assistants** - One-shot setup workflows that install personal-AI frameworks into an agent (PAI-Setup)
- **Development** - Code improvement workflows (Security, Performance, Refactor, Documentation, Testing, Usage)
- **Research** - Knowledge-building workflows (Market)

### Proposing New Categories

If your playbook doesn't fit existing categories, propose a new one in your PR description. Categories should be:
- Broad enough to contain multiple playbooks
- Clearly distinct from existing categories

## Pull Request Checklist

Before submitting:

- [ ] Playbook folder follows `Category/Subcategory/` structure
- [ ] README.md describes the playbook thoroughly
- [ ] All document files (1-5, optionally 0) are present
- [ ] Documents use `- [ ]` checkbox format
- [ ] Template variables use `{{VARIABLE}}` syntax
- [ ] `manifest.json` entry added with all required fields
- [ ] `manifest.json` is valid JSON
- [ ] All `path` and `filename` values match actual files
- [ ] `id` is unique across all playbooks
- [ ] `lastUpdated` uses `YYYY-MM-DD` format
- [ ] If using `assets/` folder: assets are documented in README.md
- [ ] Tested the playbook with Maestro

## Testing Your Playbook

Before submitting:

1. Copy your playbook folder to a Maestro Auto Run location
2. Run with Loop Mode OFF first to review output
3. Check that `LOOP_1_PLAN.md` (or equivalent) generates correctly
4. Run with Loop Mode ON and verify loop/exit behavior
5. Confirm the playbook exits cleanly when done

## Questions?

- Open an issue for questions about playbook design
- Check existing playbooks for implementation patterns
- See the main [README.md](README.md) for architecture details
