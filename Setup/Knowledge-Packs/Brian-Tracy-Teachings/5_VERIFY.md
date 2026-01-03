# Phase 5: Verify Brian Tracy Teachings Installation

## Objective

Validate that the Brian Tracy Teachings knowledge pack is correctly installed and functioning.

## Verification Tests

### 1. Structure Verification

Verify all files were created:

```bash
# Check skill file
test -f .claude/skills/Brian-Tracy-Teachings/SKILL.md && echo "✓ Skill file exists" || echo "✗ Skill file missing"

# Check registry has entry
grep -q "brian-tracy-teachings" .claude/config/knowledge-packs.yaml && echo "✓ Registry entry exists" || echo "✗ Registry entry missing"

# Check embeddings exist for this pack
grep -q "brian-tracy-teachings" .claude/knowledge/vectors.json && echo "✓ Embeddings exist" || echo "✗ Embeddings missing"
```

### 2. Content Verification

Verify file contents are valid:

```bash
# Check SKILL.md has required frontmatter
head -20 .claude/skills/Brian-Tracy-Teachings/SKILL.md

# Count embeddings for this pack
grep -c "brian-tracy-teachings" .claude/knowledge/vectors.json
```

### 3. Category Distribution

Verify content coverage across categories:

```bash
# Check category distribution in embeddings
for cat in goal_setting time_management sales personal_development leadership; do
  count=$(grep -c "\"category\":\"$cat\"" .claude/knowledge/vectors.json 2>/dev/null || echo 0)
  echo "$cat: $count chunks"
done
```

**Expected**: At least 2-3 categories should have content.

### 4. Principle Coverage

Verify key principles are tagged:

```bash
# Check for key principles in embeddings
for principle in "Eat That Frog" "ABCDE Method" "Goal Setting Formula" "80/20 Rule"; do
  count=$(grep -c "\"principle\":\"$principle\"" .claude/knowledge/vectors.json 2>/dev/null || echo 0)
  echo "$principle: $count chunks"
done
```

### 5. Retrieval Test

Test that retrieval works for typical queries:

**Test Query 1: Goal Setting**
```bash
echo '{"tool_name": "Task", "tool_input": {"prompt": "How do I set effective goals?"}}' | \
  npx ts-node .claude/hooks/rag-retrieval.ts

cat .claude/context/working/rag-context.md
```

**Test Query 2: Procrastination**
```bash
echo '{"tool_name": "Task", "tool_input": {"prompt": "How do I stop procrastinating?"}}' | \
  npx ts-node .claude/hooks/rag-retrieval.ts

cat .claude/context/working/rag-context.md
```

**Test Query 3: Priorities**
```bash
echo '{"tool_name": "Task", "tool_input": {"prompt": "How should I prioritize my tasks?"}}' | \
  npx ts-node .claude/hooks/rag-retrieval.ts

cat .claude/context/working/rag-context.md
```

### 6. Skill Trigger Test

Verify skill triggers correctly by checking trigger words:

| Query | Should Trigger | Expected Content |
|-------|----------------|------------------|
| "Help me set goals" | Yes | Goal Setting Formula |
| "I keep procrastinating" | Yes | Eat That Frog |
| "How to prioritize" | Yes | ABCDE Method |
| "Sales advice" | Yes (if sales content) | Sales principles |
| "What would Brian Tracy say?" | Yes | General wisdom |

## Verification Checklist

### Files Created
- [ ] `.claude/skills/Brian-Tracy-Teachings/SKILL.md` exists and valid
- [ ] `.claude/config/knowledge-packs.yaml` has pack registered
- [ ] `.claude/knowledge/vectors.json` contains pack embeddings

### Content Valid
- [ ] SKILL.md has correct frontmatter and triggers
- [ ] Embeddings distributed across categories
- [ ] Key principles are tagged

### Functionality
- [ ] RAG retrieval returns relevant content for goal-setting queries
- [ ] RAG retrieval returns relevant content for time management queries
- [ ] Context injection creates/updates rag-context.md
- [ ] Skill triggers on appropriate queries

## Test Results

Document verification results:

```yaml
verification_results:
  structure:
    skill_file: <pass/fail>
    registry_entry: <pass/fail>
    embeddings: <pass/fail>

  content:
    total_chunks: <count>
    categories_covered: [<list>]
    principles_tagged: [<list>]

  retrieval_tests:
    goal_setting_query: <pass/fail>
    procrastination_query: <pass/fail>
    priorities_query: <pass/fail>

  overall_status: <PASS/FAIL>
```

## Troubleshooting

### No Relevant Results
- Verify embeddings were generated for the pack
- Check chunk text contains expected keywords
- Try simpler query terms

### Wrong Category Retrieved
- Review category detection logic
- Check metadata in embeddings
- Consider re-chunking with explicit categories

### Principles Not Tagged
- Verify principle detection patterns
- Check source content contains principle keywords
- Consider manual tagging for key passages

## Success Criteria

The Brian Tracy Teachings pack is successfully installed when:

1. ✓ Skill file exists with correct triggers
2. ✓ Pack registered in knowledge-packs.yaml
3. ✓ Embeddings exist in vector store
4. ✓ Multiple categories have content
5. ✓ Key principles are tagged
6. ✓ Retrieval returns relevant content for test queries

## Installation Complete

If all verifications pass:

```
✅ Brian Tracy Teachings Knowledge Pack Successfully Installed

The agent now has expertise in Brian Tracy's teachings.

Capabilities enabled:
- Goal setting guidance using the 7-step formula
- Time management advice (Eat That Frog, ABCDE Method)
- Personal development coaching
- Productivity recommendations
- Sales advice (if sales content included)

Example queries to try:
- "How do I stop procrastinating on important tasks?"
- "Help me create an effective goal-setting system"
- "What's the best way to prioritize my work?"
- "What would Brian Tracy recommend for [situation]?"

To update knowledge: Re-run this playbook with new materials
To remove: Delete skill and remove registry entry
```
