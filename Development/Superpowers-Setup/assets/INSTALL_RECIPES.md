# Superpowers Install Recipes by Provider

Reference table of install steps for [obra/superpowers](https://github.com/obra/superpowers), keyed by Maestro `toolType`. Documents 2 and 3 read this file to plan and execute the install for the detected provider.

Each recipe declares whether steps are **agent-automatable** (the playbook agent can run them itself) or **user-required** (the playbook must hand the user a clear instruction because the harness only accepts the command from interactive input).

---

## `claude-code` (Claude Code)

**Automatable**: No. Claude Code plugin commands are interactive slash commands the agent cannot self-trigger inside its own session.

**User-required steps** (paste in the Claude Code prompt, in order):

```text
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

Alternative single-step path using Anthropic's official marketplace (already registered in fresh installs):

```text
/plugin install superpowers@claude-plugins-official
```

**Verify**:

```text
/plugin
```

Look for `superpowers` listed as enabled. Then ask the agent: `Tell me about your superpowers`.

---

## `codex` (Codex CLI / Codex App)

**Automatable**: No. Codex's plugin manager is interactive.

**User-required steps**:

- Codex CLI: type `/plugins`, search `superpowers`, select **Install Plugin**.
- Codex App (desktop): sidebar → **Plugins** → Coding section → click `+` next to **Superpowers** → confirm.

**Verify**: re-run `/plugins` and confirm `superpowers` is enabled, then ask `Tell me about your superpowers`.

---

## `opencode` (OpenCode)

**Automatable**: Yes. OpenCode reads plugins from `opencode.json`.

**Steps** (the playbook agent runs these directly):

1. Locate the OpenCode config. Prefer `~/.config/opencode/opencode.json` for a global install, or `<project>/opencode.json` for project-scoped. If neither exists, create `~/.config/opencode/opencode.json` with `{}`.
2. Add (or merge) the plugin entry. Final shape:

   ```json
   {
     "plugin": [
       "superpowers@git+https://github.com/obra/superpowers.git"
     ]
   }
   ```

   - If `plugin` is missing, add it.
   - If `plugin` exists but does not include a `superpowers@...` entry, append the entry.
   - If a `superpowers@...` entry already exists, leave it unless the user asked for a specific version pin.
3. Optionally pin to a tag/branch by suffixing `#v5.0.3` (or any ref) on the URL.
4. Optional cleanup of any prior symlink-style install (only if these paths exist):

   ```bash
   rm -f  ~/.config/opencode/plugins/superpowers.js
   rm -rf ~/.config/opencode/skills/superpowers
   rm -rf ~/.config/opencode/superpowers
   ```

   Also remove any stale `superpowers` entry under `skills.paths` in `opencode.json`.
5. Restart OpenCode for the change to take effect (user-required — the running OpenCode session will not pick up the change mid-flight).

**Windows fallback** (only if the standard `git+https` plugin URL fails to resolve):

```powershell
npm install superpowers@git+https://github.com/obra/superpowers.git --prefix "$HOME\.config\opencode"
```

Then in `opencode.json`:

```json
{ "plugin": ["~/.config/opencode/node_modules/superpowers"] }
```

**Verify** (after the user restarts OpenCode):

```bash
opencode run --print-logs "hello" 2>&1 | grep -i superpowers
```

Or in an OpenCode session: `use skill tool to list skills`, or `Tell me about your superpowers`.

---

## `factory-droid` (Factory Droid)

**Automatable**: Yes. Droid exposes shell-callable plugin commands.

**Steps** (run by the playbook agent):

```bash
droid plugin marketplace add https://github.com/obra/superpowers
droid plugin install superpowers@superpowers
```

**Verify**:

```bash
droid plugin list
```

Confirm `superpowers` is present. In a Droid session: `Tell me about your superpowers`.

---

## `copilot-cli` (GitHub Copilot CLI)

**Automatable**: Yes.

**Steps**:

```bash
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

**Verify**:

```bash
copilot plugin list
```

In a Copilot CLI session: `Tell me about your superpowers`.

---

## `gemini-cli` (Gemini CLI)

**Automatable**: Yes. Superpowers ships a `gemini-extension.json` and is a first-class Gemini extension.

**Steps**:

```bash
gemini extensions install https://github.com/obra/superpowers
```

To update later:

```bash
gemini extensions update superpowers
```

**Verify**:

```bash
gemini extensions list
```

Look for `superpowers`. In a Gemini CLI session: `Tell me about your superpowers`.

---

## `qwen3-coder` (Qwen3 Coder)

**Automatable**: No.

**Status**: Superpowers does not document an official install path for Qwen3 Coder as of the date this playbook was authored. Treat as **unsupported** — the playbook should record this in `INSTALL_PLAN.md`, skip the install step, and surface a clear note to the user.

If a community install path exists, link it from `SUPERPOWERS_SETUP.md` so a human can decide whether to follow it.

---

## Universal Notes

- **Prerequisites** that may be needed: `git` (always), `node`/`npm` (only the OpenCode Windows fallback), and the harness's own CLI on `PATH`.
- **Install scope**: Superpowers is per-harness, not per-project. Reinstall for each harness the user runs.
- **Smoke test prompt** that works across every supported harness once installed: `Tell me about your superpowers`. The agent should respond with a description of the bundled skills (brainstorming, writing-plans, using-git-worktrees, test-driven-development, etc.).
- **Source of truth**: <https://github.com/obra/superpowers> README. If a recipe here drifts from upstream, upstream wins — re-check the README before relying on these steps.
