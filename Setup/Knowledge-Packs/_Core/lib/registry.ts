/**
 * Knowledge Packs Registry
 *
 * Manages the registry of installed knowledge packs for an agent.
 * Registry stored at .claude/config/knowledge-packs.yaml
 */

import * as fs from "fs";
import * as path from "path";
import * as yaml from "js-yaml";

export interface KnowledgeSource {
  path: string;
  type: "codebase" | "documents" | "web" | "api";
  include?: string[];
  exclude?: string[];
}

export interface KnowledgePack {
  id: string;
  name: string;
  installed: string;
  version: string;
  sources: KnowledgeSource[];
  embeddings_path: string;
  skill_path?: string;
  metadata?: Record<string, unknown>;
}

export interface KnowledgePacksRegistry {
  version: string;
  installed_packs: KnowledgePack[];
}

const DEFAULT_REGISTRY: KnowledgePacksRegistry = {
  version: "1.0.0",
  installed_packs: [],
};

/**
 * Get the registry file path for an agent
 */
export function getRegistryPath(agentDir: string): string {
  return path.join(agentDir, ".claude", "config", "knowledge-packs.yaml");
}

/**
 * Load the knowledge packs registry
 */
export function loadRegistry(agentDir: string): KnowledgePacksRegistry {
  const registryPath = getRegistryPath(agentDir);

  if (!fs.existsSync(registryPath)) {
    return { ...DEFAULT_REGISTRY };
  }

  try {
    const content = fs.readFileSync(registryPath, "utf-8");
    const registry = yaml.load(content) as KnowledgePacksRegistry;
    return registry || { ...DEFAULT_REGISTRY };
  } catch (error) {
    console.error(`Error loading registry: ${error}`);
    return { ...DEFAULT_REGISTRY };
  }
}

/**
 * Save the knowledge packs registry
 */
export function saveRegistry(agentDir: string, registry: KnowledgePacksRegistry): void {
  const registryPath = getRegistryPath(agentDir);
  const configDir = path.dirname(registryPath);

  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }

  const content = yaml.dump(registry, {
    indent: 2,
    lineWidth: 120,
    noRefs: true,
  });

  fs.writeFileSync(registryPath, content, "utf-8");
}

/**
 * Register a new knowledge pack
 */
export function registerPack(agentDir: string, pack: KnowledgePack): void {
  const registry = loadRegistry(agentDir);

  // Remove existing pack with same ID if present
  registry.installed_packs = registry.installed_packs.filter(p => p.id !== pack.id);

  // Add new pack
  registry.installed_packs.push(pack);

  saveRegistry(agentDir, registry);
}

/**
 * Unregister a knowledge pack
 */
export function unregisterPack(agentDir: string, packId: string): boolean {
  const registry = loadRegistry(agentDir);
  const initialLength = registry.installed_packs.length;

  registry.installed_packs = registry.installed_packs.filter(p => p.id !== packId);

  if (registry.installed_packs.length < initialLength) {
    saveRegistry(agentDir, registry);
    return true;
  }

  return false;
}

/**
 * Get a specific knowledge pack by ID
 */
export function getPack(agentDir: string, packId: string): KnowledgePack | undefined {
  const registry = loadRegistry(agentDir);
  return registry.installed_packs.find(p => p.id === packId);
}

/**
 * Check if a knowledge pack is installed
 */
export function isPackInstalled(agentDir: string, packId: string): boolean {
  return getPack(agentDir, packId) !== undefined;
}

/**
 * Get all installed packs
 */
export function getAllPacks(agentDir: string): KnowledgePack[] {
  const registry = loadRegistry(agentDir);
  return registry.installed_packs;
}
