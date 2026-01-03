# Phase 2: Plan Structure

## Objective

Design the Brian Tracy Teachings skill and plan the embedding strategy.

## Skill Design

### Generate SKILL.md Content

Create a skill definition optimized for personal development advice:

```markdown
---
name: Brian-Tracy-Teachings
version: 1.0.0
priority: 70
triggers:
  - goal
  - goals
  - time management
  - productivity
  - procrastination
  - sales
  - selling
  - success
  - achievement
  - motivation
  - discipline
  - brian tracy
  - eat that frog
  - priorities
context_budget: 6000
---

# Brian Tracy Teachings

## Overview

Expertise in Brian Tracy's personal development, sales, and business philosophy.
Provides advice grounded in his proven principles and methodologies.

### Core Areas

1. **Goal Setting**: The systematic approach to achieving any goal
2. **Time Management**: Maximizing productivity and eliminating procrastination
3. **Sales Excellence**: Psychology of selling and closing techniques
4. **Personal Development**: Building habits for success
5. **Leadership**: Leading yourself and others effectively

## How to Apply

When providing advice:
1. Check `.claude/context/working/rag-context.md` for relevant teachings
2. Reference specific Brian Tracy principles
3. Provide actionable steps based on his methodologies
4. Quote memorable phrases when appropriate

## Key Principles

### Eat That Frog
Do your most important, most challenging task first thing in the morning.

### Goal Setting Formula
1. Decide exactly what you want
2. Write it down
3. Set a deadline
4. Make a list of everything needed
5. Organize by priority
6. Take action immediately
7. Do something every day

### ABCDE Priority Method
- A = Must do (serious consequences)
- B = Should do (mild consequences)
- C = Nice to do (no consequences)
- D = Delegate
- E = Eliminate

### Zero-Based Thinking
Ask: "Knowing what I now know, would I get into this again?"

## Works Covered

{{WORKS_LIST}}
```

### Chunking Strategy

For prose/teaching content:

| Content Type | Strategy | Chunk Size | Overlap |
|--------------|----------|------------|---------|
| Book summaries | `markdown` | 800 chars | 100 |
| Transcripts | `fixed` | 1000 chars | 150 |
| Notes | `markdown` | 600 chars | 80 |
| Quotes/principles | `fixed` | 400 chars | 50 |

**Rationale**: Smaller chunks for teaching content ensures precise retrieval of specific principles.

### Metadata Enrichment

Add rich metadata to each chunk:

```yaml
chunk_metadata:
  pack_id: "brian-tracy-teachings"
  source: "<filename>"
  category: "<goal_setting|time_management|sales|...>"
  work: "<book title if known>"
  principle: "<core principle if applicable>"
```

### Embedding Configuration

```yaml
embedding_config:
  provider: "local"
  dimensions: 384
  batch_size: 50

  # Note: Local embedding works well for teaching content
  # OpenAI optional for improved semantic matching
```

## Plan Output

Document the implementation plan:

```yaml
implementation_plan:
  skill:
    name: "Brian-Tracy-Teachings"
    path: ".claude/skills/Brian-Tracy-Teachings/SKILL.md"
    triggers: [goal, goals, time management, productivity, sales, success, brian tracy]
    priority: 70  # Slightly lower than codebase (75) to complement

  ingestion:
    strategy: "markdown"
    files_to_process: <count>
    estimated_chunks: <count>
    by_category:
      goal_setting: <chunk_count>
      time_management: <chunk_count>
      sales: <chunk_count>
      personal_development: <chunk_count>
      leadership: <chunk_count>

  storage:
    vectors_path: ".claude/knowledge/vectors.json"
    registry_path: ".claude/config/knowledge-packs.yaml"

  hooks:
    rag_hook: ".claude/hooks/rag-retrieval.ts"
    hook_exists: <true/false>
```

## Generated Content Preview

Preview the SKILL.md that will be created with filled placeholders.

## Principle Extraction

Extract key principles to ensure they're well-represented:

| Principle | Source | Chunk Priority |
|-----------|--------|----------------|
| Eat That Frog | ETF book | High |
| Goal Setting Formula | Goals! | High |
| ABCDE Method | ETF/Time Power | High |
| 80/20 Rule | Multiple | High |
| Zero-Based Thinking | Multiple | Medium |
| Continuous Learning | Multiple | Medium |
| Sales Success Formula | Psychology of Selling | High |

## Next Phase

Proceed to **3_EVALUATE.md** to review the plan before implementation.
