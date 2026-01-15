# codebase-expert Knowledge Pack

Installs the codebase-expert knowledge pack, enabling RAG-powered code understanding with semantic search across the codebase.

## What This Pack Does

The codebase-expert pack gives your agent deep understanding of your codebase:

- **Semantic Code Search** - Find relevant code by meaning, not just keywords
- **Architecture Understanding** - Understand how components connect
- **Pattern Recognition** - Identify common patterns and conventions
- **Context-Aware Assistance** - Get help that understands your specific codebase

## Prerequisites

- OpenCode Cognitive Infrastructure must be installed first
- A codebase to analyze (the agent's working directory)

## Installation

Run this playbook after OpenCode Cognitive Infrastructure is set up. The playbook will:

1. Analyze the codebase structure
2. Index code files for semantic search
3. Install the codebase-expert skill
4. Configure RAG retrieval plugin (optional)

## After Installation

The agent will automatically:
- Retrieve relevant code context when answering questions
- Understand the codebase architecture
- Reference specific files and functions in responses

## Skill Triggers

The codebase-expert skill activates on queries about:
- Code structure and architecture
- Finding specific functionality
- Understanding how components work
- Debugging and troubleshooting

## Assets

This playbook includes the following assets in the `assets/` folder:

| Asset | Purpose |
|-------|---------|
| `lib/embeddings.ts` | Text embedding generation (placeholder - configure provider) |
| `lib/vector-store.ts` | Vector storage for semantic search |
| `lib/chunking.ts` | Document chunking strategies |
| `lib/registry.ts` | Knowledge pack registration |
| `templates/skills/codebase-expert/SKILL.md` | Skill definition template |

Reference assets using `{{AUTORUN_FOLDER}}/assets/` in playbook documents.

### Configuration Required

The `embeddings.ts` file contains a **placeholder implementation**. You must configure an actual embedding provider (OpenAI, Ollama, etc.) for semantic search to work. See the file comments for configuration examples.

## OpenCode-Specific Notes

This pack follows OpenCode conventions:
- Skill name uses lowercase-with-hyphens (`codebase-expert`)
- Files install to `.opencode/skill/` and `.opencode/memory/`
- Plugins use TypeScript with `@opencode-ai/plugin` types

---

*codebase-expert Knowledge Pack v1.0.0*
