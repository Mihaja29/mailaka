"""Command to list emails in the inbox."""

import click

from ..core import ProviderFactory, InboxStorage
from ..utils import echo, echo_separator, styled, FG_RED_FLUO, FG_GREY_PEARL, ProviderError


@click.command()
@click.option("--limit", type=int, default=None, help="Nombre maximal de messages")
@click.option("--offset", type=int, default=0, help="Décalage pour pagination")
def inbox(limit, offset):
    """Liste les emails reçus."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()
    
    if not active_inbox:
        click.echo("Aucune adresse email active.")
        click.echo("Utilisez 'mailaka new' pour créer une nouvelle adresse.")
        raise click.Abort()
    
    try:
        provider_instance = ProviderFactory.get_provider(active_inbox.provider)
        messages = provider_instance.get_messages(active_inbox, limit=limit, offset=offset)
        
        echo_separator()
        echo("  BOÎTE DE RÉCEPTION", bold=True)
        echo(f"  {styled(active_inbox.address, fg=FG_RED_FLUO, bold=True)}")
        echo_separator()
        
        if not messages:
            click.echo()
            echo("  Aucun message pour le moment.", fg=FG_GREY_PEARL)
            click.echo()
            echo_separator()
            return
        
        click.echo()
        for idx, message in enumerate(messages, 1):
            echo(f"  [{styled(str(idx), fg=FG_RED_FLUO)}] ID: {styled(message.id, fg=FG_GREY_PEARL)}")
            echo(f"      De      : {message.sender}")
            echo(f"      Sujet   : {message.subject}")
            if message.date:
                echo(f"      Date    : {message.date}", fg=FG_GREY_PEARL)
            click.echo()
        
        echo_separator()
        echo(f"  Total: {len(messages)} message(s)", fg=FG_GREY_PEARL)
        echo("  Utilisez 'mailaka read <id>' pour lire un message.", fg=FG_GREY_PEARL)
        echo_separator()
        
    except ProviderError as exc:
        raise click.ClickException(f"Erreur lors de la récupération des messages: {exc}")
