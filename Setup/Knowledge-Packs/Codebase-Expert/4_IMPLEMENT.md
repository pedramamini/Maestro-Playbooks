# Phase 4: Implement Installation

## Objective

Execute the Codebase Expert knowledge pack installation.

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

### Step 4: Index Codebase

For each source file:
1. Read file content
2. Chunk appropriately (by function/class for code)
3. Generate embeddings
4. Store in vector store

### Step 5: Create Index Metadata

Create `.claude/context/knowledge/codebase/index.json`:

```json
{
  "created": "<date>",
  "files_indexed": <count>,
  "chunks": <count>,
  "languages": ["<lang1>", "<lang2>"],
  "last_updated": "<date>"
}
```

### Step 6: Update Registry

Add to `.claude/config/knowledge-packs.yaml`:

```yaml
- id: codebase-expert
  name: "Codebase Expert"
  installed: "<date>"
  version: "1.0.0"
  sources:
    - path: ".claude/context/knowledge/codebase/"
      type: "directory"
  skill_path: ".claude/skills/Codebase-Expert/SKILL.md"
```

### Step 7: Configure RAG Hook

Ensure RAG retrieval hook is configured in settings.json.

## Post-Implementation

- Verify all files created
- Test semantic search
- Validate skill activation

## Next Phase

Proceed to **5_VERIFY.md** to verify installation.
