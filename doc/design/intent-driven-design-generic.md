---
title: Intent-Driven Design (IDD)
status: Draft
date: 2026-05-19
author: Superhighway Factory
audience: Engineering teams, delivery leads, architects, product owners
type: Reusable methodology asset
---

# Intent-Driven Design (IDD)

> A methodology for turning a big idea into traceable, right-sized
> deliverables — ensuring that every downstream artefact (spec, plan,
> decision, task, code, infrastructure) can answer the question:
> "what intent does this serve?"

---

## 1. What IDD Is

Intent-Driven Design is a structured methodology that sits upstream of
feature-level specification work. It solves a specific problem: teams
that build the right things the wrong way, or the wrong things the right
way, because the original business intent was never captured in a form
that downstream work can reference, verify against, or be held
accountable to.

IDD operates at the level of the **big idea** — the business initiative,
the platform decision, the modernisation programme, the product strategy.
It captures that big idea as a structured, falsifiable claim, then
provides the machinery to decompose it into right-sized features that
can be specified, planned, and implemented independently while
maintaining traceability back to the original intent.

The methodology produces two families of design document:

1. **Architecture Design Documents** — technical decisions, component
   topology, quality attributes, and infrastructure shape, all anchored
   to the intent they serve.
2. **Business Design Documents** — problem framing, success criteria,
   stakeholder context, and acceptance boundaries that define what
   "done" means in business terms.

Both trace to a single upstream source: the **structured intent** — a
seven-section document that locks in the WHY before any HOW is explored.

---

## 2. The Problem

### 2.1 The "Green Gates, Broken Reality" failure mode

In conventional delivery, the chain from idea to implementation has
implicit links:

```
big idea (verbal) → ticket (brief) → spec (detailed) → code → deploy
       ↑                                                         ↑
       │              drift accumulates silently                 │
       └─────────────────────────────────────────────────────────┘
                      discovered post-merge
```

Each transition is a lossy compression. The ticket captures a fragment of
the conversation. The spec interprets the ticket through the lens of
whoever writes it. The implementation interprets the spec. By the time
code ships, it may satisfy every gate — tests pass, lint is clean, the
PR was reviewed — yet deliver something the business didn't ask for.

The failure mode is insidious because every individual gate is green.
Tests pass against the spec. The spec passes its own review. The PR
passes code review. But nobody checked whether the spec still advances
the original intent, because the intent was never captured in a form
that makes that check possible.

### 2.2 The decomposition gap

Big ideas don't fit in a single sprint. They need to be broken down. But
decomposition without structure produces one of two failure modes:

1. **Feature soup** — work items that individually make sense but don't
   compose into the intended whole. Each feature advances *something*,
   but nobody can trace back to confirm it advances *the intent*.

2. **Monolithic specs** — attempts to specify the entire big idea at
   feature-level detail, producing 50-page documents that nobody reads,
   that go stale before implementation begins, and that resist change.

IDD solves this by separating the big idea (intent) from its
decomposition (backlog) and providing explicit machinery for the
transition between them.

### 2.3 Why existing approaches fall short

| Approach | Strength | Gap |
|----------|----------|-----|
| User stories | Captures who/what/why concisely | Too granular for big ideas; no structured decomposition from strategy to story |
| PRDs/BRDs | Rich business context | Monolithic; no stable identifiers; disconnected from implementation |
| OKRs | Outcome-oriented | Too high-altitude to trace to features; no decomposition machinery |
| Acceptance criteria | Testable claims | Describe WHAT not WHY; can drift without detection |
| Spec-Driven Development | Structured feature delivery | Assumes intent is already clear; doesn't capture or validate the WHY |
| Epics + stories | Hierarchical breakdown | Hierarchy is organisational, not logical; no traceability contract |

IDD fills the gap between high-level goals and feature-level work. It is
the bridge that turns a big idea into right-sized deliverables without
losing the thread of WHY.

---

## 3. Core Principles

### 3.1 Intent is a big idea, not a feature

Intent operates at the level of business initiative, not user story.
"Migrate our portfolio construction system to a modern stack" is an
intent. "Add a button to export results as PDF" is a feature. The intent
is the big idea that justifies a programme of work; features are the
decomposed pieces that deliver it.

IDD captures the big idea first, then provides structured decomposition
into right-sized features. This is the opposite of bottom-up planning,
where features are identified ad-hoc and then retrospectively grouped
into an "epic" label.

### 3.2 Every artefact traces to intent

No spec is written without an intent reference. No decision is taken
without explaining what intent it serves. No test exists without naming
the requirement it proves. The traceability chain is explicit and
machine-inspectable:

```
INT-001  →  US-001  →  FR-001  →  DEC-001  →  ENT-001  →  T-001
  │           │          │           │           │           │
intent.md  spec.md    spec.md    plan.md    data-model   tasks.md
(big idea) (feature)  (requirement) (decision)  (entity)   (task)
```

### 3.3 Separate concerns by altitude

Decisions made at the wrong altitude produce waste:

| Altitude | Question | Artefact |
|----------|----------|----------|
| **Intent** | WHY — the business case | `intent.md` |
| **Steering** | HOW-AT-A-HIGH-LEVEL — which patterns, which technologies | ADRs + `steering.md` |
| **Definition** | WHAT SHAPE — what the system looks like | `architecture.md` |
| **Backlog** | WHAT PIECES — right-sized features that deliver the intent | GitHub issues / feature specs |
| **Specification** | WHAT EXACTLY — per-feature requirements | `spec.md` per feature |
| **Implementation** | HOW CONCRETELY — code, tests, infrastructure | Source code |

Conflating any two means decisions get made at the wrong altitude.
Picking a database before establishing whether persistent storage is
needed. Writing feature specs before the architectural constraints are
known. Decomposing into tasks before the decomposition into features is
validated.

### 3.4 Phase gates prevent drift

Each phase is **gated**, **sequential**, and **idempotent within phase**:

- **Gated** — the next phase refuses to proceed until the current phase
  validates.
- **Sequential** — no phase skipping; no implicit advancement.
- **Idempotent** — re-running a phase with the same inputs produces the
  same artefacts.

### 3.5 Propose-then-confirm

IDD tooling never writes artefacts silently. Every phase:

1. Proposes a structured output.
2. Presents it for human review.
3. Records explicit approval in an append-only audit log.
4. Only then marks the phase complete.

### 3.6 Append-only audit trail

Every prompt, response, decision, and gate outcome is recorded with
timestamps. The log is non-blocking, append-only, and structured. It
provides a complete record of who decided what, when, and why.

---

## 4. The IDD Workflow

### 4.1 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  1. INTENT — capture the big idea                               │
│  Output: intent.md (7 sections)                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│  2. STEER — make high-level decisions                           │
│  Output: ADRs + steering.md                                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│  3. DEFINE — produce the architecture/business design            │
│  Output: architecture.md OR business-design.md                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│  4. DECOMPOSE — break into right-sized features                 │
│  Output: reviewed backlog of feature-level issues               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│  5. SPECIFY & IMPLEMENT — per-feature SDD cycle                 │
│  Output: spec.md → plan.md → tasks.md → implementation PRs     │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 1: Intent Capture

The entry point. Someone arrives with a big idea and the system captures
it as a structured, falsifiable claim.

#### Inputs accepted

| Input type | Description |
|------------|-------------|
| Free-form description | A verbal or written statement of the big idea |
| Existing document | Business case, PRD, email thread, meeting notes, strategy deck |
| Interactive Q&A | The system elicits each section through guided conversation |
| Prior intent | Resume an in-flight capture |

#### Output: `intent.md` (seven sections)

```markdown
---
intent_id: INT-001
captured_at: <ISO 8601 timestamp>
actor: <who captured this>
schema_version: '1.0.0'
---

# Intent — <project-name>

## Context
What world does this project live in? The problem space, not the
solution space. Constraints, prior art, the current state of affairs.

## Intent
The big idea in a single declarative sentence. This is the claim that
all downstream work must advance. It must be falsifiable — you can
point at the shipped system and say "yes, this satisfies the intent"
or "no, this does not."

## Motivation
Why now? What changed that makes this urgent or valuable? What is the
cost of inaction?

## Quality Attributes
Non-functional requirements that load-bear on architecture: latency,
throughput, data residency, RTO/RPO, compliance, security posture.
These are the constraints that shape the HOW.

## Success Criteria
Observable outcomes that demonstrate the intent has been satisfied.
Each criterion must be testable — by automated test, metric, or
explicit stakeholder sign-off.

## Assumptions
Explicit assumptions, each tagged with a confidence level
(high/medium/low). Assumptions are claims believed true but not
verified. They become risks when confidence is low.

## Clarifications
Open questions that must be resolved before downstream phases can
proceed. Each has an ID, prompt, and resolution status.
```

#### Why a single sentence for Intent?

The discipline of expressing the big idea in one sentence forces clarity.
If you can't state it in one sentence, you either have multiple intents
(which should be captured separately) or you haven't yet distilled the
core claim from the surrounding context. The Context and Motivation
sections provide the richness; the Intent section provides the anchor.

#### Validation gate

Phase 1 is not complete until:

- `context`, `intent`, `motivation`, and `success_criteria` are non-empty
- The Intent section is a single declarative sentence
- The operator explicitly confirms

### 4.3 Phase 2: Architectural Steering

Turns captured intent into reviewed high-level decisions.

#### Inputs

- `intent.md` from Phase 1 (must exist and validate)
- Organisational constraints, technology landscape, team capabilities

#### Outputs

| Artefact | Purpose |
|----------|---------|
| One ADR per decision | Captures the decision in RADE format (Reference, Alternatives, Decision, Effects) |
| `steering.md` | Project-specific guardrails and conventions |

#### The Reference field

Every ADR produced under IDD includes a **Reference** field naming the
intent claim it serves. An ADR that cannot name its upstream intent is
either premature or orphaned. This is the mechanism that prevents
speculative architecture.

### 4.4 Phase 3: Definition

Composes intent + steering into a design document.

#### Architecture Design Document (technical big ideas)

When the intent is primarily technical, Phase 3 produces an Architecture
Design Document — a 12-section contract:

| # | Section | Content |
|---|---------|---------|
| 1 | System context | What the system is, who uses it, what it connects to |
| 2 | Intent reference | The INT-* identifier(s) this architecture serves |
| 3 | Components | Major runtime components, responsibilities, interfaces |
| 4 | Data stores | Persistence: what, where, encryption, retention |
| 5 | Networking | Connectivity, exposure model, security boundaries |
| 6 | Compute | Where code runs and why |
| 7 | Observability | Logging, metrics, traces, alarms |
| 8 | Security | Auth, secrets, encryption, IAM, threat mitigations |
| 9 | Deployment | CI/CD, environments, promotion, rollback |
| 10 | Quality attributes | NFRs from intent mapped to decisions |
| 11 | Decisions | References to steering ADRs |
| 12 | Risks and assumptions | Unresolved risks, assumption register |

#### Business Design Document (business-oriented big ideas)

When the intent is primarily business-oriented, Phase 3 produces a
Business Design Document:

| # | Section | Content |
|---|---------|---------|
| 1 | Problem framing | What problem, for whom, cost of inaction |
| 2 | Intent statement | The single declarative business intent |
| 3 | Stakeholder map | Who cares, what they need, how they interact |
| 4 | Current state | How things work today — pain points, workarounds |
| 5 | Desired state | How things should work — outcomes not solutions |
| 6 | Success model | Quantified criteria: KPIs, metrics, acceptance |
| 7 | Constraints | Non-negotiable boundaries |
| 8 | Assumptions register | Unverified beliefs with confidence levels |
| 9 | Risk register | What could go wrong, mitigations |
| 10 | Scope boundaries | In, out, and why |
| 11 | Acceptance criteria | Testable claims that define "done" |
| 12 | Decision log | Business decisions with rationale |

### 4.5 Phase 4: Decompose — From Big Idea to Right-Sized Features

This is the critical transition from IDD to feature-level work. The big
idea (intent) has been captured, the architectural decisions made, and the
design document produced. Now it must be broken into pieces that teams
can deliver independently.

#### The decomposition problem

A big idea is not a feature. It is a programme of work that might span
weeks or months. Trying to specify it at feature-level detail produces a
monolith. Trying to implement it without decomposition produces chaos.
The decomposition phase turns a single intent into a backlog of
right-sized features, each:

- **Small enough** to specify, plan, and implement in a bounded time
- **Large enough** to deliver independently meaningful value
- **Traceable** to the parent intent and specific success criteria
- **Independently testable** against its own acceptance criteria
- **Dependency-aware** with explicit blocking relationships

#### Decomposition rules

The backlog decomposition follows a structured playbook:

**1. Identify outcome boundaries**

Each feature should advance exactly one observable outcome. If a proposed
feature advances multiple unrelated outcomes, it should be split. If
multiple proposed features advance the same outcome, they should be
reviewed for overlap.

**2. Right-size by delivery cadence**

| Size | Delivery window | Characteristics |
|------|-----------------|-----------------|
| XS | < 1 day | Single-concern, minimal review surface |
| S | 1–2 days | One component, one test boundary |
| M | 3–5 days | Cross-component, integration test needed |
| L | 1–2 weeks | Architectural significance, multiple PRs |
| XL | > 2 weeks | Must decompose further — not implementable as-is |

XL items are not features — they are sub-intents that need their own
decomposition pass. This is a hard rule: nothing enters implementation
that cannot be delivered within 2 weeks.

**3. Classify by type**

Every decomposed feature gets a type classification:

- `feat` — new capability that didn't exist before
- `chore` — necessary work that doesn't change user-visible behaviour
- `bug` — correction of existing behaviour
- `refactor` — restructuring without behaviour change
- `docs` — documentation improvement
- `test` — test coverage improvement

**4. Assign priority relative to intent**

- **P0** — blocks all other work; the intent cannot advance without this
- **P1** — needed in the current delivery cycle
- **P2** — needed in the next cycle
- **P3** — needed eventually; not time-critical

**5. Map to success criteria**

Every feature must reference at least one success criterion from the
intent. A feature that cannot name the success criterion it advances is
either out of scope or the success criteria are incomplete.

#### Decomposition output: The reviewed backlog

Each item in the decomposed backlog contains:

```markdown
## Feature: <imperative title>

**Intent reference:** INT-001
**Success criteria advanced:** SC-002, SC-003
**Type:** feat
**Size:** M
**Priority:** P1

### Context
Why this feature exists in the context of the parent intent.

### Acceptance criteria
- [ ] <testable claim 1>
- [ ] <testable claim 2>
- [ ] <testable claim 3>

### Out of scope
What this feature explicitly does NOT cover.

### Dependencies
- Blocked by: <feature-id> (if any)
- Blocks: <feature-id> (if any)
```

#### Anti-patterns the decomposition catches

| Anti-pattern | Detection | Resolution |
|--------------|-----------|------------|
| **Epic-shaped features** | Multiple unrelated outcomes in one body | Split into per-outcome features + tracking issue |
| **Features with no acceptance criteria** | Missing AC section | Rejected — cannot enter backlog |
| **Orphaned features** | Cannot name a success criterion from intent | Either out of scope or success criteria need updating |
| **Dependency cycles** | A blocks B blocks A | Redesign to break the cycle |
| **XL features** | Size estimate > 2 weeks | Must decompose further before entering backlog |

#### The three modes of backlog operation

1. **Create** — propose-then-confirm. The system drafts decomposed
   features from the intent + design document, presents them for review,
   and only on confirmation creates the backlog items.

2. **Validate** — read-only audit. Given an existing backlog, inspect
   each item against the decomposition rules and produce a findings
   report (missing AC, missing intent reference, wrong size, etc.).

3. **Link-back** — append traceability references from the intent and
   design documents to the produced backlog items, and vice versa.

### 4.6 Phase 5: Specify & Implement (per feature)

Once the backlog exists, each feature enters the Spec-Driven Development
(SDD) lifecycle independently:

```
specify → plan → tasks → implement
```

Each feature's spec references:
- The parent intent (`INT-001`)
- The specific success criteria it advances (`SC-002`)
- The architectural decisions that constrain it (`ADR-003`)
- Its decomposition context (why this piece, at this size, now)

This is where IDD hands off to SDD. The per-feature cycle is
well-understood; IDD's contribution is ensuring it starts from the right
place with the right context.

---

## 5. The Big Idea → Feature Pipeline (Visual)

```
                        ┌─────────────────────┐
                        │     BIG IDEA        │
                        │  (verbal, docs,     │
                        │   strategy, need)   │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   PHASE 1: INTENT CAPTURE   │
                    │   7-section structured doc   │
                    │   Single declarative claim   │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   PHASE 2: STEERING         │
                    │   ADRs + conventions         │
                    │   High-level HOW decisions   │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   PHASE 3: DEFINE           │
                    │   Architecture or Business   │
                    │   Design Document            │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   PHASE 4: DECOMPOSE        │
                    │   Break big idea into        │
                    │   right-sized features        │
                    │                              │
                    │   ┌──────┐ ┌──────┐ ┌────┐  │
                    │   │Feat 1│ │Feat 2│ │ .. │  │
                    │   └──┬───┘ └──┬───┘ └──┬─┘  │
                    └──────┼────────┼─────────┼────┘
                           │        │         │
              ┌────────────▼─┐  ┌───▼──────┐  │
              │ SPECIFY      │  │ SPECIFY   │  ...
              │ PLAN         │  │ PLAN      │
              │ TASKS        │  │ TASKS     │
              │ IMPLEMENT    │  │ IMPLEMENT │
              └──────────────┘  └───────────┘

              Each feature independently enters
              the SDD lifecycle with full context
```

---

## 6. Inputs Taxonomy

IDD accepts diverse inputs and synthesises them into structured intent.
The richer the inputs, the higher quality the captured intent and the
more effective the decomposition.

### 6.1 Business inputs (→ Business Design Documents)

| Input category | Examples | Informs |
|----------------|----------|---------|
| Business case | ROI model, cost-benefit, executive brief | Motivation, Success Criteria |
| Stakeholder context | Org chart, RACI, sponsor expectations | Context, Assumptions |
| Problem statement | Incidents, complaints, operational pain | Context, Motivation, Intent |
| Regulatory requirement | Compliance mandate, audit finding | Context, Quality Attributes |
| Market analysis | Competitor review, industry trend | Motivation, Context |
| User research | Interviews, surveys, journey maps | Intent, Success Criteria |
| Strategic objective | OKR, roadmap item, quarterly goal | Motivation, Success Criteria |
| Legacy documentation | Existing systems, operational runbooks | Context, Quality Attributes |
| Meeting notes | Steering committee minutes, design reviews | Context, Clarifications |

### 6.2 Technical inputs (→ Architecture Design Documents)

| Input category | Examples | Informs |
|----------------|----------|---------|
| Data sources | File inventories, API catalogues, schemas | Context, Quality Attributes |
| Non-functional requirements | SLAs, SLOs, latency budgets | Quality Attributes |
| Infrastructure constraints | Network topology, residency rules | Context, Assumptions |
| Technology landscape | Approved tech, platform capabilities | Assumptions, Context |
| Integration points | Upstream/downstream systems, APIs | Context, Clarifications |
| Observability requirements | SLO targets, audit requirements | Quality Attributes, Success Criteria |
| Security posture | Threat model, compliance framework | Quality Attributes, Assumptions |
| Existing architecture | Diagrams, deployment topology | Context, Assumptions |

### 6.3 Analytical inputs (→ Domain/Data Design Documents)

| Input category | Examples | Informs |
|----------------|----------|---------|
| Raw data snapshots | CSV exports, database dumps, spreadsheets | Context |
| Legacy business rules | Macros, formulas, stored procedures | Context, Quality Attributes |
| Domain expertise | SME interviews, operational SOPs | Clarifications, Assumptions |
| Validation criteria | Known-good outputs, parity targets | Success Criteria |

---

## 7. The Traceability Model

### 7.1 Identifier scheme

| Prefix | Level | Altitude | Lives in |
|--------|-------|----------|----------|
| `INT-NNN` | Intent (big idea) | Strategy | `intent.md` |
| `SC-NNN` | Success criterion | Strategy | `intent.md` § Success Criteria |
| `QA-NNN` | Quality attribute | Strategy | `intent.md` § Quality Attributes |
| `US-NNN` | User story | Feature | `spec.md` |
| `FR-NNN` | Functional requirement | Feature | `spec.md` |
| `DEC-NNN` | Design decision | Architecture | ADR / `plan.md` |
| `ENT-NNN` | Data entity | Architecture | Data model |
| `T-NNN` | Task | Implementation | `tasks.md` |
| `INV-NNN` | Invariant | Constraint | `invariants.md` |

### 7.2 Traceability rules

1. Every feature in the backlog references at least one `INT-NNN` and
   at least one `SC-NNN`.
2. Every requirement (`FR-NNN`) references the feature it belongs to.
3. Every decision (`DEC-NNN`) references the intent or quality attribute
   it serves.
4. Every task (`T-NNN`) references the requirement it implements.
5. An artefact that cannot name its upstream reference is orphaned.

### 7.3 Drift detection

Because every artefact carries a reference to its upstream intent:

- A feature that doesn't reference a success criterion is out of scope.
- A decision that doesn't reference an intent is speculative.
- A task that doesn't reference a requirement is untraced.
- A requirement whose parent intent has changed is potentially stale.

Drift is detectable at the document level — before code is written.

---

## 8. How Intent Shapes Design Documents

### 8.1 Intent → Architecture

```
Intent section              Architecture section
──────────────              ────────────────────
Context           ────────▶ System context, Networking
Intent statement  ────────▶ Intent reference, Components
Quality Attributes ───────▶ Quality attributes, Compute, Data stores
Success Criteria  ────────▶ Observability (what to measure)
Assumptions       ────────▶ Risks and assumptions, Decisions
Clarifications    ────────▶ MUST BE RESOLVED (blocks production)
```

### 8.2 Intent → Business Design

```
Intent section              Business Design section
──────────────              ───────────────────────
Context           ────────▶ Problem framing, Current state
Intent statement  ────────▶ Intent statement, Desired state
Motivation        ────────▶ Problem framing (urgency), Constraints
Quality Attributes ───────▶ Constraints, Success model
Success Criteria  ────────▶ Success model, Acceptance criteria
Assumptions       ────────▶ Assumptions register, Risk register
Clarifications    ────────▶ Resolved → Decision log; Open → BLOCKS
```

### 8.3 Intent → Backlog decomposition

```
Intent section              Decomposition input
──────────────              ────────────────────
Intent statement  ────────▶ Defines the boundary of "in scope"
Success Criteria  ────────▶ Each criterion becomes 1+ features
Quality Attributes ───────▶ Cross-cutting constraints on every feature
Assumptions       ────────▶ High-risk assumptions may need spike features
Clarifications    ────────▶ Unresolved → spike or research feature
Context           ────────▶ Informs dependency ordering
```

---

## 9. Anti-patterns IDD Prevents

### 9.1 Solution-first thinking

**Symptom:** "We need a Lambda that calls DynamoDB and..."
**Response:** Capture the intent first. If you can't state the business
intent in a single sentence, you're not ready to choose technologies.

### 9.2 Implicit intent

**Symptom:** "Everyone knows why we're building this."
**Response:** If it's never written, it can never be verified. Implicit
intent is untestable intent. Write it down.

### 9.3 Premature architecture

**Symptom:** Choosing a database before establishing whether persistent
storage is needed.
**Response:** Phase gates enforce altitude separation. Steering cannot
begin until intent validates.

### 9.4 Monolithic decomposition

**Symptom:** A single epic-shaped spec that tries to specify the entire
big idea at feature-level detail.
**Response:** IDD separates intent (the big idea) from decomposition
(the features). The big idea lives in `intent.md`; right-sized features
live in the backlog. The design document is the bridge between them.

### 9.5 Orphaned decisions

**Symptom:** ADRs that exist but don't explain which intent they serve.
**Response:** The RADE format requires a Reference field. Decisions
without intent references are flagged.

### 9.6 Drift-invisible delivery

**Symptom:** Features that satisfy all tests but miss the original need.
**Response:** The traceability chain makes drift visible at the document
level, before implementation begins.

### 9.7 Feature soup

**Symptom:** A backlog of items that individually make sense but don't
compose into the intended whole.
**Response:** Every feature must reference a success criterion from the
intent. Features that can't name what they advance are out of scope.

### 9.8 Context loss across handoffs

**Symptom:** New team members re-derive decisions because the reasoning
was never captured.
**Response:** The audit log, ADRs, and intent document provide the full
decision record.

---

## 10. Relationship to Spec-Driven Development (SDD)

### 10.1 IDD is upstream of SDD

```
IDD (Intent-Driven Design)          SDD (Spec-Driven Development)
───────────────────────────          ────────────────────────────
Captures the WHY (big idea)          Captures WHAT and HOW (features)
Produces intent.md                   Consumes intent reference
Produces ADRs + steering             Consumes constraints
Produces design documents            Produces spec.md + plan.md
Produces decomposed backlog          Consumes backlog items
                                     Drives implementation
```

### 10.2 The handoff

IDD produces a reviewed backlog of right-sized features. Each feature
enters SDD's lifecycle independently:

```
IDD output (per feature):            SDD input:
─────────────────────────            ──────────
• Intent reference (INT-001)    →    Context for spec.md
• Success criteria (SC-002)     →    Acceptance criteria seed
• Architectural constraints     →    Plan constraints
• Feature acceptance criteria   →    Spec validation target
• Dependency map                →    Task ordering
```

### 10.3 What IDD adds that SDD alone doesn't provide

| Capability | SDD alone | IDD + SDD |
|------------|-----------|-----------|
| Big idea capture | Assumed pre-existing | Explicit, validated, structured |
| Architectural steering | Ad-hoc | Gated, audited, traceable |
| Intent traceability | Partial (FR → T) | Full (INT → SC → US → FR → DEC → T) |
| Decomposition discipline | Features assumed right-sized | Explicit sizing + validation |
| Drift detection | At implementation time | At specification time |
| Business sign-off | Informal | Explicit approval in audit log |

---

## 11. When to Use IDD

### 11.1 Use IDD when

- The work represents a **big idea** — a programme, not a task
- The business intent is ambiguous, contested, or multi-stakeholder
- The project has architectural significance (one-way-door decisions)
- Regulatory or compliance requirements demand traceability
- The work crosses team boundaries or has a long time horizon
- Legacy modernisation where original intent was never documented
- The cost of building the wrong thing exceeds the cost of capturing
  intent

### 11.2 Skip IDD when

- The intent is trivially obvious (bug fix, dependency update)
- The work is purely mechanical (library bump, config change)
- The scope fits in a single sprint with no architectural decisions
- The team is already aligned and just needs to execute

For lightweight work, SDD's feature-level flow is sufficient. IDD adds
value when the risk of building the wrong thing — or decomposing it
incorrectly — exceeds the cost of structured intent capture.

---

## 12. Portability

IDD does not depend on any specific:

- Cloud provider or infrastructure platform
- Programming language or framework
- CI/CD system or project management tool
- AI tooling (though AI skills can accelerate each phase)

What transfers to any context:

1. The seven-section intent document structure
2. The four-phase workflow (intent → steer → define → decompose)
3. The big-idea-to-feature decomposition playbook
4. The identifier scheme and traceability chain
5. The phase-gate discipline
6. The append-only audit trail
7. The propose-then-confirm interaction model
8. The clarification system for ambiguity resolution
9. The altitude-separation principle
10. The right-sizing rubric for backlog items

---

## 13. Implementing IDD

### 13.1 Minimum viable adoption

To adopt IDD, a team needs:

1. **The intent template** — the seven-section document, adapted to
   local conventions.
2. **A decomposition playbook** — rules for breaking intent into
   right-sized features (Section 4.5 provides the reference).
3. **A traceability convention** — identifier scheme that links features
   back to intent (can be as simple as "every issue title starts with
   the intent ID").
4. **A phase-gate agreement** — the team agrees that specification
   doesn't begin until intent is captured and reviewed.

### 13.2 Full adoption

Full adoption adds:

- Tooling for interactive intent capture
- Automated validation gates
- Append-only audit logging
- Cross-artefact traceability checking
- Architecture/Business Design Document templates
- Backlog decomposition automation
- Integration with issue tracking and CI/CD

### 13.3 Adoption anti-patterns

| Anti-pattern | Why it fails |
|--------------|-------------|
| Capturing intent retroactively | Loses the forcing function; becomes documentation not design |
| Skipping decomposition | Produces monolithic specs or feature soup |
| Treating intent as a formality | Perfunctory capture doesn't prevent drift |
| Decomposing without design | Features are sized wrong because constraints aren't known |
| Over-ceremonialising small work | IDD is for big ideas; small fixes should just be fixed |

---

## 14. Glossary

| Term | Definition |
|------|------------|
| **Big idea** | A business initiative, programme, or strategy-level goal that requires structured decomposition before implementation |
| **Intent** | A single declarative sentence capturing what a project exists to achieve |
| **IDD** | Intent-Driven Design — this methodology |
| **SDD** | Spec-Driven Development — the downstream feature-level methodology |
| **Steering** | High-level architectural decisions that constrain the solution space |
| **Definition** | The concrete shape of a system (architecture) or problem (business design) |
| **Decomposition** | The structured process of breaking a big idea into right-sized features |
| **Right-sized** | Small enough to deliver in ≤2 weeks, large enough to be independently meaningful |
| **Phase gate** | A validation checkpoint that blocks downstream work until upstream is complete |
| **Traceability chain** | The linked sequence of identifiers from intent through to task |
| **Drift** | Divergence between what was intended and what was built |
| **Altitude** | The level of abstraction at which a decision is made |
| **RADE** | ADR format: Reference, Alternatives, Decision, Effects |
| **Clarification** | A structured question raised when the intent is ambiguous |
| **Feature soup** | A backlog of items that individually pass review but don't compose into the intended whole |
| **Orphaned artefact** | Any document that cannot name its upstream intent reference |
