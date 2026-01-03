# Phase 3: Evaluate Plan

## Objective

Review and validate the implementation plan before proceeding.

## Evaluation Checklist

### 1. Skill Definition Review

Verify the planned SKILL.md:

- [ ] **Name** is clear and descriptive
- [ ] **Triggers** cover relevant query patterns
- [ ] **Priority** (75) allows other skills to take precedence when more specific
- [ ] **Context budget** (8000) is appropriate for code explanations
- [ ] **Overview** accurately describes the codebase

### 2. Chunking Strategy Validation

Verify chunking approach:

- [ ] Strategy matches content types (code vs docs)
- [ ] Chunk size appropriate for embedding model
- [ ] Overlap prevents context loss at boundaries
- [ ] Exclusions are correct (node_modules, .git, etc.)

### 3. File Selection Review

Verify file selection:

- [ ] High-priority files include core business logic
- [ ] Entry points are captured
- [ ] Documentation is included
- [ ] Tests included (for behavior reference)
- [ ] No sensitive files (secrets, credentials) included

**Security Check:**
```
Ensure these are EXCLUDED:
- .env files
- *credentials*
- *secret*
- *.pem, *.key
- config files with API keys
```

### 4. Storage Validation

Verify storage paths:

- [ ] Vectors path is within `.claude/knowledge/`
- [ ] Registry path is `.claude/config/knowledge-packs.yaml`
- [ ] Skill path is `.claude/skills/Codebase-Expert/`

### 5. Hook Configuration

Verify RAG hook setup:

- [ ] RAG hook will be installed at `.claude/hooks/rag-retrieval.ts`
- [ ] Hook is registered in `.claude/settings.json`
- [ ] Hook triggers on appropriate tools (Read, Grep, Glob)

### 6. Conflict Check

Check for potential conflicts:

- [ ] No existing Codebase-Expert skill (or update is intended)
- [ ] No conflicting embeddings in vector store
- [ ] Settings.json can accommodate new hook

## Estimated Impact

Calculate the expected outcome:

```yaml
estimated_impact:
  new_chunks: <count>
  storage_size_kb: <estimated>
  skill_file: 1
  hook_files: 1 (if not exists)

  capabilities_added:
    - Answer questions about codebase structure
    - Explain function/class implementations
    - Guide feature implementation
    - Navigate to relevant code quickly
```

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Large codebase slow to embed | Medium | Use batch processing, show progress |
| Sensitive data exposure | Low | Exclusion patterns, security check |
| Poor retrieval quality | Medium | Tune chunk size, test queries |
| Hook conflicts | Low | Check existing hooks first |

## Approval Gate

**Confirm the following before proceeding:**

1. ✓ Skill definition is appropriate for the codebase
2. ✓ Chunking strategy will produce quality embeddings
3. ✓ No sensitive files will be ingested
4. ✓ Storage paths are correct
5. ✓ No critical conflicts detected

## Adjustments Needed

If any issues found, document required changes:

```yaml
adjustments:
  - description: "<what needs to change>"
    reason: "<why>"
    action: "<how to fix>"
```

## Next Phase

If evaluation passes, proceed to **4_IMPLEMENT.md** to execute the plan.

If adjustments needed, return to **2_PLAN_STRUCTURE.md** to revise.
