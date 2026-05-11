# Usage Documentation Analysis - Feature Discovery

## Context
- **Playbook:** Usage
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Survey the codebase to discover user-facing features and read the current README.md to understand what's documented. This establishes the baseline for comparing actual features vs documented features.

## Instructions

1. **Read the README** at `{{AGENT_PATH}}/[README_PATH]`
2. **Survey the codebase** to identify major user-facing features
3. **Create a feature inventory** listing both documented and actual features
4. **Output report** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_FEATURE_INVENTORY.md`

## Analysis Checklist

- [ ] **Read configured values**: Read the agent prompt for `[README_PATH]`, `[AUTO_FIX_IMPORTANCE]`, and `[AUTO_FIX_EFFORT]`. Use these values throughout this playbook wherever you see the corresponding placeholders.

- [ ] **Discover features and scan README (if needed)**: First check if `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_FEATURE_INVENTORY.md` already exists with feature data (at least one feature listed in either "Features Documented in README" or "Features Found in Code" tables). If it does, skip the survey and mark this task complete—the feature inventory is already in place. If it doesn't exist, read the project's README at `{{AGENT_PATH}}/[README_PATH]` to extract what features are currently documented. Survey the codebase (entry points, CLI commands, API endpoints, UI components, configuration options) to identify actual user-facing features. Output a feature inventory to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_FEATURE_INVENTORY.md`.

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

Create/update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_FEATURE_INVENTORY.md` with:

```markdown
# Feature Inventory - Loop {{LOOP_NUMBER}}

## README Analysis

### README Location
`{{AGENT_PATH}}/README.md`

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
