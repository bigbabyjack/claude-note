"""CLI commands for claude-note."""

from __future__ import annotations

from pathlib import Path

import click

from claude_note.config import Config
from claude_note.note import Note, add_note, read_note


@click.group()
def main():
    """claude-note: A simple note-taking CLI tool."""
    pass


@main.command()
@click.argument("path")
@click.argument("content")
def add(path: str, content: str):
    """Add content to a note file."""
    note: Note = add_note(Path(path), content)
    click.echo(f"Note added at {note.path}")


@main.command()
@click.argument("path")
def read(path: str):
    """Read a note file."""
    note = Note(Path(path))
    content = read_note(note)
    click.echo(content)


@main.group()
def config():
    """Manage configuration."""
    pass


@config.command()
@click.option("--notes-dir", default="notes", help="Directory for notes")
@click.option("--path", default="config.json", help="Config file path")
def init(notes_dir: str, path: str):
    """Initialize configuration file."""
    cfg = Config(path=Path(path), notes_dir=Path(notes_dir))
    cfg.save()
    click.echo(f"Config initialized at {cfg.path}")


@config.command()
@click.option("--path", default="config.json", help="Config file path")
def show(path: str):
    """Show current configuration."""
    try:
        cfg = Config.load(Path(path))
        click.echo(f"Config file: {cfg.path}")
        click.echo(f"Notes directory: {cfg.notes_dir}")
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("Run 'claude-note config init' to create a config file")


@config.command()
@click.argument("key")
@click.argument("value")
@click.option("--path", default="config.json", help="Config file path")
def set(key: str, value: str, path: str):
    """Set a configuration value."""
    config_path = Path(path)
    try:
        cfg = Config.load(config_path)
    except FileNotFoundError:
        click.echo("Config file not found. Run 'claude-note config init' first.")
        return

    if key == "notes_dir":
        cfg = Config(path=cfg.path, notes_dir=Path(value))
        cfg.save()
        click.echo(f"Updated notes_dir to: {value}")
    else:
        click.echo(f"Error: Unknown config key '{key}'", err=True)
        click.echo("Available keys: notes_dir")


if __name__ == "__main__":
    main()
