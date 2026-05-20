# Intent: [PROJECT NAME]

**Intent ID**: INT-[NNN]
**Captured**: [DATE]
**Actor**: [who captured this]
**Status**: Draft

## Context

<!--
  What world does this project live in? The problem space, not the solution
  space. Include constraints, prior art, the current state of affairs, and
  any organisational/regulatory context that shapes the design space.
-->

[Describe the environment, constraints, and problem space]

## Intent

<!--
  The big idea in a SINGLE DECLARATIVE SENTENCE. This is the claim that all
  downstream work must advance. It must be falsifiable — you can point at the
  shipped system and say "yes, this satisfies the intent" or "no, it does not."

  If you cannot express it in one sentence, you either have multiple intents
  (capture them separately) or you haven't distilled the core claim yet.
-->

[Single declarative sentence expressing the big idea]

## Motivation

<!--
  Why now? What changed that makes this urgent or valuable? What is the cost
  of inaction? This section justifies the timing, not the idea itself.
-->

[Why this is being done now]

## Quality Attributes

<!--
  Non-functional requirements that load-bear on architecture. These are the
  constraints that shape HOW the intent is satisfied. Each should be specific
  enough to inform a design decision.

  Tag each with an ID (QA-NNN) for traceability.
-->

- **QA-001**: [e.g., "Latency: API responses < 200ms p99"]
- **QA-002**: [e.g., "Data residency: all PII must remain in eu-west-1"]
- **QA-003**: [e.g., "Availability: 99.9% uptime during business hours"]

## Success Criteria

<!--
  Observable outcomes that demonstrate the intent has been satisfied. Each
  must be testable — by automated test, metric, or explicit stakeholder
  sign-off.

  Tag each with an ID (SC-NNN) for traceability.
-->

- **SC-001**: [Measurable outcome, e.g., "Analysts can complete a portfolio run via the web interface"]
- **SC-002**: [Measurable outcome, e.g., "System produces outputs within tolerance of legacy system"]
- **SC-003**: [Measurable outcome, e.g., "Onboarding a new analyst takes < 1 day"]

## Assumptions

<!--
  Explicit assumptions the team believes to be true but has not verified.
  Tag each with a confidence level (high/medium/low). Low-confidence
  assumptions are risks that may need spike work or validation.
-->

- **ASM-001** [high]: [e.g., "The existing data sources will remain available unchanged"]
- **ASM-002** [medium]: [e.g., "The team has Python expertise sufficient for the migration"]
- **ASM-003** [low]: [e.g., "The legacy system's business rules are fully documented in the VBA"]

## Clarifications

<!--
  Open questions that must be resolved before downstream phases can proceed.
  Each has an ID, a prompt (the question), and a resolution (the answer, or
  OPEN if unresolved).

  OPEN clarifications block Phase 2 (steering). This is intentional — it
  forces ambiguity resolution before architecture begins.
-->

### CLR-001
**Prompt:** [Specific question about the intent]
**Resolution:** [Answer, or OPEN — blocks /intent.steer]

### CLR-002
**Prompt:** [Specific question]
**Resolution:** [Answer, or OPEN]
