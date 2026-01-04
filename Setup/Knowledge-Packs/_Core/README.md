# Knowledge Packs Core Utilities

Shared utilities for Knowledge Pack playbooks, providing RAG (Retrieval-Augmented Generation) capabilities.

## Components

### Hooks

- **rag-retrieval.ts** - Pre-tool hook that injects relevant context before responses

### Libraries

- **registry.ts** - Knowledge pack registration and management
- **embeddings.ts** - Text embedding generation for semantic search
- **vector-store.ts** - Vector storage and similarity search
- **chunking.ts** - Document chunking strategies for optimal retrieval

## Usage

These utilities are used by Knowledge Pack playbooks to enable semantic search and context injection. Individual knowledge packs reference these shared components rather than duplicating functionality.

## Requirements

- Node.js 18+
- TypeScript

---

*Knowledge Packs Core Utilities v1.0.0*
