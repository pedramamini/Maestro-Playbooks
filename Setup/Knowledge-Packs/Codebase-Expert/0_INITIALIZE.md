# Phase 0: Initialize Codebase Expert Knowledge Pack

## Objective

Validate prerequisites for installing the Codebase Expert knowledge pack.

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

### 3. Identify Target Codebase

Determine which codebase to ingest:

- Look for codebase path in the current directory or parent directories
- Check for common indicators:
  - `package.json` (Node.js project)
  - `pyproject.toml` or `setup.py` (Python project)
  - `go.mod` (Go project)
  - `Cargo.toml` (Rust project)
  - `src/` directory
- If multiple codebases possible, use the primary project directory

**Record the codebase path for the ANALYZE phase.**

### 4. Check for Existing Installation

Check if Codebase-Expert pack is already installed:

```bash
cat .claude/config/knowledge-packs.yaml 2>/dev/null | grep "codebase-expert"
```

If already installed:
- This will be an **update** operation
- Existing embeddings will be replaced
- Other knowledge packs will be preserved

### 5. Verify _Core Utilities

Check that _Core utilities are available:

If running from Maestro-Playbooks:
- `Setup/Knowledge-Packs/_Core/` should contain the shared utilities

If _Core not found:
- The RAG hook will need to be copied from the playbook templates
- Embedding will use local algorithm (no external API required)

## Validation Checklist

- [ ] `.claude/` directory exists with required subdirectories
- [ ] Node.js or Bun runtime available
- [ ] Target codebase identified and accessible
- [ ] _Core utilities located or local fallback available

## Output

Record the following for subsequent phases:

```yaml
agent_directory: "<path to agent>"
codebase_path: "<path to codebase to ingest>"
is_update: <true/false>
runtime: "<node/bun>"
```

## Next Phase

Proceed to **1_ANALYZE.md** to scan the codebase and plan the ingestion.
