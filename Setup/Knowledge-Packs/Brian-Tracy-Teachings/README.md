# Brian Tracy Teachings Knowledge Pack

A knowledge pack that gives any Claude Cognitive Infrastructure agent expertise in Brian Tracy's personal development, sales, and business philosophy.

## Overview

This playbook ingests Brian Tracy's books, speeches, and teachings to create a "Brian Tracy Teachings" skill that enables RAG-powered advice on:

- **Personal Development**: Goal setting, time management, self-discipline
- **Sales Excellence**: Psychology of selling, closing techniques, prospecting
- **Business Success**: Leadership, management, entrepreneurship
- **Peak Performance**: Habits, productivity, continuous improvement

## Prerequisites

- Target agent must have **Claude Cognitive Infrastructure** already installed
- Source materials (books, transcripts, notes) available on filesystem
- Node.js/Bun runtime available

## What Gets Created

```
.claude/
├── config/
│   └── knowledge-packs.yaml    # Pack registration (created/updated)
├── knowledge/
│   └── vectors.json            # Embeddings storage (created/updated)
├── skills/
│   └── Brian-Tracy-Teachings/
│       └── SKILL.md            # Brian Tracy expertise skill
└── context/
    └── working/
        └── rag-context.md      # Auto-injected relevant teachings
```

## Source Materials

The playbook can ingest various formats:

**Text-Based:**
- `.md` - Markdown notes and summaries
- `.txt` - Plain text transcripts
- `.pdf` - Book PDFs (requires PDF extraction)

**Recommended Sources:**
- Book summaries and notes
- Speech/podcast transcripts
- Course materials
- Personal notes from seminars

**Key Works to Include:**
- *Eat That Frog!* - Time management and procrastination
- *The Psychology of Selling* - Sales mastery
- *Goals!* - Goal setting methodology
- *Maximum Achievement* - Personal development system
- *No Excuses!* - Self-discipline
- *The 21 Success Secrets of Self-Made Millionaires*

## Usage

Run this playbook on an agent that already has Claude Cognitive Infrastructure:

```
Agent Directory/         # Must have .claude/ already
├── CLAUDE.md
└── .claude/
    └── ...              # Existing infrastructure
```

Point the playbook at your Brian Tracy materials during the ANALYZE phase.

## How It Works

Once installed, the agent can:

1. **Apply Brian Tracy Principles**: When asked for advice, draws from his teachings
2. **Quote and Reference**: Cites specific books and concepts
3. **Goal Setting Framework**: Uses his goal-setting methodology
4. **Sales Coaching**: Provides Tracy's sales techniques and psychology

## Example Interactions

After installation, the agent can handle queries like:

- "Help me set goals using Brian Tracy's method"
- "What does Brian Tracy say about overcoming procrastination?"
- "How should I approach this sales call according to Tracy's principles?"
- "What are Brian Tracy's time management strategies?"

## Customization

You can customize the teachings focus:

- **Sales Focus**: Emphasize *Psychology of Selling* and sales materials
- **Productivity Focus**: Emphasize *Eat That Frog* and time management
- **Business Focus**: Emphasize leadership and management materials
- **Personal Development**: Balance across all categories

## Ethical Note

This knowledge pack is designed for educational purposes, helping agents provide advice inspired by Brian Tracy's publicly available teachings. Ensure you have legitimate access to any materials you ingest (purchased books, authorized transcripts, etc.).

---

*Part of the Knowledge Packs system for Claude Cognitive Infrastructure*
