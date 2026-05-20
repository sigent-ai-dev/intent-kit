# Business Design: [PROJECT NAME]

**Intent Reference**: INT-[NNN]
**Date**: [DATE]
**Status**: Draft

## 1. Problem Framing

<!--
  What problem exists, for whom, and what is the cost of not solving it.
  This section establishes the business case at a level stakeholders can
  validate without technical knowledge.
-->

[Problem description]

## 2. Intent Statement

<!--
  The single declarative business intent — copied from intent.md.
  This is the anchor that all other sections must serve.
-->

**INT-[NNN]**: [Single declarative sentence from intent.md]

## 3. Stakeholder Map

<!--
  Who cares about this initiative, what they need from it, and how they'll
  interact with the solution.
-->

| Stakeholder | Role | Needs | Interaction |
|-------------|------|-------|-------------|
| [Name/group] | [Their role] | [What they need] | [How they engage] |

## 4. Current State

<!--
  How things work today — processes, systems, pain points, workarounds.
  Be specific about what's broken or inefficient.
-->

[Current state description]

## 5. Desired State

<!--
  How things should work — described in terms of OUTCOMES, not solutions.
  Avoid prescribing implementation; describe the experience and results.
-->

[Desired outcomes]

## 6. Success Model

<!--
  Quantified criteria that define success. Each maps to a Success Criterion
  (SC-NNN) from the intent. Include KPIs, metrics, and acceptance measures.
-->

| SC ID | Criterion | Metric | Target | Measurement method |
|-------|-----------|--------|--------|-------------------|
| SC-001 | [From intent] | [What to measure] | [Target value] | [How to measure] |

## 7. Constraints

<!--
  Non-negotiable boundaries — regulatory, budgetary, temporal, organisational.
  These shape the solution space but don't prescribe the solution.
-->

- [Constraint 1 — e.g., "Must comply with GDPR Article 17"]
- [Constraint 2 — e.g., "Budget capped at £X for FY26"]
- [Constraint 3 — e.g., "Must integrate with existing SSO"]

## 8. Assumptions Register

<!--
  What we believe but haven't verified. Each tagged with confidence and
  an invalidation trigger (what would prove us wrong).
-->

| ID | Assumption | Confidence | Invalidation trigger |
|----|-----------|------------|---------------------|
| ASM-001 | [From intent] | high | [What would prove this wrong] |

## 9. Risk Register

<!--
  What could go wrong, likelihood, impact, and mitigations.
-->

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|------------|
| RISK-001 | [Description] | [H/M/L] | [H/M/L] | [Strategy] |

## 10. Scope Boundaries

<!--
  What's explicitly in scope, what's explicitly out, and why.
  This prevents scope creep by making boundaries visible.
-->

**In scope:**
- [Item 1]
- [Item 2]

**Out of scope:**
- [Item 1 — reason]
- [Item 2 — reason]

## 11. Acceptance Criteria

<!--
  Testable claims that define "done" at the business level. Each traces
  to a success criterion (SC-NNN) and is independently verifiable.
-->

- **AC-001** (SC-001): [Testable claim]
- **AC-002** (SC-002): [Testable claim]

## 12. Decision Log

<!--
  Business decisions made during intent capture and steering, with rationale.
  These are not technical ADRs — they're business-level choices.
-->

| Date | Decision | Rationale | Decided by |
|------|----------|-----------|------------|
| [DATE] | [What was decided] | [Why] | [Who] |
