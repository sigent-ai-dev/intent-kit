# Intent Kit

**Turn big ideas into right-sized, traceable deliverables.**

Intent Kit is an open-source toolkit for Intent-Driven Design (IDD) — a methodology that captures structured business intent before any specification, architecture, or implementation work begins. It is the upstream companion to [Spec Kit](https://github.com/github/spec-kit), filling the gap between strategy and feature-level work.

---

## What is Intent-Driven Design?

Intent-Driven Design flips the relationship between ideas and implementation. Instead of starting with features and retrospectively grouping them into epics, IDD starts with the **big idea** — the business initiative that justifies a programme of work — and provides structured machinery to:

1. **Capture** the intent as a falsifiable, seven-section document
2. **Steer** high-level architectural decisions anchored to the intent
3. **Define** the system shape (Architecture or Business Design Document)
4. **Decompose** the big idea into right-sized features ready for SDD

Every downstream artefact — spec, plan, decision, task, code — traces back to the captured intent through stable identifiers.

## Why Intent Kit?

Spec Kit answers "how do we specify, plan, and implement a feature?" Intent Kit answers the prior question: **"why does this feature exist, and how do we guarantee that answer remains visible through every layer of the system?"**

Without structured intent:
- Specs validate cleanly but the shipped feature drifts from what was needed ("green gates, broken reality")
- Backlogs become feature soup — items that individually make sense but don't compose into the intended whole
- Architectural decisions exist without explaining which business need they serve
- New team members re-derive decisions because the original reasoning was never captured

## The IDD Workflow

```
Big Idea → Intent → Steer → Define → Decompose → [Spec Kit takes over]
```

| Phase | Command | Output |
|-------|---------|--------|
| 1. Capture | `/intent.capture` | `intent.md` (7 sections) |
| 2. Steer | `/intent.steer` | ADRs + `steering.md` |
| 3. Define | `/intent.define` | `architecture.md` or `business-design.md` |
| 4. Decompose | `/intent.decompose` | Reviewed backlog of right-sized features |

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

```bash
/intent.capture We need to modernise our legacy portfolio construction system — it's a 60MB Excel workbook that 3 analysts rely on daily, and we need it in a maintainable stack behind a web interface
```

### 3. Steer architectural decisions

```bash
/intent.steer
```

### 4. Define the design

```bash
/intent.define
```

### 5. Decompose into features

```bash
/intent.decompose
```

Each decomposed feature is ready for Spec Kit's `/speckit.specify` workflow.

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
│   └── constitution.md           # Project principles (shared with Spec Kit)
├── specs/                        # Spec Kit feature directories land here
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

## Integration with Spec Kit

Intent Kit is designed as the upstream companion to Spec Kit:

```
Intent Kit                           Spec Kit
─────────                           ────────
/intent.capture                     
/intent.steer                       
/intent.define                      
/intent.decompose ──────────────▶   /speckit.specify (per feature)
                                    /speckit.plan
                                    /speckit.tasks
                                    /speckit.implement
```

The decompose phase produces feature descriptions ready for `/speckit.specify`. Each carries:
- Intent reference (INT-001)
- Success criteria it advances (SC-002, SC-003)
- Architectural constraints from steering
- Acceptance criteria seed

## Documentation

- [IDD Methodology](./intent-driven.md) — the full methodology document
- [Installation Guide](./docs/installation.md)
- [Quick Start](./docs/quickstart.md)
- [Template Reference](./docs/templates.md)
- [Integration with Spec Kit](./docs/speckit-integration.md)
- [IDD Methodology (detailed)](./doc/design/intent-driven-design-generic.md)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
