/**
 * Document Chunking Strategies
 *
 * Split documents into chunks suitable for embedding and retrieval.
 * Different strategies for different content types.
 */

export interface Chunk {
  id: string;
  text: string;
  metadata: {
    source: string;
    chunk_index: number;
    start_line?: number;
    end_line?: number;
    type?: string;
    [key: string]: unknown;
  };
}

export interface ChunkingConfig {
  strategy: "fixed" | "semantic" | "code" | "markdown";
  chunkSize?: number; // Target chunk size in characters
  chunkOverlap?: number; // Overlap between chunks
  minChunkSize?: number; // Minimum chunk size
}

const DEFAULT_CONFIG: ChunkingConfig = {
  strategy: "fixed",
  chunkSize: 1000,
  chunkOverlap: 100,
  minChunkSize: 100,
};

/**
 * Generate a unique chunk ID
 */
function generateChunkId(source: string, index: number): string {
  const hash = source
    .split("")
    .reduce((acc, char) => ((acc << 5) - acc + char.charCodeAt(0)) >>> 0, 0)
    .toString(16);
  return `${hash}-${index}`;
}

/**
 * Fixed-size chunking with overlap
 */
function fixedChunk(
  text: string,
  source: string,
  config: ChunkingConfig
): Chunk[] {
  const { chunkSize = 1000, chunkOverlap = 100, minChunkSize = 100 } = config;
  const chunks: Chunk[] = [];

  let start = 0;
  let index = 0;

  while (start < text.length) {
    let end = start + chunkSize;

    // Try to break at a natural boundary (sentence, paragraph)
    if (end < text.length) {
      const breakPoints = ["\n\n", "\n", ". ", "! ", "? "];
      for (const bp of breakPoints) {
        const lastBreak = text.lastIndexOf(bp, end);
        if (lastBreak > start + minChunkSize) {
          end = lastBreak + bp.length;
          break;
        }
      }
    }

    const chunkText = text.slice(start, end).trim();

    if (chunkText.length >= minChunkSize) {
      chunks.push({
        id: generateChunkId(source, index),
        text: chunkText,
        metadata: {
          source,
          chunk_index: index,
          type: "fixed",
        },
      });
      index++;
    }

    start = end - chunkOverlap;
    if (start >= text.length - minChunkSize) break;
  }

  return chunks;
}

/**
 * Code-aware chunking
 * Respects function/class boundaries
 */
function codeChunk(
  text: string,
  source: string,
  config: ChunkingConfig
): Chunk[] {
  const { chunkSize = 1500, minChunkSize = 100 } = config;
  const chunks: Chunk[] = [];
  const lines = text.split("\n");

  // Patterns that indicate logical boundaries
  const boundaryPatterns = [
    /^(export\s+)?(async\s+)?function\s+\w+/, // Function declarations
    /^(export\s+)?(default\s+)?class\s+\w+/, // Class declarations
    /^(export\s+)?const\s+\w+\s*=\s*(async\s+)?\(/, // Arrow functions
    /^(export\s+)?interface\s+\w+/, // TypeScript interfaces
    /^(export\s+)?type\s+\w+/, // TypeScript types
    /^def\s+\w+/, // Python functions
    /^class\s+\w+/, // Python classes
    /^##\s+/, // Markdown headers
  ];

  let currentChunk: string[] = [];
  let currentSize = 0;
  let chunkStartLine = 0;
  let index = 0;

  function saveChunk(endLine: number) {
    const chunkText = currentChunk.join("\n").trim();
    if (chunkText.length >= minChunkSize) {
      chunks.push({
        id: generateChunkId(source, index),
        text: chunkText,
        metadata: {
          source,
          chunk_index: index,
          start_line: chunkStartLine + 1,
          end_line: endLine + 1,
          type: "code",
        },
      });
      index++;
    }
    currentChunk = [];
    currentSize = 0;
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const isBoundary = boundaryPatterns.some(p => p.test(line.trim()));

    // Start new chunk at logical boundaries if current chunk is large enough
    if (isBoundary && currentSize > minChunkSize) {
      saveChunk(i - 1);
      chunkStartLine = i;
    }

    currentChunk.push(line);
    currentSize += line.length + 1;

    // Force split if chunk gets too large
    if (currentSize >= chunkSize) {
      saveChunk(i);
      chunkStartLine = i + 1;
    }
  }

  // Save remaining content
  if (currentChunk.length > 0) {
    saveChunk(lines.length - 1);
  }

  return chunks;
}

/**
 * Markdown-aware chunking
 * Respects header hierarchy and sections
 */
function markdownChunk(
  text: string,
  source: string,
  config: ChunkingConfig
): Chunk[] {
  const { chunkSize = 1200, minChunkSize = 100 } = config;
  const chunks: Chunk[] = [];
  const lines = text.split("\n");

  let currentChunk: string[] = [];
  let currentSize = 0;
  let currentHeader = "";
  let chunkStartLine = 0;
  let index = 0;

  function saveChunk(endLine: number) {
    const chunkText = currentChunk.join("\n").trim();
    if (chunkText.length >= minChunkSize) {
      chunks.push({
        id: generateChunkId(source, index),
        text: chunkText,
        metadata: {
          source,
          chunk_index: index,
          start_line: chunkStartLine + 1,
          end_line: endLine + 1,
          type: "markdown",
          header: currentHeader || undefined,
        },
      });
      index++;
    }
    currentChunk = [];
    currentSize = 0;
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const headerMatch = line.match(/^(#{1,3})\s+(.+)/);

    // New section at headers
    if (headerMatch && currentSize > minChunkSize) {
      saveChunk(i - 1);
      chunkStartLine = i;
      currentHeader = headerMatch[2];
    } else if (headerMatch) {
      currentHeader = headerMatch[2];
    }

    currentChunk.push(line);
    currentSize += line.length + 1;

    // Force split at paragraph boundaries if too large
    if (currentSize >= chunkSize && line.trim() === "") {
      saveChunk(i);
      chunkStartLine = i + 1;
    }
  }

  // Save remaining content
  if (currentChunk.length > 0) {
    saveChunk(lines.length - 1);
  }

  return chunks;
}

/**
 * Chunk a document using the specified strategy
 */
export function chunkDocument(
  text: string,
  source: string,
  config: ChunkingConfig = DEFAULT_CONFIG
): Chunk[] {
  switch (config.strategy) {
    case "code":
      return codeChunk(text, source, config);
    case "markdown":
      return markdownChunk(text, source, config);
    case "semantic":
    case "fixed":
    default:
      return fixedChunk(text, source, config);
  }
}

/**
 * Auto-detect chunking strategy based on file extension
 */
export function autoDetectStrategy(filename: string): ChunkingConfig["strategy"] {
  const ext = filename.toLowerCase().split(".").pop();

  const codeExtensions = [
    "ts", "tsx", "js", "jsx", "py", "rb", "go", "rs", "java",
    "c", "cpp", "h", "hpp", "cs", "swift", "kt", "scala"
  ];

  const markdownExtensions = ["md", "mdx", "markdown"];

  if (codeExtensions.includes(ext || "")) {
    return "code";
  } else if (markdownExtensions.includes(ext || "")) {
    return "markdown";
  }

  return "fixed";
}
