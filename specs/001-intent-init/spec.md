# Feature Specification: Intent Init Command

**Feature Branch**: `1-intent-init`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Implement the `intent init` command that scaffolds the `.intent/` directory structure, copies templates, creates state.json, and generates agent command files.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Bootstrap a new IDD project (Priority: P1)

A developer starting a new initiative wants to set up the Intent-Driven Design structure in their project so they can begin capturing business intent. They run `intent init <project>` and get a ready-to-use `.intent/` directory with all templates and agent commands in place.

**Why this priority**: This is the core value of the command — without it, no IDD workflow can begin.

**Independent Test**: Can be fully tested by running `intent init myproject` in an empty directory and verifying the complete directory tree is created with all expected files.

**Acceptance Scenarios**:

1. **Given** a project directory without `.intent/`, **When** user runs `intent init myproject`, **Then** `.intent/` is created with subdirectories `adr/draft/`, `adr/accepted/`, `backlog/`, and files `intent.md`, `adr/_template.md`, `state.json`, `audit.md`
2. **Given** a project directory without `.intent/`, **When** user runs `intent init myproject`, **Then** `state.json` contains all phases marked incomplete with `current_phase: null`
3. **Given** a project directory without `.intent/`, **When** user runs `intent init myproject`, **Then** a success message is printed with guidance on next steps (run `/intent.capture`)

---

### User Story 2 - Choose AI agent for command generation (Priority: P1)

A developer using Gemini CLI (or any non-default agent) wants their IDD commands installed in the correct agent directory so they can immediately invoke `/intent.capture` from their preferred tool.

**Why this priority**: Multi-agent support is a core differentiator of Intent Kit — users must be able to choose their agent at init time.

**Independent Test**: Can be tested by running `intent init myproject --ai gemini` and verifying files appear in `.gemini/commands/` rather than `.claude/commands/`.

**Acceptance Scenarios**:

1. **Given** no `--ai` flag provided, **When** user runs `intent init myproject`, **Then** command files are placed in `.claude/commands/` (default agent)
2. **Given** `--ai gemini` flag, **When** user runs `intent init myproject --ai gemini`, **Then** command files are placed in `.gemini/commands/`
3. **Given** any supported `--ai` value, **When** init completes, **Then** all 5 command files (capture, steer, define, decompose, clarify) are present in the target agent directory

---

### User Story 3 - Prevent accidental overwrite (Priority: P2)

A developer who already has an IDD project accidentally runs `intent init` again. The command should warn them and refuse to overwrite existing work unless they explicitly opt in.

**Why this priority**: Data safety — protecting existing intent documents from accidental destruction.

**Independent Test**: Can be tested by running `intent init` twice in the same directory and verifying the second invocation fails with a clear message.

**Acceptance Scenarios**:

1. **Given** `.intent/` already exists, **When** user runs `intent init myproject`, **Then** command exits with an error message explaining the directory already exists
2. **Given** `.intent/` already exists, **When** user runs `intent init myproject --force`, **Then** existing `.intent/` is replaced with fresh scaffolding but agent command files are preserved
3. **Given** `.intent/` already exists and `--force` is NOT provided, **Then** no files are modified or deleted

---

### Edge Cases

- What happens when the user provides an unsupported `--ai` value? Command should list supported agents and exit with an error.
- What happens when the filesystem is read-only? Command should report a clear permission error.
- What happens when template files are missing from the installed package? Command should report which templates are missing rather than crashing.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create the `.intent/` directory with subdirectories `adr/draft/`, `adr/accepted/`, and `backlog/`
- **FR-002**: System MUST copy `intent-template.md` to `.intent/intent.md` as an empty template ready for `/intent.capture`
- **FR-003**: System MUST copy `adr/_template.md` to `.intent/adr/_template.md`
- **FR-004**: System MUST create `.intent/state.json` with initial state: all phases incomplete, `current_phase` set to null, and `project_name` set to the provided argument
- **FR-005**: System MUST create `.intent/audit.md` with a header section that includes the project name
- **FR-006**: System MUST accept an `--ai` flag with supported values (claude, gemini, copilot, cursor, q, windsurf) defaulting to claude
- **FR-007**: System MUST copy all 5 command templates (capture, steer, define, decompose, clarify) from `templates/commands/` to the agent-specific directory
- **FR-008**: System MUST print a success message with next steps upon completion
- **FR-009**: System MUST refuse to proceed if `.intent/` already exists, unless `--force` flag is provided. `--force` only replaces the `.intent/` directory; agent command files are left untouched unless missing
- **FR-010**: System MUST display a clear error when an unsupported `--ai` value is provided, listing valid options

### Key Entities

- **Project State** (`state.json`): Tracks phase progression — which phases are complete, current active phase, intent identifier, project name, timestamps
- **Audit Log** (`audit.md`): Append-only record of all IDD workflow actions — captures who did what and when
- **Agent Config**: Mapping of agent names to their target directory paths and command file naming conventions

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can bootstrap a new IDD project in under 5 seconds with a single command
- **SC-002**: 100% of generated files match the expected template structure (no missing sections, no placeholder corruption)
- **SC-003**: Users of all 6 supported AI agents can invoke `/intent.capture` immediately after running init without additional setup
- **SC-004**: Accidental overwrites are prevented in 100% of cases where `.intent/` already exists and `--force` is not provided

## Clarifications

### Session 2026-05-20

- Q: Should `--force` also overwrite agent command files that the user may have customized? → A: No — `--force` only replaces `.intent/`, leaves agent commands untouched unless missing.
- Q: Should `project_name` be persisted or is it purely cosmetic? → A: Store in `state.json` and use in audit log entries.

## Assumptions

- The CLI is installed via `uv tool install` and available on PATH as `intent`
- Template files are bundled with the installed package and accessible at runtime
- The target project directory is writable by the current user
- Only one AI agent is configured per init invocation (multi-agent simultaneous install is out of scope for this feature)
- The `project_name` argument is used for display/metadata purposes, not for creating a new directory (init operates in the current working directory)
