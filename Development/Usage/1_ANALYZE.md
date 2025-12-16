# Usage Documentation Analysis - Feature Discovery

## Context
- **Playbook:** Usage
- **Agent:** 🎼 Maestro
- **Project:** /Users/pedram/Projects/Maestro
- **Auto Run Folder:** /Users/pedram/Projects/Maestro/tmp/Playbooks
- **Loop:** 1

## Objective

Survey the codebase to discover user-facing features and read the current README.md to understand what's documented. This establishes the baseline for comparing actual features vs documented features.

## Instructions

1. **Read the README.md** at `/Users/pedram/Projects/Maestro/README.md` (or `/Users/pedram/Projects/Maestro/readme.md`)
2. **Survey the codebase** to identify major user-facing features
3. **Create a feature inventory** listing both documented and actual features
4. **Output report** to `/Users/pedram/Projects/Maestro/tmp/Playbooks/LOOP_1_FEATURE_INVENTORY.md`

## Analysis Checklist

- [ ] **Discover features and scan README**: Read the project's README.md to extract what features are currently documented. Survey the codebase (entry points, CLI commands, API endpoints, UI components, configuration options) to identify actual user-facing features. Output a feature inventory to `/Users/pedram/Projects/Maestro/tmp/Playbooks/LOOP_1_FEATURE_INVENTORY.md`.

## What to Look For in the Codebase

### User-Facing Features
- **CLI commands** - Command-line arguments, subcommands, flags
- **API endpoints** - REST routes, GraphQL queries/mutations
- **UI components** - Major screens, dialogs, interactive elements
- **Configuration options** - Settings, environment variables, config files
- **Integrations** - Third-party services, plugins, extensions
- **Keyboard shortcuts** - Hotkeys, key bindings
- **File formats** - Input/output file types supported

### Feature Indicators
- Entry point files (main, index, app)
- Route definitions
- Command parsers
- Menu/navigation structures
- Settings/preferences code
- Export/import functionality
- Help text and usage strings

## What to Extract from README

### Documented Features
- Feature lists or bullet points
- "Getting Started" steps
- Command examples
- Configuration instructions
- API documentation
- Screenshots/demos referenced
- Changelog mentions

### README Structure
- Main sections and headings
- Installation instructions
- Usage examples
- Feature descriptions
- Known limitations

## Output Format

Create/update `/Users/pedram/Projects/Maestro/tmp/Playbooks/LOOP_1_FEATURE_INVENTORY.md` with:

```markdown
# Feature Inventory - Loop 1

## README Analysis

### README Location
`/Users/pedram/Projects/Maestro/README.md`

### README Structure
| Section | Description | Line Numbers |
|---------|-------------|--------------|
| [section name] | [what it covers] | [start-end] |
| ... | ... | ... |

### Features Documented in README
| Feature | Section | Description in README |
|---------|---------|----------------------|
| [feature name] | [section] | [how it's described] |
| ... | ... | ... |

---

## Codebase Analysis

### Project Type
- **Language/Framework:** [e.g., TypeScript/React, Python/FastAPI]
- **Application Type:** [CLI, Web App, Desktop App, Library, etc.]

### Features Found in Code
| Feature | Location | Type | User-Facing? |
|---------|----------|------|--------------|
| [feature name] | [file/module] | [CLI/API/UI/Config] | Yes/No |
| ... | ... | ... | ... |

---

## Feature Summary

### Totals
- **Features in README:** [count]
- **Features in Code:** [count]
- **Potential Gaps:** [count] (code features not in README)
- **Potential Stale:** [count] (README features not in code)

### Quick Classification

#### Likely Undocumented (in code, not in README)
1. [feature] - [brief description]
2. ...

#### Possibly Stale (in README, not found in code)
1. [feature] - [what README says]
2. ...

#### Confirmed Documented (in both)
1. [feature] - [status: accurate / needs update]
2. ...
```

## Guidelines

- **Focus on user-facing features** - Internal implementation details don't need README coverage
- **Be thorough but not granular** - Major features, not every function
- **Note feature names** - Use the same terminology as the codebase
- **Check for staleness** - Features removed from code but still in README
- **Consider the audience** - What would a new user need to know?
