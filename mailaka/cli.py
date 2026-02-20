"""Main CLI entry point for Mailaka."""

import click
import sys

from mailaka import __version__
from mailaka.commands import (
    new,
    inbox,
    read,
    delete,
    attachments,
    download,
    status,
    list_inboxes,
)
from mailaka.interactive import start_interactive_mode
from mailaka.utils import echo, styled, FG_RED_FLUO


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--no-interactive", is_flag=True, help="Désactiver le mode interactif")
def main(ctx, no_interactive):
    """Mailaka - Générateur d'emails éphémères."""
    if ctx.invoked_subcommand is None:
        if not no_interactive and sys.stdin.isatty():
            start_interactive_mode()
        else:
            ctx.get_help()


# Register commands
main.add_command(new)
main.add_command(inbox)
main.add_command(read)
main.add_command(delete)
main.add_command(attachments)
main.add_command(download)
main.add_command(status)
main.add_command(list_inboxes)


@main.command()
def version():
    """Affiche la version."""
    echo(f"  Mailaka version {styled(__version__, fg=FG_RED_FLUO, bold=True)}")
    click.echo()


if __name__ == "__main__":
    main()
