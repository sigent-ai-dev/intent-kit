# Intent Kit Constitution

## Core Principles

1. **Intent before implementation** — no specification, architecture, or code is produced without a captured, validated intent reference.
2. **Big ideas decompose into right-sized features** — IDD operates at initiative level; features are the output of decomposition, not the input.
3. **Every artefact traces upstream** — specs trace to features, features trace to success criteria, success criteria trace to intent.
4. **Phase gates are hard** — no skipping, no implicit advancement, no silent completion.
5. **Propose-then-confirm** — nothing is written without human review and explicit approval.
6. **Audit everything** — every decision, prompt, response, and gate outcome is recorded.

## Quality Standards

- Intent documents must be falsifiable (can verify satisfaction)
- Success criteria must be testable (by metric, test, or sign-off)
- ADRs must reference the intent claim they serve
- Decomposed features must reference success criteria they advance
- No feature larger than 2 weeks enters the backlog

## Integration Contract

- Intent Kit outputs are Spec Kit inputs
- The `/intent.decompose` command produces strings ready for `/speckit.specify`
- Traceability identifiers (INT-NNN, SC-NNN, QA-NNN) are preserved through to implementation
