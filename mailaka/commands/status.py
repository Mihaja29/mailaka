"""Command to show status of active email."""

import click

from ..core import InboxStorage
from ..utils import echo, echo_separator, styled, FG_RED_FLUO, FG_GREY_PEARL


@click.command()
def status():
    """Affiche l'adresse active et le temps restant."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()
    
    echo_separator()
    echo("  STATUT", bold=True)
    echo_separator()
    click.echo()
    
    if not active_inbox:
        echo("  Aucune adresse email active", fg=FG_GREY_PEARL)
        click.echo()
        echo("  Utilisez 'mailaka new' pour créer une nouvelle adresse.", fg=FG_GREY_PEARL)
    else:
        echo(f"  Adresse active : {styled(active_inbox.address, fg=FG_RED_FLUO, bold=True)}")
        echo(f"  Provider       : {styled(active_inbox.provider, fg=FG_GREY_PEARL)}")
        click.echo()
        echo("  Durée de vie   : Variable selon le provider", fg=FG_GREY_PEARL)
        echo("     • 1secmail     : Permanent (jusqu'à inactivité)", fg=FG_GREY_PEARL)
        echo("     • mail.tm      : Permanent (avec compte)", fg=FG_GREY_PEARL)
        echo("     • guerrillamail: ~1 heure", fg=FG_GREY_PEARL)
        click.echo()
        echo("  Stockage       : Local (~/.mailaka_inboxes.json)", fg=FG_GREY_PEARL)
    
    click.echo()
    echo_separator()
