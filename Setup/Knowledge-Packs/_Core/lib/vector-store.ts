/**
 * Vector Store Abstraction
 *
 * Provides a unified interface for storing and querying embeddings.
 * Supports local JSON storage (default) and external vector databases.
 */

import * as fs from "fs";
import * as path from "path";
import { cosineSimilarity } from "./embeddings";

export interface VectorDocument {
  id: string;
  text: string;
  embedding: number[];
  metadata: {
    source: string;
    chunk_index?: number;
    pack_id: string;
    [key: string]: unknown;
  };
}

export interface SearchResult {
  document: VectorDocument;
  score: number;
}

export interface VectorStoreConfig {
  type: "local" | "chroma" | "pinecone";
  path?: string; // For local storage
  apiKey?: string; // For cloud providers
  indexName?: string;
}

/**
 * Local JSON-based vector store
 * Simple but effective for small to medium knowledge bases
 */
export class LocalVectorStore {
  private storePath: string;
  private documents: VectorDocument[] = [];

  constructor(storePath: string) {
    this.storePath = storePath;
    this.load();
  }

  /**
   * Load documents from disk
   */
  private load(): void {
    if (fs.existsSync(this.storePath)) {
      try {
        const content = fs.readFileSync(this.storePath, "utf-8");
        this.documents = JSON.parse(content);
      } catch (error) {
        console.error(`Error loading vector store: ${error}`);
        this.documents = [];
      }
    }
  }

  /**
   * Save documents to disk
   */
  private save(): void {
    const dir = path.dirname(this.storePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(this.storePath, JSON.stringify(this.documents, null, 2), "utf-8");
  }

  /**
   * Add documents to the store
   */
  add(documents: VectorDocument[]): void {
    // Remove duplicates by ID
    const existingIds = new Set(this.documents.map(d => d.id));
    const newDocs = documents.filter(d => !existingIds.has(d.id));

    this.documents.push(...newDocs);
    this.save();
  }

  /**
   * Update or insert documents
   */
  upsert(documents: VectorDocument[]): void {
    for (const doc of documents) {
      const index = this.documents.findIndex(d => d.id === doc.id);
      if (index >= 0) {
        this.documents[index] = doc;
      } else {
        this.documents.push(doc);
      }
    }
    this.save();
  }

  /**
   * Delete documents by ID
   */
  delete(ids: string[]): void {
    const idSet = new Set(ids);
    this.documents = this.documents.filter(d => !idSet.has(d.id));
    this.save();
  }

  /**
   * Delete all documents for a specific pack
   */
  deleteByPack(packId: string): void {
    this.documents = this.documents.filter(d => d.metadata.pack_id !== packId);
    this.save();
  }

  /**
   * Search for similar documents
   */
  search(queryEmbedding: number[], options: {
    topK?: number;
    packIds?: string[];
    minScore?: number;
  } = {}): SearchResult[] {
    const { topK = 5, packIds, minScore = 0.0 } = options;

    let candidates = this.documents;

    // Filter by pack IDs if specified
    if (packIds && packIds.length > 0) {
      const packIdSet = new Set(packIds);
      candidates = candidates.filter(d => packIdSet.has(d.metadata.pack_id));
    }

    // Calculate similarities
    const results: SearchResult[] = candidates.map(doc => ({
      document: doc,
      score: cosineSimilarity(queryEmbedding, doc.embedding),
    }));

    // Filter by minimum score and sort by similarity
    return results
      .filter(r => r.score >= minScore)
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);
  }

  /**
   * Get all documents
   */
  getAll(): VectorDocument[] {
    return [...this.documents];
  }

  /**
   * Get documents by pack ID
   */
  getByPack(packId: string): VectorDocument[] {
    return this.documents.filter(d => d.metadata.pack_id === packId);
  }

  /**
   * Get document count
   */
  count(): number {
    return this.documents.length;
  }

  /**
   * Get document count by pack
   */
  countByPack(packId: string): number {
    return this.documents.filter(d => d.metadata.pack_id === packId).length;
  }
}

/**
 * Create a vector store instance
 */
export function createVectorStore(config: VectorStoreConfig): LocalVectorStore {
  switch (config.type) {
    case "local":
    default:
      if (!config.path) {
        throw new Error("Path required for local vector store");
      }
      return new LocalVectorStore(config.path);
  }
}

/**
 * Get the default vector store path for an agent
 */
export function getDefaultStorePath(agentDir: string): string {
  return path.join(agentDir, ".claude", "knowledge", "vectors.json");
}
