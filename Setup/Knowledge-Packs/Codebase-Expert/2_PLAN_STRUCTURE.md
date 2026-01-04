# Phase 2: Plan Structure

## Objective

Plan the indexing and installation structure for the Codebase Expert pack.

## Installation Structure

```
.claude/
├── skills/
│   └── Codebase-Expert/
│       └── SKILL.md           # Skill definition
├── context/
│   └── knowledge/
│       └── codebase/
│           └── index.json     # Codebase index metadata
└── config/
    └── knowledge-packs.yaml   # Registry entry
```

## Indexing Strategy

### Files to Index

Include:
- Source code files (.ts, .js, .py, .go, etc.)
- Configuration files (package.json, tsconfig.json, etc.)
- Documentation (.md files in docs/)

Exclude:
- node_modules/
- .git/
- Build outputs (dist/, build/)
- Binary files
- Large generated files

### Chunking Strategy

- **Code files**: Chunk by function/class
- **Config files**: Keep whole
- **Documentation**: Chunk by section

### Embedding Plan

- Generate embeddings for each chunk
- Store in vector store for semantic search
- Index by file path and content type

## Skill Configuration

```yaml
name: Codebase-Expert
version: 1.0.0
priority: 80
triggers:
  - code
  - codebase
  - architecture
  - implementation
  - function
  - class
  - module
context_budget: 8000
```

## Next Phase

Proceed to **3_EVALUATE.md** to evaluate the plan.
