"""Interactive mode for Mailaka."""

import os
import subprocess

import click

from mailaka import __version__
from mailaka.core import InboxStorage, ProviderFactory, ProviderError
from mailaka.utils import (
    echo,
    echo_separator,
    styled,
    BANNER,
    FG_GREY_PEARL,
    FG_RED_FLUO,
    FG_BLUE_NIGHT,
)


# Commandes disponibles avec descriptions
MAILAKA_COMMANDS = {
    "/new": "Créer adresse [TEMP: 15min | LONG: sécurisé]",
    "/delete": "Supprimer messages/inboxes (1,2-4)",
    "/inbox": "Voir messages reçus",
    "/read": "Lire un message",
    "/attachments": "Voir + télécharger pièces jointes",
    "/download": "Télécharger pièces jointes",
    "/inboxes": "Lister inboxes [TEMP|LONG]",
    "/note": "Ajouter note sur inbox",
    "/status": "Afficher adresse active",
    "/check": "Vérifier email/domaine",
    "/export": "Exporter vers JSON",
    "/import": "Importer depuis JSON",
    "/clear": "Effacer l'écran",
    "/help": "Afficher l'aide",
    "/version": "Afficher version",
    "/exit": "Quitter",
}


def show_commands_filtered(prefix=""):
    """Affiche les commandes filtrées par préfixe."""
    click.echo()
    
    if not prefix:
        echo("  Commandes disponibles:", bold=True)
        click.echo()
        for cmd, desc in MAILAKA_COMMANDS.items():
            click.echo(f"    {styled(cmd, fg=FG_RED_FLUO, bold=True):<20} {desc}")
    else:
        # Chercher les commandes qui commencent par le préfixe
        prefix_lower = prefix.lower()
        matching = [(cmd, desc) for cmd, desc in MAILAKA_COMMANDS.items() 
                   if cmd.lower().startswith(f"/{prefix_lower}")]
        
        if matching:
            echo(f"  Commandes '/{prefix}':", bold=True)
            click.echo()
            for cmd, desc in matching:
                click.echo(f"    {styled(cmd, fg=FG_RED_FLUO, bold=True):<20} {desc}")
        else:
            echo(f"  Aucune commande '/{prefix}'", fg=FG_GREY_PEARL)
    
    click.echo()
    echo("  Sans '/' = commande système (quitte Mailaka)", fg=FG_GREY_PEARL)
    click.echo()


def parse_selection(selection_str: str, max_items: int) -> list:
    """Parse selection string like '1,3,5' or '1-3' or '1,2-4,6' into list of indices."""
    if not selection_str:
        return []
    
    indices = set()
    parts = selection_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            # Range like "1-3"
            try:
                start, end = part.split('-')
                start_idx = int(start.strip()) - 1
                end_idx = int(end.strip()) - 1
                for idx in range(start_idx, end_idx + 1):
                    if 0 <= idx < max_items:
                        indices.add(idx)
            except ValueError:
                continue
        else:
            # Single number
            try:
                idx = int(part) - 1
                if 0 <= idx < max_items:
                    indices.add(idx)
            except ValueError:
                continue
    
    return sorted(list(indices))


def show_progress(message, duration=0.5):
    """Show progress percentage for loading operations."""
    import time
    
    steps = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    for percent in steps:
        prefix = f"  [{percent:>3}%]"
        line = f"{prefix} {message}"
        click.echo(line, nl=False)
        time.sleep(duration / len(steps))
        if percent < 100:
            click.echo("\r", nl=False)
    
    click.echo()


def echo_check(text):
    """Echo success with checkmark."""
    click.echo(f"  [{styled('OK', fg=FG_RED_FLUO, bold=True)}] {text}")


def echo_cross(text):
    """Echo error with cross."""
    click.echo(f"  [{styled('ERR', fg=FG_RED_FLUO, bold=True)}] {text}")


def start_interactive_mode():
    """Start the interactive CLI mode."""
    click.clear()
    click.echo(BANNER)
    echo_separator()

    version_label = f"v{styled(__version__, fg=FG_BLUE_NIGHT)}"
    echo(f"  {version_label} — Recevez et lisez vos messages directement dans le terminal", bold=True)
    echo_separator()
    click.echo()

    # Affichage des commandes disponibles
    echo("  Commandes disponibles:", bold=True)
    click.echo()
    echo(f"    {styled('new', fg=FG_RED_FLUO, bold=True)}           Créer adresse(s) (syntaxe: 1,3 ou 2-4)")
    echo(f"    {styled('inbox', fg=FG_RED_FLUO, bold=True)}          Voir les messages reçus")
    echo(f"    {styled('read', fg=FG_RED_FLUO, bold=True)}            Lire un message")
    echo(f"    {styled('delete', fg=FG_RED_FLUO, bold=True)}          Supprimer plusieurs (messages ou emails)")
    echo(f"    {styled('attachments', fg=FG_RED_FLUO, bold=True)}     Voir + télécharger pièces jointes")
    echo(f"    {styled('download', fg=FG_RED_FLUO, bold=True)}        Télécharger les pièces jointes")
    echo(f"    {styled('status', fg=FG_RED_FLUO, bold=True)}          Voir le statut actuel")
    echo(f"    {styled('inboxes', fg=FG_RED_FLUO, bold=True)}         Lister toutes les inboxes")
    echo(f"    {styled('clear', fg=FG_RED_FLUO, bold=True)}          Effacer l'écran")
    echo(f"    {styled('help', fg=FG_RED_FLUO, bold=True)}           Afficher l'aide")
    echo(f"    {styled('exit/quit/q', fg=FG_RED_FLUO, bold=True)}    Quitter")
    click.echo()
    echo("  Commande inconnue = quitte Mailaka", fg=FG_GREY_PEARL)
    click.echo()
    echo_separator()
    click.echo()

    storage = InboxStorage()
    active_inbox = storage.get_latest()
    inboxes = storage.load()

    if active_inbox:
        echo(
            f"  Adresse active: {styled(active_inbox.address, fg=FG_RED_FLUO, bold=True)}"
        )
        echo(f"  Provider: {active_inbox.provider}", fg=FG_GREY_PEARL)
        echo(f"  Inboxes: {len(inboxes)}/5", fg=FG_GREY_PEARL)
    else:
        echo("  Aucune adresse active", fg=FG_GREY_PEARL)
        echo("  Tapez 'new' pour créer une adresse", fg=FG_GREY_PEARL)

    click.echo()
    echo_separator()
    click.echo()

    while True:
        try:
            user_input = click.prompt(
                styled("mailaka", fg=FG_RED_FLUO, bold=True)
                + styled(">", fg=FG_GREY_PEARL),
                prompt_suffix=" ",
                default="",
                show_default=False,
            ).strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []

            if command in ["exit", "quit", "q"]:
                click.echo()
                echo("  Au revoir!", fg=FG_BLUE_NIGHT, bold=True)
                click.echo()
                break

            elif command == "clear":
                click.clear()
                click.echo(BANNER)
                echo_separator()
                continue

            elif command == "help" or command == "h":
                show_help()

            elif command == "new":
                handle_new(args)
                active_inbox = storage.get_latest()

            elif command == "inbox":
                handle_inbox()

            elif command == "read":
                if args:
                    if "@" in args[0]:
                        echo_cross("Usage incorrect: vous avez entré une adresse email.")
                        echo("  Utilisez l'ID du message (ex: read 699683acf7155aba733bf480)", fg=FG_GREY_PEARL)
                        echo("  Voir les IDs avec: inbox", fg=FG_GREY_PEARL)
                    else:
                        handle_read(args[0])
                else:
                    handle_read_interactive()

            elif command == "delete":
                if args:
                    if "@" in args[0]:
                        # Suppression d'une inbox par son adresse email
                        handle_delete_inbox(args[0])
                    else:
                        # Suppression d'un message par son ID
                        handle_delete(args[0])
                else:
                    handle_delete_interactive()

            elif command == "attachments":
                if args:
                    if "@" in args[0]:
                        echo_cross("Usage incorrect: vous avez entré une adresse email.")
                        echo("  Utilisez l'ID du message (ex: attachments 699683acf7155aba733bf480)", fg=FG_GREY_PEARL)
                        echo("  Voir les IDs avec: inbox", fg=FG_GREY_PEARL)
                    else:
                        handle_attachments(args[0])
                else:
                    handle_attachments_interactive()

            elif command == "download":
                if args:
                    if "@" in args[0]:
                        echo_cross("Usage incorrect: vous avez entré une adresse email.")
                        echo("  Utilisez l'ID du message (ex: download 699683acf7155aba733bf480)", fg=FG_GREY_PEARL)
                        echo("  Voir les IDs avec: inbox", fg=FG_GREY_PEARL)
                    else:
                        handle_download(args[0])
                else:
                    handle_download_interactive()

            elif command == "inboxes":
                handle_inboxes()

            elif command == "note":
                handle_note(args)

            elif command == "status":
                handle_status()

            elif command == "check":
                if args:
                    handle_check(args[0])
                else:
                    echo_cross("Usage: check \u003cemail@domain.com\u003e")

            elif command == "export":
                filepath = args[0] if args else "mailaka_backup.json"
                handle_export(filepath)

            elif command == "import":
                if args:
                    handle_import(args[0])
                else:
                    echo_cross("Usage: import \u003cfichier.json\u003e")

            elif command == "version":
                echo(
                    f"  Mailaka version {styled(__version__, fg=FG_RED_FLUO, bold=True)}"
                )

            else:
                # Commande externe - quitter mailaka et l'exécuter
                import subprocess
                import shlex
                
                echo(f"  Commande externe détectée: {command}", fg=FG_GREY_PEARL)
                echo("  Sortie de Mailaka...", fg=FG_BLUE_NIGHT)
                click.echo()
                
                # Reconstituer la commande complète
                full_cmd = user_input
                try:
                    subprocess.run(full_cmd, shell=True, check=False)
                except Exception as e:
                    echo_cross(f"Erreur exécution: {e}")
                
                # Quitter mailaka après exécution
                break

            click.echo()

        except (KeyboardInterrupt, EOFError):
            click.echo()
            click.echo()
            echo("  Au revoir!", fg=FG_BLUE_NIGHT, bold=True)
            click.echo()
            break
        except Exception as e:
            echo_cross(f"Erreur: {str(e)}")
            click.echo()


def show_help():
    """Display help message."""
    click.echo()
    echo("  Commandes disponibles:", bold=True)
    click.echo()
    click.echo(
        f"    {styled('new', fg=FG_RED_FLUO, bold=True):<20} Créer adresse(s) [TEMP: 15min | LONG: [SECURISE] sécurisé]"
    )
    click.echo(
        f"    {styled('delete', fg=FG_RED_FLUO, bold=True):<20} Supprimer multiples (messages: 1,2-4 ou inboxes: 1,3)"
    )
    click.echo(
        f"    {styled('inbox', fg=FG_RED_FLUO, bold=True):<20} Voir les messages de l'adresse active"
    )
    click.echo(
        f"    {styled('read', fg=FG_RED_FLUO, bold=True):<20} Lire un message (choix interactif)"
    )
    click.echo(
        f"    {styled('delete', fg=FG_RED_FLUO, bold=True):<20} Supprimer multiples (messages: 1,2-4 ou inboxes: 1,3)"
    )
    click.echo(
        f"    {styled('attachments', fg=FG_RED_FLUO, bold=True):<20} Voir ET télécharger toutes les pièces jointes"
    )
    click.echo(
        f"    {styled('check', fg=FG_RED_FLUO, bold=True):<20} Vérifier email/domaine (disify)"
    )
    click.echo(
        f"    {styled('download', fg=FG_RED_FLUO, bold=True):<20} Télécharger pièces jointes (choix interactif)"
    )
    click.echo(
        f"    {styled('inboxes', fg=FG_RED_FLUO, bold=True):<20} Lister inboxes [⏳: temps restant | 🔒: long terme]"
    )
    click.echo(
        f"    {styled('status', fg=FG_RED_FLUO, bold=True):<20} Afficher l'adresse active"
    )
    click.echo(
        f"    {styled('version', fg=FG_RED_FLUO, bold=True):<20} Afficher la version"
    )
    click.echo(f"    {styled('clear', fg=FG_RED_FLUO, bold=True):<20} Effacer l'écran")
    click.echo(
        f"    {styled('help', fg=FG_RED_FLUO, bold=True):<20} Afficher cette aide"
    )
    click.echo(f"    {styled('exit', fg=FG_RED_FLUO, bold=True):<20} Quitter")
    click.echo()


def handle_new(args):
    """Handle the 'new' command with interactive provider selection."""
    provider_name = args[0] if args else None
    from datetime import datetime

    try:
        click.echo()
        
        # [SECURISE] Choix du type d'inbox: temporaire ou long terme
        click.echo()
        echo("  Quel type d'adresse ?", bold=True)
        click.echo()
        click.echo(f"    [{styled('1', fg=FG_RED_FLUO, bold=True)}] Temporaire (auto-suppression après 15min)")
        click.echo(f"    [{styled('2', fg=FG_RED_FLUO, bold=True)}] Long terme (persistance + sécurité renforcée)")
        click.echo()
        
        inbox_type_choice = click.prompt(
            styled("  Votre choix", fg=FG_RED_FLUO, bold=True),
            prompt_suffix=" ",
            default="1",
            show_default=False
        ).strip()
        
        inbox_type = "longterm" if inbox_type_choice == "2" else "temp"
        
        if inbox_type == "longterm":
            click.echo()
            echo("  [SECURISE] Mode Long Terme activé", fg=FG_BLUE_NIGHT, bold=True)
            echo("  Sécurités appliquées:", fg=FG_GREY_PEARL)
            echo("    • Token API chiffré (Fernet)", fg=FG_GREY_PEARL)
            echo("    • Identifiants protégés en mémoire", fg=FG_GREY_PEARL)
            echo("    • Limite: 3 inboxes long terme max", fg=FG_GREY_PEARL)
            echo("    • Protection contre la récupération", fg=FG_GREY_PEARL)
            click.echo()
        
        # Si aucun provider spécifié, afficher le menu de sélection par domaines
        if provider_name is None:
            # Collecter tous les domaines disponibles
            all_domains = []
            provider_map = {}  # domain -> provider
            
            # Providers features
            CUSTOMIZABLE_PROVIDERS = ('mailtm', 'mail_gw')
            ATTACHMENT_PROVIDERS = ('mailtm', 'mail_gw', 'guerrillamail')
            
            # Helper pour construire le label
            def build_label(domain_name, provider_name):
                features = []
                if provider_name in CUSTOMIZABLE_PROVIDERS:
                    features.append("personnalisable")
                if provider_name in ATTACHMENT_PROVIDERS:
                    features.append("PJ supportés")
                if features:
                    return f"{domain_name} ({', '.join(features)})"
                return domain_name
            
            # mail.tm
            domain_label = build_label("mail.tm (domain aléatoire)", "mailtm")
            all_domains.append(domain_label)
            provider_map[domain_label] = "mailtm"
            
            # dropmail - pas de PJ
            all_domains.append("dropmail.me")
            provider_map["dropmail.me"] = "dropmail"
            
            # tempmail_io - pas de PJ
            try:
                from mailaka.core import ProviderFactory
                temp_provider = ProviderFactory.get_provider("tempmail_io")
                for d in temp_provider.get_available_domains():
                    all_domains.append(f"@{d}")
                    provider_map[f"@{d}"] = ("tempmail_io", d)
            except:
                pass
            
            # mail.gw
            try:
                gw_provider = ProviderFactory.get_provider("mail_gw")
                for d in gw_provider.get_available_domains():
                    domain_label = build_label(f"@{d}", "mail_gw")
                    all_domains.append(domain_label)
                    provider_map[domain_label] = ("mail_gw", d)
            except:
                pass
            
            # guerrillamail - PJ supportés
            domain_label = build_label("@guerrillamailblock.com", "guerrillamail")
            all_domains.append(domain_label)
            provider_map[domain_label] = "guerrillamail"
            
            # Pagination : 5 domaines par page
            page_size = 5
            total_pages = (len(all_domains) + page_size - 1) // page_size
            current_page = 0
            
            while True:
                start_idx = current_page * page_size
                end_idx = min(start_idx + page_size, len(all_domains))
                page_domains = all_domains[start_idx:end_idx]
                
                click.echo()
                echo(f"  Choisissez un domaine (Page {current_page + 1}/{total_pages}):", bold=True)
                click.echo()
                
                for idx, domain in enumerate(page_domains, 1):
                    click.echo(f"    [{styled(str(idx), fg=FG_RED_FLUO, bold=True)}] {domain}")
                
                # Options de navigation
                click.echo()
                if current_page < total_pages - 1:
                    click.echo(f"    [{styled('0', fg=FG_BLUE_NIGHT, bold=True)}] Page suivante →")
                if current_page > 0:
                    click.echo(f"    [{styled('00', fg=FG_BLUE_NIGHT, bold=True)}] ← Page précédente")
                click.echo()
                echo("  Syntaxe: 1,3,5 ou 1-3 ou 1,2-4,6 (plusieurs domaines)", fg=FG_GREY_PEARL)
                click.echo()
                
                choice = click.prompt(
                    styled("  Votre choix", fg=FG_RED_FLUO, bold=True),
                    prompt_suffix=" ",
                    default="1",
                    show_default=False
                ).strip()
                
                if choice == "0" and current_page < total_pages - 1:
                    current_page += 1
                    continue
                elif choice == "00" and current_page > 0:
                    current_page -= 1
                    continue
                
                # Parser la sélection multiple
                selected_indices = parse_selection(choice, len(page_domains))
                
                if selected_indices:
                    selected_domains = [page_domains[idx] for idx in selected_indices]
                    break
                else:
                    echo_cross("Choix invalide")
            
            # Vérifier si personnalisation possible
            supports_custom = False
            for selected_domain in selected_domains:
                provider_info = provider_map[selected_domain]
                prov_name = provider_info[0] if isinstance(provider_info, tuple) else provider_info
                if prov_name in ('mailtm', 'mail_gw'):
                    supports_custom = True
                    break
            
            # Demander personnalisation seulement si applicable
            local_part = None
            if supports_custom:
                use_custom = click.prompt(
                    styled("  Personnaliser le nom? (y/n)", fg=FG_RED_FLUO, bold=True),
                    prompt_suffix=" ",
                    default="n",
                    show_default=False
                ).strip().lower()
                
                if use_custom in ('y', 'yes', 'oui'):
                    custom_name = click.prompt(
                        styled("  Nom souhaité (a-z, 0-9, ., _, -)", fg=FG_RED_FLUO, bold=True),
                        prompt_suffix=" ",
                        default="",
                        show_default=False
                    ).strip()
                    if custom_name:
                        local_part = custom_name
            
            # Créer plusieurs inboxes
            created_inboxes = []
            for selected_domain in selected_domains:
                # Déterminer le provider et domaine
                provider_info = provider_map[selected_domain]
                if isinstance(provider_info, tuple):
                    prov_name, domain = provider_info
                else:
                    prov_name = provider_info
                    domain = None
                
                try:
                    show_progress(f"Création avec {selected_domain}", duration=0.3)
                    provider = ProviderFactory.get_provider(prov_name)
                    
                    # Passer local_part seulement pour mail.tm et mail.gw
                    if prov_name in ('mailtm', 'mail_gw') and local_part:
                        if domain:
                            inbox = provider.create_inbox(domain=domain, local_part=local_part)
                        else:
                            inbox = provider.create_inbox(local_part=local_part)
                    elif domain:
                        inbox = provider.create_inbox(domain=domain)
                    else:
                        inbox = provider.create_inbox()
                    
                    created_inboxes.append(inbox)
                    provider_name = prov_name
                except Exception as e:
                    echo_cross(f"Échec pour {selected_domain}: {str(e)[:50]}")
                    continue
            
            if not created_inboxes:
                raise ProviderError("Aucun email créé")
            
            # [SECURISE] Ajouter type et date aux inboxes créées
            from datetime import datetime
            for inbox in created_inboxes:
                inbox.inbox_type = inbox_type
                inbox.created_at = datetime.now().isoformat()
                
                # [SECURISE] Chiffrer token pour long terme
                if inbox_type == "longterm" and inbox.token:
                    try:
                        from cryptography.fernet import Fernet
                        key = Fernet.generate_key()
                        f = Fernet(key)
                        inbox.token = f.encrypt(inbox.token.encode()).decode()
                        inbox._encryption_key = key.decode()
                    except:
                        pass  # Si cryptography pas installé
            
            # [SECURISE] Vérifier limite inboxes long terme (max 3)
            storage = InboxStorage()
            inboxes = storage.load()
            
            if inbox_type == "longterm":
                longterm_count = sum(1 for i in inboxes if i.inbox_type == "longterm")
                if longterm_count >= 3:
                    echo_cross("Limite de 3 inboxes long terme atteinte")
                    echo("  Supprimez une inbox long terme existante", fg=FG_GREY_PEARL)
                    return
            
            # 🗑️ Auto-suppression des inboxes temporaires expirées (>15min)
            current_time = datetime.now()
            expired_temp = []
            kept_inboxes = []
            for i in inboxes:
                if i.inbox_type == "temp" and i.created_at:
                    try:
                        created = datetime.fromisoformat(i.created_at)
                        if (current_time - created).total_seconds() > 900:  # 15min
                            expired_temp.append(i)
                            continue
                    except:
                        pass
                kept_inboxes.append(i)
            
            if expired_temp:
                echo(f"  {len(expired_temp)} inbox(s) temporaire(s) expirée(s) supprimée(s)", fg=FG_GREY_PEARL)
                inboxes = kept_inboxes
            
            # Ajouter nouvelles inboxes
            for inbox in created_inboxes:
                # Limiter à 5 inboxes maximum
                while len(inboxes) >= 5:
                    removed = inboxes.pop(0)
                    echo(f"  Limite de 5 atteinte, ancien email supprimé: {removed.address[:30]}...", fg=FG_GREY_PEARL)
                
                inboxes.append(inbox)
            
            storage.save(inboxes)
            
            click.echo()
            if len(created_inboxes) == 1:
                inbox = created_inboxes[0]
                echo_check(f"Adresse créée: {inbox.address}")
                echo(f"  Type: {styled(inbox_type.upper(), fg=FG_BLUE_NIGHT, bold=True)}", fg=FG_GREY_PEARL)
                echo(f"  Provider: {inbox.provider}", fg=FG_GREY_PEARL)
                if inbox_type == "longterm":
                    echo(f"  [SECURISE] Token chiffré", fg=FG_BLUE_NIGHT)
                else:
                    echo(f"  [TEMP] Expiration: 15 minutes", fg=FG_GREY_PEARL)
            else:
                echo_check(f"{len(created_inboxes)} adresses {inbox_type} créées:")
                for inbox in created_inboxes:
                    echo(f"  • {inbox.address}", fg=FG_RED_FLUO)
            
            echo(f"  Total: {len(inboxes)}/5 inboxes", fg=FG_GREY_PEARL)
            return

        elif provider_name == "auto":
            show_progress("Création d'une adresse (mode auto)")
            providers_to_try = ["mail_gw", "tempmail_io", "mailtm", "guerrillamail"]
            last_error = None
            
            inbox = None
            for prov_name in providers_to_try:
                try:
                    show_progress(f"Essai avec {prov_name}", duration=0.3)
                    provider = ProviderFactory.get_provider(prov_name)
                    inbox = provider.create_inbox()
                    
                    # [SECURISE] Ajouter type et date
                    inbox.inbox_type = inbox_type
                    inbox.created_at = datetime.now().isoformat()
                    
                    provider_name = prov_name
                    break
                except Exception as e:
                    last_error = e
                    echo(f"    {prov_name} indisponible", fg=FG_GREY_PEARL)
                    continue
            else:
                raise last_error or ProviderError("Aucun provider disponible")
            
            # [SECURISE] Mode auto: sauvegarder avec même logique
            if inbox:
                storage = InboxStorage()
                inboxes = storage.load()
                
                # Vérifier limite long terme
                if inbox_type == "longterm":
                    longterm_count = sum(1 for i in inboxes if i.inbox_type == "longterm")
                    if longterm_count >= 3:
                        echo_cross("Limite de 3 inboxes long terme atteinte")
                        return
                
                # Auto-suppression temp expirées
                current_time = datetime.now()
                kept_inboxes = []
                expired_count = 0
                for i in inboxes:
                    if i.inbox_type == "temp" and i.created_at:
                        try:
                            created = datetime.fromisoformat(i.created_at)
                            if (current_time - created).total_seconds() > 900:
                                expired_count += 1
                                continue
                        except:
                            pass
                    kept_inboxes.append(i)
                
                if expired_count:
                    echo(f"  {expired_count} inbox(s) temp(s) expirée(s) supprimée(s)", fg=FG_GREY_PEARL)
                    inboxes = kept_inboxes
                
                while len(inboxes) >= 5:
                    removed = inboxes.pop(0)
                    echo(f"  Limite de 5 atteinte, ancien email supprimé: {removed.address[:30]}...", fg=FG_GREY_PEARL)
                
                inboxes.append(inbox)
                storage.save(inboxes)
                
                click.echo()
                echo_check(f"[AUTO] Adresse créée: {inbox.address}")
                echo(f"  Type: {styled(inbox_type.upper(), fg=FG_BLUE_NIGHT, bold=True)}", fg=FG_GREY_PEARL)
                echo(f"  Provider: {inbox.provider}", fg=FG_GREY_PEARL)
                if inbox_type == "longterm":
                    echo(f"  [SECURISE] Token chiffré", fg=FG_BLUE_NIGHT)
                else:
                    echo(f"  [TEMP] Expiration: 15 minutes", fg=FG_GREY_PEARL)
                echo(f"  Total: {len(inboxes)}/5 inboxes", fg=FG_GREY_PEARL)
                return
        else:
            show_progress(f"Chargement de {provider_name}")
            provider = ProviderFactory.get_provider(provider_name)
            inbox = provider.create_inbox()
            
            # [SECURISE] Ajouter type et date
            inbox.inbox_type = inbox_type
            inbox.created_at = datetime.now().isoformat()
            
            storage = InboxStorage()
            inboxes = storage.load()
            
            # [SECURISE] Vérifier limite long terme pour mode auto
            if inbox_type == "longterm":
                longterm_count = sum(1 for i in inboxes if i.inbox_type == "longterm")
                if longterm_count >= 3:
                    echo_cross("Limite de 3 inboxes long terme atteinte")
                    return
            
            # 🗑️ Auto-suppression temp expirées
            current_time = datetime.now()
            kept_inboxes = []
            expired_count = 0
            for i in inboxes:
                if i.inbox_type == "temp" and i.created_at:
                    try:
                        created = datetime.fromisoformat(i.created_at)
                        if (current_time - created).total_seconds() > 900:
                            expired_count += 1
                            continue
                    except:
                        pass
                kept_inboxes.append(i)
            
            if expired_count:
                echo(f"  {expired_count} inbox(s) temp(s) expirée(s) supprimée(s)", fg=FG_GREY_PEARL)
                inboxes = kept_inboxes
            
            while len(inboxes) >= 5:
                removed = inboxes.pop(0)
                echo(f"  Limite de 5 atteinte, ancien email supprimé: {removed.address[:30]}...", fg=FG_GREY_PEARL)
            
            inboxes.append(inbox)
            storage.save(inboxes)
            
            click.echo()
            echo_check(f"Adresse créée: {inbox.address}")
            echo(f"  Type: {styled(inbox_type.upper(), fg=FG_BLUE_NIGHT, bold=True)}", fg=FG_GREY_PEARL)
            echo(f"  Provider: {inbox.provider}", fg=FG_GREY_PEARL)
            if inbox_type == "longterm":
                echo(f"  [SECURISE] Token chiffré", fg=FG_BLUE_NIGHT)
            else:
                echo(f"  [TEMP] Expiration: 15 minutes", fg=FG_GREY_PEARL)
            echo(f"  Total: {len(inboxes)}/5 inboxes", fg=FG_GREY_PEARL)

    except Exception as e:
        echo_cross(f"Échec de création: {str(e)}")


def handle_inbox():
    """Handle the 'inbox' command."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        echo_cross("Aucune adresse email active.")
        echo("  Utilisez 'new' pour créer une nouvelle adresse.", fg=FG_GREY_PEARL)
        return

    try:
        show_progress(f"Récupération des messages pour {active_inbox.address[:25]}...")

        provider = ProviderFactory.get_provider(active_inbox.provider)
        messages = provider.get_messages(active_inbox)

        if not messages:
            click.echo()
            echo("  Aucun message reçu", fg=FG_GREY_PEARL)
            return

        click.echo()
        echo(f"  {len(messages)} message(s) reçu(s):", bold=True)
        click.echo()

        for msg in messages:
            click.echo(f"    ID: {styled(msg.id, fg=FG_RED_FLUO, bold=True)}")
            click.echo(f"    De: {msg.sender}")
            click.echo(f"    Sujet: {msg.subject}")
            click.echo(f"    Date: {msg.date}")
            click.echo()

    except Exception as e:
        echo_cross(f"Erreur: {str(e)}")


def handle_read(message_id):
    """Handle the 'read' command."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        echo_cross("Aucune adresse email active.")
        return

    try:
        show_progress(f"Lecture du message {message_id[:15]}...")

        provider = ProviderFactory.get_provider(active_inbox.provider)
        message = provider.read_message(active_inbox, message_id)

        if not message:
            echo_cross(f"Message {message_id} introuvable")
            return

        click.echo()
        echo_separator()
        echo(f"  De: {message.sender}", bold=True)
        echo(f"  Sujet: {message.subject}", bold=True)
        echo(f"  Date: {message.date}", fg=FG_GREY_PEARL)
        echo_separator()
        click.echo()
        click.echo(message.body or "(pas de contenu)")
        click.echo()
        echo_separator()

    except Exception as e:
        echo_cross(f"Erreur: {str(e)}")


def handle_status():
    """Handle the 'status' command."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        click.echo()
        echo("  Aucune adresse email active", fg=FG_GREY_PEARL)
        echo("  Utilisez 'new' pour créer une nouvelle adresse", fg=FG_GREY_PEARL)
        return

    click.echo()
    echo("  Adresse active:", bold=True)
    click.echo()
    click.echo(f"    Email: {styled(active_inbox.address, fg=FG_RED_FLUO, bold=True)}")
    click.echo(f"    Provider: {active_inbox.provider}")
    if active_inbox.token:
        click.echo(f"    Token: {active_inbox.token}")
        click.echo()


def handle_check(email: str):
    """Handle the 'check' command - validate email with Disify."""
    from mailaka.core.provider import validate_email_disify
    
    show_progress(f"Validation de {email}")
    
    result = validate_email_disify(email)
    
    click.echo()
    echo(f"  Résultat pour {styled(email, fg=FG_RED_FLUO, bold=True)}:", bold=True)
    click.echo()
    
    # Format valid
    if result.get("format"):
        echo_check("Format valide")
    else:
        echo_cross("Format invalide")
    
    # DNS/MX records
    if result.get("dns"):
        echo_check("Domaine avec enregistrements MX")
    else:
        echo_cross("Domaine sans MX (peut ne pas recevoir d'emails)")
    
    # Disposable check
    if result.get("disposable"):
        echo_cross("[WARN] Domaine temporaire/disposable détecté")
    else:
        echo_check("Domaine non-temporaire (probablement légitime)")
    
    if "error" in result:
        echo_cross(f"Erreur: {result['error']}")


def handle_export(filepath: str):
    """Handle the 'export' command - backup all inboxes to JSON."""
    import json
    from datetime import datetime
    
    storage = InboxStorage()
    inboxes = storage.load()
    
    if not inboxes:
        echo_cross("Aucune inbox à exporter")
        return
    
    try:
        data = {
            "exported_at": datetime.now().isoformat(),
            "count": len(inboxes),
            "inboxes": [
                {
                    "address": inbox.address,
                    "provider": inbox.provider,
                    "token": inbox.token,
                }
                for inbox in inboxes
            ]
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        echo_check(f"{len(inboxes)} inbox(s) exportée(s) vers {filepath}")
        
    except Exception as e:
        echo_cross(f"Échec export: {str(e)}")


def handle_import(filepath: str):
    """Handle the 'import' command - restore inboxes from JSON."""
    import json
    
    if not os.path.exists(filepath):
        echo_cross(f"Fichier non trouvé: {filepath}")
        return
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        inboxes_data = data.get("inboxes", [])
        if not inboxes_data:
            echo_cross("Aucune inbox trouvée dans le fichier")
            return
        
        storage = InboxStorage()
        existing = storage.load()
        
        imported = 0
        skipped = 0
        
        for inbox_data in inboxes_data:
            # Vérifier si déjà existe
            if any(i.address == inbox_data["address"] for i in existing):
                skipped += 1
                continue
            
            # Créer l'inbox
            from mailaka.core.models import Inbox
            inbox = Inbox(
                address=inbox_data["address"],
                provider=inbox_data["provider"],
                token=inbox_data.get("token", ""),
            )
            existing.append(inbox)
            imported += 1
        
        # Limiter à 5 maximum
        while len(existing) > 5:
            removed = existing.pop(0)
            echo(f"  Limite de 5 atteinte, ancienne inbox supprimée: {removed.address[:30]}...", fg=FG_GREY_PEARL)
        
        storage.save(existing)
        
        echo_check(f"Importé: {imported} | Déjà existant: {skipped} | Total: {len(existing)}/5")
        
    except json.JSONDecodeError:
        echo_cross("Fichier JSON invalide")
    except Exception as e:
        echo_cross(f"Échec import: {str(e)}")


def handle_delete(message_id):
    """Handle the 'delete' command for messages."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        echo_cross("Aucune adresse email active.")
        return

    try:
        show_progress(f"Suppression du message {message_id[:15]}...")

        provider = ProviderFactory.get_provider(active_inbox.provider)
        provider.delete_message(active_inbox, message_id)

        echo_check(f"Message {message_id} supprimé")

    except Exception as e:
        echo_cross(f"Erreur: {str(e)}")


def handle_delete_inbox(email_address):
    """Handle the deletion of an inbox by email address."""
    storage = InboxStorage()
    inboxes = storage.load()
    
    # Chercher l'inbox avec cette adresse
    inbox_to_delete = None
    for inbox in inboxes:
        if inbox.address == email_address:
            inbox_to_delete = inbox
            break
    
    if not inbox_to_delete:
        echo_cross(f"Aucune inbox trouvée avec l'adresse: {email_address}")
        echo("  Voir les inboxes sauvegardées avec: inboxes", fg=FG_GREY_PEARL)
        return
    
    try:
        show_progress(f"Suppression de l'inbox {email_address[:20]}...")

        # Retirer cette inbox de la liste
        inboxes.remove(inbox_to_delete)
        storage.save(inboxes)
        
        echo_check(f"Inbox {email_address} supprimée du stockage local")
        
    except Exception as e:
        echo_cross(f"Erreur: {str(e)}")


def handle_attachments(message_id):
    """Handle the 'attachments' command - list and auto-download all attachments."""
    # Debug: Vérifier le message_id complet
    echo(f"  DEBUG: message_id reçu = '{message_id}' (len={len(message_id)})", fg=FG_GREY_PEARL)
    
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        echo_cross("Aucune adresse email active.")
        return

    try:
        show_progress(f"Récupération des pièces jointes...")

        provider = ProviderFactory.get_provider(active_inbox.provider)
        attachments = provider.get_attachments(active_inbox, message_id)

        if not attachments:
            echo("  Aucune pièce jointe", fg=FG_GREY_PEARL)
            return

        click.echo()
        echo(f"  {len(attachments)} pièce(s) jointe(s) trouvée(s):", bold=True)
        click.echo()

        for att in attachments:
            # Handle both dict and object formats
            if isinstance(att, dict):
                filename = att.get('filename', att.get('name', 'unknown'))
                size = att.get('size', att.get('bytes', 0))
                att_id = att.get('id', att.get('attachment_id', ''))
            else:
                filename = getattr(att, 'filename', getattr(att, 'name', 'unknown'))
                size = getattr(att, 'size', getattr(att, 'bytes', 0))
                att_id = getattr(att, 'id', getattr(att, 'attachment_id', ''))
            
            # Debug: show what we're working with
            if not att_id:
                echo_cross(f"    Pas d'ID pour: {filename}")
                if isinstance(att, dict):
                    echo(f"      Clés disponibles: {list(att.keys())}", fg=FG_GREY_PEARL)
                continue
            
            click.echo(f"    [PJ] {styled(filename, fg=FG_RED_FLUO, bold=True)} ({size:,} bytes) [ID: {att_id}]")
            
            # Auto-download all attachments
            try:
                echo(f"    DEBUG: DL msg_id={message_id} (len={len(message_id)}), att_id={att_id}", fg=FG_GREY_PEARL)
                data = provider.download_attachment(active_inbox, message_id, att_id)
                if data:
                    # Sanitize filename
                    safe_filename = "".join(c for c in filename if c.isalnum() or c in "._- ").strip()
                    if not safe_filename:
                        safe_filename = f"attachment_{att_id[:10]}"
                    with open(safe_filename, 'wb') as f:
                        f.write(data)
                    echo_check(f"    Téléchargé: ./{safe_filename} ({len(data)} bytes)")
                else:
                    echo_cross(f"    Échec {filename}: pas de données")
            except Exception as e:
                echo_cross(f"    Échec {filename}: {str(e)[:80]}")
        
        click.echo()
        echo(f"  Tous les fichiers téléchargés dans: {os.getcwd()}", fg=FG_GREY_PEARL)

    except Exception as e:
        echo_cross(f"Erreur: {str(e)}")


def handle_download(message_id):
    """Handle the 'download' command - download all attachments for a message."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        echo_cross("Aucune adresse email active.")
        return

    try:
        show_progress(f"Téléchargement des pièces jointes...")

        provider = ProviderFactory.get_provider(active_inbox.provider)
        attachments = provider.get_attachments(active_inbox, message_id)

        if not attachments:
            echo("  Aucune pièce jointe à télécharger", fg=FG_GREY_PEARL)
            return

        click.echo()
        echo(f"  {len(attachments)} fichier(s) à télécharger:", bold=True)
        click.echo()

        for att in attachments:
            # Handle both dict and object formats
            if isinstance(att, dict):
                filename = att.get('filename', att.get('name', 'unknown'))
                att_id = att.get('id', att.get('attachment_id', ''))
            else:
                filename = getattr(att, 'filename', getattr(att, 'name', 'unknown'))
                att_id = getattr(att, 'id', getattr(att, 'attachment_id', ''))
            
            try:
                data = provider.download_attachment(active_inbox, message_id, att_id)
                if data:
                    with open(filename, 'wb') as f:
                        f.write(data)
                    echo_check(f"  [DL] {filename}")
                else:
                    echo_cross(f"  ❌ {filename}: pas de données")
            except Exception as e:
                echo_cross(f"  ❌ {filename}: {str(e)[:40]}")
        
        click.echo()
        echo(f"  Fichiers dans: {os.getcwd()}", fg=FG_GREY_PEARL)

    except Exception as e:
        echo_cross(f"Erreur: {str(e)}")


def handle_inboxes():
    """Handle the 'inboxes' command."""
    from datetime import datetime
    
    storage = InboxStorage()
    inboxes = storage.get_all()
    
    # 🗑️ Auto-suppression des temporaires expirés à l'affichage
    current_time = datetime.now()
    kept_inboxes = []
    expired_count = 0
    
    for inbox in inboxes:
        if inbox.inbox_type == "temp" and inbox.created_at:
            try:
                created = datetime.fromisoformat(inbox.created_at)
                elapsed = (current_time - created).total_seconds()
                if elapsed > 900:  # 15 minutes
                    expired_count += 1
                    continue  # Skip expired
                remaining_min = int((900 - elapsed) / 60)
                inbox._remaining = remaining_min  # Temporary attribute
            except:
                inbox._remaining = None
        kept_inboxes.append(inbox)
    
    # Sauvegarder si des inboxes ont été supprimées
    if expired_count > 0:
        storage.save(kept_inboxes)
        echo(f"  🗑️ {expired_count} inbox(s) temporaire(s) expirée(s) supprimée(s)", fg=FG_GREY_PEARL)
        inboxes = kept_inboxes
    
    if not inboxes:
        echo("  Aucune inbox sauvegardée", fg=FG_GREY_PEARL)
        return

    click.echo()
    echo(f"  {len(inboxes)} inbox(s) sauvegardée(s):", bold=True)
    echo("  Commande 'note <numero>' pour gérer les notes", fg=FG_GREY_PEARL)
    click.echo()

    for idx, inbox in enumerate(inboxes, 1):
        is_active = " (active)" if inbox == storage.get_latest() else ""
        
        # Déterminer type et affichage
        inbox_type = getattr(inbox, 'inbox_type', 'temp')
        if inbox_type == "longterm":
            type_indicator = styled("[SECURISE] LONG", fg=FG_BLUE_NIGHT, bold=True)
        else:
            remaining = getattr(inbox, '_remaining', None)
            if remaining is not None:
                type_indicator = styled(f"[TEMP] {remaining}min", fg=FG_GREY_PEARL)
            else:
                type_indicator = styled("[TEMP] TEMP", fg=FG_GREY_PEARL)
        
        click.echo(f"    [{styled(str(idx), fg=FG_RED_FLUO, bold=True)}] {styled(inbox.address, fg=FG_RED_FLUO, bold=True)} {type_indicator}{is_active}")
        click.echo(f"      Provider: {inbox.provider}")
        if inbox.comment:
            click.echo(f"      Note: {styled(inbox.comment, fg=FG_BLUE_NIGHT, bold=True)}")
        click.echo()


def handle_note(args):
    """Handle the 'note' command to add/edit comment on an inbox."""
    if not args:
        echo_cross("Usage: note \u003cnumero_inbox\u003e [texte_de_la_note]")
        echo("  Ex: note 1 'Pour inscription Spotify'", fg=FG_GREY_PEARL)
        echo("  Ex: note 2 (pour effacer la note)", fg=FG_GREY_PEARL)
        return
    
    storage = InboxStorage()
    inboxes = storage.load()
    
    if not inboxes:
        echo_cross("Aucune inbox à annoter")
        return
    
    try:
        idx = int(args[0])
        if idx < 1 or idx > len(inboxes):
            echo_cross(f"Numéro invalide. Range: 1-{len(inboxes)}")
            return
        
        inbox = inboxes[idx - 1]
        
        # Si texte fourni directement
        if len(args) > 1:
            comment = " ".join(args[1:])
        else:
            # Demander interactivement
            current = inbox.comment or ""
            if current:
                echo(f"  Note actuelle: {current}", fg=FG_GREY_PEARL)
            comment = click.prompt(
                styled("  Nouvelle note (vide pour effacer)", fg=FG_RED_FLUO, bold=True),
                prompt_suffix=" ",
                default=current,
                show_default=False
            ).strip()
        
        # Mettre à jour la note
        inbox.comment = comment if comment else None
        storage.save(inboxes)
        
        if inbox.comment:
            echo_check(f"Note ajoutée pour {inbox.address}")
            echo(f"  Note: {inbox.comment}", fg=FG_BLUE_NIGHT)
        else:
            echo_check(f"Note effacée pour {inbox.address}")
        
    except ValueError:
        echo_cross("Entrez un numéro valide")


def _select_message_interactive():
    """Show inbox messages and let user select one by number."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        echo_cross("Aucune adresse email active.")
        return None

    try:
        show_progress("Chargement des messages")

        provider = ProviderFactory.get_provider(active_inbox.provider)
        messages = provider.get_messages(active_inbox)

        if not messages:
            click.echo()
            echo("  Aucun message reçu", fg=FG_GREY_PEARL)
            return None

        click.echo()
        echo(f"  {len(messages)} message(s) disponible(s):", bold=True)
        click.echo()

        # Afficher la liste numérotée
        for idx, msg in enumerate(messages, 1):
            click.echo(f"    [{styled(str(idx), fg=FG_RED_FLUO, bold=True)}] {styled(msg.id[:20] + '...', fg=FG_GREY_PEARL)}")
            click.echo(f"        De: {msg.sender}")
            click.echo(f"        Sujet: {msg.subject or '(sans sujet)'}")
            click.echo(f"        Date: {msg.date}")
            click.echo()

        # Demander la sélection
        selected = click.prompt(
            styled("  Entrez le numéro du message", fg=FG_RED_FLUO, bold=True),
            prompt_suffix=" ",
            default="",
            show_default=False
        ).strip()

        if not selected:
            return None

        try:
            idx = int(selected)
            if 1 <= idx <= len(messages):
                return messages[idx - 1].id
            else:
                echo_cross(f"Numéro invalide. Choisissez entre 1 et {len(messages)}")
                return None
        except ValueError:
            echo_cross("Entrez un numéro valide")
            return None

    except Exception as e:
        echo_cross(f"Erreur: {str(e)}")
        return None


def handle_read_interactive():
    """Handle read with interactive selection."""
    message_id = _select_message_interactive()
    if message_id:
        handle_read(message_id)


def handle_delete_interactive():
    """Handle delete with menu selection and multiple choice."""
    click.echo()
    echo("  Que voulez-vous supprimer ?", bold=True)
    click.echo()
    click.echo(f"    [{styled('1', fg=FG_RED_FLUO, bold=True)}] Supprimer des messages")
    click.echo(f"    [{styled('2', fg=FG_RED_FLUO, bold=True)}] Supprimer des emails (inboxes)")
    click.echo()
    
    choice = click.prompt(
        styled("  Votre choix", fg=FG_RED_FLUO, bold=True),
        prompt_suffix=" ",
        default="",
        show_default=False
    ).strip()
    
    if choice == "1":
        # Suppression multiple de messages
        messages = _select_messages_interactive_multiple()
        if messages:
            click.echo()
            echo_check(f"{len(messages)} message(s) à supprimer")
            for msg_id in messages:
                try:
                    handle_delete(msg_id)
                except Exception as e:
                    echo_cross(f"Échec suppression {msg_id}: {str(e)[:30]}")
    elif choice == "2":
        # Afficher les inboxes disponibles
        storage = InboxStorage()
        inboxes = storage.load()
        
        if not inboxes:
            echo_cross("Aucune inbox à supprimer")
            return
        
        click.echo()
        echo("  Inboxes disponibles:", bold=True)
        echo("  Syntaxe: 1,3 ou 2-4 ou 1,3-5 (plusieurs)", fg=FG_GREY_PEARL)
        click.echo()
        for idx, inbox in enumerate(inboxes, 1):
            is_active = " (active)" if inbox == storage.get_latest() else ""
            click.echo(f"    [{styled(str(idx), fg=FG_RED_FLUO, bold=True)}] {inbox.address}{is_active}")
        click.echo()
        
        selected = click.prompt(
            styled("  Numéro(s) des inboxes à supprimer", fg=FG_RED_FLUO, bold=True),
            prompt_suffix=" ",
            default="",
            show_default=False
        ).strip()
        
        indices = parse_selection(selected, len(inboxes))
        if indices:
            click.echo()
            echo_check(f"{len(indices)} inbox(s) à supprimer")
            for idx in indices:
                try:
                    handle_delete_inbox(inboxes[idx].address)
                except Exception as e:
                    echo_cross(f"Échec suppression inbox {idx+1}: {str(e)[:30]}")
        else:
            echo_cross("Entrez des numéros valides")
    else:
        echo_cross("Choix invalide")


def handle_attachments_interactive():
    """Handle attachments with interactive selection."""
    message_id = _select_message_interactive()
    if message_id:
        handle_attachments(message_id)


def handle_download_interactive():
    """Handle download with interactive selection."""
    message_id = _select_message_interactive()
    if message_id:
        handle_download(message_id)


def _select_messages_interactive_multiple():
    """Show inbox messages and let user select multiple by numbers."""
    storage = InboxStorage()
    active_inbox = storage.get_latest()

    if not active_inbox:
        echo_cross("Aucune adresse email active.")
        return []

    try:
        show_progress("Chargement des messages")

        provider = ProviderFactory.get_provider(active_inbox.provider)
        messages = provider.get_messages(active_inbox)

        if not messages:
            click.echo()
            echo("  Aucun message reçu", fg=FG_GREY_PEARL)
            return []

        click.echo()
        echo(f"  {len(messages)} message(s) disponible(s):", bold=True)
        echo("  Syntaxe: 1,3 ou 2-4 ou 1,3-5 (plusieurs messages)", fg=FG_GREY_PEARL)
        click.echo()

        # Afficher la liste numérotée
        for idx, msg in enumerate(messages, 1):
            click.echo(f"    [{styled(str(idx), fg=FG_RED_FLUO, bold=True)}] {styled(msg.id[:20] + '...', fg=FG_GREY_PEARL)}")
            click.echo(f"        De: {msg.sender}")
            click.echo(f"        Sujet: {msg.subject or '(sans sujet)'}")
            click.echo(f"        Date: {msg.date}")
            click.echo()

        # Demander la sélection
        selected = click.prompt(
            styled("  Numéro(s) des messages", fg=FG_RED_FLUO, bold=True),
            prompt_suffix=" ",
            default="",
            show_default=False
        ).strip()

        indices = parse_selection(selected, len(messages))
        if indices:
            return [messages[idx].id for idx in indices]
        else:
            echo_cross("Sélection invalide")
            return []

    except Exception as e:
        echo_cross(f"Erreur: {str(e)}")
        return []
