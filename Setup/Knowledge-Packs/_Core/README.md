# Knowledge Packs - Core Utilities

Shared utilities for all Knowledge Packs in the Claude Cognitive Infrastructure ecosystem.

## Overview

Knowledge Packs are modular domain expertise packages that can be stacked on any agent with Claude Cognitive Infrastructure installed. This `_Core` directory contains shared utilities used by all packs.

## Components

### Registry System

The registry tracks installed knowledge packs in `.claude/config/knowledge-packs.yaml`:

```yaml
installed_packs:
  - id: codebase-expert
    name: "Codebase Expert"
    installed: 2025-01-03
    version: "1.0.0"
    sources:
      - path: "/path/to/repo"
        type: "codebase"
    embeddings_path: ".claude/knowledge/codebase-expert/"

  - id: brian-tracy-teachings
    name: "Brian Tracy Teachings"
    installed: 2025-01-03
    version: "1.0.0"
    sources:
      - path: "/path/to/books"
        type: "documents"
    embeddings_path: ".claude/knowledge/brian-tracy-teachings/"
```

### Hooks

- **`rag-retrieval.ts`** - PreToolUse hook that queries all installed knowledge packs and injects relevant context based on user intent

### Libraries

- **`registry.ts`** - Functions to read/write the knowledge packs registry
- **`embeddings.ts`** - Embedding generation utilities (supports multiple providers)
- **`vector-store.ts`** - Vector database abstraction (local JSON, Chroma, Pinecone)
- **`chunking.ts`** - Document chunking strategies for different content types

## Installation

The `_Core` utilities are automatically installed when you run any Knowledge Pack playbook for the first time. They check for existing installation and skip if already present.

## Supported Vector Stores

1. **Local JSON** (default) - No external dependencies, stores in `.claude/knowledge/`
2. **Chroma** - Local vector database
3. **Pinecone** - Cloud vector database

## How Knowledge Packs Work

1. **Installation** - Pack playbook ingests source documents, generates embeddings
2. **Registration** - Pack registers itself in `knowledge-packs.yaml`
3. **Retrieval** - RAG hook queries relevant packs based on user intent
4. **Injection** - Relevant context injected into agent's working memory

## Creating New Knowledge Packs

See existing packs (Codebase-Expert, Brian-Tracy-Teachings) as templates. Each pack needs:

1. Standard 6-document playbook structure (0_INITIALIZE through 5_VERIFY)
2. Skill template in `templates/skills/{PackName}/SKILL.md`
3. Chunking strategy appropriate for content type
4. Verification tests

---

*Part of the Claude Cognitive Infrastructure ecosystem*
