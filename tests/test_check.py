"""Tests for intent check command."""

import json

from typer.testing import CliRunner

from intent_cli import app

runner = CliRunner()


def _init_project(tmp_path, **state_overrides):
    """Helper to create a minimal valid IDD project."""
    intent_dir = tmp_path / ".intent"
    intent_dir.mkdir()
    (intent_dir / "adr" / "draft").mkdir(parents=True)
    (intent_dir / "adr" / "accepted").mkdir(parents=True)
    (intent_dir / "backlog").mkdir()

    state = {
        "project_name": "test",
        "intent_id": "INT-001",
        "current_phase": None,
        "phases": {
            "capture": {"complete": False},
            "steer": {"complete": False},
            "define": {"complete": False},
            "decompose": {"complete": False},
        },
        "created_at": "2026-01-01T00:00:00Z",
    }
    state.update(state_overrides)
    (intent_dir / "state.json").write_text(json.dumps(state))

    intent_md = """# Intent

## Context

Some context here.

## Intent

A single declarative sentence describing the big idea.

## Motivation

Why now.

## Quality Attributes

- QA-001: Performance

## Success Criteria

- SC-001: It works

## Assumptions

- Users exist

## Clarifications

- None
"""
    (intent_dir / "intent.md").write_text(intent_md)
    return intent_dir


def test_check_valid_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _init_project(tmp_path)
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0
    assert "All checks passed" in result.output


def test_check_gate_violation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _init_project(
        tmp_path,
        phases={
            "capture": {"complete": False},
            "steer": {"complete": True},
            "define": {"complete": False},
            "decompose": {"complete": False},
        },
    )
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 1
    assert "FAIL" in result.output
    assert "steer" in result.output
    assert "capture" in result.output


def test_check_missing_intent_sections(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = _init_project(
        tmp_path,
        phases={
            "capture": {"complete": True},
            "steer": {"complete": False},
            "define": {"complete": False},
            "decompose": {"complete": False},
        },
    )
    # Overwrite intent.md with missing sections
    (intent_dir / "intent.md").write_text("# Intent\n\n## Context\n\nJust context.\n")
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 1
    assert "Missing sections" in result.output


def test_check_adr_missing_reference(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = _init_project(tmp_path)
    adr_file = intent_dir / "adr" / "accepted" / "001-test.md"
    adr_file.write_text("# ADR-001\n\nSome decision without reference.\n")
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 1
    assert "Reference" in result.output
    assert "001-test.md" in result.output


def test_check_adr_with_reference_passes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = _init_project(tmp_path)
    adr_file = intent_dir / "adr" / "accepted" / "001-test.md"
    adr_file.write_text("# ADR-001\n\n**Reference**: INT-001, SC-002\n\nDecision.\n")
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0


def test_check_no_intent_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 1
    assert "does not exist" in result.output


def test_check_verbose_shows_details(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _init_project(
        tmp_path,
        phases={
            "capture": {"complete": True},
            "steer": {"complete": False},
            "define": {"complete": False},
            "decompose": {"complete": False},
        },
    )
    result = runner.invoke(app, ["check", "--verbose"])
    assert result.exit_code == 0
    assert "Found:" in result.output
