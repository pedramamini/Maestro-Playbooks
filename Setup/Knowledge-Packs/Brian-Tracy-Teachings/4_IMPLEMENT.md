# Phase 4: Implement Brian Tracy Teachings

## Objective

Execute the implementation plan: ingest materials, generate embeddings, create skill.

## Implementation Steps

### 1. Create Directory Structure

```bash
# Create required directories
mkdir -p .claude/skills/Brian-Tracy-Teachings
mkdir -p .claude/knowledge
mkdir -p .claude/context/working
```

### 2. Verify RAG Hook Installed

Check if RAG hook exists (may already exist from another pack):

```bash
ls .claude/hooks/rag-retrieval.ts 2>/dev/null
```

If not exists, install from _Core templates.

### 3. Process Source Materials

Read and chunk each source file:

```typescript
// Pseudo-code for ingestion
const files = scanDirectory(sourcePath, {
  include: ['**/*.md', '**/*.txt'],
  exclude: []
});

const chunks = [];
for (const file of files) {
  const content = readFile(file);
  const category = detectCategory(file, content); // goal_setting, sales, etc.

  const fileChunks = chunkDocument(content, file, {
    strategy: 'markdown',
    chunkSize: 800,
    chunkOverlap: 100
  });

  // Enrich with metadata
  for (const chunk of fileChunks) {
    chunk.metadata.category = category;
    chunk.metadata.pack_id = 'brian-tracy-teachings';

    // Detect if chunk contains a key principle
    const principle = detectPrinciple(chunk.text);
    if (principle) {
      chunk.metadata.principle = principle;
    }
  }

  chunks.push(...fileChunks);
}
```

### 4. Category Detection

Classify content by topic:

```typescript
function detectCategory(filename: string, content: string): string {
  const lower = (filename + content).toLowerCase();

  if (lower.includes('goal') || lower.includes('achieve')) {
    return 'goal_setting';
  }
  if (lower.includes('frog') || lower.includes('time') || lower.includes('procrastin')) {
    return 'time_management';
  }
  if (lower.includes('sell') || lower.includes('sales') || lower.includes('close')) {
    return 'sales';
  }
  if (lower.includes('lead') || lower.includes('manag')) {
    return 'leadership';
  }
  return 'personal_development';
}
```

### 5. Principle Detection

Tag chunks containing key principles:

```typescript
const PRINCIPLES = {
  'eat that frog': 'Eat That Frog',
  'do the hardest task first': 'Eat That Frog',
  'abcde': 'ABCDE Method',
  'a-b-c-d-e': 'ABCDE Method',
  'zero-based thinking': 'Zero-Based Thinking',
  'knowing what i now know': 'Zero-Based Thinking',
  '80/20': '80/20 Rule',
  'pareto': '80/20 Rule',
  'write it down': 'Goal Setting Formula',
  'set a deadline': 'Goal Setting Formula',
  'continuous learning': 'Continuous Learning',
  'read every day': 'Continuous Learning'
};

function detectPrinciple(text: string): string | null {
  const lower = text.toLowerCase();
  for (const [pattern, principle] of Object.entries(PRINCIPLES)) {
    if (lower.includes(pattern)) {
      return principle;
    }
  }
  return null;
}
```

### 6. Generate Embeddings

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
      metadata: batch[j].metadata
    });
  }

  console.log(`Processed ${Math.min(i + BATCH_SIZE, chunks.length)}/${chunks.length} chunks`);
}
```

### 7. Store Embeddings

Save to vector store (append to existing):

```typescript
const vectorStore = createVectorStore({
  type: 'local',
  path: '.claude/knowledge/vectors.json'
});

// Remove old brian-tracy embeddings (for updates)
vectorStore.deleteByPack('brian-tracy-teachings');

// Add new embeddings
vectorStore.add(documents);
```

### 8. Register Knowledge Pack

Update `.claude/config/knowledge-packs.yaml`:

```yaml
version: "1.0.0"
installed_packs:
  # ... existing packs ...

  - id: brian-tracy-teachings
    name: "Brian Tracy Teachings"
    installed: "{{CURRENT_DATE}}"
    version: "1.0.0"
    sources:
      - path: "{{SOURCE_PATH}}"
        type: "documents"
    embeddings_path: ".claude/knowledge/vectors.json"
    skill_path: ".claude/skills/Brian-Tracy-Teachings/SKILL.md"
    metadata:
      chunks: {{CHUNK_COUNT}}
      files: {{FILE_COUNT}}
      categories:
        goal_setting: {{COUNT}}
        time_management: {{COUNT}}
        sales: {{COUNT}}
        personal_development: {{COUNT}}
        leadership: {{COUNT}}
```

### 9. Create Skill File

Write `.claude/skills/Brian-Tracy-Teachings/SKILL.md` from template:

**Fill in the following placeholders:**
- `{{WORKS_LIST}}` - List of works/sources covered
- `{{INSTALL_DATE}}` - Current date
- `{{CHUNK_COUNT}}` - Number of chunks created
- `{{CATEGORIES_SUMMARY}}` - Breakdown by category

### 10. Verify Installation

Run quick verification:

```bash
# Check skill exists
ls -la .claude/skills/Brian-Tracy-Teachings/SKILL.md

# Check embeddings include this pack
cat .claude/knowledge/vectors.json | grep "brian-tracy-teachings" | head -1

# Check registry
grep "brian-tracy" .claude/config/knowledge-packs.yaml
```

## Implementation Summary

Document what was created:

```yaml
implementation_summary:
  skill_created: ".claude/skills/Brian-Tracy-Teachings/SKILL.md"
  embeddings_stored: ".claude/knowledge/vectors.json"
  registry_updated: ".claude/config/knowledge-packs.yaml"

  statistics:
    files_processed: <count>
    chunks_generated: <count>
    embeddings_created: <count>
    by_category:
      goal_setting: <count>
      time_management: <count>
      sales: <count>
      personal_development: <count>
      leadership: <count>

  principles_tagged:
    - "Eat That Frog": <chunk_count>
    - "ABCDE Method": <chunk_count>
    - "Goal Setting Formula": <chunk_count>
    # etc.
```

## Next Phase

Proceed to **5_VERIFY.md** to test the installation.
