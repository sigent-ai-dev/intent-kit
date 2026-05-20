# Architecture Design: [PROJECT NAME]

**Intent Reference**: INT-[NNN]
**Date**: [DATE]
**Status**: Draft

## 1. System Context

<!--
  What the system is, who uses it, what it connects to. C4 Level 1 view.
  Include actors, external systems, and the boundary of this system.
-->

[System context description]

## 2. Intent Reference

<!--
  MANDATORY. Which intent(s) this architecture serves and which quality
  attributes drive the design decisions below.
-->

- **Intent**: INT-[NNN] — [quote the single declarative sentence]
- **Driving quality attributes**: QA-001, QA-002, QA-003

## 3. Components

<!--
  Major runtime components, their responsibilities, and interfaces.
  C4 Level 2 view. Each component should have a clear single responsibility.
-->

| Component | Responsibility | Interface |
|-----------|---------------|-----------|
| [Name] | [What it does] | [How others interact with it] |

## 4. Data Stores

<!--
  Persistence layer — what's stored, where, encryption, retention, residency.
  Reference QA-* attributes that drive these choices.
-->

| Store | What it holds | Technology | Encryption | Retention |
|-------|--------------|------------|------------|-----------|
| [Name] | [Data description] | [e.g., PostgreSQL] | [at-rest + in-transit] | [policy] |

## 5. Networking

<!--
  Connectivity model, exposure boundaries, security perimeter.
  Reference QA-* attributes for residency/latency requirements.
-->

[Network topology and exposure model]

## 6. Compute

<!--
  Where code runs and why. The choice of compute platform should trace
  to specific quality attributes (cost, latency, scale, team expertise).
-->

| Workload | Platform | Justification |
|----------|----------|---------------|
| [Name] | [e.g., Lambda, ECS, K8s] | [Why this platform — reference QA-*] |

## 7. Observability

<!--
  Logging, metrics, traces, alarms. How will you know the system is healthy?
  Map success criteria (SC-*) to observable metrics.
-->

- **Logging**: [approach]
- **Metrics**: [what's measured, where it goes]
- **Traces**: [distributed tracing approach]
- **Alarms**: [SLO-based alerting]

## 8. Security

<!--
  Authentication, authorisation, secrets management, encryption posture,
  IAM model, threat mitigations.
-->

- **Authentication**: [approach]
- **Authorisation**: [model]
- **Secrets**: [management approach]
- **Encryption**: [at-rest, in-transit]

## 9. Deployment

<!--
  CI/CD pipeline topology, environments, promotion gates, rollback strategy.
-->

- **Environments**: [e.g., dev → staging → production]
- **Promotion**: [gating strategy]
- **Rollback**: [strategy]
- **CI/CD**: [pipeline shape]

## 10. Quality Attributes Mapping

<!--
  Map each QA-* from the intent to the architectural decision(s) that
  satisfy it. This is the verification that every constraint is addressed.
-->

| Quality Attribute | Addressed by | Decision reference |
|-------------------|-------------|-------------------|
| QA-001 | [Component/pattern] | ADR-[NNN] |
| QA-002 | [Component/pattern] | ADR-[NNN] |

## 11. Decisions

<!--
  References to steering ADRs that shaped this architecture.
  Each should link back to the intent claim it serves.
-->

| ADR | Title | Intent reference |
|-----|-------|-----------------|
| ADR-001 | [Title] | QA-001, SC-002 |

## 12. Risks and Assumptions

<!--
  Unresolved risks and the assumption register with confidence levels.
  Low-confidence assumptions are candidates for spike work.
-->

| ID | Description | Confidence | Mitigation |
|----|-------------|------------|------------|
| ASM-001 | [From intent] | high | [How we'd respond if wrong] |
| RISK-001 | [New risk from architecture] | — | [Mitigation strategy] |
