/**
 * Document Chunking
 *
 * Strategies for splitting documents into chunks for embedding.
 */

interface Chunk {
  content: string;
  index: number;
  metadata?: {
    startLine?: number;
    endLine?: number;
    source?: string;
  };
}

interface ChunkingOptions {
  maxChunkSize?: number;
  overlap?: number;
  preserveParagraphs?: boolean;
}

const defaultOptions: ChunkingOptions = {
  maxChunkSize: 1000,
  overlap: 100,
  preserveParagraphs: true,
};

/**
 * Split text into chunks by character count
 */
export function chunkBySize(
  text: string,
  options: ChunkingOptions = {}
): Chunk[] {
  const { maxChunkSize, overlap } = { ...defaultOptions, ...options };
  const chunks: Chunk[] = [];

  let start = 0;
  let index = 0;

  while (start < text.length) {
    const end = Math.min(start + maxChunkSize!, text.length);

    chunks.push({
      content: text.slice(start, end),
      index,
    });

    start = end - overlap!;
    index++;
  }

  return chunks;
}

/**
 * Split text into chunks by paragraph
 */
export function chunkByParagraph(
  text: string,
  options: ChunkingOptions = {}
): Chunk[] {
  const { maxChunkSize } = { ...defaultOptions, ...options };
  const paragraphs = text.split(/\n\n+/);
  const chunks: Chunk[] = [];

  let currentChunk = '';
  let index = 0;

  for (const paragraph of paragraphs) {
    if (currentChunk.length + paragraph.length > maxChunkSize!) {
      if (currentChunk) {
        chunks.push({
          content: currentChunk.trim(),
          index,
        });
        index++;
      }
      currentChunk = paragraph;
    } else {
      currentChunk += (currentChunk ? '\n\n' : '') + paragraph;
    }
  }

  if (currentChunk) {
    chunks.push({
      content: currentChunk.trim(),
      index,
    });
  }

  return chunks;
}

/**
 * Split code into chunks by function/class
 */
export function chunkByCodeBlock(
  code: string,
  options: ChunkingOptions = {}
): Chunk[] {
  const { maxChunkSize } = { ...defaultOptions, ...options };
  const chunks: Chunk[] = [];

  // Simple regex-based splitting for common patterns
  const patterns = [
    /^(export\s+)?(async\s+)?function\s+\w+/gm,
    /^(export\s+)?class\s+\w+/gm,
    /^(export\s+)?const\s+\w+\s*=/gm,
  ];

  const lines = code.split('\n');
  let currentChunk: string[] = [];
  let startLine = 0;
  let index = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const isBlockStart = patterns.some(p => p.test(line));

    if (isBlockStart && currentChunk.length > 0) {
      const content = currentChunk.join('\n');
      if (content.trim()) {
        chunks.push({
          content,
          index,
          metadata: { startLine, endLine: i - 1 },
        });
        index++;
      }
      currentChunk = [];
      startLine = i;
    }

    currentChunk.push(line);

    // Force split if chunk is too large
    if (currentChunk.join('\n').length > maxChunkSize!) {
      chunks.push({
        content: currentChunk.join('\n'),
        index,
        metadata: { startLine, endLine: i },
      });
      index++;
      currentChunk = [];
      startLine = i + 1;
    }
  }

  if (currentChunk.length > 0) {
    const content = currentChunk.join('\n');
    if (content.trim()) {
      chunks.push({
        content,
        index,
        metadata: { startLine, endLine: lines.length - 1 },
      });
    }
  }

  return chunks;
}

/**
 * Smart chunking that detects content type
 */
export function smartChunk(
  content: string,
  options: ChunkingOptions = {}
): Chunk[] {
  // Detect if content looks like code
  const codeIndicators = [
    /^import\s+/m,
    /^export\s+/m,
    /function\s+\w+\s*\(/,
    /class\s+\w+/,
    /const\s+\w+\s*=/,
  ];

  const isCode = codeIndicators.some(p => p.test(content));

  if (isCode) {
    return chunkByCodeBlock(content, options);
  }

  if (options.preserveParagraphs) {
    return chunkByParagraph(content, options);
  }

  return chunkBySize(content, options);
}

export default {
  chunkBySize,
  chunkByParagraph,
  chunkByCodeBlock,
  smartChunk,
};
