"""Command to list stored inboxes."""

import click

from ..core import InboxStorage
from ..utils import echo, echo_separator, styled, FG_RED_FLUO, FG_GREY_PEARL


@click.command(name="inboxes")
def list_inboxes():
    """Liste les inboxes sauvegardées."""
    storage = InboxStorage()
    inboxes = storage.load()

    echo_separator()
    echo("  INBOXES SAUVEGARDÉES", bold=True)
    echo_separator()

    if not inboxes:
        click.echo()
        echo("  Aucune inbox sauvegardée.", fg=FG_GREY_PEARL)
        click.echo()
        echo_separator()
        return

    click.echo()
    for idx, inbox in enumerate(inboxes, 1):
        echo(
            f"  [{styled(str(idx), fg=FG_RED_FLUO)}] {styled(inbox.address, fg=FG_RED_FLUO, bold=True)}"
        )
        echo(f"      Provider : {inbox.provider}", fg=FG_GREY_PEARL)
        if inbox.login:
            echo(f"      Login    : {inbox.login}", fg=FG_GREY_PEARL)
        if inbox.domain:
            echo(f"      Domaine  : {inbox.domain}", fg=FG_GREY_PEARL)
        click.echo()

    echo_separator()
    echo(f"  Total: {len(inboxes)} inbox(es)", fg=FG_GREY_PEARL)
    echo_separator()
