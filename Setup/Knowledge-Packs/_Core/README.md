# Knowledge Packs Core Utilities

Shared utilities for Knowledge Pack playbooks, providing RAG (Retrieval-Augmented Generation) capabilities.

> **Important**: These utilities are **reference implementations** that require configuration before use. See the [Configuration Required](#configuration-required) section for details.

## Components

### Hooks

- **rag-retrieval.ts** - Pre-tool hook that injects relevant context before responses

### Libraries

- **registry.ts** - Knowledge pack registration and management
- **embeddings.ts** - Text embedding generation for semantic search
- **vector-store.ts** - Vector storage and similarity search
- **chunking.ts** - Document chunking strategies for optimal retrieval

## Configuration Required

### Embedding Provider

The `embeddings.ts` file contains a **placeholder implementation** that returns random vectors. For the Codebase Expert (or any Knowledge Pack) to function properly, you must configure an actual embedding provider.

**Supported options:**

1. **OpenAI Embeddings** (recommended)
   ```typescript
   // Replace generateEmbedding() implementation with:
   import OpenAI from 'openai';
   const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

   const response = await openai.embeddings.create({
     model: 'text-embedding-3-small',
     input: text,
   });
   return response.data[0].embedding;
   ```

2. **Local Models** (Ollama, llama.cpp)
   ```typescript
   // For Ollama:
   const response = await fetch('http://localhost:11434/api/embeddings', {
     method: 'POST',
     body: JSON.stringify({ model: 'nomic-embed-text', prompt: text }),
   });
   return (await response.json()).embedding;
   ```

3. **Other Providers** (Cohere, Hugging Face, etc.)
   - Modify `embeddings.ts` to call your provider's API

### Hook Execution

The RAG hook (`rag-retrieval.ts`) is designed as a **reference implementation** for pre-tool context injection. Claude Code does not currently have built-in hook execution for custom TypeScript hooks.

**Integration approaches:**

1. **Manual Integration** - Copy relevant context retrieval logic into your workflow
2. **Script Wrapper** - Run the hook as a pre-processing step before Claude sessions
3. **MCP Server** - Implement as an MCP (Model Context Protocol) server for Claude integration
4. **Future Claude Code Hooks** - The hook format is designed to be compatible with potential future Claude Code hook systems

## Skill Activation System

Skills in the Claude Cognitive Infrastructure use a **convention-based activation** system:

### How It Works

1. **Frontmatter Metadata** - Each SKILL.md contains YAML frontmatter:
   ```yaml
   triggers:
     - code
     - codebase
     - architecture
   context_budget: 8000
   ```

2. **Trigger Keywords** - When a user message contains trigger keywords, the skill is considered relevant

3. **Context Budget** - The `context_budget` field indicates how many tokens of context the skill can contribute

4. **Manual Activation** - Currently, skill activation is **manual**:
   - Read SKILL.md when working in that domain
   - Include skill context in your prompts
   - Use skills as reference documentation

5. **Automated Activation** (Future) - The metadata format supports future automated systems that could:
   - Scan user messages for trigger keywords
   - Automatically inject relevant skill context
   - Respect context budgets for token management

## Usage

These utilities are used by Knowledge Pack playbooks to enable semantic search and context injection. Individual knowledge packs reference these shared components rather than duplicating functionality.

## Requirements

- Node.js 18+
- TypeScript
- Embedding provider API key (OpenAI, etc.) or local model

---

*Knowledge Packs Core Utilities v1.0.0*
