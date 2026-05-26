"""Tests for intent capture CLI subcommand."""

import json
from unittest.mock import patch

from typer.testing import CliRunner

from intent_cli import app

runner = CliRunner()


def test_capture_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".intent").mkdir()
    result = runner.invoke(app, ["capture", "config", "--url", "https://agent.example.com"])
    assert result.exit_code == 0
    assert "Configured" in result.output

    config = json.loads((tmp_path / ".intent" / "config.json").read_text())
    assert config["capture_agent_url"] == "https://agent.example.com"


def test_capture_start_no_url(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["capture", "start"])
    assert result.exit_code == 1
    assert "No capture agent URL" in result.output


def test_capture_start_with_url(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    mock_response = {
        "session_id": "abc123",
        "join_url": "https://agent.example.com/join/abc123",
        "status": "pending",
    }

    with patch("intent_cli.capture._call_api", return_value=mock_response):
        result = runner.invoke(app, ["capture", "start", "--url", "https://agent.example.com"])
    assert result.exit_code == 0
    assert "abc123" in result.output
    assert "join/abc123" in result.output


def test_capture_status_with_session(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    mock_response = {
        "session_id": "abc123",
        "status": "active",
        "progress": {"sections_covered": ["Context", "Intent"]},
        "participants": ["alice", "bob"],
    }

    with patch("intent_cli.capture._call_api", return_value=mock_response):
        result = runner.invoke(
            app, ["capture", "status", "abc123", "--url", "https://agent.example.com"]
        )
    assert result.exit_code == 0
    assert "active" in result.output
    assert "Context" in result.output


def test_capture_connect_writes_output(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    call_count = {"n": 0}

    def mock_api(base_url, method, path, body=None):
        call_count["n"] += 1
        if "/result" in path:
            return {
                "intent_md": "# Intent\n\n## Context\n\nTest\n",
                "state": {
                    "project_name": "test",
                    "intent_id": "INT-001",
                    "current_phase": "capture",
                    "phases": {"capture": {"complete": True}},
                },
                "audit_md": "# Audit\n\n## Entry\n",
            }
        return {"status": "complete", "progress": {"sections_covered": []}}

    with patch("intent_cli.capture._call_api", side_effect=mock_api):
        result = runner.invoke(
            app, ["capture", "connect", "abc123", "--url", "https://agent.example.com"]
        )
    assert result.exit_code == 0
    assert "Session complete" in result.output
    assert (tmp_path / ".intent" / "intent.md").is_file()
    assert (tmp_path / ".intent" / "state.json").is_file()
    assert (tmp_path / ".intent" / "audit.md").is_file()
