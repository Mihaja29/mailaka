"""Command to download an attachment."""

from pathlib import Path

import click

from ..core import ProviderFactory, InboxStorage
from ..utils import echo, echo_separator, FG_GREY_PEARL, ProviderError


@click.command()
@click.argument("message_id")
@click.argument("attachment_id")
@click.option("--output", "-o", help="Chemin de sortie pour le fichier")
def download(message_id, attachment_id, output):
    """Télécharge une pièce jointe."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        click.echo("Aucune adresse email active.")
        click.echo("Utilisez 'mailaka new' pour créer une nouvelle adresse.")
        raise click.Abort()

    try:
        provider_instance = ProviderFactory.get_provider(active_inbox.provider)
        payload = provider_instance.download_attachment(active_inbox, message_id, attachment_id)
    except ProviderError as exc:
        raise click.ClickException(f"Téléchargement impossible: {exc}")

    output_path = Path(output) if output else Path(attachment_id).name
    output_path = Path(output_path)
    try:
        output_path.write_bytes(payload)
    except OSError as exc:
        raise click.ClickException(f"Impossible d'écrire le fichier: {exc}")

    echo_separator()
    echo("  PIÈCE JOINTE TÉLÉCHARGÉE", bold=True)
    echo_separator()
    click.echo()
    echo(f"  Fichier : {output_path}", fg=FG_GREY_PEARL)
    echo(f"  Provider: {active_inbox.provider}", fg=FG_GREY_PEARL)
    click.echo()
    echo_separator()
