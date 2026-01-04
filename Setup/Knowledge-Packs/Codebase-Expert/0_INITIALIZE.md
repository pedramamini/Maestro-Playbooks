# Phase 0: Initialize

## Objective

Validate prerequisites for installing the Codebase Expert knowledge pack.

## Prerequisites Checklist

### 1. Claude Cognitive Infrastructure

Verify the agent has Claude Cognitive Infrastructure installed:

- [ ] `.claude/` directory exists
- [ ] `.claude/skills/` directory exists
- [ ] `.claude/context/` directory exists
- [ ] `.claude/VERSION` contains valid version

### 2. Codebase Presence

Verify there is a codebase to analyze:

- [ ] Source code files exist in the agent directory
- [ ] At least one recognized language present (js, ts, py, go, etc.)

### 3. _Core Utilities

Verify Knowledge Packs _Core is available:

- [ ] _Core utilities are accessible
- [ ] RAG retrieval hook can be installed

## Validation Steps

1. Check for `.claude/` directory
2. Scan for source code files
3. Identify primary languages
4. Verify _Core availability

## Next Phase

Once prerequisites are validated, proceed to **1_ANALYZE.md**.
