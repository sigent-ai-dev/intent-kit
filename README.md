# Intent Kit

**Turn big ideas into right-sized, traceable deliverables.**

Intent Kit is an open-source toolkit for Intent-Driven Design (IDD) — a methodology that captures structured business intent before any specification, architecture, or implementation work begins. It fills the gap between strategy and feature-level work, handing off to whichever specification or development workflow your team uses.

---

## What is Intent-Driven Design?

Intent-Driven Design flips the relationship between ideas and implementation. Instead of starting with features and retrospectively grouping them into epics, IDD starts with the **big idea** — the business initiative that justifies a programme of work — and provides structured machinery to:

1. **Capture** the intent as a falsifiable, seven-section document
2. **Steer** high-level architectural decisions anchored to the intent
3. **Define** the system shape (Architecture or Business Design Document)
4. **Decompose** the big idea into right-sized features ready for SDD

Every downstream artefact — spec, plan, decision, task, code — traces back to the captured intent through stable identifiers.

## Why Intent Kit?

Downstream tools (Spec Kit, AI-DLC, OpenSpec, plain GitHub Issues) answer "how do we specify, plan, and implement a feature?" Intent Kit answers the prior question: **"why does this feature exist, and how do we guarantee that answer remains visible through every layer of the system?"**

Without structured intent:
- Specs validate cleanly but the shipped feature drifts from what was needed ("green gates, broken reality")
- Backlogs become feature soup — items that individually make sense but don't compose into the intended whole
- Architectural decisions exist without explaining which business need they serve
- New team members re-derive decisions because the original reasoning was never captured

## The IDD Workflow

```
Big Idea → Intent → Steer → Define → Decompose → [your SDD workflow takes over]
```

| Phase | Command | Output |
|-------|---------|--------|
| 1. Capture | `/intent.capture` | `intent.md` (7 sections) |
| 2. Steer | `/intent.steer` | ADRs + `steering.md` |
| 3. Define | `/intent.define` | `architecture.md` or `business-design.md` |
| 4. Decompose | `/intent.decompose` | Right-sized features ready for your downstream workflow |

Each phase is **gated** (next phase refuses to proceed until current validates), **sequential** (no skipping), and **idempotent** (safe to re-run).

## Get Started

### 1. Install Intent CLI

```bash
uv tool install intent-cli --from git+https://github.com/sigent-ai-dev/intent-kit.git
```

Then use:

```bash
intent init <PROJECT_NAME>
intent check
```

### 2. Capture intent

Launch your AI assistant in the project directory. The `/intent.*` commands are available.

```
/intent.capture We need to modernise our legacy portfolio construction system
```

The command uses **propose-and-steer** elicitation — it interprets your input and lets you correct:

```
AI: Here's my read of what you're describing:

    The big idea: Replace a fragile Excel-based portfolio construction
    workbook with a maintainable web application that preserves the
    analysts' existing workflow while enabling collaboration and auditability.

    What I think is driving this: The 60MB workbook is a single point of
    failure — if it corrupts or the analyst who maintains it leaves,
    the team loses a critical capability.

    Success would look like:
    - Analysts can construct portfolios through a web interface
    - Multiple analysts can work simultaneously
    - Full audit trail of portfolio changes

    Am I reading this right, or should I adjust my understanding?

User: Right direction but the main driver is actually regulatory —
      we've been told the Excel approach won't pass the next audit.

AI: Got it — compliance is the driver, not just operational risk.
    That changes the quality attributes significantly. Let me draft
    the full intent with audit/compliance as the primary motivation...
```

If your input is detailed enough, the command skips straight to drafting — no interaction needed.

### 3. Steer architectural decisions

```
/intent.steer
```

Produces ADRs (Architectural Decision Records) anchored to the intent's quality attributes and success criteria.

### 4. Define the design

```
/intent.define
```

Produces either an Architecture Design Document or Business Design Document depending on the nature of the intent.

### 5. Decompose into features

```
/intent.decompose
```

Breaks the big idea into right-sized features formatted for your configured downstream workflow (Spec Kit, AI-DLC, GitHub Issues, or plain markdown).

## Supported AI Agents

| Agent | Directory | Status |
|-------|-----------|--------|
| Claude Code | `.claude/commands/` | Full |
| Gemini CLI | `.gemini/commands/` | Full |
| GitHub Copilot | `.github/agents/` | Full |
| Cursor | `.cursor/commands/` | Full |
| Amazon Q Developer | `.amazonq/prompts/` | Full |
| Windsurf | `.windsurf/workflows/` | Full |

## Project Structure (bootstrapped)

```
your-project/
├── .intent/
│   ├── intent.md                 # Phase 1 output
│   ├── steering.md               # Phase 2 output
│   ├── architecture.md           # Phase 3 output (technical)
│   ├── business-design.md        # Phase 3 output (business)
│   ├── backlog/                  # Phase 4 output
│   │   ├── features.md           # Decomposed feature list
│   │   └── dependency-map.md     # Feature dependency graph
│   ├── adr/
│   │   ├── draft/                # Steering ADRs in progress
│   │   ├── accepted/             # Reviewed and accepted
│   │   └── _template.md          # ADR RADE template
│   ├── audit.md                  # Append-only decision log
│   └── state.json                # Phase state machine
├── memory/
│   └── constitution.md           # Project principles
├── specs/                        # Downstream feature directories land here
│   └── ...
└── doc/
    └── design/                   # Design documents
```

## Core Concepts

### Intent is a Big Idea

Intent operates at the level of business initiative, not user story. "Migrate our portfolio construction system to a modern stack" is an intent. "Add a button to export results" is a feature. IDD captures the big idea first, then decomposes it into features.

### The Seven Sections

Every intent document captures:

1. **Context** — the world the project lives in
2. **Intent** — the big idea in a single declarative sentence
3. **Motivation** — why now, cost of inaction
4. **Quality Attributes** — NFRs that shape architecture
5. **Success Criteria** — observable outcomes that prove the intent satisfied
6. **Assumptions** — explicit beliefs with confidence levels
7. **Clarifications** — open questions that block downstream work

### Right-Sized Decomposition

The decompose phase breaks the big idea into features that are:
- Small enough to deliver in ≤ 2 weeks
- Large enough to be independently meaningful
- Traceable to specific success criteria
- Independently testable
- Dependency-aware

### Traceability Chain

```
INT-001 → SC-001 → US-001 → FR-001 → DEC-001 → T-001
(intent)  (success) (story) (requirement) (decision) (task)
```

Every identifier at level N references at least one at level N-1.

## Downstream Integrations

Intent Kit is workflow-agnostic. The decompose phase produces feature descriptions formatted for your chosen downstream tool:

| Adapter | Output | Downstream Tool |
|---------|--------|-----------------|
| `speckit` | `speckit-ready.md` | [Spec Kit](https://github.com/github/spec-kit) — Spec-Driven Development |
| `aidlc` | `aidlc-ready.md` | [AI-DLC](https://github.com/awslabs/aidlc-workflows) — AI Development Lifecycle |
| `github-issues` | `issues-ready.md` | GitHub Issues — lightweight backlog |
| `plain` | `features-ready.md` | Plain markdown — no downstream tool |

Configure at init time:

```bash
intent init my-project --downstream speckit      # default
intent init my-project --downstream aidlc
intent init my-project --downstream github-issues
intent init my-project --downstream plain
```

```
Intent Kit                           Your SDD Workflow
─────────                           ─────────────────
/intent.capture                     
/intent.steer                       
/intent.define                      
/intent.decompose ──────────────▶   Spec Kit, AI-DLC, OpenSpec, Issues, etc.
```

Each decomposed feature carries:
- Intent reference (INT-001)
- Success criteria it advances (SC-002, SC-003)
- Architectural constraints from steering
- Acceptance criteria seed

## Examples

See [`examples/`](./examples/) for full worked examples:

- **[Portfolio System](./examples/portfolio-system/)** — Compliance-driven modernisation, shows full 4-phase workflow with real interactions
- **[Developer Platform](./examples/developer-platform/)** — Vague input ("internal developer platform"), shows how propose-and-steer draws out the real intent through correction

## Documentation

- [Installation Guide](./docs/installation.md)
- [Quick Start](./docs/quickstart.md)
- [IDD Methodology](./docs/methodology.md)
- [Template Reference](./docs/templates.md)
- [Downstream Integrations](./docs/downstream-integrations.md)
- [IDD Methodology (source)](./doc/design/intent-driven-design-generic.md)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
