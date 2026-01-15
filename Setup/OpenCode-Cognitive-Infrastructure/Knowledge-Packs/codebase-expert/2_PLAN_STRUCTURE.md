# Phase 2: Plan Structure

## Objective

Plan the indexing and installation structure for the codebase-expert pack.

## Installation Structure

```
.opencode/
├── skill/
│   └── codebase-expert/
│       └── SKILL.md           # Skill definition
├── memory/
│   └── knowledge/
│       └── codebase/
│           └── index.json     # Codebase index metadata
├── plugin/
│   └── lib/
│       ├── embeddings.ts      # Embedding generation
│       ├── vector-store.ts    # Vector storage
│       └── chunking.ts        # Document chunking
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
name: codebase-expert
description: Deep expertise in the current codebase. USE WHEN user asks about code structure, architecture, implementations, or wants to find specific functionality.
```

## Next Phase

Proceed to **3_EVALUATE.md** to evaluate the plan.
