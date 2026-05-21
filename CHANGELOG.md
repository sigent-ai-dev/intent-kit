# Changelog

All notable changes to Intent Kit are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-20

### Added

- `intent init <project>` command — scaffolds `.intent/` directory with templates, state tracking, and AI agent command files
- `intent check` command — validates phase gates, intent document schema, ADR traceability, decomposition quality, and speckit-ready output
- Multi-agent support: Claude, Gemini, Copilot, Cursor, Q Developer, Windsurf
- Per-agent template format adaptation (YAML frontmatter for Claude/Gemini/Cursor, simplified for Copilot, plain markdown for Q/Windsurf)
- `--force` flag for safe reinitialisation (preserves agent commands)
- `--fix` flag for auto-correcting simple state.json issues
- `--verbose` flag for detailed check output
- Cross-tool traceability validation (Intent Kit → Spec Kit)
- Shell scripts for CI automation (`scripts/check.sh`, `scripts/init.sh` + PowerShell equivalents)
- GitHub Actions CI (lint + test + build on Python 3.11/3.12)
- IDD methodology templates (capture, steer, define, decompose, clarify)
- ADR template (RADE format with mandatory Reference field)
- Architecture and business design document templates
- Spec Kit integration guide (`docs/speckit-integration.md`)
- 30 unit tests covering all CLI commands and validation logic
