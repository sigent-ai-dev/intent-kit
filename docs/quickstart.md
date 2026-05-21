# Quick Start

## 1. Initialise a Project

```bash
intent init my-project
```

This creates:

```
.intent/
├── intent.md          # Phase 1 output (template)
├── state.json         # Phase state machine
├── audit.md           # Append-only decision log
├── adr/
│   ├── draft/
│   ├── accepted/
│   └── _template.md
└── backlog/

.claude/commands/      # AI agent commands (default: claude)
├── intent.capture.md
├── intent.steer.md
├── intent.define.md
├── intent.decompose.md
└── intent.clarify.md
```

## 2. Choose Your Agent

```bash
intent init my-project --ai gemini    # Gemini CLI
intent init my-project --ai copilot   # GitHub Copilot
intent init my-project --ai cursor    # Cursor
intent init my-project --ai q         # Amazon Q Developer
intent init my-project --ai windsurf  # Windsurf
```

## 3. Capture Intent

Open your AI agent in the project directory and run:

```
/intent.capture We need to modernise our legacy portfolio construction system —
it's a 60MB Excel workbook that 3 analysts rely on daily, and we need it in a
maintainable stack behind a web interface
```

## 4. Steer Architecture

```
/intent.steer
```

## 5. Define the Design

```
/intent.define
```

## 6. Decompose into Features

```
/intent.decompose
```

Each decomposed feature is ready for Spec Kit's `/speckit.specify`.

## 7. Validate State

At any point, check your project is valid:

```bash
intent check           # Quick pass/fail
intent check --verbose # Detailed output
intent check --fix     # Auto-correct simple issues
```

## Next Steps

- Read the [IDD Methodology](methodology.md) for the full framework
- See [Spec Kit Integration](speckit-integration.md) for the handoff workflow
- Check [Templates](templates.md) for customisation options
