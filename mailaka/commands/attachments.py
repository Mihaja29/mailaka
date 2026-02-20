"""Command to list email attachments."""

import click

from ..core import ProviderFactory, InboxStorage, Provider
from ..utils import (
    echo,
    echo_separator,
    styled,
    FG_RED_FLUO,
    FG_GREY_PEARL,
    ProviderError,
)


@click.command()
@click.argument("message_id")
def attachments(message_id):
    """Liste les pièces jointes d'un email."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        click.echo("Aucune adresse email active.")
        click.echo("Utilisez 'mailaka new' pour créer une nouvelle adresse.")
        raise click.Abort()

    try:
        provider_instance = ProviderFactory.get_provider(active_inbox.provider)

        method = provider_instance.__class__.get_attachments
        if method is Provider.get_attachments:
            click.echo("Ce provider ne supporte pas les pièces jointes.")
            return

        attachments_list = provider_instance.get_attachments(active_inbox, message_id)

        echo_separator()
        echo(f"  PIÈCES JOINTES - Message {message_id}", bold=True)
        echo_separator()

        if not attachments_list:
            click.echo()
            echo("  Aucune pièce jointe dans ce message.", fg=FG_GREY_PEARL)
            click.echo()
            echo_separator()
            return

        click.echo()
        for idx, attachment in enumerate(attachments_list, 1):
            echo(
                f"  [{styled(str(idx), fg=FG_RED_FLUO)}] {attachment.get('filename', 'unknown')}"
            )
            echo(f"      Taille  : {attachment.get('size', 'N/A')}", fg=FG_GREY_PEARL)
            echo(
                f"      Type    : {attachment.get('contentType', 'N/A')}",
                fg=FG_GREY_PEARL,
            )
            if "id" in attachment:
                echo(f"      ID      : {attachment['id']}", fg=FG_GREY_PEARL)
            click.echo()

        echo_separator()
        echo(f"  Total: {len(attachments_list)} pièce(s) jointe(s)", fg=FG_GREY_PEARL)
        echo(
            "  Utilisez 'mailaka download <message-id> <attachment-id>' pour télécharger.",
            fg=FG_GREY_PEARL,
        )
        echo_separator()

    except ProviderError as exc:
        raise click.ClickException(
            f"Erreur lors de la récupération des pièces jointes: {exc}"
        )
