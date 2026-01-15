/**
 * Embeddings Generation
 *
 * Generates text embeddings for semantic search capabilities.
 *
 * ⚠️  CONFIGURATION REQUIRED ⚠️
 *
 * This file contains a PLACEHOLDER implementation that returns random vectors.
 * You MUST replace generateEmbedding() with a real embedding provider:
 *
 * Option 1: OpenAI (recommended)
 * ```
 * import OpenAI from 'openai';
 * const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
 *
 * export async function generateEmbedding(text: string): Promise<number[]> {
 *   const response = await openai.embeddings.create({
 *     model: 'text-embedding-3-small',
 *     input: text,
 *   });
 *   return response.data[0].embedding;
 * }
 * ```
 *
 * Option 2: Ollama (local)
 * ```
 * export async function generateEmbedding(text: string): Promise<number[]> {
 *   const response = await fetch('http://localhost:11434/api/embeddings', {
 *     method: 'POST',
 *     body: JSON.stringify({ model: 'nomic-embed-text', prompt: text }),
 *   });
 *   return (await response.json()).embedding;
 * }
 * ```
 *
 * See _Core/README.md for more options.
 */

interface EmbeddingConfig {
  model: string;
  dimensions: number;
  batchSize: number;
}

const defaultConfig: EmbeddingConfig = {
  model: 'text-embedding-3-small',
  dimensions: 1536,
  batchSize: 100,
};

/**
 * Generate embedding for a single text
 *
 * ⚠️  PLACEHOLDER - Returns random vectors!
 * Replace this function with a real embedding provider.
 */
export async function generateEmbedding(
  text: string,
  config: Partial<EmbeddingConfig> = {}
): Promise<number[]> {
  const finalConfig = { ...defaultConfig, ...config };

  // ⚠️  PLACEHOLDER IMPLEMENTATION - REPLACE ME!
  // This returns random vectors which will NOT provide meaningful semantic search.
  // See the file header comments for implementation examples.
  console.warn(
    '⚠️  embeddings.ts: Using placeholder implementation. ' +
    'Configure a real embedding provider for semantic search to work.'
  );
  return new Array(finalConfig.dimensions).fill(0).map(() => Math.random());
}

/**
 * Generate embeddings for multiple texts
 */
export async function generateEmbeddings(
  texts: string[],
  config: Partial<EmbeddingConfig> = {}
): Promise<number[][]> {
  const finalConfig = { ...defaultConfig, ...config };
  const results: number[][] = [];

  // Process in batches
  for (let i = 0; i < texts.length; i += finalConfig.batchSize) {
    const batch = texts.slice(i, i + finalConfig.batchSize);
    const batchResults = await Promise.all(
      batch.map(text => generateEmbedding(text, config))
    );
    results.push(...batchResults);
  }

  return results;
}

/**
 * Calculate cosine similarity between two embeddings
 */
export function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) {
    throw new Error('Embeddings must have same dimensions');
  }

  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

export default {
  generateEmbedding,
  generateEmbeddings,
  cosineSimilarity,
};
