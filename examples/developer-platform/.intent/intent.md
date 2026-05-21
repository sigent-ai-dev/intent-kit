# Intent: Developer Golden Paths

**Intent ID**: INT-001
**Captured**: 2026-05-21
**Actor**: user

## Context

Small engineering team without a dedicated platform team. Each new service or feature starts from scratch with ad-hoc technology choices, leading to inconsistency across the codebase (multiple auth approaches, different ORMs, varied CI setups). Onboarding new developers takes longer than necessary because there are no standardised patterns to learn.

## Intent

Codify the team's technical decisions into enforceable golden paths so developers inherit proven patterns by default and achieve consistency across services without a dedicated platform team.

## Motivation

Inconsistency compounds with team growth — every new hire inherits a different mental model of how things are built. Setup overhead on every new service wastes senior engineering time on solved problems. Acting now while the team is small is dramatically cheaper than retrofitting later.

## Quality Attributes

- **QA-001**: Developer experience — golden paths must feel like acceleration, not bureaucracy
- **QA-002**: Consistency — services built from golden paths share auth, data access, CI, and observability patterns
- **QA-003**: Escapability — teams can deviate with documented justification (ADR), not silently
- **QA-004**: Maintainability — golden paths evolve with the team's learning, not ossify

## Success Criteria

- **SC-001**: New service goes from init to deployed-with-CI in under 1 hour using a golden path
- **SC-002**: New developer ships their first feature within 5 working days of starting
- **SC-003**: 90% of services use the same auth approach (measured by codebase audit)
- **SC-004**: Deviations from golden paths are documented (ADR exists for each deviation)

## Assumptions

- **ASM-001** [medium]: The team will agree on "the one way" for auth, data access, and CI (requires facilitated decision-making)
- **ASM-002** [high]: Templates and scaffolding are sufficient — no runtime platform or service mesh needed
- **ASM-003** [high]: Developers are senior enough to use templates without hand-holding

## Clarifications

### CLR-001
**Prompt:** What is the current tech stack? (Language, frameworks, cloud provider)
**Resolution:** OPEN — needed before steering to determine what the golden paths contain

### CLR-002
**Prompt:** Are there existing services that represent "the good pattern" to encode, or are we designing from scratch?
**Resolution:** OPEN — shapes whether this is extraction or invention
