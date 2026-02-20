"""Command to create a new temporary email address."""

import click

from ..core import ProviderFactory, InboxStorage
from ..utils import echo, echo_success, echo_error, styled, FG_RED_FLUO, FG_GREY_PEARL, ProviderError


@click.command()
@click.option(
    "--provider",
    type=click.Choice(["1secmail", "mailtm", "guerrillamail", "auto"], case_sensitive=False),
    default="auto",
    show_default=True,
    help="Fournisseur d'email à utiliser",
)
def new(provider):
    """Crée une nouvelle adresse email temporaire."""
    storage = InboxStorage()
    
    if provider.lower() == "auto":
        provider_order = ProviderFactory.get_all_provider_names()
    else:
        provider_order = [provider.lower()]
    
    last_error = None
    
    for provider_name in provider_order:
        try:
            provider_instance = ProviderFactory.get_provider(provider_name)
            inbox = provider_instance.create_inbox()
            storage.add(inbox)
            
            echo_success("Nouvelle adresse email créée")
            click.echo()
            echo(f"  Adresse  : {styled(inbox.address, fg=FG_RED_FLUO, bold=True)}")
            echo(f"  Provider : {styled(inbox.provider, fg=FG_GREY_PEARL)}")
            
            if inbox.password:
                echo(f"  Password : {styled(inbox.password, fg=FG_GREY_PEARL)}")
            if inbox.token:
                echo(f"  Token    : {styled(inbox.token, fg=FG_GREY_PEARL)}")
            
            click.echo()
            echo("  L'adresse a été sauvegardée et activée.", fg=FG_GREY_PEARL)
            echo("  Utilisez 'mailaka inbox' pour voir vos messages.", fg=FG_GREY_PEARL)
            
            return
            
        except ProviderError as exc:
            last_error = exc
            continue
    
    if last_error:
        echo_error(f"Échec de création: {last_error}")
        raise click.ClickException(str(last_error))
    
    raise click.ClickException("Tous les providers ont échoué")
