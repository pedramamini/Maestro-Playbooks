# Document 0: Validate Configuration and Establish Scope

## Context

- **Playbook**: Market Research
- **Agent**: {{AGENT_NAME}}
- **Auto Run Folder**: {{AUTORUN_FOLDER}}
- **Date**: {{DATE}}
- **Loop**: {{LOOP_NUMBER}}

## Purpose

Fail fast, before spending a single token on research.

This playbook previously shipped with a **working example value** for the target
market, which meant a user who forgot to configure it got thirty loops of a
vault about the wrong subject, with no signal that anything was wrong. That is
the failure this document exists to prevent.

It also establishes the **scope boundary** - the one input that determines
whether the finished vault is a sharp corpus or a generic industry list.

This document runs once. If `MARKET_CONFIG.md` already exists and records
`STATUS: READY`, every task below is a no-op.

## Tasks

### Task 1: Skip if already validated

- [ ] **Check for prior validation**: If `{{AUTORUN_FOLDER}}/MARKET_CONFIG.md`
      exists and contains `STATUS: READY`, this playbook has already passed
      preflight on an earlier loop. Mark every remaining task in this document
      complete without doing anything and stop. Otherwise continue.

### Task 2: Read the configuration

- [ ] **Read the agent prompt** and record the configured values for
      `MARKET_TOPIC`, `SCOPE_IN`, `SCOPE_OUT`, `DOMAIN_ENTITY`, `SEED_SOURCE`,
      `OUTPUT_FOLDER`, `MAX_ENTITIES` and `DEPTH_SWITCH_AT`. Quote each value
      verbatim - do not normalize or interpret yet.

### Task 3: Halt on an unconfigured market

- [ ] **Refuse to run on defaults**: If `MARKET_TOPIC` still contains the string
      `<UNSET` - or is empty, or is one of the commented-out example values -
      do **not** proceed.

      Write a **halt marker** into this document, directly below this task: an
      HTML comment whose entire body is

      ```text
      maestro:halt: MARKET_TOPIC is unconfigured. Edit the Auto Run prompt and re-run.
      ```

      The marker is described rather than shown, because a literal one sitting
      in this file would halt the playbook the moment the document is read.

      Leave this task **unchecked** so the stopping point stays visible, and
      make your final message exactly this:

      > **Nothing ran.** `MARKET_TOPIC` is still at its `<UNSET>` default.
      > Open the Auto Run prompt, replace that line with the market you want
      > researched, then start the playbook again. Also remove the
      > `maestro:halt` marker from `0_CONFIGURE.md` - a stale marker blocks the
      > re-run.

      Do not guess a market. Do not proceed to document 1.

### Task 4: Establish the scope boundary

- [ ] **Resolve the antonym pair**: The boundary is stated as two opposed
      sentences: what is in scope, and the specific adjacent market that is not.

      **If `SCOPE_IN` and `SCOPE_OUT` are both configured**, use them verbatim.

      **If either is still `<UNSET>`**, derive a proposal. Run three or four web
      searches on `MARKET_TOPIC` to see how the market describes itself, then
      identify the neighboring market that shares its vocabulary but serves a
      different beneficiary. Ask: *if someone handed me 200 companies matching
      these keywords, what single split would cut the list roughly in half and
      put the half that matters on one side?* That split is the pair.

      A derived pair is a **proposal, not a decision**. Mark it as such in
      `SCOPE.md` and say so in your closing message, so the user can correct it
      before the corpus is built on top of it.

- [ ] **Write `[OUTPUT_FOLDER]/SCOPE.md`**:

      ```markdown
      ---
      type: scope
      status: user-configured | agent-proposed
      last_reviewed: {{DATE}}
      ---

      # Scope

      ## The filter

      **IN:**  [SCOPE_IN]
      **OUT:** [SCOPE_OUT]

      ## Why this line

      [Two or three sentences: what question does this vault exist to answer,
      and why does that question stop being answerable if the out-of-scope side
      is admitted.]

      ## The test

      [State the operative test in one line - usually "which party is the
      beneficiary" or "which asset is the one being served". Never "which words
      appear on the homepage".]

      ## Edge rules

      Recurring judgment calls, decided once rather than re-argued:

      - A company doing both is included only if the in-scope side is the
        primary business. Score it 50-69 and say which part is which.
      - Being funded by a fund we track is not evidence of scope membership.
      - Appearing on an industry award shortlist is not evidence of scope
        membership. Those lists optimize for novelty, not for this boundary.

      ## Overloaded terms

      Words that mean different things on either side of the line. Validate
      these per candidate rather than trusting the slogan.

      | Term | In-scope meaning | Out-of-scope meaning |
      |---|---|---|
      | [term] | [meaning] | [meaning] |
      ```

- [ ] **Create `[OUTPUT_FOLDER]/REJECTIONS.md`** as an empty log:

      ```markdown
      ---
      type: reference
      title: Rejected Category Candidates
      ---

      # Rejected Category Candidates

      Durable record of clusters surfaced during discovery that were
      **intentionally not tracked**. Each entry preserves its rationale so later
      loops do not re-litigate the same question.

      Log at **cluster** level once three or more candidates share a reason -
      not per company. Individual companies get scored, not deleted.

      **Guiding filter:** see `SCOPE.md`.

      ---

      *(No rejections logged yet.)*
      ```

### Task 5: Resolve the domain entity type

- [ ] **Name the sixth entity**: If `DOMAIN_ENTITY` is configured, use it. If it
      is `<UNSET>`, propose one: the object people in this market refer to
      constantly that is not a Company, Product, Category, Person or Capital.

      If no such object exists, record `DOMAIN_ENTITY: none` - that is a valid
      answer for some markets, and better than inventing a type nobody needs.
      Do not propose more than two.

### Task 6: Record the seed source

- [ ] **Resolve `SEED_SOURCE`**: If it is a path, confirm it exists and is
      readable now. If it is a URL, confirm it fetches. If it is a list of
      names, record them. If it is `<UNSET>`, note that discovery will start
      cold - this is allowed but produces a weaker first loop, so say so in your
      closing message.

      Do **not** halt on a missing seed source. It degrades the run; it does not
      invalidate it.

### Task 7: Install the tooling

- [ ] **Copy the assets into the vault**:

      ```bash
      mkdir -p [OUTPUT_FOLDER]/Tools
      cp {{AUTORUN_FOLDER}}/assets/health_check.py [OUTPUT_FOLDER]/Tools/
      cp {{AUTORUN_FOLDER}}/assets/kb.yaml [OUTPUT_FOLDER]/kb.yaml
      ```

      Then confirm the validator runs at all:

      ```bash
      python3 -c "import yaml" 2>/dev/null && echo "pyyaml: ok" || echo "pyyaml: MISSING"
      ```

      If PyYAML is missing, record it as a degradation and note that
      `health_check.py` cannot run until `pip install pyyaml`. Do not halt -
      research still works without the validator, it just goes unchecked.

      `kb.yaml` is a template at this point. `1_ANALYZE` fills in the entity
      types and enumerations once the market survey says what this market
      actually needs.

### Task 8: Write the config record

- [ ] **Write `{{AUTORUN_FOLDER}}/MARKET_CONFIG.md`** containing: every resolved
      value, whether the scope pair was user-configured or agent-proposed, the
      resolved domain entity, the seed source status, any degradations, and a
      final line reading exactly `STATUS: READY`.

- [ ] **Tell the user what is about to happen**: state, in four lines, the
      market, the scope pair, the domain entity and the run budget. Flag
      explicitly if the scope pair was proposed rather than configured. This is
      the last cheap moment to catch a wrong boundary - every card created after
      this inherits it.

## How to Know You're Done

`MARKET_CONFIG.md` exists with `STATUS: READY`, `SCOPE.md` and `REJECTIONS.md`
exist in the output folder, and the user has been told the boundary the run is
about to operate under.

If Task 3 halted, none of the above is true and that is the correct outcome.
