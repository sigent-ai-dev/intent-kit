"""Template resolution and generation for Intent Kit."""

import json
from datetime import datetime, timezone
from pathlib import Path

_TEMPLATES_DIR: Path | None = None


def _find_templates_dir() -> Path:
    """Locate the templates directory, checking package data first then repo root."""
    global _TEMPLATES_DIR
    if _TEMPLATES_DIR is not None:
        return _TEMPLATES_DIR

    # Try package data location (installed via wheel with force-include)
    pkg_data = Path(__file__).parent / "data" / "templates"
    if pkg_data.is_dir():
        _TEMPLATES_DIR = pkg_data
        return _TEMPLATES_DIR

    # Fallback: repo root (editable install or development)
    repo_root = Path(__file__).parent.parent.parent
    repo_templates = repo_root / "templates"
    if repo_templates.is_dir():
        _TEMPLATES_DIR = repo_templates
        return _TEMPLATES_DIR

    raise FileNotFoundError(
        "Cannot locate templates directory. "
        "Expected at: {pkg_data} or {repo_templates}"
    )


def get_template(relative_path: str) -> str:
    """Read a template file by its relative path within the templates directory."""
    templates_dir = _find_templates_dir()
    template_file = templates_dir / relative_path
    if not template_file.is_file():
        raise FileNotFoundError(f"Template not found: {relative_path}")
    return template_file.read_text(encoding="utf-8")


def get_template_path(relative_path: str) -> Path:
    """Get the absolute path to a template file."""
    templates_dir = _find_templates_dir()
    template_file = templates_dir / relative_path
    if not template_file.is_file():
        raise FileNotFoundError(f"Template not found: {relative_path}")
    return template_file


def generate_state_json(project_name: str) -> str:
    """Generate initial state.json content."""
    state = {
        "project_name": project_name,
        "intent_id": "INT-001",
        "current_phase": None,
        "phases": {
            "capture": {"complete": False},
            "steer": {"complete": False},
            "define": {"complete": False},
            "decompose": {"complete": False},
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(state, indent=2) + "\n"


def generate_audit_md(project_name: str, agent: str) -> str:
    """Generate initial audit.md content with init entry."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""# Audit Log — {project_name}

## {timestamp} — Project initialised

**Actor**: user
**Phase**: init
**Outcome**: complete
**Details**: IDD structure created with {agent} agent commands
"""
