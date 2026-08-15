# Message Bus Playbook

Puts your agent on the other end of your text messages.

Drop `@maestro` into any iMessage thread — solo or group, from your phone,
watch, laptop, or iPad — and the agent picks it up, does the work with real
tools, and texts one reply back into that same thread.

There is nothing to install on the client. The client is the Messages app you
already use.

## Overview

| | |
|---|---|
| **Category** | Assistants |
| **Platform** | macOS only |
| **Loops** | No — a five-document setup run |
| **Needs** | **Full Disk Access**, Maestro Cue (Encore), `imsg`, Python 3, Node |
| **Writes** | `INSTALL_DIR`, `WORK_DIR/automation/`, `.maestro/cue.yaml` |
| **Bundled** | `assets/maestro_message_scanner.py`, `assets/Maestro-Message-Channel.md`, `assets/cue-subscription.yaml` |
| **Default terminal state** | **Disarmed** — you switch it on |

## The design: a cheap gate in front of an expensive agent

A Cue `time.heartbeat` runs a small Python script every three minutes. The
script does a fast read-only scan of the local iMessage database, finds nothing
almost every time, and exits having spent zero tokens. Only on a hit does it
call `maestro-cli send` and pay for an agent.

That is 480 firings a day, nearly all costing one database read. **The node that
decides whether to work is never the node that does the work.** Make the watcher
an agent that "checks whether anything interesting happened" and you have built
a machine that burns a fortune to discover nothing 480 times a day.

## Three things that make this harder than it looks

**macOS hides your own messages.** `chat.db` stores `NULL` in the `text` column
for anything you send — the content lives in a binary `attributedBody` blob.
Most iMessage tooling only searches `text`, which means it literally cannot see
the messages this whole system depends on: the commands *you* type. The scanner
byte-matches the marker inside the raw blob, then hands off to `imsg` to decode.
This is why the trigger marker must be plain ASCII.

**Do not open `chat.db` with `immutable=1`.** It is live and WAL-backed;
`immutable` ignores the `-wal` file and goes blind to messages that just
arrived. The bus would miss fresh commands until macOS happened to checkpoint,
which could be minutes. `mode=ro` only.

**Full Disk Access cannot be granted by a script.** Detected by attempting the
read, handled by installing disarmed, resolved by a deep link at the end.

## How the permission and safety gates are handled

| Gate | Detected how | If missing |
|---|---|---|
| Full Disk Access | Document 1 **attempts the read** and catches the failure | Halts before installing anything, opens the FDA pane |
| Maestro Cue (Encore) | `settings get encoreFeatures.maestroCue` | Planned as an explicit opt-in, enabled in document 3, **disclosed** in document 5 |
| `imsg` | `command -v` | Installed in document 3; the subscription is not created without it |
| Handler agent id | Resolved and confirmed against `list agents` | Halts — a typo here installs a bus that dispatches into nothing |

## Safety model

- **One master by default.** The scan is scoped to `is_from_me = 1` in SQL, so
  only messages **you** send can drive the agent. Nobody else in a thread can
  trigger it — not even in a group chat where they can watch it reply. Widening
  `ALLOWED_SENDERS` is possible, disclosed in the summary if used, and not the
  default.
- **Installed disarmed.** The Cue subscription is created with `enabled: false`.
  The bus starts listening because a human turned it on, not because a playbook
  finished.
- **Verify sends nothing.** With `MAESTRO_HANDLER_AGENT_ID` unset the scanner
  stays in dry-run, so the whole detect-and-decode path is proven end to end
  while dispatch is structurally impossible.
- **The watermark never backfires.** On a first run with no watermark the
  scanner records the current maximum rowid and exits without dispatching, so it
  can never act on message history. Updates re-seed rather than inherit.
- **It cannot re-trigger itself.** Replies carry a prefix containing no marker.
- **Turning it off is one line**, and document 5 puts that line in the handoff
  whether or not it armed anything.

## Document chain

| # | Document | Does |
|---|----------|------|
| 1 | `1_DETECT` | Platform, **the read probe**, Cue gate, `imsg`, resolves the handler id |
| 2 | `2_PLAN` | Cue opt-in, arming decision, watermark plan, every literal command |
| 3 | `3_INSTALL` | Installs, seeds the watermark, creates the subscription **disabled** |
| 4 | `4_VERIFY` | Re-runnable. Dry run proves detect + decode, sends nothing |
| 5 | `5_SUMMARY` | Arms only on `auto` + clean verify; handoff; how to stop it |

## Configuration

| Variable | Default | What it does |
|---|---|---|
| `HANDLER_AGENT_ID` | `self` | Agent that fulfills commands; `self` resolves to this one |
| `TRIGGER_MARKER` | `@maestro` | Must be plain ASCII — it is byte-matched in a blob |
| `ALLOWED_SENDERS` | `self` | **Consequential.** `self` = only you can drive the agent |
| `ARM_ON_INSTALL` | `manual` | `manual` leaves it off; `auto` arms only on a clean verify |
| `POLL_MINUTES` | `3` | Scan interval |
| `WORK_DIR` | `{{AGENT_PATH}}` | Must be the handler agent's `cwd` — the spec path resolves from it |
| `INSTALL_DIR` | `~/bin/maestro-message-bus` | Where the scanner goes |

## What it does not do

- **Up to `POLL_MINUTES` of latency.** It is a poll, not a push. Invisible for
  "book a table", slow for "what's 2+2".
- **One command at a time.** The serial drain that makes it reliable also means
  a burst is processed in sequence.
- **macOS only, and it needs Full Disk Access.** That is the price of meeting
  you inside the app you already use instead of behind another login.

## Bundled assets

| File | What |
|---|---|
| `maestro_message_scanner.py` | The gate. ~300 lines, standard library plus `imsg`. |
| `Maestro-Message-Channel.md` | The behavior and voice contract the handler reads on every dispatch. **Rewrite the voice section in your own texting style.** |
| `cue-subscription.yaml` | Annotated template for the subscription block. |

> **Exchange only.** The `assets/` folder travels with Playbook Exchange
> installs. Maestro's peer-to-peer share flow transports markdown only and drops
> `assets/`. If you received this by share, install from the Exchange, or pull
> the two files from their source gists:
> [scanner](https://gist.github.com/pedramamini/5470bde338cd27d0ce4acff04a199661) ·
> [handler spec](https://gist.github.com/pedramamini/123b0dbe02ded0c47aadfa5e3f2fca0a)

## Origin

Derived from [The @Maestro Message Bus](https://pedsidian.pedramamini.com/Claude/Blog/2026-05-28-maestro-message-bus).
Scripts by Pedram Amini.
