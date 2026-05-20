# Contributing to Intent Kit

Thank you for your interest in contributing to Intent Kit.

## Development Setup

```bash
git clone https://github.com/superhighway-factory/intent-kit.git
cd intent-kit
uv venv
uv pip install -e ".[dev]"
```

## Project Structure

```
intent-kit/
├── src/intent_cli/          # CLI source (Python, typer-based)
├── templates/
│   ├── commands/            # AI agent command definitions
│   │   ├── capture.md       # /intent.capture command
│   │   ├── steer.md         # /intent.steer command
│   │   ├── define.md        # /intent.define command
│   │   ├── decompose.md     # /intent.decompose command
│   │   └── clarify.md       # /intent.clarify command
│   ├── adr/                 # ADR templates
│   ├── intent-template.md   # The 7-section intent template
│   ├── architecture-template.md  # 12-section architecture design
│   └── business-design-template.md  # 12-section business design
├── scripts/                 # Shell scripts for automation
├── docs/                    # Documentation site source
├── doc/design/              # Design documents (IDD methodology)
├── memory/                  # Project constitution
└── tests/                   # Test suite
```

## How to Contribute

### Adding a New AI Agent

Follow the same pattern as Spec Kit — add agent config to `src/intent_cli/__init__.py` and ensure the commands directory is generated on `intent init`.

### Improving Templates

Templates are the heart of Intent Kit. To improve one:
1. Edit the template in `templates/`
2. Test with a real project (run the workflow end-to-end)
3. Ensure the seven sections still validate correctly

### Adding Commands

New commands go in `templates/commands/`. Each must:
- Have a clear `description` in frontmatter
- Define `handoffs` to the logical next step
- Include a Gate Check section (what must exist before this runs)
- Include validation of outputs before marking complete

## Code of Conduct

Be kind, constructive, and focused on making the methodology better.

## Spec Kit Integration

Intent Kit is designed to hand off to Spec Kit. When testing the full flow, ensure that `/intent.decompose` produces output that `/speckit.specify` can consume without modification.
