# Data Model: Intent Check Command

## Entities

### CheckResult

| Field | Type | Description |
|-------|------|-------------|
| name | string | Human-readable check name (e.g., "Phase gate: capture → steer") |
| passed | boolean | Whether the check passed |
| severity | "error" \| "warning" | Determines exit code impact |
| message | string | One-line summary shown in normal output |
| details | string \| None | Extended info shown only in verbose mode |

### ValidationReport

| Field | Type | Description |
|-------|------|-------------|
| results | list[CheckResult] | All check results in execution order |
| has_errors | boolean | True if any result has severity=error and passed=false |
| has_warnings | boolean | True if any result has severity=warning and passed=false |

## Check Registry

| Check Name | Trigger | Severity | Source |
|------------|---------|----------|--------|
| Project exists | Always | error | `.intent/` directory |
| State file valid | Always | error | `.intent/state.json` parseable |
| Phase gate consistency | Always | error | No phase complete without predecessor |
| Current phase valid | Always | error | current_phase not past incomplete predecessor |
| Intent sections present | capture complete | error | 7 H2 headings in `intent.md` |
| Intent is single sentence | capture complete | warning | ≤3 sentence boundaries in Intent section |
| Success criteria count | capture complete | warning | ≤7 items in Success Criteria section |
| Open clarifications count | capture complete | warning | ≤5 OPEN items in Clarifications section |
| ADR traceability | adr/accepted/ non-empty | error | Reference field in each ADR |

## Phase Order (for gate validation)

```
capture → steer → define → decompose
```

Gate rule: `phases[N].complete == true` requires `phases[N-1].complete == true`
