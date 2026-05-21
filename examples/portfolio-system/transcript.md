# Example: Portfolio Construction System

This example shows the full IDD workflow for a compliance-driven modernisation initiative.

## Phase 1: Capture

### Input

```
/intent.capture We need to modernise our legacy portfolio construction system —
it's a 60MB Excel workbook that 3 analysts rely on daily, and we need it in a
maintainable stack behind a web interface
```

### Interaction

**AI:**

> Here's my read of what you're describing:
>
> **The big idea**: Replace a fragile Excel-based portfolio construction workbook with a maintainable web application that preserves the analysts' existing workflow while enabling collaboration and auditability.
>
> **What I think is driving this**: The 60MB workbook is a single point of failure — if it corrupts or the analyst who maintains it leaves, the team loses a critical capability.
>
> **Success would look like**:
> - Analysts can construct portfolios through a web interface
> - Multiple analysts can work simultaneously without merge conflicts
> - Full audit trail of every portfolio change
>
> **What I'm assuming**: This is a regulated finance environment (portfolio construction implies asset management), so data integrity and audit are non-negotiable.
>
> Am I reading this right, or should I adjust my understanding?

**User:**

> Right direction but the main driver is actually regulatory — we've been told the Excel approach won't pass the next audit in March. The workbook has no change history, no access controls, and no validation. Those are the three things the auditor flagged.

**AI:**

> Got it — compliance is the primary driver with a hard deadline (March audit). That's much sharper than general "modernisation." The three audit findings (no change history, no access controls, no validation) become the success criteria directly.
>
> Let me draft the full intent:

### Output: `.intent/intent.md`

```markdown
# Intent: Portfolio Construction Modernisation

**Intent ID**: INT-001
**Captured**: 2026-05-21
**Actor**: user

## Context

The firm's portfolio construction process runs on a 60MB Excel workbook maintained by 3 analysts. The workbook has been flagged by auditors for lacking change history, access controls, and data validation. The next audit is March 2027.

## Intent

Deliver a web-based portfolio construction system that satisfies audit requirements for change history, access control, and validation while preserving the analysts' existing workflow.

## Motivation

The March 2027 audit will fail if the current Excel approach remains. Remediation after audit failure would be more expensive and time-constrained than proactive replacement. The firm risks regulatory action if portfolio construction controls are deemed inadequate.

## Quality Attributes

- QA-001: Auditability — every change to portfolio data must be logged with timestamp, actor, and before/after values
- QA-002: Access control — role-based permissions (analyst, reviewer, admin) with authentication
- QA-003: Data validation — all portfolio inputs validated against business rules before persistence
- QA-004: Availability — system available during market hours (8am-5pm local, weekdays)
- QA-005: Data integrity — no data loss; daily backups with point-in-time recovery

## Success Criteria

- SC-001: System passes external audit for change history controls
- SC-002: System passes external audit for access control requirements
- SC-003: System passes external audit for data validation
- SC-004: Analysts can complete their daily portfolio construction workflow without returning to Excel
- SC-005: Concurrent multi-user editing without data conflicts

## Assumptions

- The current Excel formulas and logic are well-understood and documented (confidence: medium)
- The firm has infrastructure for hosting a web application (confidence: high)
- The 3 analysts are willing to change their workflow if the new system is at least as capable (confidence: medium)
- The audit requirements are fixed — we're not negotiating scope with the auditor (confidence: high)

## Clarifications

- CLR-001: RESOLVED — the March 2027 deadline is hard; no extension possible
- CLR-002: OPEN — are there specific audit frameworks (SOC2, ISO 27001) that define the required controls, or is this based on auditor's professional judgment?
```

---

## Phase 2: Steer

### Input

```
/intent.steer
```

### Output: `.intent/adr/accepted/001-web-framework.md`

```markdown
---
adr: 001
title: Use server-rendered web application with progressive enhancement
status: accepted
date: 2026-05-21
intent-reference: QA-004, SC-004
---

# ADR 001 — Web Application Architecture

## Reference

This decision serves: INT-001, specifically QA-004 (availability during market hours) and SC-004 (analysts complete daily workflow via web).

## Alternatives

| Option | Pros | Cons |
|--------|------|------|
| SPA (React/Vue) | Rich interactivity, offline capable | Complex auth, slower initial load, harder to audit |
| Server-rendered (Django/Rails) | Simple auth, fast audit trail, proven patterns | Less interactive, page reloads |
| Spreadsheet-like (EtherCalc/ONLYOFFICE) | Familiar to analysts | Hard to add validation, limited audit |

## Decision

Server-rendered web application (Django) with progressive enhancement for interactive elements. The audit trail and access controls are simpler to implement and verify in a server-rendered architecture.

## Effects

- Authentication and authorization handled server-side (simpler audit story)
- Change history captured at the request level (every form submission = audit entry)
- Analysts will experience page-based navigation rather than spreadsheet-like interaction
- Progressive enhancement can add interactivity for portfolio calculations without compromising audit
```

---

## Phase 4: Decompose (excerpt)

### Output: `.intent/backlog/speckit-ready.md`

```markdown
## Ready for /speckit.specify

### 1. Portfolio data model and validation engine

**Intent**: INT-001
**Advances**: SC-003, SC-004
**Constrained by**: ADR-001 (server-rendered Django)

**Invocation**:

/speckit.specify Portfolio data model and validation engine — Implement the core data model for portfolio construction (assets, weights, constraints) with server-side validation rules that enforce business logic before persistence. Intent: INT-001. Advances SC-003, SC-004. Constrained by ADR-001: Django server-rendered architecture. Acceptance criteria seed: (1) Portfolio model captures all fields from current Excel (2) Validation rejects invalid weight allocations (3) All validation errors surfaced to user with specific field reference. Traceability: INT-001 > SC-003 > portfolio-data-model

---

### 2. Audit trail and change history

**Intent**: INT-001
**Advances**: SC-001
**Constrained by**: ADR-001 (server-rendered Django)

**Invocation**:

/speckit.specify Audit trail and change history — Implement immutable audit log capturing every portfolio change with timestamp, actor, and before/after values. Must satisfy external auditor requirements for change history controls. Intent: INT-001. Advances SC-001. Constrained by ADR-001: server-side architecture enables request-level capture. Acceptance criteria seed: (1) Every portfolio modification creates an audit entry (2) Audit entries are immutable (3) Audit log is queryable by date range and actor. Traceability: INT-001 > SC-001 > audit-trail
```
