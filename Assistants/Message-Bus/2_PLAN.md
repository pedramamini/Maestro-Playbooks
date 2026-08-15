# Document 2: Plan the Install

## Context

- **Playbook**: Message Bus
- **Agent**: {{AGENT_NAME}}
- **Project**: {{AGENT_PATH}}
- **Date**: {{DATE}}
- **Working Folder**: {{AUTORUN_FOLDER}}

## Purpose

Write down every decision and every literal command before anything runs — in
particular the **arming decision** and the **watermark decision**, which are the
two choices that can misfire on a real person's message threads.

## Tasks

### Task 1: Read detection

- [ ] **Read `{{AUTORUN_FOLDER}}/BUS_DETECT.md`.** The DETECT SUMMARY is
      authoritative. If it says `BLOCKED`, document 1 already halted; if you are
      reading a `BLOCKED` summary here, stop and say so rather than proceeding.

### Task 2: Plan the Cue opt-in

- [ ] **Decide how to handle `encoreFeatures.maestroCue`**:

      | Detected state | Plan |
      |---|---|
      | `true` | Nothing to do |
      | `false` | Document 3 enables it with `settings set encoreFeatures.maestroCue true`, and document 5 tells the user it was turned on |

      Record the pitch line document 5 will use: Cue is Maestro's event-driven
      automation engine — "when this happens, fire this at this agent." The
      message bus is one subscription on it. Enabling it is instant and needs no
      restart.

      Never enable an Encore feature without recording that you did. A user who
      finds a feature switched on and does not know why has lost trust in the
      install.

### Task 3: Decide the arming state

- [ ] **Choose the terminal state, and write down why**:

      | `[ARM_ON_INSTALL]` | Terminal state |
      |---|---|
      | `manual` (default) | **DISARMED** — everything installed, Cue subscription created but **disabled**, `MAESTRO_HANDLER_AGENT_ID` present in the command line but the subscription not enabled |
      | `auto` | **ARMED** — subscription enabled at the end of a clean verify, and only then |

      Under `auto`, arming is still conditional: if document 4's verify is
      anything other than clean, document 5 reports the failure and leaves the
      subscription disabled. `auto` means "arm it if it works", never "arm it
      regardless".

      The scanner has a second, independent safety: with
      `MAESTRO_HANDLER_AGENT_ID` unset it stays in dry-run and dispatches
      nothing. Document 3 uses that for the verify pass, so the bus can be
      proven end-to-end without a single message being sent.

### Task 4: Plan the watermark

- [ ] **Plan the seed, and be explicit that it must never backfire**: the
      scanner keeps a high-water mark of the last message rowid it has seen.
      On a first run with no watermark file it records the current maximum and
      exits **without dispatching**, so it can never act on message history.

      The plan is therefore: document 3 runs the scanner once with no flags to
      seed the watermark, and confirms the output says it seeded and processed
      nothing. If a watermark file already exists (an update), document 3
      re-seeds with `--reseed` to draw a fresh line rather than inheriting a
      stale position and replaying a backlog.

      Record the state file path: `<WORK_DIR>/automation/state/message_bus_watermark.json`.

### Task 5: Resolve the working directory conflict

- [ ] **Settle `[WORK_DIR]` against the handler agent's real `cwd`**: the
      scanner resolves the spec document relative to the handler agent's working
      directory. If `BUS_DETECT.md` recorded a conflict, resolve in favour of the
      **agent's actual `cwd`** and record the override, because that is the path
      the agent will actually resolve at dispatch time. Write the final resolved
      `WORK_DIR` into the plan; every later reference uses it.

### Task 6: Write the literal commands

- [ ] **Write out every command document 3 will run, fully resolved** — no `~`,
      no unexpanded variables:

      1. `brew install steipete/tap/imsg` (only if detection said missing)
      2. `settings set encoreFeatures.maestroCue true` (only if planned above)
      3. `mkdir -p <INSTALL_DIR>` and `mkdir -p <WORK_DIR>/automation/state`
      4. `cp {{AUTORUN_FOLDER}}/assets/maestro_message_scanner.py <INSTALL_DIR>/`
      5. `cp {{AUTORUN_FOLDER}}/assets/Maestro-Message-Channel.md <WORK_DIR>/automation/`
      6. the config edits to the scanner's header block (Task 7)
      7. the seeding run: `VAULT_DIR=<WORK_DIR> /usr/bin/python3 <INSTALL_DIR>/maestro_message_scanner.py`
      8. the Cue subscription (Task 8)

### Task 7: Plan the scanner config edits

- [ ] **List the exact header values to change** in
      `<INSTALL_DIR>/maestro_message_scanner.py`. The script's config block is at
      the top and is meant to be edited:

      | Constant | Set to | Notes |
      |---|---|---|
      | `MARKER` | `[TRIGGER_MARKER]` | Only if not the `@maestro` default |
      | `ALLOWED_SENDERS` | `None`, or a Python list of handles | `None` = your own messages only. Leave `None` unless `[ALLOWED_SENDERS]` was explicitly set. |
      | `NODE_BIN` | the absolute `node` path from detection | Cue's `PATH` is minimal |

      Prefer the environment variables where they exist rather than editing the
      file — `VAULT_DIR`, `MAESTRO_HANDLER_AGENT_ID`, `MAESTRO_CLI_PATH`,
      `NODE_BIN` are all read from the environment, so they belong in the Cue
      command line, not in a patched source file. Edit the source **only** for
      `MARKER` and `ALLOWED_SENDERS`, which have no environment override.

      Note that changing `ALLOWED_SENDERS` away from `None` is the single
      highest-consequence edit in this playbook: it lets someone other than the
      user drive their agent. Only plan it if `[ALLOWED_SENDERS]` was explicitly
      configured, and record it in the plan in those words.

### Task 8: Plan the Cue subscription

- [ ] **Write the exact subscription block** document 3 will add, with real
      values substituted:

      ```yaml
      - name: maestro-message-bus
        event: time.heartbeat
        agent_id: <resolved handler agent id>
        pipeline_name: Messages
        label: '<TRIGGER_MARKER> Message Bus'
        interval_minutes: <POLL_MINUTES>
        enabled: false          # ARMED plans flip this to true in document 5
        action: command
        command:
          mode: shell
          shell: >-
            MAESTRO_HANDLER_AGENT_ID=<resolved id>
            VAULT_DIR=<WORK_DIR>
            NODE_BIN=<absolute node path>
            /usr/bin/python3 <INSTALL_DIR>/maestro_message_scanner.py --live
      ```

      A template copy of this block ships at
      `{{AUTORUN_FOLDER}}/assets/cue-subscription.yaml` — use it as the shape and
      substitute, rather than composing YAML from memory.

      Prefer creating the subscription through `maestro-cli` if a create/import
      verb exists on this build (check `maestro-cli cue --help`). Fall back to
      editing `{{AGENT_PATH}}/.maestro/cue.yaml` directly, appending under the
      existing subscription list and preserving everything already there.

### Task 9: Write the plan

- [ ] **Write `{{AUTORUN_FOLDER}}/BUS_INSTALL_PLAN.md`** containing: the Cue
      opt-in decision, the arming decision with its reason, the watermark plan,
      the resolved `WORK_DIR`, every literal command in order, the scanner config
      edits, the full subscription block, and a plain-language statement of what
      the user will still owe at the end.
