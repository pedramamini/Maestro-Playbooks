# Phase 5: Verify Installation

## Objective

Verify the codebase-expert knowledge pack is correctly installed.

## Verification Checklist

### 1. Files Present

- [ ] `.opencode/skill/codebase-expert/SKILL.md` exists
- [ ] `.opencode/memory/knowledge/codebase/` exists
- [ ] `.opencode/memory/knowledge/codebase/index.json` exists
- [ ] `.opencode/plugin/lib/` contains utility files

### 2. Skill Configuration

- [ ] SKILL.md has valid YAML frontmatter
- [ ] Name is lowercase (`codebase-expert`)
- [ ] Description contains `USE WHEN` trigger
- [ ] Description under 1024 characters

### 3. Index Quality

- [ ] Files were indexed
- [ ] Chunk count is reasonable
- [ ] Languages detected correctly

### 4. Registry Entry

- [ ] Pack is registered in knowledge-packs.yaml
- [ ] Sources path is correct
- [ ] Skill path is correct

## Functional Testing

### Test 1: Skill Discovery

In OpenCode, ask: "What skills are available?"

**Expected**: codebase-expert should appear in the list.

### Test 2: Code Search

Ask: "Where is the main entry point?"

**Expected**: Agent finds and references the main entry file.

### Test 3: Architecture

Ask: "How is the project structured?"

**Expected**: Agent describes directory structure and organization.

### Test 4: Functionality

Ask: "How does [specific feature] work?"

**Expected**: Agent retrieves and explains relevant code.

## Validation Commands

### Check Skill Name

```bash
# Should be lowercase with hyphens
ls -la .opencode/skill/
```

### Verify SKILL.md Format

```bash
# Check frontmatter
head -20 .opencode/skill/codebase-expert/SKILL.md
```

### Check Index

```bash
cat .opencode/memory/knowledge/codebase/index.json
```

## Success Criteria

- All files present
- Skill name follows OpenCode convention (lowercase-with-hyphens)
- Index populated
- Semantic search working
- Skill discoverable by OpenCode

## Troubleshooting

### Skill Not Found

- Verify skill name is lowercase with hyphens
- Check SKILL.md has valid frontmatter
- Ensure `.opencode/skill/codebase-expert/SKILL.md` exists

### No Search Results

- Verify files were indexed
- Check embedding generation is configured
- Confirm vector store populated

### Wrong Results

- Review chunking strategy
- Check file exclusions
- Verify language detection

## Installation Complete

The codebase-expert knowledge pack is now installed.

---

*codebase-expert Knowledge Pack v1.0.0*
