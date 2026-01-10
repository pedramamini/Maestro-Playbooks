# Phase 4: Implement Installation

## Objective

Execute the Codebase Expert knowledge pack installation.

## Prerequisites

> **Important**: Before proceeding, you must configure an embedding provider. The default `embeddings.ts` contains placeholder code that returns random vectors. See `Setup/Knowledge-Packs/_Core/README.md` for configuration options.

### Embedding Provider Options

1. **OpenAI** (recommended): Set `OPENAI_API_KEY` environment variable
2. **Ollama** (local): Run `ollama pull nomic-embed-text`
3. **Other**: Modify `_Core/lib/embeddings.ts` for your provider

## Implementation Steps

### Step 1: Create Skill Directory

```bash
mkdir -p .claude/skills/Codebase-Expert
```

### Step 2: Install SKILL.md

Copy the skill template to:
`.claude/skills/Codebase-Expert/SKILL.md`

### Step 3: Create Knowledge Directory

```bash
mkdir -p .claude/context/knowledge/codebase
```

### Step 4: Configure Embedding Provider

Before indexing, update `_Core/lib/embeddings.ts` with your chosen provider:

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

### Step 5: Index Codebase

For each source file:
1. Read file content
2. Chunk appropriately (by function/class for code)
3. Generate embeddings using your configured provider
4. Store in vector store

**Example indexing script:**
```typescript
import { chunkCode } from './_Core/lib/chunking';
import { generateEmbedding } from './_Core/lib/embeddings';
import { VectorStore } from './_Core/lib/vector-store';

const store = new VectorStore('codebase');

for (const file of sourceFiles) {
  const chunks = chunkCode(file.content, file.language);
  for (const chunk of chunks) {
    const embedding = await generateEmbedding(chunk.text);
    store.add(embedding, chunk.text, { source: file.path });
  }
}
```

### Step 6: Create Index Metadata

Create `.claude/context/knowledge/codebase/index.json`:

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

### Step 7: Update Registry

Add to `.claude/config/knowledge-packs.yaml`:

```yaml
- id: codebase-expert
  name: "Codebase Expert"
  installed: "<date>"
  version: "1.0.0"
  embedding_provider: "<your-provider>"
  sources:
    - path: ".claude/context/knowledge/codebase/"
      type: "directory"
  skill_path: ".claude/skills/Codebase-Expert/SKILL.md"
```

### Step 8: Configure RAG Hook (Optional)

The RAG retrieval hook in `_Core/hooks/rag-retrieval.ts` is a reference implementation. Integration options:

1. **Manual**: Query the vector store directly when you need code context
2. **MCP Server**: Implement as an MCP server for Claude integration
3. **Wrapper Script**: Run as preprocessing before Claude sessions

## Post-Implementation

- [ ] Verify all files created
- [ ] Test embedding generation with a sample query
- [ ] Verify vector store contains indexed chunks
- [ ] Test semantic search returns relevant results

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Random/irrelevant results | Embedding provider not configured (still using placeholder) |
| API errors | Check API key and network connectivity |
| Empty results | Verify indexing completed and vector store has data |

## Next Phase

Proceed to **5_VERIFY.md** to verify installation.
