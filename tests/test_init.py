"""Tests for intent init command."""

import json

from typer.testing import CliRunner

from intent_cli import app

runner = CliRunner()


def test_init_creates_directory_structure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "test-project"])
    assert result.exit_code == 0

    intent_dir = tmp_path / ".intent"
    assert intent_dir.is_dir()
    assert (intent_dir / "adr" / "draft").is_dir()
    assert (intent_dir / "adr" / "accepted").is_dir()
    assert (intent_dir / "backlog").is_dir()
    assert (intent_dir / "intent.md").is_file()
    assert (intent_dir / "adr" / "_template.md").is_file()
    assert (intent_dir / "state.json").is_file()
    assert (intent_dir / "audit.md").is_file()


def test_init_state_json_schema(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner.invoke(app, ["init", "my-project"])

    state = json.loads((tmp_path / ".intent" / "state.json").read_text())
    assert state["project_name"] == "my-project"
    assert state["intent_id"] == "INT-001"
    assert state["current_phase"] is None
    assert all(not p["complete"] for p in state["phases"].values())
    assert "created_at" in state


def test_init_audit_contains_project_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner.invoke(app, ["init", "audit-test"])

    audit = (tmp_path / ".intent" / "audit.md").read_text()
    assert "audit-test" in audit
    assert "Project initialised" in audit


def test_init_default_agent_is_claude(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner.invoke(app, ["init", "test-project"])

    commands_dir = tmp_path / ".claude" / "commands"
    assert commands_dir.is_dir()
    assert (commands_dir / "intent.capture.md").is_file()
    assert (commands_dir / "intent.steer.md").is_file()
    assert (commands_dir / "intent.define.md").is_file()
    assert (commands_dir / "intent.decompose.md").is_file()
    assert (commands_dir / "intent.clarify.md").is_file()


def test_init_gemini_agent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner.invoke(app, ["init", "test-project", "--ai", "gemini"])

    commands_dir = tmp_path / ".gemini" / "commands"
    assert commands_dir.is_dir()
    assert (commands_dir / "intent.capture.md").is_file()


def test_init_copilot_agent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner.invoke(app, ["init", "test-project", "--ai", "copilot"])

    commands_dir = tmp_path / ".github" / "agents"
    assert commands_dir.is_dir()
    assert (commands_dir / "intent-capture.md").is_file()


def test_init_refuses_overwrite_without_force(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner.invoke(app, ["init", "test-project"])
    result = runner.invoke(app, ["init", "test-project"])
    assert result.exit_code == 1
    assert "already exists" in result.output


def test_init_force_replaces_intent_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner.invoke(app, ["init", "test-project"])

    marker = tmp_path / ".intent" / "custom-file.md"
    marker.write_text("user content")

    result = runner.invoke(app, ["init", "test-project", "--force"])
    assert result.exit_code == 0
    assert not marker.exists()
    assert (tmp_path / ".intent" / "state.json").is_file()


def test_init_force_preserves_agent_commands(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner.invoke(app, ["init", "test-project", "--ai", "gemini"])

    # Customize an agent command
    cmd_file = tmp_path / ".gemini" / "commands" / "intent.capture.md"
    cmd_file.write_text("customized content")

    # Force reinit with different agent
    runner.invoke(app, ["init", "test-project", "--force", "--ai", "claude"])

    # Gemini commands should be untouched
    assert cmd_file.read_text() == "customized content"


def test_init_invalid_agent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "test-project", "--ai", "invalid"])
    assert result.exit_code == 1
    assert "Unsupported AI agent" in result.output
    assert "claude" in result.output
