/**
 * RAG Retrieval Hook
 *
 * Pre-tool hook that retrieves relevant context from knowledge packs
 * and injects it into the conversation before tool execution.
 */

import { VectorStore } from '../lib/vector-store';
import { Registry } from '../lib/registry';
import { generateEmbedding } from '../lib/embeddings';

interface HookContext {
  toolName: string;
  toolInput: Record<string, unknown>;
  conversationHistory: Array<{ role: string; content: string }>;
}

interface RetrievalResult {
  content: string;
  source: string;
  score: number;
}

/**
 * Configuration for the RAG retrieval hook
 */
const config = {
  maxResults: 5,
  minScore: 0.7,
  contextBudget: 4000,
};

/**
 * Extract the current query/intent from conversation
 */
function extractQuery(context: HookContext): string {
  const lastUserMessage = context.conversationHistory
    .filter(m => m.role === 'user')
    .pop();

  return lastUserMessage?.content || '';
}

/**
 * Retrieve relevant context from registered knowledge packs
 */
async function retrieveContext(query: string): Promise<RetrievalResult[]> {
  const registry = Registry.getInstance();
  const activePacks = registry.getActivePacks();

  if (activePacks.length === 0) {
    return [];
  }

  const queryEmbedding = await generateEmbedding(query);
  const results: RetrievalResult[] = [];

  for (const pack of activePacks) {
    const vectorStore = VectorStore.forPack(pack.id);
    const packResults = await vectorStore.search(queryEmbedding, {
      limit: config.maxResults,
      minScore: config.minScore,
    });

    results.push(...packResults.map(r => ({
      content: r.content,
      source: `${pack.name}: ${r.metadata?.source || 'unknown'}`,
      score: r.score,
    })));
  }

  // Sort by score and limit to budget
  return results
    .sort((a, b) => b.score - a.score)
    .slice(0, config.maxResults);
}

/**
 * Format retrieved context for injection
 */
function formatContext(results: RetrievalResult[]): string {
  if (results.length === 0) {
    return '';
  }

  const contextParts = results.map(r =>
    `[Source: ${r.source}]\n${r.content}`
  );

  return `
<retrieved-context>
The following context was retrieved from knowledge packs and may be relevant:

${contextParts.join('\n\n---\n\n')}
</retrieved-context>
`;
}

/**
 * Main hook function - called before tool execution
 */
export async function preToolCall(context: HookContext): Promise<string | null> {
  // Only inject context for certain tools
  const contextualTools = ['Read', 'Write', 'Edit', 'Bash'];

  if (!contextualTools.includes(context.toolName)) {
    return null;
  }

  try {
    const query = extractQuery(context);
    if (!query) {
      return null;
    }

    const results = await retrieveContext(query);
    if (results.length === 0) {
      return null;
    }

    return formatContext(results);
  } catch (error) {
    console.error('RAG retrieval error:', error);
    return null;
  }
}

export default { preToolCall };
