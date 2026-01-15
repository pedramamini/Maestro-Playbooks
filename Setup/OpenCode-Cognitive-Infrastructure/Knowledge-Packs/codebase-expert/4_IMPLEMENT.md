# Phase 4: Implement Installation

## Objective

Execute the codebase-expert knowledge pack installation.

---

## Prerequisites

> **Important**: Before proceeding, you must configure an embedding provider. The default `embeddings.ts` contains placeholder code that returns random vectors. See the assets folder for the file to configure.

### Embedding Provider Options

1. **OpenAI** (recommended): Set `OPENAI_API_KEY` environment variable
2. **Ollama** (local): Run `ollama pull nomic-embed-text`
3. **Other**: Modify `{{AUTORUN_FOLDER}}/assets/lib/embeddings.ts` for your provider

## Implementation Steps

### Step 1: Create Skill Directory

```bash
mkdir -p .opencode/skill/codebase-expert
```

### Step 2: Install SKILL.md

Copy the skill template from `{{AUTORUN_FOLDER}}/assets/templates/skills/codebase-expert/SKILL.md` to:
`.opencode/skill/codebase-expert/SKILL.md`

### Step 3: Create Knowledge Directory

```bash
mkdir -p .opencode/memory/knowledge/codebase
```

### Step 4: Configure Embedding Provider

Before indexing, update `{{AUTORUN_FOLDER}}/assets/lib/embeddings.ts` with your chosen provider:

**For OpenAI:**
```typescript
import OpenAI from 'openai';
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });
  return response.data[0].embedding;
}
```

**For Ollama (local):**
```typescript
export async function generateEmbedding(text: string): Promise<number[]> {
  const response = await fetch('http://localhost:11434/api/embeddings', {
    method: 'POST',
    body: JSON.stringify({ model: 'nomic-embed-text', prompt: text }),
  });
  return (await response.json()).embedding;
}
```

### Step 5: Install Library Files

Copy the library files from `{{AUTORUN_FOLDER}}/assets/lib/` to `.opencode/plugin/lib/`:

```bash
mkdir -p .opencode/plugin/lib
cp {{AUTORUN_FOLDER}}/assets/lib/*.ts .opencode/plugin/lib/
```

### Step 6: Index Codebase

For each source file:
1. Read file content
2. Chunk appropriately (by function/class for code)
3. Generate embeddings using your configured provider
4. Store in vector store

**Example indexing script:**

```typescript
import { chunkCode } from '.opencode/plugin/lib/chunking';
import { generateEmbedding } from '.opencode/plugin/lib/embeddings';
import { VectorStore } from '.opencode/plugin/lib/vector-store';

const store = new VectorStore('codebase');

for (const file of sourceFiles) {
  const chunks = chunkCode(file.content, file.language);
  for (const chunk of chunks) {
    const embedding = await generateEmbedding(chunk.text);
    store.add(embedding, chunk.text, { source: file.path });
  }
}
```

### Step 7: Create Index Metadata

Create `.opencode/memory/knowledge/codebase/index.json`:

```json
{
  "created": "<date>",
  "files_indexed": <count>,
  "chunks": <count>,
  "languages": ["<lang1>", "<lang2>"],
  "embedding_provider": "<openai|ollama|other>",
  "embedding_model": "<model-name>",
  "last_updated": "<date>"
}
```

### Step 8: Update Registry

Create or update `.opencode/config/knowledge-packs.yaml`:

```yaml
packs:
  - id: codebase-expert
    name: "Codebase Expert"
    installed: "<date>"
    version: "1.0.0"
    embedding_provider: "<your-provider>"
    sources:
      - path: ".opencode/memory/knowledge/codebase/"
        type: "directory"
    skill_path: ".opencode/skill/codebase-expert/SKILL.md"
```

### Step 9: Create RAG Plugin (Optional)

For automatic context injection, create `.opencode/plugin/rag-retrieval.ts`:

```typescript
import type { Plugin } from "@opencode-ai/plugin";
import { VectorStore } from "./lib/vector-store";
import { generateEmbedding } from "./lib/embeddings";

export const RagRetrieval: Plugin = async ({ client, $ }) => {
  const store = new VectorStore('codebase');

  return {
    tool: {
      execute: {
        before: async (input, output) => {
          // Extract query from user input if relevant
          // Search vector store
          // Inject context if matches found
        }
      }
    }
  };
};

export default RagRetrieval;
```

---

## Post-Implementation

- [ ] Verify all files created
- [ ] Test embedding generation with a sample query
- [ ] Verify vector store contains indexed chunks
- [ ] Test semantic search returns relevant results
- [ ] Skill name follows lowercase convention (`codebase-expert`)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Random/irrelevant results | Embedding provider not configured (still using placeholder) |
| API errors | Check API key and network connectivity |
| Empty results | Verify indexing completed and vector store has data |
| Skill not found | Check skill name is lowercase with hyphens |

## Next Phase

Proceed to **5_VERIFY.md** to verify installation.
