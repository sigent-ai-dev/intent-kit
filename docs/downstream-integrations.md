# Downstream Integrations

Intent Kit is workflow-agnostic. After the four IDD phases complete, the decompose phase hands off to whichever specification or development workflow your team uses.

## Supported Adapters

| Adapter | Output File | Downstream Tool |
|---------|-------------|-----------------|
| `speckit` | `speckit-ready.md` | [Spec Kit](https://github.com/github/spec-kit) — Spec-Driven Development |
| `aidlc` | `aidlc-ready.md` | [AI-DLC](https://github.com/awslabs/aidlc-workflows) — AI Development Lifecycle |
| `github-issues` | `issues-ready.md` | GitHub Issues — lightweight backlog |
| `plain` | `features-ready.md` | Plain markdown — no downstream tool |

## Configuration

Set the adapter at project initialisation:

```bash
intent init my-project --downstream speckit       # default
intent init my-project --downstream aidlc
intent init my-project --downstream github-issues
intent init my-project --downstream plain
```

Or update later in `.intent/config.json`:

```json
{
  "downstream": "aidlc"
}
```

## The Handoff Flow

```
Intent Kit                           Your Downstream Workflow
─────────                           ────────────────────────
/intent.capture  →  intent.md
/intent.steer    →  ADRs + steering.md
/intent.define   →  architecture.md
/intent.decompose → <adapter>-ready.md ──▶  Your SDD tool (per feature)
```

Intent Kit handles "big idea → features" decomposition. Your downstream tool handles individual "feature → implementation".

## Adapter Details

### Spec Kit

Produces `/speckit.specify` invocations ready to paste into your AI agent:

```
/speckit.specify Implement portfolio optimisation API — Expose the core
optimisation engine via REST endpoints. Intent: INT-001. Advances SC-001,
SC-003. Constrained by ADR-003: Use event-driven architecture.
```

### AI-DLC

Produces structured feature entries compatible with AI-DLC workflow documents:

```markdown
### 1. Portfolio Optimisation API

- **Intent**: INT-001
- **Advances**: SC-001, SC-003
- **Constraints**: ADR-003
- **Description**: Expose the core optimisation engine via REST endpoints
```

### GitHub Issues

Produces `gh issue create` commands ready for shell execution:

```bash
gh issue create --title "Portfolio Optimisation API" \
  --body "Intent: INT-001. Advances SC-001, SC-003. ..."
```

### Plain Markdown

Produces a simple numbered feature list with traceability metadata — suitable for teams that don't use a formal SDD tool.

## Traceability Chain

Every artefact traces back to the original intent regardless of downstream tool:

```
INT-001 → SC-001 → Feature → [downstream artefacts] → code
(intent)  (success) (decompose) (your SDD tool)       (implementation)
```

### How It's Preserved

| Stage | Identifier | Where It Lives |
|-------|------------|----------------|
| Intent | INT-001 | `.intent/intent.md` |
| Success Criteria | SC-001 | `.intent/intent.md` § Success Criteria |
| Feature | Feature #1 | `.intent/backlog/features.md` |
| Downstream Spec | — | Depends on adapter (e.g. `specs/` for Spec Kit) |
| Implementation | — | Commit messages, PR descriptions |

## Validation

`intent check` validates the cross-tool boundary using adapter-aware rules:

```bash
intent check --verbose
```

When decompose is complete, it checks:
- The adapter-specific output file exists and contains valid content
- Every feature references at least one SC-NNN
- No XL features in the backlog
- Every success criterion is covered by at least one feature

## ID Stability

Feature numbering in `features.md` is positional and stable:
- New features get the next available number
- Removed features have their numbers retired (never reused)
- Re-running decompose doesn't change existing IDs

This ensures traceability references remain valid over time.

## Writing Custom Adapters

To add a new adapter, add an entry to `ADAPTER_CONFIGS` in `src/intent_cli/adapters.py`:

```python
"openspec": {
    "name": "OpenSpec",
    "output_file": "openspec-ready.md",
    "invocation_prefix": None,
    "invocation_pattern": r"^###\s+\d+\.\s+.+",
    "description": "OpenSpec framework output",
}
```

Then update the decompose template to handle the new format.

## Troubleshooting

### "No valid output found for adapter"

The decompose phase didn't produce the expected output file for your configured adapter. Re-run `/intent.decompose`.

### Downstream spec missing traceability section

The spec was created manually or from a different source. Add traceability metadata manually referencing the relevant INT-NNN and SC-NNN.

### "Success criteria not covered by any feature"

A success criterion in `intent.md` has no corresponding feature in `features.md`. Either add a feature that advances it, or reconsider whether the SC belongs in the intent.
