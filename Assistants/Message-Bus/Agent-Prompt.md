# Message Bus Agent Prompt

**IMPORTANT: Configure the placeholders below before running this playbook.**

This playbook wires an agent into your iMessage threads. Read the
**Safety** section at the bottom before you run it.

---

## Configuration

### Identity

<!-- CONFIGURE: The Maestro agent id that will RECEIVE and fulfill commands.
     Usually this agent. Find it in the agent's settings, or leave `self` and
     the playbook resolves it from the running agent. -->
**HANDLER_AGENT_ID:** `self`

<!-- CONFIGURE: The trigger marker you type into a thread. Must be plain ASCII —
     the scanner byte-matches it inside the message blob. Pick something you
     would never type by accident. -->
**TRIGGER_MARKER:** `@maestro`

<!-- Examples: @maestro, @jarvis, @bus, ++do -->

### Scope and safety

<!-- CONFIGURE: Who is allowed to drive the agent.
     `self` is the safe default and means ONLY messages you send can trigger it.
     Anything else opens your agent to other people. -->
**ALLOWED_SENDERS:** `self`

<!-- Valid values:
- self                              only your own outbound messages (recommended)
- +15125551212,someone@example.com  additionally allow these handles
-->

<!-- CONFIGURE: Whether the playbook ARMS the bus at the end, or leaves it
     installed and disarmed for you to switch on yourself after reviewing.
     `manual` is the safe default. -->
**ARM_ON_INSTALL:** `manual`

<!-- Valid values:
- manual    install everything, leave the Cue subscription disabled (recommended)
- auto      enable the Cue subscription at the end of a clean verify
-->

### Scheduling

<!-- CONFIGURE: How often the cheap scanner checks for new commands. Lower is
     more responsive and hits the message database more often. -->
**POLL_MINUTES:** `3`

<!-- CONFIGURE: Working directory for the scanner's state, logs, and the
     handler spec document. The scanner writes <WORK_DIR>/automation/state/ and
     reads <WORK_DIR>/automation/Maestro-Message-Channel.md. -->
**WORK_DIR:** `{{AGENT_PATH}}`

<!-- CONFIGURE: Where the scanner script gets installed. -->
**INSTALL_DIR:** `~/bin/maestro-message-bus`

---

## Agent Instructions

You are installing a **message bus**: a cheap deterministic gate that watches
iMessage for a trigger marker, and an expensive agent that only wakes when the
gate finds one.

That split is the whole design. A Cue `time.heartbeat` runs a small Python
script every `[POLL_MINUTES]` minutes. The script does a fast read-only scan of
the local iMessage database, finds nothing almost every time, and exits having
spent zero tokens. Only on a hit does it call `maestro-cli send` and pay for an
agent. **The node that decides whether to work must never be the node that does
the work.**

Two files ship with this playbook in `{{AUTORUN_FOLDER}}/assets`:

- `maestro_message_scanner.py` — the gate. Standard library plus the `imsg` CLI.
- `Maestro-Message-Channel.md` — the behavior and voice contract the handler
  agent reads on every dispatch.

Three things make this harder than it looks, and all three are handled in the
task documents. Do not work around them:

1. **macOS hides your own messages.** `chat.db` stores `NULL` in the `text`
   column for anything you send; the content lives in a binary `attributedBody`
   blob. The scanner byte-matches the marker inside that blob. This is why
   `[TRIGGER_MARKER]` must be plain ASCII.
2. **Do not open `chat.db` with `immutable=1`.** It is live and WAL-backed;
   `immutable` ignores the `-wal` file and goes blind to messages that just
   arrived. Read `mode=ro` only.
3. **Full Disk Access is required and cannot be granted by a script.** Detect it
   by attempting the read, install into a disarmed state if it is missing, and
   hand the user a deep link at the end.

Configured values appear in the task documents as `[HANDLER_AGENT_ID]`,
`[TRIGGER_MARKER]`, `[ALLOWED_SENDERS]`, `[ARM_ON_INSTALL]`, `[POLL_MINUTES]`,
`[WORK_DIR]`, and `[INSTALL_DIR]`. Read them from this prompt — do not guess.

## Safety

This gives an AI agent the ability to read message threads and send messages
from the user's own number. Treat every step as consequential:

- The default scope is **one master: the user, and only the user**. Messages
  from other people in a thread are never triggers, even in a group chat where
  they can watch the agent reply. Only change this if the user explicitly
  configured `[ALLOWED_SENDERS]`.
- The default install is **disarmed**. The bus does not start listening because
  a playbook finished; it starts because a human turned it on.
- Never dispatch a blank command. Advance past it, log it loudly, and keep the
  queue moving.
- The agent's replies carry a prefix containing no marker, so a reply can never
  re-trigger the scanner. Never put the literal marker in a reply.
