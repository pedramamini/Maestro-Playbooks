# Phase 0: Initialize

## Objective

Validate prerequisites for installing the codebase-expert knowledge pack.

## Prerequisites Checklist

### 1. OpenCode Cognitive Infrastructure

Verify the agent has OpenCode Cognitive Infrastructure installed:

- [ ] `.opencode/` directory exists
- [ ] `.opencode/skill/` directory exists
- [ ] `.opencode/memory/` directory exists
- [ ] `.opencode/VERSION` contains valid version

### 2. Codebase Presence

Verify there is a codebase to analyze:

- [ ] Source code files exist in the agent directory
- [ ] At least one recognized language present (js, ts, py, go, etc.)

### 3. Runtime Requirements

Verify required tools are available:

- [ ] Node.js (v18+) or Bun runtime
- [ ] npm available for dependencies

## Validation Steps

1. Check for `.opencode/` directory
2. Scan for source code files
3. Identify primary languages
4. Verify runtime availability

## Next Phase

Once prerequisites are validated, proceed to **1_ANALYZE.md**.
