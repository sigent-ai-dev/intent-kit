"""Agent configuration for Intent Kit multi-agent support."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfig:
    name: str
    directory: str
    file_pattern: str  # {command} is replaced with the command name


AGENTS: dict[str, AgentConfig] = {
    "claude": AgentConfig("claude", ".claude/commands", "intent.{command}.md"),
    "gemini": AgentConfig("gemini", ".gemini/commands", "intent.{command}.md"),
    "copilot": AgentConfig("copilot", ".github/agents", "intent-{command}.md"),
    "cursor": AgentConfig("cursor", ".cursor/commands", "intent.{command}.md"),
    "q": AgentConfig("q", ".amazonq/prompts", "intent-{command}.md"),
    "windsurf": AgentConfig("windsurf", ".windsurf/workflows", "intent-{command}.md"),
}

SUPPORTED_AGENTS = list(AGENTS.keys())

COMMANDS = ["capture", "steer", "define", "decompose", "clarify"]
