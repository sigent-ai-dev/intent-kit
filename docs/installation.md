# Installation

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

## Install from GitHub

```bash
uv tool install intent-cli --from git+https://github.com/sigent-ai-dev/intent-kit.git
```

## Install from PyPI

```bash
uv tool install intent-cli
```

## Verify Installation

```bash
intent --help
```

You should see:

```
Usage: intent [OPTIONS] COMMAND [ARGS]...

Intent Kit CLI — bootstrap projects for Intent-Driven Design.

Commands:
  init   Initialise a new project with IDD structure and templates.
  check  Validate the current project's IDD state (phase gates, traceability).
```

## Development Install

For contributing to Intent Kit:

```bash
git clone https://github.com/sigent-ai-dev/intent-kit.git
cd intent-kit
uv sync --dev
uv run intent --help
```

## Uninstall

```bash
uv tool uninstall intent-cli
```
