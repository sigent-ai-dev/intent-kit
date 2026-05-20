# Implementation Plan: Intent Init Command

**Branch**: `1-intent-init` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-intent-init/spec.md`

## Summary

Implement the `intent init <project>` CLI command that scaffolds a `.intent/` directory with templates, state tracking, and AI agent command files. The command uses Typer for CLI framework, copies bundled template files using `importlib.resources`, and supports 6 AI agents via a config dictionary.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: typer, rich (already in pyproject.toml)

**Storage**: Filesystem only (JSON for state, Markdown for templates)

**Testing**: pytest with tmp_path fixtures

**Target Platform**: Cross-platform (macOS, Linux, Windows) via `uv tool install`

**Project Type**: CLI tool

**Performance Goals**: Init completes in <5 seconds (filesystem I/O only)

**Constraints**: Must work without network access; templates bundled in package

**Scale/Scope**: Single user, single project directory at a time

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Intent before implementation | PASS | Spec complete, clarifications resolved |
| Big ideas decompose into features | PASS | This is a single decomposed feature from the IDD initiative |
| Every artefact traces upstream | PASS | Traced to INT-001 via issue #1 |
| Phase gates are hard | PASS | Init creates state.json that enforces gates downstream |
| Propose-then-confirm | PASS | Spec reviewed, clarifications answered |
| Audit everything | PASS | Init creates audit.md and writes first entry |

No violations. Proceeding.

## Project Structure

### Documentation (this feature)

```text
specs/001-intent-init/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI contract)
└── tasks.md             # Phase 2 output (via /speckit-tasks)
```

### Source Code (repository root)

```text
src/intent_cli/
├── __init__.py          # CLI entry point (existing — modify)
├── agents.py            # Agent config dictionary (new)
└── templates.py         # Template resolution and copying (new)

templates/
├── commands/            # 5 command templates (existing)
├── intent-template.md   # Intent document template (existing)
├── architecture-template.md  # (existing)
├── business-design-template.md  # (existing)
└── adr/
    └── _template.md     # ADR template (existing)

tests/
└── test_init.py         # Unit tests for init command (new)
```

**Structure Decision**: Single-package CLI. All logic lives in `src/intent_cli/`. No separate `models/` or `services/` needed — this is a thin scaffolding tool with two modules beyond the entry point.
