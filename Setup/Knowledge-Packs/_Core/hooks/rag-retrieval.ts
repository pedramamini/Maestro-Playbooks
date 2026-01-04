#!/usr/bin/env npx ts-node
/**
 * RAG Retrieval Hook
 *
 * PreToolUse hook that queries installed knowledge packs and injects
 * relevant context into the agent's working memory.
 *
 * Triggers on: Read, Grep, Glob, WebSearch (query-related tools)
 */

import * as fs from "fs";
import * as path from "path";
import * as yaml from "js-yaml";

// Types
interface KnowledgePack {
  id: string;
  name: string;
  embeddings_path: string;
}

interface VectorDocument {
  id: string;
  text: string;
  embedding: number[];
  metadata: {
    source: string;
    pack_id: string;
    [key: string]: unknown;
  };
}

interface HookInput {
  tool_name: string;
  tool_input: Record<string, unknown>;
}

// Cosine similarity
function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;

  let dot = 0, magA = 0, magB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    magA += a[i] * a[i];
    magB += b[i] * b[i];
  }

  const mag = Math.sqrt(magA) * Math.sqrt(magB);
  return mag === 0 ? 0 : dot / mag;
}

// Simple local embedding (matches embeddings.ts)
function localEmbed(text: string, dimensions: number = 384): number[] {
  const tokens = text
    .toLowerCase()
    .replace(/[^\w\s]/g, " ")
    .split(/\s+/)
    .filter(t => t.length > 0);

  const embedding = new Array(dimensions).fill(0);

  for (const token of tokens) {
    let hash = 0;
    for (let i = 0; i < token.length; i++) {
      hash = (hash * 31 + token.charCodeAt(i)) >>> 0;
    }

    for (let i = 0; i < 3; i++) {
      const pos = (hash + i * 127) % dimensions;
      embedding[pos] += 1 / (1 + i);
    }
  }

  const magnitude = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0));
  if (magnitude > 0) {
    for (let i = 0; i < dimensions; i++) {
      embedding[i] /= magnitude;
    }
  }

  return embedding;
}

// Extract query from tool input
function extractQuery(toolName: string, toolInput: Record<string, unknown>): string | null {
  switch (toolName) {
    case "Read":
      return toolInput.file_path as string || null;
    case "Grep":
      return toolInput.pattern as string || null;
    case "Glob":
      return toolInput.pattern as string || null;
    case "WebSearch":
      return toolInput.query as string || null;
    case "Task":
      return toolInput.prompt as string || null;
    default:
      return null;
  }
}

// Load knowledge packs registry
function loadRegistry(agentDir: string): KnowledgePack[] {
  const registryPath = path.join(agentDir, ".claude", "config", "knowledge-packs.yaml");

  if (!fs.existsSync(registryPath)) {
    return [];
  }

  try {
    const content = fs.readFileSync(registryPath, "utf-8");
    const registry = yaml.load(content) as { installed_packs?: KnowledgePack[] };
    return registry?.installed_packs || [];
  } catch {
    return [];
  }
}

// Load vector store
function loadVectorStore(agentDir: string): VectorDocument[] {
  const storePath = path.join(agentDir, ".claude", "knowledge", "vectors.json");

  if (!fs.existsSync(storePath)) {
    return [];
  }

  try {
    const content = fs.readFileSync(storePath, "utf-8");
    return JSON.parse(content);
  } catch {
    return [];
  }
}

// Search for relevant documents
function searchDocuments(
  query: string,
  documents: VectorDocument[],
  topK: number = 3,
  minScore: number = 0.3
): Array<{ doc: VectorDocument; score: number }> {
  if (documents.length === 0) return [];

  const queryEmbedding = localEmbed(query);

  const results = documents
    .map(doc => ({
      doc,
      score: cosineSimilarity(queryEmbedding, doc.embedding),
    }))
    .filter(r => r.score >= minScore)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);

  return results;
}

// Write context to working memory
function injectContext(agentDir: string, results: Array<{ doc: VectorDocument; score: number }>, packs: KnowledgePack[]): void {
  if (results.length === 0) return;

  const packMap = new Map(packs.map(p => [p.id, p.name]));
  const workingDir = path.join(agentDir, ".claude", "context", "working");

  if (!fs.existsSync(workingDir)) {
    fs.mkdirSync(workingDir, { recursive: true });
  }

  const contextPath = path.join(workingDir, "rag-context.md");

  let content = `# Retrieved Knowledge Context\n\n`;
  content += `*Auto-injected by RAG retrieval hook*\n\n`;

  for (const { doc, score } of results) {
    const packName = packMap.get(doc.metadata.pack_id) || doc.metadata.pack_id;
    content += `## From: ${packName}\n`;
    content += `**Source:** ${doc.metadata.source}\n`;
    content += `**Relevance:** ${(score * 100).toFixed(1)}%\n\n`;
    content += `${doc.text}\n\n`;
    content += `---\n\n`;
  }

  fs.writeFileSync(contextPath, content, "utf-8");
}

// Main hook logic
async function main() {
  try {
    // Read hook input from stdin
    const input = fs.readFileSync(0, "utf-8");
    const hookInput: HookInput = JSON.parse(input);

    // Get agent directory (parent of .claude)
    const agentDir = process.cwd();

    // Only process query-related tools
    const queryTools = ["Read", "Grep", "Glob", "WebSearch", "Task"];
    if (!queryTools.includes(hookInput.tool_name)) {
      process.exit(0);
    }

    // Extract query from tool input
    const query = extractQuery(hookInput.tool_name, hookInput.tool_input);
    if (!query || query.length < 3) {
      process.exit(0);
    }

    // Load registry and check for installed packs
    const packs = loadRegistry(agentDir);
    if (packs.length === 0) {
      process.exit(0);
    }

    // Load vector store
    const documents = loadVectorStore(agentDir);
    if (documents.length === 0) {
      process.exit(0);
    }

    // Search for relevant documents
    const results = searchDocuments(query, documents, 3, 0.3);

    // Inject context if found
    if (results.length > 0) {
      injectContext(agentDir, results, packs);
    }

    process.exit(0);
  } catch (error) {
    // Fail silently - never crash Claude Code
    console.error(`RAG hook error: ${error}`);
    process.exit(0);
  }
}

main();
