# Phase 0: Initialize Brian Tracy Teachings Knowledge Pack

## Objective

Validate prerequisites for installing the Brian Tracy Teachings knowledge pack.

## Prerequisites Check

### 1. Verify Claude Cognitive Infrastructure Exists

Check that the target agent has Claude Cognitive Infrastructure installed:

```
Required structure:
.claude/
├── config/
├── context/
├── skills/
└── hooks/
```

**If `.claude/` directory does not exist:**
- STOP - Run the "Claude Cognitive Infrastructure Setup" playbook first
- This knowledge pack requires the base infrastructure

### 2. Verify Runtime Available

Check for Node.js or Bun:

```bash
node --version || bun --version
```

At least one must be available for embedding generation.

### 3. Locate Source Materials

Identify Brian Tracy materials to ingest:

**Look for:**
- Book summaries (`.md`, `.txt` files)
- Transcripts from audiobooks/podcasts
- Course materials
- Personal notes from seminars
- PDF books (note: requires text extraction)

**Common locations:**
- `~/Documents/Books/Brian Tracy/`
- `~/Notes/Personal Development/`
- `~/Downloads/` (recent purchases)

**Ask user if materials not found automatically.**

### 4. Validate Source Quality

Check that source materials are suitable:

```bash
# Count available files
find <source_path> -type f \( -name "*.md" -o -name "*.txt" \) | wc -l

# Check total content size
find <source_path> -type f \( -name "*.md" -o -name "*.txt" \) -exec cat {} \; | wc -c
```

**Minimum recommended:**
- At least 3-5 source files
- At least 50KB of content
- Mix of topics (sales, goals, productivity)

### 5. Check for Existing Installation

Check if Brian-Tracy-Teachings pack is already installed:

```bash
cat .claude/config/knowledge-packs.yaml 2>/dev/null | grep "brian-tracy"
```

If already installed:
- This will be an **update** operation
- Existing embeddings will be replaced
- Other knowledge packs will be preserved

### 6. Categorize Available Materials

Organize materials by topic:

| Category | Files | Priority |
|----------|-------|----------|
| Goal Setting | | High |
| Time Management | | High |
| Sales/Selling | | High |
| Personal Development | | Medium |
| Leadership/Management | | Medium |
| General Wisdom | | Low |

## Validation Checklist

- [ ] `.claude/` directory exists with required subdirectories
- [ ] Node.js or Bun runtime available
- [ ] Source materials located (minimum 50KB)
- [ ] Materials organized by category
- [ ] Legal access to materials confirmed

## Output

Record the following for subsequent phases:

```yaml
agent_directory: "<path to agent>"
source_path: "<path to Brian Tracy materials>"
is_update: <true/false>
runtime: "<node/bun>"

materials_found:
  total_files: <count>
  total_size_kb: <size>
  categories:
    goal_setting: <count>
    time_management: <count>
    sales: <count>
    personal_development: <count>
    leadership: <count>
```

## Next Phase

Proceed to **1_ANALYZE.md** to analyze the materials and plan ingestion.
