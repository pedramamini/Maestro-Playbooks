# PAI Install Notes

Pinned reference for the PAI bootstrap, the bundled wizard, and the post-install surface. Documents 2-4 read this file. Edit it as upstream PAI evolves.

**Source of truth**: <https://github.com/danielmiessler/Personal_AI_Infrastructure>. If anything here drifts from the upstream README, upstream wins — re-check the README before relying on these steps.

---

## 0. Supported AI Agent Systems (per upstream)

The PAI homepage at <https://ourpai.ai> lists these AI agent systems on top of which PAI runs:

- **Claude Code** — native; the v5.0.0 bootstrap installs to `~/.claude/`, which Claude Code reads natively.
- **OpenCode** — listed by upstream. The bootstrap still writes to `~/.claude/`; harness-specific wiring (if any) is documented in the PAI repo. Check upstream before assuming the install is complete for OpenCode-driven workflows.
- **Pi** — listed by upstream as an AI agent system. Pi is not a Maestro `toolType` (it is a separate consumer product); installing PAI on the host machine is the relevant action and Pi connects per the upstream docs.
- **Codex** — Daniel has stated Codex support is coming. No install path is available yet.

Anything outside this list (Factory Droid, Copilot CLI, Gemini CLI, Qwen3 Coder, etc.) does not have a documented PAI install path; the playbook will skip cleanly and point at the upstream repo.

---

## 1. Bootstrap (the one-liner)

```bash
curl -sSL https://ourpai.ai/install.sh | bash
```

This is a public, HTTPS-only script. It performs five steps:

1. **Verifies prerequisites**: `curl`, `bash`, `rsync`, `tar`. Offers to install `bun` if missing — but **only when stdin is a TTY and `CI` is unset**. Inside a Maestro Bash subprocess this check fails and the script exits, so install `bun` first.
2. **Backs up `~/.claude/`** to `~/.claude.backup-{TIMESTAMP}` if it exists.
3. **Downloads the v5.0.0 release tarball** from `https://github.com/danielmiessler/Personal_AI_Infrastructure/archive/refs/tags/v5.0.0.tar.gz`.
4. **Places it at `~/.claude/`** via `rsync -a`.
5. **Hands off to `~/.claude/install.sh`** (the bundled wizard) via `exec`.

### Bootstrap environment variables

- `PAI_VERSION=5.0.0` — pin a specific version (default: `5.0.0`).
- `DRY_RUN=1` — print every command instead of running it. Useful for smoke-testing.
- `PAI_AUTO_INSTALL_BUN=0` — disable the auto-install of `bun` (bootstrap will exit with a clear message if `bun` is missing).
- `PAI_TEST_AUTOMATED=1` — propagated to the bundled wizard. Forces CLI mode and (critically) every interactive prompt returns its sensible default. **This is the key flag that makes the install runnable end-to-end from a Maestro Bash subprocess.**

### Automation path (the playbook's default for Claude Code)

The bootstrap + bundled wizard form a complete unattended install when:

1. `bun` is already on `PATH` (so the bootstrap's TTY-gated auto-install of bun is skipped).
2. `PAI_TEST_AUTOMATED=1` is set (so the wizard runs in CLI mode and uses defaults).
3. `~/Library/LaunchAgents/` is writable by the user (default on macOS).

Concretely, the agent runs:

```bash
# Pre-step: install bun if missing (the bootstrap's auto-install needs a TTY we don't have)
command -v bun >/dev/null 2>&1 || curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"

# Main install: bootstrap streams to bash with PAI_TEST_AUTOMATED=1
PAI_TEST_AUTOMATED=1 bash -c 'curl -sSL https://ourpai.ai/install.sh | bash'
```

The wizard completes through all 9 steps (system-detect, prerequisites, api-keys, identity, repository, configuration, voice, telegram, validation) and produces a working install with placeholder identity (`principalName="User"`, `aiName="PAI"`). The user runs `/interview` later in a fresh Claude Code session to customize the DA identity, voice, and TELOS.

After the wizard succeeds, the bundled `install.sh` ends with:

```bash
if [ -r /dev/tty ]; then
  exec zsh -i -c 'source ~/.zshrc && pai' < /dev/tty
else
  info "Install complete. To start pai, run:  source ~/.zshrc && pai"
fi
```

In a Maestro Bash subprocess `/dev/tty` is not readable, so it gracefully prints the launch instruction and exits zero — no hang.

### Risks the automation accepts

- **Replacing `~/.claude/` mid-session**: the running Claude Code agent reads its config from `~/.claude/`. Between the `mv` (old → backup) and the `rsync` (new tree in place) there is a brief window — a few seconds — when hooks/skills cannot be found. This rarely matters in practice because Claude Code reads these lazily, but it is a real risk window. Document it in the user-facing summary.
- **Generic identity**: automated runs use `principalName="User"`, `aiName="PAI"`. The user must run `/interview` afterwards to make it theirs. This is non-blocking but worth surfacing.

### Why not `git clone`?

Bootstrap notes call this out: HTTPS-only works for anonymous users, is immune to local `git config url.<x>.insteadOf` rewrites, has no SSH-agent dependency, and removes `git` from the prereq list (the wizard still uses `git` if present, but the bootstrap does not).

---

## 2. Manual install fallback

```bash
git clone https://github.com/danielmiessler/Personal_AI_Infrastructure.git
cd Personal_AI_Infrastructure/Releases/v5.0.0
cp -R .claude ~/
cd ~/.claude && ./install.sh
```

Equivalent to the bootstrap but uses `git`. Backups are not automatic with this path — back up `~/.claude/` manually first if needed.

---

## 3. The bundled wizard (`~/.claude/install.sh`)

After the bootstrap places files, the wizard:

1. Re-checks prereqs (`curl`, `git` — auto-installs via `xcode-select` / `brew` / `apt-get` / `yum`; `bun` — auto-installs from <https://bun.sh/install>; symlinks bun into `/usr/local/bin` or `/opt/homebrew/bin` so non-interactive shells can find it).
2. Adds `bun` to `PATH` in `~/.zshenv`, `~/.zprofile`, `~/.zshrc`, `~/.bash_profile`. **This is intentional and survives reboots.**
3. Detects environment and picks GUI vs CLI mode:
   - Headless Linux/BSD with no `$DISPLAY` / `$WAYLAND_DISPLAY` → CLI.
   - SSH session (`$SSH_CONNECTION` / `$SSH_TTY` set) → CLI.
   - `PAI_TEST_AUTOMATED=1` → CLI.
   - Otherwise → GUI.
4. Runs `bun run PAI/PAI-Install/main.ts --mode <gui|cli>`. Both modes are interactive; neither runs unattended.
5. After the wizard exits successfully, `exec`s into `zsh -i -c 'source ~/.zshrc && pai'` if a controlling TTY is available.

### What the wizard asks for

- DA name, voice, personality.
- ElevenLabs API key (skippable — voice falls back to desktop notifications).
- Confirmation to register `com.pai.pulse` as a launchd service.

### Forcing CLI mode

Set `PAI_TEST_AUTOMATED=1` before the bootstrap. CLI mode is still interactive; this only avoids the GUI launch.

---

## 4. Post-install verification surface

| Probe | Command | Expected result |
|---|---|---|
| PAI directory | `[ -d "$HOME/.claude/PAI" ]` | exists |
| Bundled installer | `[ -f "$HOME/.claude/install.sh" ]` | exists |
| User config | `[ -d "$HOME/.claude/PAI/USER" ]` | exists |
| Algorithm version | `cat "$HOME/.claude/PAI/ALGORITHM/LATEST"` | `6.3.0` (or newer) |
| DA identity | `[ -f "$HOME/.claude/PAI/USER/DA_IDENTITY.md" ]` | exists after wizard finishes |
| Backup directory | `ls -d ~/.claude.backup-*` | one or more entries if `~/.claude/` existed before |
| Pulse launchd service | `launchctl list \| grep com.pai.pulse` | one matching line |
| Pulse health | `curl -sS --max-time 3 http://localhost:31337/api/pulse/health` | JSON response |
| Pulse dashboard | `open http://localhost:31337` | dashboard renders |

`launchctl` may not list `com.pai.pulse` until the user logs out and back in — `launchd` loads the agent on next login. If it is missing right after install, that is normal.

---

## 5. Bun caveat (important)

The bootstrap requires `bun`, but its auto-install path requires:
- `[ -t 0 ]` — stdin is a TTY
- `CI` env var is unset

A Maestro agent running the bootstrap via the Bash tool fails the TTY check, so the script exits at the bun-install step. **Install `bun` first** if it is missing:

```bash
curl -fsSL https://bun.sh/install | bash
```

Then open a fresh terminal so `bun` is on `PATH` before running the bootstrap.

---

## 6. Recovery

If anything goes sideways, the previous `~/.claude/` is at `~/.claude.backup-{TIMESTAMP}`:

```bash
rm -rf ~/.claude
mv ~/.claude.backup-{TIMESTAMP} ~/.claude
```

The bootstrap prints the exact backup path when it creates one — it is not abbreviated in the actual filename, the `{TIMESTAMP}` here is just notation for the date-time stamp the script generates.

---

## 7. After install — the critical step

Run `/interview` in a **fresh Claude Code session** (not the agent that ran this playbook — that agent's `~/.claude/` was replaced underneath it). The interview captures TELOS, Ideal State, Preferences, and Identity. Without TELOS, the DA has nothing to optimize against.
