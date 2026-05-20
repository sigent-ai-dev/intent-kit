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


def test_check_speckit_ready_valid(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = _init_project(
        tmp_path,
        phases={
            "capture": {"complete": True},
            "steer": {"complete": True},
            "define": {"complete": True},
            "decompose": {"complete": True},
        },
    )
    (intent_dir / "backlog" / "features.md").write_text(
        "### 1. Implement auth\n\n**Size**: M\n**Success criteria**: SC-001\n\n"
    )
    speckit_file = intent_dir / "backlog" / "speckit-ready.md"
    speckit_file.write_text(
        "## Ready for /speckit.specify\n\n"
        "/speckit.specify Implement auth — User login. Intent: INT-001. Advances SC-001.\n"
    )
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0
    assert "invocations found" in result.output


def test_check_speckit_ready_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = _init_project(
        tmp_path,
        phases={
            "capture": {"complete": True},
            "steer": {"complete": True},
            "define": {"complete": True},
            "decompose": {"complete": True},
        },
    )
    (intent_dir / "backlog" / "features.md").write_text(
        "### 1. Feature\n\n**Size**: M\n**Success criteria**: SC-001\n\n"
    )
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 1
    assert "speckit-ready.md not found" in result.output


def test_check_speckit_ready_missing_sc(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = _init_project(
        tmp_path,
        phases={
            "capture": {"complete": True},
            "steer": {"complete": True},
            "define": {"complete": True},
            "decompose": {"complete": True},
        },
    )
    (intent_dir / "backlog" / "features.md").write_text(
        "### 1. Implement auth\n\n**Size**: M\n**Success criteria**: SC-001\n\n"
    )
    speckit_file = intent_dir / "backlog" / "speckit-ready.md"
    speckit_file.write_text(
        "## Ready for /speckit.specify\n\n/speckit.specify Implement auth — No traceability here.\n"
    )
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0  # warning, not error
    assert "missing SC-NNN" in result.output


def test_check_speckit_skipped_when_decompose_incomplete(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _init_project(
        tmp_path,
        phases={
            "capture": {"complete": True},
            "steer": {"complete": True},
            "define": {"complete": True},
            "decompose": {"complete": False},
        },
    )
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0
    assert "speckit-ready" not in result.output


def test_check_xl_features_rejected(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = _init_project(
        tmp_path,
        phases={
            "capture": {"complete": True},
            "steer": {"complete": True},
            "define": {"complete": True},
            "decompose": {"complete": True},
        },
    )
    features_file = intent_dir / "backlog" / "features.md"
    features_file.write_text("### 1. Big feature\n\n**Size**: XL\n**Success criteria**: SC-001\n\n")
    speckit_file = intent_dir / "backlog" / "speckit-ready.md"
    speckit_file.write_text("/speckit.specify Big feature — context. Advances SC-001.\n")
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 1
    assert "XL" in result.output


def test_check_orphaned_features_warned(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = _init_project(
        tmp_path,
        phases={
            "capture": {"complete": True},
            "steer": {"complete": True},
            "define": {"complete": True},
            "decompose": {"complete": True},
        },
    )
    features_file = intent_dir / "backlog" / "features.md"
    features_file.write_text(
        "### 1. Good feature\n\n"
        "**Size**: M\n"
        "**Success criteria**: SC-001\n\n"
        "### 2. Orphan feature\n\n"
        "**Size**: S\n"
        "No SC reference here.\n\n"
    )
    speckit_file = intent_dir / "backlog" / "speckit-ready.md"
    speckit_file.write_text("/speckit.specify Good feature — context. Advances SC-001.\n")
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0  # warning not error
    assert "without SC-NNN" in result.output


def test_check_backlog_completeness(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = _init_project(
        tmp_path,
        phases={
            "capture": {"complete": True},
            "steer": {"complete": True},
            "define": {"complete": True},
            "decompose": {"complete": True},
        },
    )
    # intent.md has SC-001, features only cover SC-001 — should pass
    features_file = intent_dir / "backlog" / "features.md"
    features_file.write_text("### 1. Feature\n\n**Success criteria**: SC-001\n\n")
    speckit_file = intent_dir / "backlog" / "speckit-ready.md"
    speckit_file.write_text("/speckit.specify Feature — context. Advances SC-001.\n")
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0
    assert "success criteria covered" in result.output


def test_check_fix_adds_missing_fields(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    intent_dir = tmp_path / ".intent"
    intent_dir.mkdir()
    (intent_dir / "adr" / "draft").mkdir(parents=True)
    (intent_dir / "adr" / "accepted").mkdir(parents=True)
    (intent_dir / "backlog").mkdir()
    # Minimal state.json missing fields
    (intent_dir / "state.json").write_text(
        '{"phases": {"capture": {"complete": false}, '
        '"steer": {"complete": false}, "define": {"complete": false}, '
        '"decompose": {"complete": false}}, "current_phase": null}'
    )
    (intent_dir / "intent.md").write_text("# placeholder")

    result = runner.invoke(app, ["check", "--fix"])
    assert "FIXED" in result.output
    assert "created_at" in result.output

    import json

    state = json.loads((intent_dir / "state.json").read_text())
    assert "created_at" in state
    assert "intent_id" in state
    assert "project_name" in state
