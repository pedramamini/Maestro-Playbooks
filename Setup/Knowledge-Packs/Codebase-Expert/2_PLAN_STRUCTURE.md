# Phase 2: Plan Structure

## Objective

Design the Codebase Expert skill and plan the chunking/embedding strategy.

## Skill Design

### Generate SKILL.md Content

Based on the codebase analysis, create a skill definition:

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

Deep expertise in the {{PROJECT_NAME}} codebase. This skill provides:

- **Code Understanding**: Explain how specific functions, classes, and modules work
- **Architecture Knowledge**: Understand the overall system design and patterns
- **Implementation Guidance**: Help implement features consistent with existing patterns
- **Navigation**: Quickly locate relevant code for any task

## Codebase Profile

- **Type**: {{PROJECT_TYPE}}
- **Primary Language**: {{PRIMARY_LANGUAGE}}
- **Key Directories**: {{KEY_DIRECTORIES}}
- **Architecture Pattern**: {{ARCHITECTURE_PATTERN}}

## How to Use

When answering questions about this codebase:

1. **Check RAG Context**: Look for `.claude/context/working/rag-context.md` for auto-retrieved relevant code
2. **Follow Patterns**: Recommend implementations consistent with existing code style
3. **Reference Sources**: Cite specific files and line numbers when explaining code

## Key Components

{{KEY_COMPONENTS_LIST}}

## Architectural Decisions

{{ARCHITECTURE_NOTES}}
```

### Chunking Strategy

Based on file types, determine chunking approach:

| Content Type | Strategy | Chunk Size | Overlap |
|--------------|----------|------------|---------|
| TypeScript/JavaScript | `code` | 1500 chars | 100 |
| Python | `code` | 1500 chars | 100 |
| Go/Rust | `code` | 1500 chars | 100 |
| Markdown docs | `markdown` | 1200 chars | 100 |
| Config files | `fixed` | 800 chars | 50 |

### File Priority

Assign ingestion priority:

**High Priority (ingest first):**
- README files
- Entry points (index.ts, main.py)
- Core business logic
- API definitions
- Type definitions

**Medium Priority:**
- Utility functions
- Helper modules
- Tests (for understanding expected behavior)

**Low Priority (optional):**
- Generated files
- Vendor code
- Build scripts

### Embedding Configuration

```yaml
embedding_config:
  provider: "local"  # Use local embedding by default
  dimensions: 384
  batch_size: 50

  # Optional: Use OpenAI for better quality
  # provider: "openai"
  # model: "text-embedding-3-small"
  # api_key: "${OPENAI_API_KEY}"
```

## Plan Output

Document the implementation plan:

```yaml
implementation_plan:
  skill:
    name: "Codebase-Expert"
    path: ".claude/skills/Codebase-Expert/SKILL.md"
    triggers: [code, codebase, implementation, architecture]

  ingestion:
    strategy: "code"
    files_to_process: <count>
    estimated_chunks: <count>
    priority_order:
      - high: [README.md, src/index.ts, ...]
      - medium: [src/utils/*, tests/*]
      - low: [scripts/*, configs/*]

  storage:
    vectors_path: ".claude/knowledge/vectors.json"
    registry_path: ".claude/config/knowledge-packs.yaml"

  hooks:
    rag_hook: ".claude/hooks/rag-retrieval.ts"
    hook_exists: <true/false>
```

## Generated Content Preview

Preview the SKILL.md that will be created:

```markdown
# [Generated SKILL.md content here]
```

## Next Phase

Proceed to **3_EVALUATE.md** to review the plan before implementation.
