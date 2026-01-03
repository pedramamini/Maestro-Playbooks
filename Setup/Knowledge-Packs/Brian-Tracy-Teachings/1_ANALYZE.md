# Phase 1: Analyze Brian Tracy Materials

## Objective

Analyze the source materials to understand content and plan optimal ingestion.

## Analysis Steps

### 1. Inventory Source Materials

List all available files:

```bash
find <source_path> -type f \( -name "*.md" -o -name "*.txt" -o -name "*.pdf" \) -exec ls -lh {} \;
```

### 2. Categorize by Work/Topic

Map files to Brian Tracy's key works and topics:

**Goal Setting:**
- *Goals!* - The 12-step goal-setting system
- *Maximum Achievement* - Personal success program
- Goal-setting worksheets and templates

**Time Management:**
- *Eat That Frog!* - 21 ways to stop procrastinating
- *Time Power* - Time management system
- Daily planning methods

**Sales & Selling:**
- *The Psychology of Selling* - Sales mastery
- *Advanced Selling Strategies* - Complex sales
- *The Art of Closing the Sale* - Closing techniques

**Personal Development:**
- *No Excuses!* - Self-discipline
- *Change Your Thinking, Change Your Life* - Mindset
- *Create Your Own Future* - Personal responsibility

**Business & Leadership:**
- *How the Best Leaders Lead* - Leadership principles
- *TurboStrategy* - Business strategy
- *Delegation & Supervision* - Management

### 3. Extract Key Concepts

Identify core concepts to emphasize:

**Brian Tracy's Core Principles:**
1. **Eat That Frog** - Do the hardest task first
2. **Goal Setting Formula** - Clear, written, deadline, plan, action
3. **Law of Cause and Effect** - Success leaves clues
4. **Continuous Learning** - Read 1 hour daily
5. **The 80/20 Rule** - Focus on high-value activities
6. **Zero-Based Thinking** - "Knowing what I know now..."
7. **ABCDE Method** - Priority setting
8. **Sales Success Formula** - Prospecting, presenting, closing

### 4. Assess Content Quality

For each file, evaluate:

```yaml
file_assessment:
  - file: "<filename>"
    topic: "<category>"
    quality: high|medium|low
    content_type: summary|transcript|notes|full_text
    key_concepts: [<list>]
    estimated_chunks: <count>
```

**Quality Indicators:**
- **High**: Direct quotes, structured content, actionable advice
- **Medium**: Summaries, paraphrased content
- **Low**: Fragmented notes, incomplete content

### 5. Identify Quotable Passages

Mark sections with memorable quotes/principles:

- "Eat that frog!" - Do your most important task first
- "Your life only gets better when you get better"
- "Move out of your comfort zone"
- "Clarity is the key to peak performance"
- "Set priorities and work on the highest-value activities"

### 6. Plan Content Structure

Organize for optimal retrieval:

```yaml
content_structure:
  principles:
    - name: "Eat That Frog"
      sources: [<files>]
      key_points: [<list>]

    - name: "Goal Setting System"
      sources: [<files>]
      key_points: [<list>]

    - name: "Psychology of Selling"
      sources: [<files>]
      key_points: [<list>]

  categories:
    - goal_setting: <file_count>
    - time_management: <file_count>
    - sales: <file_count>
    - personal_development: <file_count>
    - leadership: <file_count>
```

## Analysis Output

Document the following:

```yaml
materials_analysis:
  source_path: "<path>"
  total_files: <count>
  total_size_kb: <size>

  by_category:
    goal_setting:
      files: [<list>]
      estimated_chunks: <count>
    time_management:
      files: [<list>]
      estimated_chunks: <count>
    sales:
      files: [<list>]
      estimated_chunks: <count>
    personal_development:
      files: [<list>]
      estimated_chunks: <count>
    leadership:
      files: [<list>]
      estimated_chunks: <count>

  key_works_covered:
    - "Eat That Frog!"
    - "Goals!"
    - "The Psychology of Selling"
    # etc.

  chunking_strategy: "markdown"  # Best for prose content
  estimated_total_chunks: <count>
```

## Next Phase

Proceed to **2_PLAN_STRUCTURE.md** to design the skill and embedding strategy.
