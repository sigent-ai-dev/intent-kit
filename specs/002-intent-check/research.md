# Research: Intent Check Command

## Decision 1: Validation result data structure

**Decision**: Each check returns a `CheckResult` dataclass with `name`, `passed`, `severity` (error/warning), `message`, and optional `details` (for verbose mode).

**Rationale**: Uniform structure makes it easy to aggregate results, filter by severity, and format output consistently. The `details` field is only populated when `--verbose` is set.

**Alternatives considered**:
- Raising exceptions for failures — harder to collect all failures before reporting
- Returning dicts — loses type safety and IDE support

## Decision 2: Intent document section detection

**Decision**: Parse `intent.md` by scanning for H2 headings (`## Context`, `## Intent`, etc.). The 7 required sections are matched case-insensitively.

**Rationale**: Simple regex/line scan is fast and sufficient. The template defines exact heading names, so partial matching isn't needed.

**Required headings**: Context, Intent, Motivation, Quality Attributes, Success Criteria, Assumptions, Clarifications

## Decision 3: ADR Reference field detection

**Decision**: Search each ADR for a line matching `**Reference**:` (bold markdown) or `## Reference` (H2 heading). The value after the colon/heading must be non-empty (not just whitespace).

**Rationale**: The ADR template uses RADE format. The Reference field is part of that format. Both inline bold and heading styles are common in markdown ADR templates.

## Decision 4: Sentence boundary detection for Intent section

**Decision**: Count sentence boundaries using a simple heuristic: split on `. ` (period + space), `! `, `? ` — count must be ≤3 boundaries (meaning ≤3 sentences). Ignore periods in abbreviations or numbers by requiring a capital letter or end-of-string after the boundary.

**Rationale**: A full NLP sentence parser would be overkill. The intent section is human-written and expected to be concise. A simple heuristic catches the common case (multi-paragraph intents) without false-flagging abbreviations.

## Decision 5: Exit code semantics

**Decision**:
- Exit 0: All checks pass (warnings are allowed)
- Exit 1: Any error-severity check fails

**Error-severity checks**: gate violations (FR-001, FR-002), missing intent sections (FR-003), ADR traceability (FR-007), missing `.intent/` (FR-011)

**Warning-severity checks**: >7 success criteria (FR-005), >5 open clarifications (FR-006), intent not a single sentence (FR-004 — advisory, since "≤3 sentence boundaries" allows some flexibility)
