/**
 * Embeddings Utilities
 *
 * Generate embeddings for text content using various providers.
 * Supports local and cloud-based embedding models.
 */

export interface EmbeddingConfig {
  provider: "local" | "openai" | "anthropic" | "cohere";
  model?: string;
  apiKey?: string;
  dimensions?: number;
}

export interface EmbeddingResult {
  text: string;
  embedding: number[];
  metadata?: Record<string, unknown>;
}

const DEFAULT_CONFIG: EmbeddingConfig = {
  provider: "local",
  dimensions: 384, // Default for local models
};

/**
 * Simple local embedding using term frequency
 * This is a fallback when no external API is available
 */
function localEmbed(text: string, dimensions: number = 384): number[] {
  // Normalize and tokenize
  const tokens = text
    .toLowerCase()
    .replace(/[^\w\s]/g, " ")
    .split(/\s+/)
    .filter(t => t.length > 0);

  // Create a simple hash-based embedding
  const embedding = new Array(dimensions).fill(0);

  for (const token of tokens) {
    // Hash the token to get consistent positions
    let hash = 0;
    for (let i = 0; i < token.length; i++) {
      hash = (hash * 31 + token.charCodeAt(i)) >>> 0;
    }

    // Distribute the token across multiple dimensions
    for (let i = 0; i < 3; i++) {
      const pos = (hash + i * 127) % dimensions;
      embedding[pos] += 1 / (1 + i);
    }
  }

  // Normalize to unit vector
  const magnitude = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0));
  if (magnitude > 0) {
    for (let i = 0; i < dimensions; i++) {
      embedding[i] /= magnitude;
    }
  }

  return embedding;
}

/**
 * Generate embeddings using OpenAI API
 */
async function openaiEmbed(
  texts: string[],
  apiKey: string,
  model: string = "text-embedding-3-small"
): Promise<number[][]> {
  const response = await fetch("https://api.openai.com/v1/embeddings", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      input: texts,
      model: model,
    }),
  });

  if (!response.ok) {
    throw new Error(`OpenAI API error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.data.map((item: { embedding: number[] }) => item.embedding);
}

/**
 * Generate embedding for a single text
 */
export async function embed(
  text: string,
  config: EmbeddingConfig = DEFAULT_CONFIG
): Promise<EmbeddingResult> {
  let embedding: number[];

  switch (config.provider) {
    case "openai":
      if (!config.apiKey) {
        throw new Error("OpenAI API key required");
      }
      const results = await openaiEmbed([text], config.apiKey, config.model);
      embedding = results[0];
      break;

    case "local":
    default:
      embedding = localEmbed(text, config.dimensions);
      break;
  }

  return {
    text,
    embedding,
  };
}

/**
 * Generate embeddings for multiple texts (batch)
 */
export async function embedBatch(
  texts: string[],
  config: EmbeddingConfig = DEFAULT_CONFIG
): Promise<EmbeddingResult[]> {
  switch (config.provider) {
    case "openai":
      if (!config.apiKey) {
        throw new Error("OpenAI API key required");
      }
      const embeddings = await openaiEmbed(texts, config.apiKey, config.model);
      return texts.map((text, i) => ({
        text,
        embedding: embeddings[i],
      }));

    case "local":
    default:
      return texts.map(text => ({
        text,
        embedding: localEmbed(text, config.dimensions),
      }));
  }
}

/**
 * Calculate cosine similarity between two embeddings
 */
export function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) {
    throw new Error("Embeddings must have same dimensions");
  }

  let dotProduct = 0;
  let magnitudeA = 0;
  let magnitudeB = 0;

  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    magnitudeA += a[i] * a[i];
    magnitudeB += b[i] * b[i];
  }

  magnitudeA = Math.sqrt(magnitudeA);
  magnitudeB = Math.sqrt(magnitudeB);

  if (magnitudeA === 0 || magnitudeB === 0) {
    return 0;
  }

  return dotProduct / (magnitudeA * magnitudeB);
}
