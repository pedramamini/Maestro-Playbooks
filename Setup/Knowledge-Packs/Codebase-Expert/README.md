# Codebase Expert Knowledge Pack

A knowledge pack that gives any Claude Cognitive Infrastructure agent deep expertise in a specific codebase.

## Overview

This playbook ingests a codebase, generates embeddings for code and documentation, and creates a "Codebase Expert" skill that enables RAG-powered code understanding.

## Prerequisites

- Target agent must have **Claude Cognitive Infrastructure** already installed
- Target codebase must be accessible on the filesystem
- Node.js/Bun runtime available

## What Gets Created

```
.claude/
├── config/
│   └── knowledge-packs.yaml    # Pack registration (created/updated)
├── knowledge/
│   └── vectors.json            # Embeddings storage (created/updated)
├── skills/
│   └── Codebase-Expert/
│       └── SKILL.md            # Codebase expertise skill
└── context/
    └── working/
        └── rag-context.md      # Auto-injected relevant context
```

## Configuration

The playbook automatically:

1. **Scans** the target codebase for code files and documentation
2. **Chunks** content using code-aware splitting (respects function/class boundaries)
3. **Embeds** chunks using local embedding (or OpenAI if configured)
4. **Registers** the pack in the knowledge registry
5. **Creates** a Codebase-Expert skill

### Supported File Types

**Code:**
- TypeScript/JavaScript (`.ts`, `.tsx`, `.js`, `.jsx`)
- Python (`.py`)
- Go (`.go`)
- Rust (`.rs`)
- And more...

**Documentation:**
- Markdown (`.md`, `.mdx`)
- Text (`.txt`)
- README files

### Exclusions (automatic)

- `node_modules/`
- `.git/`
- `dist/`, `build/`, `out/`
- Binary files
- Large generated files

## Usage

Run this playbook on an agent that already has Claude Cognitive Infrastructure:

```
Agent Directory/         # Must have .claude/ already
├── CLAUDE.md
└── .claude/
    └── ...              # Existing infrastructure
```

Point the playbook at the codebase you want to ingest during the ANALYZE phase.

## How RAG Works

Once installed, the RAG retrieval hook:

1. **Intercepts** query-related tool calls (Read, Grep, Glob, etc.)
2. **Searches** the vector store for relevant code snippets
3. **Injects** context into `.claude/context/working/rag-context.md`
4. **Agent** automatically has relevant code context for responses

## Updating Knowledge

Re-run this playbook to update the codebase knowledge. It will:
- Re-scan for new/changed files
- Update embeddings
- Preserve other installed knowledge packs

---

*Part of the Knowledge Packs system for Claude Cognitive Infrastructure*
