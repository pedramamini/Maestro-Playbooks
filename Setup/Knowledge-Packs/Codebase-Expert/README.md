# Codebase Expert Knowledge Pack

Installs the Codebase Expert knowledge pack, enabling RAG-powered code understanding with semantic search across the codebase.

## What This Pack Does

The Codebase Expert pack gives your agent deep understanding of your codebase:

- **Semantic Code Search** - Find relevant code by meaning, not just keywords
- **Architecture Understanding** - Understand how components connect
- **Pattern Recognition** - Identify common patterns and conventions
- **Context-Aware Assistance** - Get help that understands your specific codebase

## Prerequisites

- Claude Cognitive Infrastructure must be installed first
- A codebase to analyze (the agent's working directory)

## Installation

Run this playbook after Claude Cognitive Infrastructure is set up. The playbook will:

1. Analyze the codebase structure
2. Index code files for semantic search
3. Install the Codebase-Expert skill
4. Configure RAG retrieval hooks

## After Installation

The agent will automatically:
- Retrieve relevant code context when answering questions
- Understand the codebase architecture
- Reference specific files and functions in responses

## Skill Triggers

The Codebase-Expert skill activates on queries about:
- Code structure and architecture
- Finding specific functionality
- Understanding how components work
- Debugging and troubleshooting

## Assets

This playbook includes the following assets in the `assets/` folder:

| Asset | Purpose |
|-------|---------|
| `hooks/rag-retrieval.ts` | Pre-tool hook for context injection |
| `lib/embeddings.ts` | Text embedding generation (placeholder - configure provider) |
| `lib/vector-store.ts` | Vector storage for semantic search |
| `lib/chunking.ts` | Document chunking strategies |
| `lib/registry.ts` | Knowledge pack registration |
| `templates/skills/Codebase-Expert/SKILL.md` | Skill definition template |

Reference assets using `{{AUTORUN_FOLDER}}/assets/` in playbook documents.

### Configuration Required

The `embeddings.ts` file contains a **placeholder implementation**. You must configure an actual embedding provider (OpenAI, Ollama, etc.) for semantic search to work. See the file comments for configuration examples.

---

*Codebase Expert Knowledge Pack v1.0.0*
