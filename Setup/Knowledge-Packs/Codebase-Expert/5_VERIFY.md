# Phase 5: Verify Codebase Expert Installation

## Objective

Validate that the Codebase Expert knowledge pack is correctly installed and functioning.

## Verification Tests

### 1. Structure Verification

Verify all files were created:

```bash
# Check skill file
test -f .claude/skills/Codebase-Expert/SKILL.md && echo "✓ Skill file exists" || echo "✗ Skill file missing"

# Check embeddings
test -f .claude/knowledge/vectors.json && echo "✓ Vector store exists" || echo "✗ Vector store missing"

# Check registry
test -f .claude/config/knowledge-packs.yaml && echo "✓ Registry exists" || echo "✗ Registry missing"

# Check RAG hook
test -f .claude/hooks/rag-retrieval.ts && echo "✓ RAG hook exists" || echo "✗ RAG hook missing"
```

### 2. Content Verification

Verify file contents are valid:

```bash
# Check SKILL.md has required frontmatter
head -20 .claude/skills/Codebase-Expert/SKILL.md

# Check vector store has documents
cat .claude/knowledge/vectors.json | head -c 500

# Check registry has codebase-expert entry
grep "codebase-expert" .claude/config/knowledge-packs.yaml
```

### 3. Embedding Count Verification

Verify expected number of embeddings:

```bash
# Count documents in vector store
cat .claude/knowledge/vectors.json | grep -c '"id":'
```

**Expected**: Should match the chunk count from implementation phase.

### 4. Hook Registration Verification

Verify RAG hook is registered in settings:

```bash
# Check settings.json includes RAG hook
cat .claude/settings.json | grep -A5 "PreToolUse"
```

### 5. Retrieval Test

Test that retrieval works:

```bash
# Create a test query file
echo '{"tool_name": "Grep", "tool_input": {"pattern": "main function"}}' > /tmp/test-query.json

# Run RAG hook manually
cd <agent_directory>
cat /tmp/test-query.json | npx ts-node .claude/hooks/rag-retrieval.ts

# Check if context was injected
cat .claude/context/working/rag-context.md 2>/dev/null
```

### 6. Skill Trigger Test

Verify skill triggers correctly:

Test queries that should activate the skill:
- "How does the authentication work in this codebase?"
- "Where is the main entry point?"
- "Explain the database connection code"

These should:
1. Trigger the RAG hook
2. Inject relevant context to `rag-context.md`
3. Activate the Codebase-Expert skill

## Verification Checklist

### Files Created
- [ ] `.claude/skills/Codebase-Expert/SKILL.md` exists and valid
- [ ] `.claude/knowledge/vectors.json` exists with embeddings
- [ ] `.claude/config/knowledge-packs.yaml` has pack registered
- [ ] `.claude/hooks/rag-retrieval.ts` exists (if newly installed)

### Content Valid
- [ ] SKILL.md has correct frontmatter (name, triggers, priority)
- [ ] Vector store contains expected chunk count
- [ ] Registry entry has correct metadata

### Functionality
- [ ] RAG hook executes without errors
- [ ] Retrieval returns relevant results for test queries
- [ ] Context injection creates/updates rag-context.md

## Test Results

Document verification results:

```yaml
verification_results:
  structure:
    skill_file: <pass/fail>
    vector_store: <pass/fail>
    registry: <pass/fail>
    rag_hook: <pass/fail>

  content:
    skill_valid: <pass/fail>
    embeddings_count: <count>
    registry_entry: <pass/fail>

  functionality:
    hook_execution: <pass/fail>
    retrieval_test: <pass/fail>
    context_injection: <pass/fail>

  overall_status: <PASS/FAIL>
```

## Troubleshooting

### RAG Hook Not Triggering
- Check `.claude/settings.json` has hook registered
- Verify hook path is correct
- Check for TypeScript compilation errors

### No Relevant Results
- Verify embeddings were generated correctly
- Check chunk size isn't too large/small
- Verify query is matching content

### Context Not Injected
- Check `.claude/context/working/` directory exists
- Verify hook has write permissions
- Check for errors in hook execution

## Success Criteria

The Codebase Expert knowledge pack is successfully installed when:

1. ✓ All files exist in correct locations
2. ✓ Embeddings count matches expected chunks
3. ✓ Registry correctly lists the pack
4. ✓ RAG hook executes without errors
5. ✓ Test queries return relevant code snippets
6. ✓ Context is injected into working memory

## Installation Complete

If all verifications pass:

```
✅ Codebase Expert Knowledge Pack Successfully Installed

The agent now has deep expertise in the {{PROJECT_NAME}} codebase.

Features enabled:
- Automatic retrieval of relevant code on queries
- Code explanation and navigation
- Implementation guidance following existing patterns

To update knowledge: Re-run this playbook
To remove: Delete .claude/skills/Codebase-Expert/ and remove registry entry
```
