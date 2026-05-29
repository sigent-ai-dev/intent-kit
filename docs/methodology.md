# Intent-Driven Design Methodology

## Core Concept

Intent-Driven Design (IDD) flips the relationship between ideas and implementation. Instead of starting with features, IDD starts with the **big idea** — the business initiative that justifies a programme of work.

## The Four Phases

### Phase 1: Capture

Turn a big idea into a structured seven-section intent document:

1. **Context** — the world the project lives in
2. **Intent** — the big idea in a single declarative sentence
3. **Motivation** — why now, cost of inaction
4. **Quality Attributes** — NFRs that shape architecture (tagged QA-NNN)
5. **Success Criteria** — observable outcomes that prove intent satisfied (tagged SC-NNN)
6. **Assumptions** — explicit beliefs with confidence levels
7. **Clarifications** — open questions that block downstream work

**Gate**: Intent must be a single falsifiable sentence. Maximum 7 success criteria. Maximum 5 open clarifications.

### Phase 2: Steer

Make high-level architectural decisions anchored to the intent:

- Produce ADRs (Architectural Decision Records) in RADE format
- Each ADR must have a **Reference** field linking to the intent
- Produce `steering.md` summarising key decisions

**Gate**: Every ADR has a non-empty Reference field.

### Phase 3: Define

Shape the system design:

- **Architecture Document** (technical projects) — 12 sections covering system shape
- **Business Design Document** (business projects) — 12 sections covering process shape

**Gate**: Either architecture.md or business-design.md exists and is complete.

### Phase 4: Decompose

Break the big idea into right-sized features:

- Each feature references specific success criteria
- Size must be ≤ L (1-2 weeks). XL features must split.
- Features are independently deliverable and testable
- Produces adapter-formatted output for your downstream workflow

**Gate**: No XL features. Every SC has at least one feature. Adapter output file exists.

## Key Principles

### Intent is a Big Idea

IDD operates at the level of business initiative, not user story. "Migrate our portfolio system to modern stack" is an intent. "Add export button" is a feature.

### Phase Gates Are Hard

No skipping. No implicit advancement. `intent check` enforces this programmatically.

### Everything Traces Upstream

```
INT-001 → SC-001 → Feature → Spec → Code
```

Every identifier at level N references at least one at level N-1.

### Right-Sized Decomposition

Features must be:

- Small enough to deliver in ≤ 2 weeks
- Large enough to be independently meaningful
- Traceable to specific success criteria
- Independently testable
- Dependency-aware

## Integration Points

IDD is the **upstream** methodology. It feeds into any downstream SDD workflow:

- **Spec Kit** — Spec-Driven Development
- **AI-DLC** — AI Development Lifecycle
- **OpenSpec** — open-source specification framework
- **GitHub Issues / Jira / Linear** — lightweight backlog via adapters
- Custom workflows via the adapter extension point
