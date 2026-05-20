# Feature Specification: Decompose Output for Spec Kit

**Feature Branch**: `7-decompose-speckit-output`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Ensure `/intent.decompose` output includes copy-pasteable `/speckit.specify` invocations with intent references, success criteria, and architectural constraints.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Copy-paste from decompose to speckit (Priority: P1)

A developer has completed the decompose phase and wants to start specifying individual features in Spec Kit. They open `.intent/backlog/speckit-ready.md` and copy the `/speckit.specify` invocation for a feature, paste it into their AI agent, and get a well-seeded specification.

**Why this priority**: This is the critical handoff point between Intent Kit and Spec Kit — the entire purpose of decomposition.

**Independent Test**: Run `/intent.decompose`, then paste the first generated invocation into `/speckit.specify` and verify it produces a meaningful spec with pre-filled context.

**Acceptance Scenarios**:

1. **Given** a completed decompose phase with features, **When** user opens `speckit-ready.md`, **Then** each feature has a numbered `/speckit.specify` invocation string that can be copied directly
2. **Given** a `/speckit.specify` invocation from the output, **When** pasted into an AI agent, **Then** the spec is seeded with the feature's context, success criteria, and constraints (not starting from scratch)
3. **Given** a feature that references SC-001, **When** the invocation is generated, **Then** it explicitly mentions "Must satisfy SC-001" or "Advances SC-001"

---

### User Story 2 - Traceability preserved in invocations (Priority: P1)

A developer wants to ensure that when features enter Spec Kit, they carry their IDD lineage so specs can trace back to the original intent.

**Why this priority**: Traceability is a core IDD principle — breaking it at the handoff defeats the purpose.

**Independent Test**: Generate a speckit-ready invocation and verify it contains INT-NNN, SC-NNN references, and relevant ADR constraints.

**Acceptance Scenarios**:

1. **Given** a feature referencing INT-001 and SC-002, **When** the invocation is generated, **Then** it contains "Intent: INT-001" and "Advances SC-002"
2. **Given** a feature constrained by ADR-003, **When** the invocation is generated, **Then** it contains "Constrained by ADR-003: [decision summary]"
3. **Given** a feature with 3 acceptance criteria, **When** the invocation is generated, **Then** the AC are included as seed criteria for the spec

---

### User Story 3 - Check validates speckit-ready output (Priority: P2)

A developer wants `intent check` to verify that the decompose output contains valid speckit invocations — catching malformed output before they try to use it.

**Why this priority**: Validation prevents wasted time from malformed invocations.

**Independent Test**: Run `intent check` on a project with decompose complete and verify it validates speckit-ready.md format.

**Acceptance Scenarios**:

1. **Given** decompose phase is marked complete, **When** `intent check` runs, **Then** it validates that `speckit-ready.md` exists and contains at least one invocation
2. **Given** a speckit-ready.md with invocations missing SC references, **When** `intent check` runs, **Then** a warning is reported
3. **Given** decompose is not complete, **When** `intent check` runs, **Then** speckit-ready validation is skipped

---

### Edge Cases

- What if a feature is marked "Spec Kit ready: no" (needs spike)? It should be excluded from speckit-ready.md but listed in a separate "Needs Spike" section.
- What if a feature has no success criteria references? The invocation should still be generated but with a warning comment.
- What if the decompose produces 0 speckit-ready features? The file should exist but state "No features ready — all require spikes."

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `/intent.decompose` command template MUST produce a `.intent/backlog/speckit-ready.md` file containing one `/speckit.specify` invocation per ready feature
- **FR-002**: Each invocation MUST include: feature title, context sentence, intent reference (INT-NNN), success criteria references (SC-NNN), and relevant ADR constraints
- **FR-003**: Each invocation MUST include acceptance criteria seed (from the decomposed feature's AC list)
- **FR-004**: The invocation format MUST be a single string consumable by `/speckit.specify` as its `$ARGUMENTS` input
- **FR-005**: Features marked "Spec Kit ready: no" MUST be excluded from invocations and listed in a "Needs Spike" section
- **FR-006**: `intent check` MUST validate speckit-ready.md when decompose phase is marked complete: file exists, contains at least one invocation, each invocation references at least one SC-NNN
- **FR-007**: The speckit-ready.md file MUST follow a defined format parseable by both humans and the check command

### Key Entities

- **Speckit Invocation**: A formatted string containing feature title + context + traceability references + AC seed, ready to paste into `/speckit.specify`
- **Speckit-Ready File**: `.intent/backlog/speckit-ready.md` — the handoff document between Intent Kit and Spec Kit

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of speckit-ready invocations produce a meaningful spec when pasted into `/speckit.specify` (no "insufficient context" errors)
- **SC-002**: Every invocation carries at least one traceability reference (INT or SC) — verified by `intent check`
- **SC-003**: Users can go from decompose output to first spec in under 30 seconds (copy-paste, no manual editing required)

## Assumptions

- The `/intent.decompose` command is an AI agent command (template in `templates/commands/decompose.md`), not Python code — the output format is defined in the template instructions
- `intent check` validates the output format but doesn't generate it
- The speckit-ready.md format is simple enough for regex validation in the check command
- `/speckit.specify` treats its entire `$ARGUMENTS` as a natural language feature description — no structured parsing required on Spec Kit's side
