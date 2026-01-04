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
  - show me
  - find the
context_budget: 8000
---

# Codebase Expert: {{PROJECT_NAME}}

## Overview

Deep expertise in the **{{PROJECT_NAME}}** codebase. This skill provides RAG-powered code understanding with automatic retrieval of relevant code snippets.

### Capabilities

- **Code Understanding**: Explain how specific functions, classes, and modules work
- **Architecture Knowledge**: Understand the overall system design and patterns
- **Implementation Guidance**: Help implement features consistent with existing patterns
- **Navigation**: Quickly locate relevant code for any task

## How RAG Works

When you ask questions about this codebase:

1. The RAG hook automatically searches indexed code
2. Relevant snippets are injected into `.claude/context/working/rag-context.md`
3. This context informs responses about the codebase

**Always check** `.claude/context/working/rag-context.md` for pre-retrieved context.

## Codebase Profile

| Attribute | Value |
|-----------|-------|
| **Project** | {{PROJECT_NAME}} |
| **Type** | {{PROJECT_TYPE}} |
| **Primary Language** | {{PRIMARY_LANGUAGE}} |
| **Location** | {{CODEBASE_PATH}} |
| **Files Indexed** | {{FILE_COUNT}} |
| **Code Chunks** | {{CHUNK_COUNT}} |

## Key Directories

{{KEY_DIRECTORIES_LIST}}

## Architecture Notes

{{ARCHITECTURE_NOTES}}

## Usage Guidelines

When answering questions about this codebase:

1. **Reference Sources**: Always cite specific files and line numbers
2. **Follow Patterns**: Recommend implementations consistent with existing code style
3. **Check Context**: Review `rag-context.md` for relevant retrieved snippets
4. **Stay Current**: Note that indexed content reflects the codebase at ingestion time

## Example Queries

- "How does authentication work in this codebase?"
- "Where is the database connection configured?"
- "Explain the error handling pattern used"
- "Show me how API routes are structured"
- "What's the testing approach in this project?"

---

*Knowledge Pack: Codebase Expert | Updated: {{INSTALL_DATE}}*
