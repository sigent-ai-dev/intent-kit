# AGENTS.md

## About Intent Kit

**Intent Kit** is a toolkit for implementing Intent-Driven Design (IDD) — a methodology that captures structured business intent before any specification or implementation work begins. It hands off to any downstream SDD workflow (Spec Kit, AI-DLC, OpenSpec, GitHub Issues, or custom).

**Intent CLI** is the command-line interface that bootstraps projects with the IDD framework. It sets up directory structures, templates, and AI agent integrations to support the four-phase intent workflow.

## Development Context

This project uses its own IDD methodology for development. Use the `/intent.*` commands for upstream design work, then hand off to your configured downstream workflow for implementation.

## Architecture

### CLI (`src/intent_cli/`)

The CLI is a Python package using `typer` + `rich`, distributed via `uv tool install`:

- `intent init <project>` — scaffolds `.intent/`, templates, agent commands
- `intent check` — validates phase state, traceability, and gate satisfaction

### Templates (`templates/`)

Templates are the core of Intent Kit. They define:

- **`intent-template.md`** — the 7-section intent document structure
- **`architecture-template.md`** — 12-section architecture design document
- **`business-design-template.md`** — 12-section business design document
- **`adr/_template.md`** — RADE-format ADR template with mandatory Reference field
- **`commands/*.md`** — AI agent command definitions (one per phase)

### Commands (`templates/commands/`)

Five commands define the IDD workflow:

| Command | Phase | Input | Output |
|---------|-------|-------|--------|
| `/intent.capture` | 1 | Big idea description | `.intent/intent.md` |
| `/intent.steer` | 2 | intent.md | ADRs + `steering.md` |
| `/intent.define` | 3 | intent + ADRs | `architecture.md` or `business-design.md` |
| `/intent.decompose` | 4 | intent + design doc | `backlog/features.md` + adapter-formatted output |
| `/intent.clarify` | any | intent.md | Resolved clarifications |

### Project State (`.intent/state.json`)

The state file tracks which phase is complete and enforces gates:

```json
{
  "current_phase": "capture | steer | define | decompose",
  "phases": {
    "capture": { "complete": true, "completed_at": "..." },
    "steer": { "complete": false },
    "define": { "complete": false },
    "decompose": { "complete": false }
  },
  "intent_id": "INT-001"
}
```

## Implementation Plan

### Phase A: Foundation (complete)

- [x] Project structure (template-driven CLI)
- [x] README with full workflow documentation
- [x] Template files for all 4 phases
- [x] Command files for all AI agents
- [x] ADR template with RADE format
- [x] Constitution / memory file
- [x] pyproject.toml with CLI entry point
- [x] CONTRIBUTING.md with development guide
- [x] CLI `init` command — scaffold `.intent/` + copy templates + generate agent commands
- [x] CLI `check` command — validate state, gates, traceability

### Phase B: CLI Implementation (complete)

- [x] Agent config dictionary for multi-agent command generation
- [x] `intent init` scaffolds all directories and agent-specific command files
- [x] `intent check` validates:
  - Phase state consistency
  - Gate satisfaction (no skipping)
  - Intent document schema (7 sections, validation rules)
  - Traceability (every ADR has a Reference field)
  - Decomposition quality (no XL features, no orphaned features)
- [x] Shell scripts for automation (bash + powershell)

### Phase C: Agent Integration (complete)

- [x] Claude Code commands (`.claude/commands/intent.*.md`)
- [x] Gemini CLI commands (`.gemini/commands/`)
- [x] GitHub Copilot agents (`.github/agents/`)
- [x] Cursor commands (`.cursor/commands/`)
- [x] Amazon Q Developer prompts (`.amazonq/prompts/`)
- [x] Windsurf workflows (`.windsurf/workflows/`)

### Phase D: Downstream Integration (complete)

- [x] `/intent.decompose` produces adapter-formatted output for any downstream workflow
- [x] Traceability identifiers flow through to downstream feature directories
- [x] `intent check` validates cross-tool traceability
- [x] Built-in adapters: speckit, aidlc, github-issues, plain
- [x] Documentation: integration guide

### Phase E: Testing & Polish (complete)

- [x] Unit tests for CLI commands (30 tests)
- [x] Integration tests (full workflow end-to-end via CI build job)
- [x] GitHub Actions CI (lint + test on Python 3.11/3.12)
- [x] Release workflow (tag-triggered: GitHub release + docs deploy)
- [x] Documentation site (MkDocs Material)

## General Practices

- Changes to `__init__.py` require a version bump in `pyproject.toml` and CHANGELOG entry.
- Templates are the source of truth — if the command file says something different from the template, the template wins.
- The methodology document (`doc/design/intent-driven-design-generic.md`) is the canonical reference for IDD concepts.
- Phase gates are non-negotiable in the implementation — the CLI and commands must enforce them.

## Key Design Decisions

1. **Workflow-agnostic** — downstream adapter pattern means any SDD framework (Spec Kit, AI-DLC, OpenSpec, plain issues) receives the same structured handoff.
2. **Templates over code** — the intelligence lives in the command markdown files (consumed by AI agents), not in Python code. The CLI is thin scaffolding.
3. **State file for gates** — `.intent/state.json` is the single source of truth for phase progression. Commands read it to enforce gates.
4. **Audit log is append-only** — `.intent/audit.md` is never rewritten, only appended.
5. **Configurable adapters** — the decompose phase produces output formatted for the configured downstream tool via `adapters.py`.
