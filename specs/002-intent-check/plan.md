# Implementation Plan: Intent Check Command

**Branch**: `2-intent-check` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-intent-check/spec.md`

## Summary

Implement the `intent check` CLI command that validates an IDD project's state: phase gate consistency, intent document schema (7 sections), and ADR traceability. Reports pass/fail per check with optional verbose output, exits non-zero on errors.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: typer, rich (existing)

**Storage**: Reads `.intent/state.json`, `.intent/intent.md`, `.intent/adr/accepted/*.md`

**Testing**: pytest with tmp_path fixtures

**Target Platform**: Cross-platform CLI

**Project Type**: CLI tool (extending existing `intent` command)

**Performance Goals**: <2 seconds for projects with up to 20 ADRs

**Constraints**: Read-only operation — never modifies project files

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| Intent before implementation | PASS | Spec complete with clarification |
| Big ideas decompose into features | PASS | Single feature from IDD initiative |
| Every artefact traces upstream | PASS | Traced to INT-001 via issue #2 |
| Phase gates are hard | PASS | This command is the gate enforcer |
| Propose-then-confirm | PASS | Spec reviewed and clarified |
| Audit everything | PASS | Check is read-only; no audit needed |

## Project Structure

### Source Code

```text
src/intent_cli/
├── __init__.py          # CLI entry point (modify — wire up check)
├── agents.py            # (existing, unchanged)
├── templates.py         # (existing, unchanged)
└── checks.py            # Validation logic (new)

tests/
├── test_init.py         # (existing)
└── test_check.py        # Check command tests (new)
```

**Structure Decision**: All validation logic in a single `checks.py` module. The check command is a pure reader — it loads files and returns results. No state mutation.
