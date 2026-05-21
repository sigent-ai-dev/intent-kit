# Intent Kit Constitution

## Core Principles

### I. Templates Over Code

The intelligence of Intent Kit lives in the command markdown files (consumed by AI agents), not in Python code. The CLI is thin scaffolding — it copies templates, validates state, and reports results. When in doubt, put logic in the template instructions, not in Python.

### II. CLI Interface

The CLI follows the `typer` + `rich` pattern. Commands are nouns (`init`, `check`). Text in/out: args → stdout, errors → stderr. Exit code 0 = success, 1 = failure. Support `--verbose` for debugging. Support `--force` for safe overwrite operations.

### III. Multi-Agent Portability

Every feature must work across all 6 supported AI agents (Claude, Gemini, Copilot, Cursor, Q, Windsurf). Agent-specific format adaptation happens at copy time via `adapt_template_for_agent()` — templates are authored in Claude format (YAML frontmatter + markdown body) and transformed for other agents.

### IV. Phase Gates Are Hard (NON-NEGOTIABLE)

No phase can advance without its predecessor being complete. The check command enforces this. The state file (`state.json`) is the single source of truth. Commands read it to enforce gates. No implicit advancement, no silent completion.

### V. Traceability Chain

Every artefact traces upstream: INT-NNN → SC-NNN → Feature → Spec → Code. Identifiers are stable (never reused). The decompose phase produces identifiers that flow through to Spec Kit. `intent check` validates this chain at every level.

### VI. Simplicity & YAGNI

Start simple. No abstractions until the third use. No feature flags. No backwards-compatibility shims. If the code can be changed directly, change it. Templates are the source of truth — if a command file says something different from the template, the template wins.

## Quality Standards

- All changes pass `ruff check` and `ruff format` (line-length: 100)
- All changes pass `pytest` (currently 30+ tests)
- Templates are tested by manual invocation across agents
- CLI exit codes are tested explicitly in the test suite
- `intent check` must never produce false positives (valid projects always pass)

## Development Workflow

- Issues decomposed from AGENTS.md with acceptance criteria
- Feature branches named `<issue-number>-<short-name>`
- Spec Kit workflow used for all features: specify → clarify → plan → tasks → implement
- PRs require CI to pass (lint + test + build)
- Admin can bypass branch protection when needed

## Governance

This constitution supersedes all other practices. Changes to core principles require:
1. A new ADR documenting the change
2. Update to this file
3. Review of all affected templates and commands

**Version**: 1.0.0 | **Ratified**: 2026-05-20 | **Last Amended**: 2026-05-20
