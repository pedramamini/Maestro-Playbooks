# Phase 4: Implement Codebase Expert

## Objective

Execute the implementation plan: ingest codebase, generate embeddings, create skill, configure hooks.

## Implementation Steps

### 1. Create Directory Structure

```bash
# Create required directories
mkdir -p .claude/skills/Codebase-Expert
mkdir -p .claude/knowledge
mkdir -p .claude/context/working
```

### 2. Install RAG Hook (if not exists)

Check if RAG hook exists:

```bash
ls .claude/hooks/rag-retrieval.ts 2>/dev/null
```

If not exists, copy from _Core templates or create inline.

Update `.claude/settings.json` to register the hook:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Grep|Glob|WebSearch|Task",
        "hooks": [
          {
            "type": "command",
            "command": "npx ts-node .claude/hooks/rag-retrieval.ts"
          }
        ]
      }
    ]
  }
}
```

### 3. Scan and Chunk Codebase

Process files in priority order:

```typescript
// Pseudo-code for ingestion
const files = scanCodebase(codebasePath, {
  include: ['**/*.ts', '**/*.tsx', '**/*.js', '**/*.py', '**/*.md'],
  exclude: ['**/node_modules/**', '**/.git/**', '**/dist/**']
});

const chunks = [];
for (const file of files) {
  const content = readFile(file);
  const strategy = detectStrategy(file); // 'code' or 'markdown'
  const fileChunks = chunkDocument(content, file, { strategy });
  chunks.push(...fileChunks);
}
```

### 4. Generate Embeddings

Process chunks in batches:

```typescript
const BATCH_SIZE = 50;
const documents = [];

for (let i = 0; i < chunks.length; i += BATCH_SIZE) {
  const batch = chunks.slice(i, i + BATCH_SIZE);
  const embeddings = await embedBatch(batch.map(c => c.text), config);

  for (let j = 0; j < batch.length; j++) {
    documents.push({
      id: batch[j].id,
      text: batch[j].text,
      embedding: embeddings[j].embedding,
      metadata: {
        ...batch[j].metadata,
        pack_id: 'codebase-expert'
      }
    });
  }

  // Progress indicator
  console.log(`Processed ${Math.min(i + BATCH_SIZE, chunks.length)}/${chunks.length} chunks`);
}
```

### 5. Store Embeddings

Save to vector store:

```typescript
const vectorStore = createVectorStore({
  type: 'local',
  path: '.claude/knowledge/vectors.json'
});

// Remove old codebase-expert embeddings (for updates)
vectorStore.deleteByPack('codebase-expert');

// Add new embeddings
vectorStore.add(documents);
```

### 6. Register Knowledge Pack

Update `.claude/config/knowledge-packs.yaml`:

```yaml
version: "1.0.0"
installed_packs:
  - id: codebase-expert
    name: "Codebase Expert: {{PROJECT_NAME}}"
    installed: "{{CURRENT_DATE}}"
    version: "1.0.0"
    sources:
      - path: "{{CODEBASE_PATH}}"
        type: "codebase"
    embeddings_path: ".claude/knowledge/vectors.json"
    skill_path: ".claude/skills/Codebase-Expert/SKILL.md"
    metadata:
      chunks: {{CHUNK_COUNT}}
      files: {{FILE_COUNT}}
      languages: [{{LANGUAGES}}]
```

### 7. Create Skill File

Write `.claude/skills/Codebase-Expert/SKILL.md`:

```markdown
---
name: Codebase-Expert
version: 1.0.0
priority: 75
triggers:
  - code
  - codebase
  - implementation
  - architecture
  - function
  - class
  - module
  - how does
  - where is
  - explain the
context_budget: 8000
---

# Codebase Expert: {{PROJECT_NAME}}

## Overview

Deep expertise in the {{PROJECT_NAME}} codebase ({{PRIMARY_LANGUAGE}}).

This skill provides RAG-powered code understanding:
- Automatic retrieval of relevant code snippets
- Architecture and pattern knowledge
- Implementation guidance consistent with existing code

## Usage

When this skill activates, relevant code context is automatically injected into `.claude/context/working/rag-context.md`.

Check this file for pre-retrieved code snippets related to the current query.

## Codebase Summary

- **Location**: {{CODEBASE_PATH}}
- **Type**: {{PROJECT_TYPE}}
- **Files indexed**: {{FILE_COUNT}}
- **Code chunks**: {{CHUNK_COUNT}}

## Key Areas

{{KEY_AREAS_LIST}}

## Architecture Notes

{{ARCHITECTURE_NOTES}}
```

### 8. Verify Installation

Run verification checks:

```bash
# Check skill exists
ls -la .claude/skills/Codebase-Expert/SKILL.md

# Check embeddings exist
ls -la .claude/knowledge/vectors.json

# Check registry updated
cat .claude/config/knowledge-packs.yaml

# Check hook registered
cat .claude/settings.json | grep rag-retrieval
```

## Implementation Summary

Document what was created:

```yaml
implementation_summary:
  skill_created: ".claude/skills/Codebase-Expert/SKILL.md"
  embeddings_stored: ".claude/knowledge/vectors.json"
  registry_updated: ".claude/config/knowledge-packs.yaml"
  hook_installed: <true/false>

  statistics:
    files_processed: <count>
    chunks_generated: <count>
    embeddings_created: <count>
    storage_size_kb: <size>

  codebase:
    name: "{{PROJECT_NAME}}"
    path: "{{CODEBASE_PATH}}"
    primary_language: "{{PRIMARY_LANGUAGE}}"
```

## Next Phase

Proceed to **5_VERIFY.md** to test the installation.
