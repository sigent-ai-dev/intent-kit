# Tasks: Intent Check Command

**Input**: Design documents from `specs/002-intent-check/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Included (extending existing test pattern from issue #1).

**Organization**: Tasks grouped by user story.

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup

- [ ] T001 Create validation module at `src/intent_cli/checks.py` with CheckResult dataclass and ValidationReport class

---

## Phase 2: Foundational

- [ ] T002 Implement phase gate validation in `src/intent_cli/checks.py` — check_phase_gates() reads state.json and validates predecessor completeness
- [ ] T003 [P] Implement intent schema validation in `src/intent_cli/checks.py` — check_intent_schema() scans intent.md for 7 required H2 headings
- [ ] T004 [P] Implement ADR traceability validation in `src/intent_cli/checks.py` — check_adr_traceability() scans accepted/ for Reference field
- [ ] T005 [P] Implement intent content checks in `src/intent_cli/checks.py` — check_intent_content() validates sentence count, SC count, clarification count

**Checkpoint**: All validation functions exist and return CheckResult lists

---

## Phase 3: User Story 1 — Validate project state (Priority: P1) MVP

- [ ] T006 [US1] Wire check command in `src/intent_cli/__init__.py` — call all validation functions, aggregate results, print summary, set exit code
- [ ] T007 [US1] Implement output formatting in `src/intent_cli/checks.py` — format_report() renders pass/fail with rich markup

**Checkpoint**: `intent check` runs and reports pass/fail

---

## Phase 4: User Story 2 — Catch invalid intent documents (Priority: P1)

- [ ] T008 [US2] Add conditional execution in check command — only run intent schema/content checks when capture phase is marked complete

**Checkpoint**: Schema checks fire only when relevant

---

## Phase 5: User Story 3 — ADR traceability (Priority: P2)

- [ ] T009 [US3] Add conditional execution — only run ADR traceability when adr/accepted/ contains .md files

**Checkpoint**: ADR check skips gracefully when no ADRs exist

---

## Phase 6: User Story 4 — Verbose output (Priority: P3)

- [ ] T010 [US4] Add `--verbose` flag to check command in `src/intent_cli/__init__.py` and pass to format_report()
- [ ] T011 [US4] Populate details field in each CheckResult when verbose is enabled

---

## Phase 7: Tests

- [ ] T012 [P] Add test for valid project passes in `tests/test_check.py`
- [ ] T013 [P] Add test for gate violation detected in `tests/test_check.py`
- [ ] T014 [P] Add test for missing intent sections in `tests/test_check.py`
- [ ] T015 [P] Add test for ADR missing Reference in `tests/test_check.py`
- [ ] T016 [P] Add test for no .intent/ directory in `tests/test_check.py`
- [ ] T017 [P] Add test for --verbose output in `tests/test_check.py`

---

## Dependencies & Execution Order

- Phase 1 → Phase 2 → Phases 3/4/5 (parallel) → Phase 6 → Phase 7
- Total: 17 tasks
- MVP: Phases 1-3 (7 tasks)
