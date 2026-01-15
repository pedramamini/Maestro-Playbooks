/**
 * Vector Store
 *
 * In-memory vector storage for semantic search.
 */

import { cosineSimilarity } from './embeddings';

interface VectorEntry {
  id: string;
  content: string;
  embedding: number[];
  metadata?: Record<string, unknown>;
}

interface SearchResult {
  id: string;
  content: string;
  score: number;
  metadata?: Record<string, unknown>;
}

interface SearchOptions {
  limit?: number;
  minScore?: number;
  filter?: (entry: VectorEntry) => boolean;
}

/**
 * Vector store for a single knowledge pack
 */
export class VectorStore {
  private static stores: Map<string, VectorStore> = new Map();

  private packId: string;
  private entries: Map<string, VectorEntry> = new Map();

  private constructor(packId: string) {
    this.packId = packId;
  }

  /**
   * Get or create a vector store for a pack
   */
  static forPack(packId: string): VectorStore {
    if (!VectorStore.stores.has(packId)) {
      VectorStore.stores.set(packId, new VectorStore(packId));
    }
    return VectorStore.stores.get(packId)!;
  }

  /**
   * Add an entry to the store
   */
  add(entry: VectorEntry): void {
    this.entries.set(entry.id, entry);
  }

  /**
   * Add multiple entries
   */
  addAll(entries: VectorEntry[]): void {
    for (const entry of entries) {
      this.add(entry);
    }
  }

  /**
   * Remove an entry
   */
  remove(id: string): boolean {
    return this.entries.delete(id);
  }

  /**
   * Search for similar entries
   */
  async search(
    queryEmbedding: number[],
    options: SearchOptions = {}
  ): Promise<SearchResult[]> {
    const {
      limit = 10,
      minScore = 0.0,
      filter,
    } = options;

    const results: SearchResult[] = [];

    for (const entry of this.entries.values()) {
      // Apply filter if provided
      if (filter && !filter(entry)) {
        continue;
      }

      const score = cosineSimilarity(queryEmbedding, entry.embedding);

      if (score >= minScore) {
        results.push({
          id: entry.id,
          content: entry.content,
          score,
          metadata: entry.metadata,
        });
      }
    }

    // Sort by score descending and limit
    return results
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  }

  /**
   * Get store size
   */
  size(): number {
    return this.entries.size;
  }

  /**
   * Clear all entries
   */
  clear(): void {
    this.entries.clear();
  }

  /**
   * Persist store to disk
   */
  async persist(path: string): Promise<void> {
    // Implementation would serialize and write to disk
  }

  /**
   * Load store from disk
   */
  async load(path: string): Promise<void> {
    // Implementation would read and deserialize from disk
  }
}

export default VectorStore;
