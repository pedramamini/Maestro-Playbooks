# Phase 1: Analyze Codebase

## Objective

Scan the target codebase to understand its structure and plan the knowledge ingestion.

## Analysis Steps

### 1. Scan Directory Structure

Map the codebase structure:

```bash
# Get directory tree (excluding common non-essential directories)
find <codebase_path> -type d \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/venv/*" \
  | head -50
```

### 2. Identify File Types

Count files by extension to understand the codebase composition:

```bash
find <codebase_path> -type f \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
```

### 3. Locate Key Files

Identify high-value files for ingestion:

**Documentation:**
- `README.md` files at any level
- `docs/` directory contents
- `*.md` files in root
- `CONTRIBUTING.md`, `CHANGELOG.md`

**Configuration:**
- `package.json` - project metadata
- `tsconfig.json` - TypeScript config
- `pyproject.toml` - Python project
- `.env.example` - environment variables

**Code Entry Points:**
- `src/index.ts` or `src/main.ts`
- `app.py` or `main.py`
- `cmd/` directory (Go)
- `src/lib.rs` (Rust)

### 4. Estimate Ingestion Scope

Calculate approximate ingestion size:

```bash
# Count total files to ingest
find <codebase_path> -type f \
  \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
     -o -name "*.py" -o -name "*.go" -o -name "*.rs" \
     -o -name "*.md" -o -name "*.txt" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  | wc -l

# Estimate total size
find <codebase_path> -type f \
  \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
     -o -name "*.py" -o -name "*.go" -o -name "*.rs" \
     -o -name "*.md" -o -name "*.txt" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -exec cat {} \; 2>/dev/null | wc -c
```

### 5. Detect Project Type

Determine the primary technology stack:

| Indicator | Project Type |
|-----------|--------------|
| `package.json` with TypeScript | TypeScript/Node.js |
| `package.json` without TypeScript | JavaScript/Node.js |
| `pyproject.toml` or `setup.py` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml` or `build.gradle` | Java |

### 6. Identify Architecture Patterns

Look for architectural indicators:

- **Monorepo:** `packages/`, `apps/`, `libs/` directories
- **Microservices:** Multiple service directories
- **MVC:** `models/`, `views/`, `controllers/`
- **Domain-Driven:** `domain/`, `infrastructure/`, `application/`

## Analysis Output

Document the following:

```yaml
codebase_analysis:
  path: "<codebase_path>"
  name: "<project name from package.json or directory>"
  type: "<typescript|javascript|python|go|rust|mixed>"

  structure:
    total_files: <count>
    total_size_kb: <size>
    primary_language: "<language>"
    secondary_languages: [<list>]

  key_directories:
    - src/
    - docs/
    - tests/

  key_files:
    - README.md
    - package.json
    - src/index.ts

  exclusions:
    - node_modules/
    - dist/
    - .git/

  chunking_strategy: "code"  # or "mixed" for docs + code
  estimated_chunks: <approximate count>
```

## Next Phase

Proceed to **2_PLAN_STRUCTURE.md** to design the skill and plan chunk generation.
