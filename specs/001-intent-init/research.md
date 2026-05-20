# Research: Intent Init Command

## Decision 1: Template bundling strategy

**Decision**: Use `importlib.resources` to access templates bundled with the installed package.

**Rationale**: Templates must be accessible after `uv tool install` without knowing the install location. `importlib.resources` (Python 3.9+) provides a clean API for accessing package data files regardless of installation method (wheel, editable, system).

**Alternatives considered**:
- `pkg_resources` — deprecated, slower, setuptools-only
- `__file__`-relative paths — breaks in zip-imported packages and some editable installs
- Vendoring templates as string constants — unmaintainable, loses markdown formatting

**Implementation note**: Templates directory must be included in the wheel via `pyproject.toml` `[tool.hatch.build.targets.wheel]` configuration. Currently only `src/intent_cli` is included — need to add `templates/` as package data or use a `data` directory inside the package.

## Decision 2: Package data layout

**Decision**: Move templates into `src/intent_cli/data/templates/` so they're automatically included in the wheel as package data.

**Rationale**: Hatchling (the build backend) includes everything under `packages` paths. Putting templates inside the package means no extra build config. The top-level `templates/` stays as the source-of-truth for development; a build step or the `include` config copies them.

**Alternative approach**: Use `[tool.hatch.build.targets.wheel.force-include]` to map `templates/ → intent_cli/data/templates/` in the built wheel. This keeps the repo layout clean (templates at top level) while still bundling them.

**Final choice**: Use `force-include` in pyproject.toml. Keeps source layout unchanged.

## Decision 3: Agent directory creation behavior

**Decision**: Create the agent command directory only if it doesn't exist. Write command files into it. Never delete existing files in the agent directory (even with `--force`).

**Rationale**: Per clarification, `--force` only replaces `.intent/`. Agent directories may contain user customizations or other tools' files. Safe to add but never safe to remove.

## Decision 4: state.json schema

**Decision**: Minimal initial schema:

```json
{
  "project_name": "<from argument>",
  "intent_id": "INT-001",
  "current_phase": null,
  "phases": {
    "capture": { "complete": false },
    "steer": { "complete": false },
    "define": { "complete": false },
    "decompose": { "complete": false }
  },
  "created_at": "<ISO 8601 timestamp>"
}
```

**Rationale**: Minimal but sufficient for gate enforcement. `current_phase` is null until `/intent.capture` runs. Each phase has a `complete` boolean; downstream commands check predecessors before allowing advancement.

## Decision 5: audit.md initial content

**Decision**: Header with project name + first entry recording init:

```markdown
# Audit Log — <project_name>

## <ISO 8601> — Project initialised

**Actor**: user
**Phase**: init
**Outcome**: complete
**Details**: IDD structure created with <agent> agent commands
```

**Rationale**: Audit log starts immediately with a useful entry. The format matches what `/intent.capture` will append later (per the capture command template).
