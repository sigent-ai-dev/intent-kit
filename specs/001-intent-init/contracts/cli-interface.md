# CLI Contract: `intent init`

## Command Signature

```
intent init <PROJECT_NAME> [--ai AGENT] [--force]
```

## Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| PROJECT_NAME | string | yes | — | Display name for the project (stored in state.json) |

## Options

| Option | Type | Required | Default | Valid Values | Description |
|--------|------|----------|---------|--------------|-------------|
| --ai | string | no | claude | claude, gemini, copilot, cursor, q, windsurf | AI agent for command file generation |
| --force | flag | no | false | — | Replace existing `.intent/` (agent commands preserved) |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — project initialised |
| 1 | Error — `.intent/` exists and `--force` not provided |
| 1 | Error — unsupported `--ai` value |
| 1 | Error — filesystem permission error |
| 1 | Error — template files missing from package |

## Stdout (success)

```
Initialising IDD project: <PROJECT_NAME>
AI assistant: <AGENT>

Created:
  .intent/intent.md
  .intent/state.json
  .intent/audit.md
  .intent/adr/_template.md
  .<agent>/commands/intent.capture.md
  .<agent>/commands/intent.steer.md
  .<agent>/commands/intent.define.md
  .<agent>/commands/intent.decompose.md
  .<agent>/commands/intent.clarify.md

Next steps:
  1. Run /intent.capture with your big idea
  2. Use `intent check` to validate project state
```

## Stderr (errors)

```
Error: .intent/ already exists. Use --force to reinitialise.
```

```
Error: Unsupported AI agent 'foo'. Supported: claude, gemini, copilot, cursor, q, windsurf
```

```
Error: Cannot write to directory — permission denied.
```
