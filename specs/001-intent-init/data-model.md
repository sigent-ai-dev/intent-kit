# Data Model: Intent Init Command

## Entities

### ProjectState (`state.json`)

| Field | Type | Description |
|-------|------|-------------|
| project_name | string | Display name from init argument |
| intent_id | string | Stable identifier (always "INT-001" for first intent) |
| current_phase | string \| null | Active phase name or null if not started |
| phases | object | Map of phase name → phase state |
| created_at | string (ISO 8601) | Timestamp of project initialisation |

### PhaseState (nested in `phases`)

| Field | Type | Description |
|-------|------|-------------|
| complete | boolean | Whether this phase has been validated and marked done |
| completed_at | string (ISO 8601) \| undefined | Timestamp when phase was completed |

### AgentConfig (in-memory, not persisted)

| Field | Type | Description |
|-------|------|-------------|
| name | string | Agent identifier (claude, gemini, copilot, cursor, q, windsurf) |
| directory | string | Relative path to command directory |
| file_pattern | string | Filename format for commands (e.g., `intent.{command}.md`) |

## Agent Configuration Table

| Agent | Directory | File Pattern |
|-------|-----------|--------------|
| claude | `.claude/commands/` | `intent.{command}.md` |
| gemini | `.gemini/commands/` | `intent.{command}.md` |
| copilot | `.github/agents/` | `intent-{command}.md` |
| cursor | `.cursor/commands/` | `intent.{command}.md` |
| q | `.amazonq/prompts/` | `intent-{command}.md` |
| windsurf | `.windsurf/workflows/` | `intent-{command}.md` |

## State Transitions

```
null → capture → steer → define → decompose
```

- `current_phase` starts as `null` (init creates state but doesn't begin a phase)
- `/intent.capture` sets `current_phase` to "capture"
- Each phase can only advance if predecessor's `complete` is true
- State transitions are handled by downstream commands, not by init

## File Tree Created by Init

```
.intent/
├── intent.md          # Copy of intent-template.md
├── state.json         # ProjectState JSON
├── audit.md           # Audit log with init entry
├── adr/
│   ├── draft/         # Empty directory for in-progress ADRs
│   ├── accepted/      # Empty directory for reviewed ADRs
│   └── _template.md   # Copy of adr/_template.md
└── backlog/           # Empty directory for decomposed features
```
