# Maestro-Playbooks

Playbooks for [RunMaestro.ai](https://github.com/pedramamini/Maestro) Agent Orchestrator.

## What Are Playbooks?

Playbooks are saved Auto Run configurations that automate multi-step code improvement workflows. Each playbook defines a sequence of markdown documents with task checkboxes that Maestro processes through AI agents, looping until exit conditions are met.

## Available Playbooks

All playbooks are in the `Development/` folder:

| Playbook | Purpose | Exit Condition |
|----------|---------|----------------|
| `Performance/` | Find and fix performance issues | No PENDING items remain |
| `Security/` | Audit and remediate vulnerabilities | No CRITICAL/HIGH severity issues |
| `Refactor/` | Simplify code, eliminate duplication | No LOW risk + HIGH benefit items |
| `Documentation/` | Achieve 90% doc coverage | Coverage >=90% or no HIGH importance gaps |
| `Testing/` | Achieve 80% test coverage | Coverage >=80% or no auto-testable work |
| `Usage/` | Update README to match actual features | No CRITICAL/HIGH importance gaps |

## Playbook Architecture

Each playbook follows a 5-document chain pattern:

```
1_ANALYZE.md     -> Survey codebase, identify targets
2_FIND_*.md      -> Find specific issues/gaps
3_EVALUATE.md    -> Rate candidates by risk/benefit/importance
4_IMPLEMENT.md   -> Execute fixes meeting criteria
5_PROGRESS.md    -> Loop gate: resets 1-4 if work remains, exits if done
```

### Loop Control Mechanism

- Documents 1-4 have `Reset: OFF` (don't auto-reset when completed)
- Document 5 has `Reset: ON` and controls the loop by conditionally resetting 1-4
- Each loop iteration creates `LOOP_N_*` working files with incremented loop number

### Generated Files

Each playbook generates working documents per loop iteration:
- `LOOP_N_GAME_PLAN.md` or `LOOP_N_ATTACK_SURFACE.md` - Investigation tactics
- `LOOP_N_CANDIDATES.md` or `LOOP_N_GAPS.md` - Issues found
- `LOOP_N_PLAN.md` - Evaluated items with ratings and status
- `*_LOG_{{AGENT_NAME}}_{{DATE}}.md` - Cumulative change log

## Status Values

Items in `LOOP_N_PLAN.md` use these statuses:

| Status | Meaning |
|--------|---------|
| `PENDING` | Ready for automated implementation |
| `IMPLEMENTED` | Completed in current loop |
| `WON'T DO` | Skipped intentionally (with reason) |
| `PENDING - MANUAL REVIEW` | Requires human decision |

## Using These Playbooks

### Setup in Maestro

1. Open Maestro and select Auto Run mode
2. Choose a playbook folder (e.g., `Development/Performance/`)
3. Configure settings:
   - **Loop Mode**: ON (for continuous iteration)
   - **Max Loops**: Set a reasonable limit (5-10)
   - Documents 1-4: `Reset: OFF`
   - Document 5: `Reset: ON`

### Review-First Approach (Recommended)

1. Run once with Loop Mode OFF
2. Review the generated `LOOP_1_PLAN.md`
3. Manually adjust statuses if needed:
   - Change `PENDING` to `WON'T DO` to skip items
   - Change to `PENDING - MANUAL REVIEW` for risky items
4. Run again with Loop Mode ON

### Template Variables

These variables are substituted by Maestro at runtime:

| Variable | Description |
|----------|-------------|
| `{{AGENT_NAME}}` | Name of the Maestro agent |
| `{{AGENT_PATH}}` | Root path of the target project |
| `{{AUTORUN_FOLDER}}` | Path to the Auto Run folder |
| `{{LOOP_NUMBER}}` | Current loop iteration (1, 2, 3...) |
| `{{DATE}}` | Today's date (YYYY-MM-DD) |
| `{{CWD}}` | Current working directory |

## Customization

### Adjusting Aggressiveness

Edit `4_IMPLEMENT.md` in any playbook to change which fixes get auto-implemented:
- Default: LOW complexity/risk + HIGH gain/benefit only
- More aggressive: Include MEDIUM complexity
- Conservative: Require VERY HIGH gain

### Adding Custom Tactics

Edit `1_ANALYZE.md` to add domain-specific investigation patterns for your tech stack.

### Creating New Playbooks

Copy an existing playbook folder and modify:
1. Update the Context section variables
2. Adjust the discovery patterns in step 2
3. Modify rating criteria in step 3
4. Change exit conditions in step 5

## Tips

1. **Start without loop mode** - Review what it finds before enabling automation
2. **Set max loops** - Prevent runaway iterations
3. **Check the logs** - Each playbook maintains a cumulative log file
4. **Commit frequently** - Each loop iteration is a good commit point
5. **Run tests** - After each batch of changes, verify nothing broke

## License

See [LICENSE](LICENSE) for details.
