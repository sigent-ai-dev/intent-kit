"""Intent CLI — bootstrap projects for Intent-Driven Design (IDD).

This CLI initialises project directories with the IDD structure,
templates, and AI agent command files needed to run the four-phase
intent workflow (capture -> steer -> define -> decompose).
"""

import shutil
from pathlib import Path

import typer
from rich.console import Console

from intent_cli.agents import AGENTS, COMMANDS, SUPPORTED_AGENTS
from intent_cli.templates import (
    adapt_template_for_agent,
    generate_audit_md,
    generate_state_json,
    get_template,
)

app = typer.Typer(
    name="intent",
    help="Intent Kit CLI — bootstrap projects for Intent-Driven Design.",
)

console = Console()

INTENT_DIR = ".intent"


@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the project to initialise"),
    ai: str = typer.Option(
        "claude",
        "--ai",
        help="AI assistant: claude, gemini, copilot, cursor, q, windsurf",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Replace existing .intent/ directory (agent commands preserved)",
    ),
):
    """Initialise a new project with IDD structure and templates."""
    intent_path = Path(INTENT_DIR)

    if ai not in SUPPORTED_AGENTS:
        console.print(
            f"[red]Error:[/] Unsupported AI agent '{ai}'. Supported: {', '.join(SUPPORTED_AGENTS)}"
        )
        raise typer.Exit(code=1)

    if intent_path.exists() and not force:
        console.print(
            "[red]Error:[/] .intent/ already exists. Use [bold]--force[/] to reinitialise."
        )
        raise typer.Exit(code=1)

    if intent_path.exists() and force:
        shutil.rmtree(intent_path)

    try:
        # Create directory structure
        (intent_path / "adr" / "draft").mkdir(parents=True)
        (intent_path / "adr" / "accepted").mkdir(parents=True)
        (intent_path / "backlog").mkdir(parents=True)

        # Copy templates
        intent_template = get_template("intent-template.md")
        (intent_path / "intent.md").write_text(intent_template, encoding="utf-8")

        adr_template = get_template("adr/_template.md")
        (intent_path / "adr" / "_template.md").write_text(adr_template, encoding="utf-8")

        # Generate state and audit
        state_json = generate_state_json(project_name)
        (intent_path / "state.json").write_text(state_json, encoding="utf-8")

        audit_md = generate_audit_md(project_name, ai)
        (intent_path / "audit.md").write_text(audit_md, encoding="utf-8")

        # Copy agent command files
        agent_config = AGENTS[ai]
        agent_dir = Path(agent_config.directory)
        agent_dir.mkdir(parents=True, exist_ok=True)

        for command in COMMANDS:
            source_content = get_template(f"commands/{command}.md")
            adapted_content = adapt_template_for_agent(source_content, ai, command)
            filename = agent_config.file_pattern.format(command=command)
            target = agent_dir / filename
            if not target.exists():
                target.write_text(adapted_content, encoding="utf-8")

    except PermissionError:
        console.print("[red]Error:[/] Cannot write to directory — permission denied.")
        raise typer.Exit(code=1)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/] {e}")
        raise typer.Exit(code=1)

    # Success output
    console.print(f"\n[bold green]Initialising IDD project:[/] {project_name}")
    console.print(f"[dim]AI assistant:[/] {ai}\n")
    console.print("[bold]Created:[/]")
    console.print(f"  {INTENT_DIR}/intent.md")
    console.print(f"  {INTENT_DIR}/state.json")
    console.print(f"  {INTENT_DIR}/audit.md")
    console.print(f"  {INTENT_DIR}/adr/_template.md")
    for command in COMMANDS:
        filename = agent_config.file_pattern.format(command=command)
        console.print(f"  {agent_config.directory}/{filename}")
    console.print("\n[bold]Next steps:[/]")
    console.print("  1. Run /intent.capture with your big idea")
    console.print("  2. Use [bold]intent check[/] to validate project state")


@app.command()
def check(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details of each check"),
    fix: bool = typer.Option(False, "--fix", help="Auto-correct simple issues"),
):
    """Validate the current project's IDD state (phase gates, traceability)."""
    from intent_cli.checks import auto_fix, run_all_checks

    intent_path = Path(INTENT_DIR)

    if fix:
        fixes = auto_fix(intent_path)
        for f in fixes:
            console.print(f"  [cyan]FIXED[/]  {f}")
        if fixes:
            console.print()

    report = run_all_checks(intent_path, verbose=verbose)

    for result in report.results:
        if result.passed:
            icon = "[green]PASS[/]"
        elif result.severity == "warning":
            icon = "[yellow]WARN[/]"
        else:
            icon = "[red]FAIL[/]"

        console.print(f"  {icon}  {result.name}: {result.message}")
        if verbose and result.details:
            console.print(f"         [dim]{result.details}[/]")

    console.print()
    if report.has_errors:
        errors = sum(1 for r in report.results if not r.passed and r.severity == "error")
        console.print(f"[red bold]Check failed[/] — {errors} error(s) found")
        raise typer.Exit(code=1)
    elif report.has_warnings:
        warnings = sum(1 for r in report.results if not r.passed and r.severity == "warning")
        console.print(f"[green bold]Check passed[/] with {warnings} warning(s)")
    else:
        console.print("[green bold]All checks passed[/]")


def main():
    app()


def __getattr__(name: str):
    if name == "__version__":
        from importlib.metadata import version

        return version("intent-cli")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
