"""Command to delete an email."""

import click

from ..core import ProviderFactory, InboxStorage
from ..utils import echo, echo_separator, FG_GREY_PEARL, ProviderError


@click.command()
@click.argument("message_id")
def delete(message_id):
    """Supprime un email."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        click.echo("Aucune adresse email active.")
        click.echo("Utilisez 'mailaka new' pour créer une nouvelle adresse.")
        raise click.Abort()

    try:
        provider_instance = ProviderFactory.get_provider(active_inbox.provider)
        provider_instance.delete_message(active_inbox, message_id)

        echo_separator()
        echo("  MESSAGE SUPPRIMÉ", bold=True)
        echo_separator()
        click.echo()
        echo(f"  ID: {message_id}", fg=FG_GREY_PEARL)
        click.echo()
        echo_separator()

    except ProviderError as exc:
        raise click.ClickException(f"Suppression impossible: {exc}")
