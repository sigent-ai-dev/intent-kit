# Feature Specification: Intent Check Command

**Feature Branch**: `2-intent-check`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Implement the `intent check` command that validates phase state consistency, gate satisfaction, intent document schema, and ADR traceability.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validate project state before progressing (Priority: P1)

A developer who has completed the capture phase wants to confirm their project is in a valid state before running `/intent.steer`. They run `intent check` and get a clear pass/fail summary showing whether all gates are satisfied and documents are well-formed.

**Why this priority**: This is the core value — gate enforcement is meaningless without validation.

**Independent Test**: Run `intent check` in a project with a valid captured intent; verify exit code 0 and all checks pass.

**Acceptance Scenarios**:

1. **Given** a project with `.intent/state.json` where capture is complete and `intent.md` has all 7 sections, **When** user runs `intent check`, **Then** all checks pass and exit code is 0
2. **Given** a project with `state.json` where steer is marked complete but capture is not, **When** user runs `intent check`, **Then** gate violation is reported and exit code is non-zero
3. **Given** a project with no `.intent/` directory, **When** user runs `intent check`, **Then** a clear error is reported ("No IDD project found")

---

### User Story 2 - Catch invalid intent documents (Priority: P1)

A developer has written an intent document but it's missing required sections or has too many open clarifications. Running `intent check` catches these problems before they propagate downstream.

**Why this priority**: Schema validation prevents garbage-in-garbage-out — malformed intents produce malformed architectures.

**Independent Test**: Run `intent check` against a project where capture is marked complete but `intent.md` is missing the Motivation section; verify the specific failure is reported.

**Acceptance Scenarios**:

1. **Given** capture is marked complete but `intent.md` is missing a mandatory section, **When** user runs `intent check`, **Then** the missing section is reported by name
2. **Given** capture is marked complete and `intent.md` has more than 7 success criteria, **When** user runs `intent check`, **Then** a warning is reported about scope
3. **Given** capture is marked complete and `intent.md` has more than 5 open clarifications, **When** user runs `intent check`, **Then** a warning is reported that the intent isn't ready for steering

---

### User Story 3 - Verify ADR traceability (Priority: P2)

A developer has accepted ADRs during the steer phase but forgot to add Reference fields linking them back to the intent. Running `intent check` catches this traceability gap.

**Why this priority**: Traceability is a core IDD principle — but it's less critical than basic gate enforcement.

**Independent Test**: Place an ADR without a Reference field in `.intent/adr/accepted/`; verify `intent check` reports the specific file.

**Acceptance Scenarios**:

1. **Given** an ADR in `adr/accepted/` with no Reference field, **When** user runs `intent check`, **Then** the filename and missing field are reported
2. **Given** all ADRs in `adr/accepted/` have non-empty Reference fields, **When** user runs `intent check`, **Then** ADR traceability check passes
3. **Given** no ADRs exist in `adr/accepted/`, **When** user runs `intent check`, **Then** the ADR check is skipped (not a failure)

---

### User Story 4 - Verbose output for debugging (Priority: P3)

A developer wants to understand exactly what `intent check` is evaluating. They run with `--verbose` to see the details of each check, including what was read and why it passed or failed.

**Why this priority**: Useful for debugging but not required for core functionality.

**Independent Test**: Run `intent check --verbose` and verify output includes details for each check (file paths read, values found, pass/fail reasoning).

**Acceptance Scenarios**:

1. **Given** a valid project, **When** user runs `intent check --verbose`, **Then** output includes each check name, what was evaluated, and why it passed
2. **Given** a project with failures, **When** user runs `intent check --verbose`, **Then** output includes the specific values that caused each failure

---

### Edge Cases

- What happens when `state.json` is malformed JSON? Command should report a parse error with the file path.
- What happens when `intent.md` exists but is empty? Schema validation should report all 7 sections missing.
- What happens when `adr/accepted/` contains non-markdown files? They should be skipped silently.
- What happens when `state.json` references a phase that doesn't exist? Report invalid phase name.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST read `.intent/state.json` and validate that no phase is marked complete without its predecessor also being complete
- **FR-002**: System MUST validate that `current_phase` is not set to a phase whose predecessor is incomplete
- **FR-003**: System MUST validate the intent document schema when capture is marked complete: all 7 sections present (Context, Intent, Motivation, Quality Attributes, Success Criteria, Assumptions, Clarifications)
- **FR-004**: System MUST validate that the Intent section contains a single declarative sentence (≤3 sentence boundaries)
- **FR-005**: System MUST warn when Success Criteria section has more than 7 items
- **FR-006**: System MUST warn when Clarifications section has more than 5 OPEN items
- **FR-007**: System MUST validate that every `.md` file in `.intent/adr/accepted/` has a non-empty Reference field (failure is an error, non-zero exit — traceability is a hard gate)
- **FR-008**: System MUST report each validation result with a clear pass/fail indicator and the check name
- **FR-009**: System MUST exit with code 0 when all checks pass and non-zero when any check fails
- **FR-010**: System MUST accept a `--verbose` flag that shows details of each check (values read, reasoning)
- **FR-011**: System MUST report a clear error when `.intent/` directory does not exist

### Key Entities

- **Validation Check**: A named validation with a pass/fail result, optional details, and severity (error vs warning)
- **Phase Gate**: A rule that a phase cannot be complete unless its predecessor is also complete
- **Intent Schema**: The 7-section structure required for a valid intent document

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Validation completes in under 2 seconds for projects with up to 20 ADRs
- **SC-002**: 100% of gate violations are caught (no false negatives for state inconsistency)
- **SC-003**: Users can identify and fix validation failures from the output alone without reading documentation
- **SC-004**: Zero false positives — valid projects always pass with exit code 0

## Clarifications

### Session 2026-05-20

- Q: Should ADR traceability failures (missing Reference field) be an error or warning? → A: Error (non-zero exit) — traceability is a hard gate per the constitution.

## Assumptions

- The `.intent/` directory was created by `intent init` and follows the expected structure
- `state.json` follows the schema defined in the init command (project_name, intent_id, current_phase, phases)
- ADR files use the RADE format with a clearly marked "Reference" field (line starting with `**Reference**:` or `## Reference`)
- The 7 sections of an intent document are identified by their H2 headings (`## Context`, `## Intent`, etc.)
- Warnings (>7 success criteria, >5 open clarifications) do not cause a non-zero exit code — only errors (gate violations, missing sections, ADR traceability failures) do
