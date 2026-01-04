/**
 * Knowledge Pack Registry
 *
 * Manages registration and discovery of installed knowledge packs.
 */

interface KnowledgePack {
  id: string;
  name: string;
  version: string;
  installed: string;
  sources: Array<{
    path: string;
    type: 'file' | 'directory' | 'embedded';
  }>;
  skillPath?: string;
  metadata?: Record<string, unknown>;
}

interface RegistryConfig {
  configPath: string;
}

/**
 * Singleton registry for knowledge packs
 */
export class Registry {
  private static instance: Registry;
  private packs: Map<string, KnowledgePack> = new Map();
  private configPath: string;

  private constructor(config: RegistryConfig) {
    this.configPath = config.configPath;
  }

  /**
   * Get the singleton instance
   */
  static getInstance(config?: RegistryConfig): Registry {
    if (!Registry.instance) {
      Registry.instance = new Registry(config || {
        configPath: '.claude/config/knowledge-packs.yaml'
      });
    }
    return Registry.instance;
  }

  /**
   * Register a new knowledge pack
   */
  register(pack: KnowledgePack): void {
    this.packs.set(pack.id, pack);
    this.persist();
  }

  /**
   * Unregister a knowledge pack
   */
  unregister(packId: string): boolean {
    const result = this.packs.delete(packId);
    if (result) {
      this.persist();
    }
    return result;
  }

  /**
   * Get a specific pack by ID
   */
  getPack(packId: string): KnowledgePack | undefined {
    return this.packs.get(packId);
  }

  /**
   * Get all registered packs
   */
  getAllPacks(): KnowledgePack[] {
    return Array.from(this.packs.values());
  }

  /**
   * Get active (non-disabled) packs
   */
  getActivePacks(): KnowledgePack[] {
    return this.getAllPacks().filter(
      pack => pack.metadata?.disabled !== true
    );
  }

  /**
   * Check if a pack is installed
   */
  isInstalled(packId: string): boolean {
    return this.packs.has(packId);
  }

  /**
   * Load registry from config file
   */
  async load(): Promise<void> {
    // Implementation would read from YAML config
    // Placeholder for actual file system operations
  }

  /**
   * Persist registry to config file
   */
  private persist(): void {
    // Implementation would write to YAML config
    // Placeholder for actual file system operations
  }
}

export default Registry;
