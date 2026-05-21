# Template Reference

Intent Kit ships with templates for all phases of IDD. These are the source of truth — command files are derived from them.

## Intent Template (`intent-template.md`)

The seven-section structure for capturing business intent:

| Section | Purpose | Rules |
|---------|---------|-------|
| Context | Environmental facts, constraints | No solution ideas |
| Intent | The big idea | Single declarative sentence |
| Motivation | Why now | Cost of inaction |
| Quality Attributes | NFRs | Tagged QA-NNN |
| Success Criteria | Observable outcomes | Tagged SC-NNN, max 7 |
| Assumptions | Beliefs not yet verified | Confidence: high/medium/low |
| Clarifications | Open questions | Tagged CLR-NNN, max 5 OPEN |

## ADR Template (`adr/_template.md`)

RADE format (Reference, Action, Decision, Evidence):

- **Reference**: Links to intent (mandatory, validated by `intent check`)
- **Action**: What was decided
- **Decision**: The chosen approach
- **Evidence**: Why this choice over alternatives

## Architecture Template (`architecture-template.md`)

12-section technical design document covering system shape, components, interfaces, data flows, deployment, and operational concerns.

## Business Design Template (`business-design-template.md`)

12-section business design document covering process shape, stakeholders, workflows, data governance, and rollout strategy.

## Command Templates (`commands/`)

Five AI agent commands, one per IDD phase:

| Template | Phase | AI Command |
|----------|-------|------------|
| `capture.md` | 1 | `/intent.capture` |
| `steer.md` | 2 | `/intent.steer` |
| `define.md` | 3 | `/intent.define` |
| `decompose.md` | 4 | `/intent.decompose` |
| `clarify.md` | any | `/intent.clarify` |

### Format Adaptation

Templates are authored in Claude Code format (YAML frontmatter + markdown body). At install time, `intent init --ai <agent>` transforms them:

| Agent | Format |
|-------|--------|
| Claude, Gemini, Cursor | YAML frontmatter preserved |
| Copilot | Simplified frontmatter (name + description) |
| Q Developer, Windsurf | Plain markdown (frontmatter stripped, title header added) |

## Customisation

Templates live in the `templates/` directory of the installed package. To customise:

1. Fork the repository
2. Edit templates in `templates/`
3. Install from your fork: `uv tool install intent-cli --from git+https://github.com/you/intent-kit.git`

The command templates are the most common customisation target — they contain the AI instructions that drive each phase.
