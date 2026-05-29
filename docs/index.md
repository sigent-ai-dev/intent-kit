# Intent Kit

**Turn big ideas into right-sized, traceable deliverables.**

Intent Kit is an open-source toolkit for Intent-Driven Design (IDD) — a methodology that captures structured business intent before any specification, architecture, or implementation work begins. It hands off to any downstream SDD workflow.

## What It Does

```
Big Idea → Intent → Steer → Define → Decompose → [your SDD workflow takes over]
```

| Phase | Command | Output |
|-------|---------|--------|
| 1. Capture | `/intent.capture` | `intent.md` (7 sections) |
| 2. Steer | `/intent.steer` | ADRs + `steering.md` |
| 3. Define | `/intent.define` | `architecture.md` or `business-design.md` |
| 4. Decompose | `/intent.decompose` | Right-sized features for your downstream workflow |

## Why It Exists

Without structured intent:

- Specs validate cleanly but the shipped feature drifts from what was needed
- Backlogs become feature soup that doesn't compose into the intended whole
- Architectural decisions exist without explaining which business need they serve
- New team members re-derive decisions because the original reasoning was never captured

## Supported AI Agents

| Agent | Status |
|-------|--------|
| Claude Code | Full |
| Gemini CLI | Full |
| GitHub Copilot | Full |
| Cursor | Full |
| Amazon Q Developer | Full |
| Windsurf | Full |

## Quick Links

- [Installation](installation.md)
- [Quick Start](quickstart.md)
- [IDD Methodology](methodology.md)
- [Downstream Integrations](downstream-integrations.md)
