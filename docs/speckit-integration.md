# Spec Kit Integration Guide

This guide explains how Intent Kit and Spec Kit work together to provide a complete workflow from business intent through to implemented features.

## Overview

```
Intent Kit                              Spec Kit
─────────                              ────────
/intent.capture  →  intent.md
/intent.steer    →  ADRs + steering.md
/intent.define   →  architecture.md
/intent.decompose → speckit-ready.md ──▶  /speckit.specify (per feature)
                                          /speckit.plan
                                          /speckit.tasks
                                          /speckit.implement
```

Intent Kit handles the "big idea" → features decomposition. Spec Kit handles individual feature → implementation.

## Installation

Install both tools:

```bash
uv tool install intent-cli --from git+https://github.com/sigent-ai-dev/intent-kit.git
uv tool install specify --from git+https://github.com/github/spec-kit.git
```

Bootstrap both in your project:

```bash
intent init my-project --ai claude
specify init my-project --integration claude
```

## The Handoff: Decompose → Specify

After completing all four IDD phases, `/intent.decompose` produces `.intent/backlog/speckit-ready.md` containing copy-pasteable `/speckit.specify` invocations.

### Example Flow

1. **Complete IDD phases 1-4**:
   ```
   /intent.capture We need to modernise our portfolio construction system...
   /intent.steer
   /intent.define
   /intent.decompose
   ```

2. **Open speckit-ready.md** and find the invocation for the first feature:
   ```
   /speckit.specify Implement portfolio optimisation API — Expose the core
   optimisation engine via REST endpoints. Intent: INT-001. Advances SC-001,
   SC-003. Constrained by ADR-003: Use event-driven architecture. Acceptance
   criteria seed: (1) API accepts portfolio weights (2) Returns optimised
   allocation within 5s (3) Handles invalid inputs gracefully. Traceability:
   INT-001 > SC-001 > portfolio-optimisation-api
   ```

3. **Paste into your AI agent** — Spec Kit receives a rich, pre-seeded description and produces a spec with context already filled in.

## Traceability Chain

Every artefact traces back to the original intent:

```
INT-001 → SC-001 → Feature → spec.md → plan.md → tasks.md → code
(intent)  (success) (decompose) (specify)  (plan)   (tasks)  (implement)
```

### How It's Preserved

| Stage | Identifier | Where It Lives |
|-------|------------|----------------|
| Intent | INT-001 | `.intent/intent.md` |
| Success Criteria | SC-001 | `.intent/intent.md` § Success Criteria |
| Feature | Feature #1 | `.intent/backlog/features.md` |
| Spec Kit Spec | — | `specs/NNN-feature/spec.md` § Traceability |
| Implementation | — | Commit messages, PR descriptions |

### The Traceability Section

When `/speckit.specify` processes an invocation from Intent Kit, the resulting spec should contain:

```markdown
## Traceability

- **Intent**: INT-001
- **Success Criteria**: SC-001, SC-003
- **Constraints**: ADR-003
- **Decomposed from**: .intent/backlog/features.md#1
```

This section is free text — Spec Kit preserves it without modification.

## Validation

`intent check` validates the cross-tool boundary:

```bash
intent check --verbose
```

When decompose is complete, it checks:
- `speckit-ready.md` exists and contains valid invocations
- Every invocation references at least one SC-NNN
- No XL features in the backlog
- Every success criterion is covered by at least one feature
- Specs in `specs/` directories contain INT/SC traceability (when present)

## ID Stability

Feature numbering in `features.md` is positional and stable:
- New features get the next available number
- Removed features have their numbers retired (never reused)
- Re-running decompose doesn't change existing IDs

This ensures traceability references remain valid over time.

## Troubleshooting

### "No /speckit.specify invocations found"

The decompose phase didn't produce `speckit-ready.md`, or it's empty. Re-run `/intent.decompose`.

### Spec missing traceability section

The spec was created manually or from a different source. Add the `## Traceability` section manually referencing the relevant INT-NNN and SC-NNN.

### "Success criteria not covered by any feature"

A success criterion in `intent.md` has no corresponding feature in `features.md`. Either add a feature that advances it, or reconsider whether the SC belongs in the intent.

### Cross-tool check warns about specs without traceability

Specs in `specs/` that were created outside the IDD workflow (e.g., ad-hoc features) won't have traceability. This is a warning, not an error. Add traceability manually if the feature originated from an intent.
