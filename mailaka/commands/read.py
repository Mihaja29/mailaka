"""Command to read a specific email."""

import click

from ..core import ProviderFactory, InboxStorage
from ..utils import echo, echo_separator, styled, FG_RED_FLUO, FG_GREY_PEARL, ProviderError


@click.command()
@click.argument("message_id")
def read(message_id):
    """Affiche le contenu d'un email."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()
    
    if not active_inbox:
        click.echo("Aucune adresse email active.")
        click.echo("Utilisez 'mailaka new' pour créer une nouvelle adresse.")
        raise click.Abort()
    
    try:
        provider_instance = ProviderFactory.get_provider(active_inbox.provider)
        message = provider_instance.read_message(active_inbox, message_id)
        
        echo_separator()
        echo("  MESSAGE", bold=True)
        echo_separator()
        click.echo()
        echo(f"  ID      : {styled(message.id, fg=FG_RED_FLUO)}")
        echo(f"  De      : {message.sender}")
        echo(f"  Sujet   : {message.subject}")
        if message.date:
            echo(f"  Date    : {message.date}")
        
        click.echo()
        echo_separator()
        click.echo()
        
        if message.body:
            click.echo(message.body)
        else:
            echo("  (Message vide)", fg=FG_GREY_PEARL)
        
        click.echo()
        echo_separator()
        
    except ProviderError as exc:
        raise click.ClickException(f"Erreur lors de la lecture du message: {exc}")
