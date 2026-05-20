"""Intent CLI — bootstrap projects for Intent-Driven Design (IDD).

This CLI initialises project directories with the IDD structure,
templates, and AI agent command files needed to run the four-phase
intent workflow (capture → steer → define → decompose).
"""
__version__ = "0.0.1"

import typer

app = typer.Typer(
    name="intent",
    help="Intent Kit CLI — bootstrap projects for Intent-Driven Design.",
)


@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the project to initialise"),
    ai: str = typer.Option(
        "claude",
        "--ai",
        help="AI assistant: claude, gemini, copilot, cursor, q, windsurf",
    ),
):
    """Initialise a new project with IDD structure and templates."""
    from rich.console import Console
    console = Console()
    console.print(f"[bold green]Initialising IDD project:[/] {project_name}")
    console.print(f"[dim]AI assistant:[/] {ai}")
    # TODO: Implement project scaffolding
    console.print("[yellow]Not yet implemented — see CONTRIBUTING.md[/]")


@app.command()
def check():
    """Validate the current project's IDD state (phase gates, traceability)."""
    from rich.console import Console
    console = Console()
    console.print("[bold]Checking IDD project state...[/]")
    # TODO: Implement validation
    console.print("[yellow]Not yet implemented — see CONTRIBUTING.md[/]")


def main():
    app()
