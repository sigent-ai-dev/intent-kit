# Tasks: Intent Init Command

**Input**: Design documents from `specs/001-intent-init/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec. Tests deferred to issue #10.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Package configuration and module scaffolding

- [ ] T001 Update pyproject.toml to include templates as package data via force-include in `src/intent_cli/__init__.py`
- [ ] T002 [P] Create agent config module at `src/intent_cli/agents.py`
- [ ] T003 [P] Create template resolution module at `src/intent_cli/templates.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that all user stories depend on

- [ ] T004 Implement template resolution in `src/intent_cli/templates.py` — function to locate and read bundled template files using importlib.resources (or path-relative fallback for editable installs)
- [ ] T005 [P] Define agent config dictionary in `src/intent_cli/agents.py` — dataclass with name, directory, file_pattern for all 6 agents (claude, gemini, copilot, cursor, q, windsurf)
- [ ] T006 [P] Add `state.json` generation helper in `src/intent_cli/templates.py` — function that produces the initial state JSON per data-model.md schema (project_name, intent_id, current_phase null, all phases incomplete, created_at)
- [ ] T007 [P] Add `audit.md` generation helper in `src/intent_cli/templates.py` — function that produces the initial audit log with project name header and init entry

**Checkpoint**: Foundation ready — CLI command implementation can begin

---

## Phase 3: User Story 1 — Bootstrap a new IDD project (Priority: P1) MVP

**Goal**: `intent init <project>` creates complete `.intent/` directory with templates and state files

**Independent Test**: Run `intent init myproject` in a temp directory; verify all expected files and directories exist with correct content

### Implementation for User Story 1

- [ ] T008 [US1] Implement `.intent/` directory scaffolding in `src/intent_cli/__init__.py` — create `.intent/`, `.intent/adr/draft/`, `.intent/adr/accepted/`, `.intent/backlog/`
- [ ] T009 [US1] Copy intent template to `.intent/intent.md` using template resolution from T004
- [ ] T010 [US1] Copy ADR template to `.intent/adr/_template.md` using template resolution from T004
- [ ] T011 [US1] Write `.intent/state.json` using generation helper from T006
- [ ] T012 [US1] Write `.intent/audit.md` using generation helper from T007
- [ ] T013 [US1] Print success message with file list and next steps per CLI contract (rich formatted output)

**Checkpoint**: `intent init myproject` creates full `.intent/` structure. Independently testable.

---

## Phase 4: User Story 2 — Choose AI agent for command generation (Priority: P1)

**Goal**: `--ai` flag installs command files in the correct agent-specific directory

**Independent Test**: Run `intent init myproject --ai gemini`; verify 5 command files exist in `.gemini/commands/`

### Implementation for User Story 2

- [ ] T014 [US2] Implement agent directory creation and command file copying in `src/intent_cli/__init__.py` — use agents.py config to determine target path, create directory if missing, copy all 5 commands with correct filename pattern
- [ ] T015 [US2] Add `--ai` flag validation in `src/intent_cli/__init__.py` — check value against agents.py supported list, print error with valid options if unsupported

**Checkpoint**: All 6 agents produce correct command files. Independently testable.

---

## Phase 5: User Story 3 — Prevent accidental overwrite (Priority: P2)

**Goal**: Refuse to overwrite existing `.intent/` unless `--force` provided

**Independent Test**: Run `intent init` twice; second invocation fails. Run with `--force`; second invocation succeeds but agent commands preserved.

### Implementation for User Story 3

- [ ] T016 [US3] Add existence check at start of init command in `src/intent_cli/__init__.py` — if `.intent/` exists and `--force` not set, print error and exit code 1
- [ ] T017 [US3] Implement `--force` flag logic in `src/intent_cli/__init__.py` — remove `.intent/` directory only (not agent command directory), then proceed with normal scaffolding
- [ ] T018 [US3] Add `--force` option to typer command signature in `src/intent_cli/__init__.py`

**Checkpoint**: Overwrite protection works. Independently testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Error handling and package configuration

- [ ] T019 [P] Add graceful error handling for filesystem permission errors in `src/intent_cli/__init__.py`
- [ ] T020 [P] Add graceful error handling for missing template files in `src/intent_cli/templates.py`
- [ ] T021 Update `pyproject.toml` — add `[tool.hatch.build.targets.wheel.force-include]` mapping `templates/` to `intent_cli/data/templates/`
- [ ] T022 Verify `uv tool install .` works and templates are accessible from installed package

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on T001 completion
- **User Story 1 (Phase 3)**: Depends on Phase 2 (T004, T006, T007)
- **User Story 2 (Phase 4)**: Depends on Phase 2 (T004, T005)
- **User Story 3 (Phase 5)**: Depends on Phase 3 (needs working init to test overwrite)
- **Polish (Phase 6)**: Depends on Phases 3-5

### User Story Dependencies

- **User Story 1 (P1)**: Foundational only — no other story dependencies
- **User Story 2 (P1)**: Foundational only — can run in parallel with US1
- **User Story 3 (P2)**: Depends on US1 being complete (needs working init to test against)

### Parallel Opportunities

- T002 and T003 can run in parallel (different files)
- T005, T006, T007 can run in parallel (different functions, same or different files)
- T019 and T020 can run in parallel (different files)
- US1 and US2 can be implemented in parallel after Phase 2

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational helpers together:
Task: "Define agent config dictionary in src/intent_cli/agents.py"
Task: "Add state.json generation helper in src/intent_cli/templates.py"
Task: "Add audit.md generation helper in src/intent_cli/templates.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T007)
3. Complete Phase 3: User Story 1 (T008-T013)
4. **STOP and VALIDATE**: `intent init myproject` creates full structure
5. This alone is a shippable MVP

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Validate → MVP shippable
3. Add US2 → Validate → Multi-agent support
4. Add US3 → Validate → Safety net
5. Polish → Production ready

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Commit after each phase completion
- Total: 22 tasks across 6 phases
