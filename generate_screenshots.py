"""Generate screenshot mockups for Mailaka project."""

from PIL import Image, ImageDraw, ImageFont
import os

def create_terminal_screenshot(filename, title, lines, width=800, height=500):
    """Create a terminal-style screenshot."""
    # Colors
    bg_color = (30, 30, 30)  # Dark terminal background
    text_color = (224, 224, 224)  # Light grey
    red_color = (255, 51, 51)  # Red fluo
    blue_color = (100, 149, 237)  # Cornflower blue for prompts
    green_color = (50, 205, 50)  # Green for success
    
    # Create image
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a monospace font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 14)
        except:
            font = ImageFont.load_default()
    
    # Draw window title bar
    draw.rectangle([(0, 0), (width, 30)], fill=(60, 60, 60))
    draw.text((10, 8), title, fill=text_color, font=font)
    
    # Draw close buttons
    draw.ellipse([(width-25, 8), (width-15, 18)], fill=(255, 59, 48))  # Red
    draw.ellipse([(width-45, 8), (width-35, 18)], fill=(255, 204, 0))  # Yellow
    draw.ellipse([(width-65, 8), (width-55, 18)], fill=(40, 205, 65))  # Green
    
    # Draw content
    y = 50
    for line in lines:
        text = line['text']
        color = line.get('color', text_color)
        
        # Handle ANSI-like color codes in text
        if '[RED]' in text:
            parts = text.split('[RED]')
            draw.text((20, y), parts[0], fill=text_color, font=font)
            draw.text((20 + len(parts[0]) * 8, y), parts[1], fill=red_color, font=font)
        elif '[BLUE]' in text:
            parts = text.split('[BLUE]')
            draw.text((20, y), parts[0], fill=text_color, font=font)
            draw.text((20 + len(parts[0]) * 8, y), parts[1], fill=blue_color, font=font)
        elif '[GREEN]' in text:
            parts = text.split('[GREEN]')
            draw.text((20, y), parts[0], fill=text_color, font=font)
            draw.text((20 + len(parts[0]) * 8, y), parts[1], fill=green_color, font=font)
        else:
            draw.text((20, y), text, fill=color, font=font)
        
        y += 22
    
    # Save
    img.save(filename)
    print(f"✅ Created: {filename}")

# Screenshot 1: Welcome banner and help
create_terminal_screenshot(
    'screenshots/01-welcome.png',
    'mailaka --help',
    [
        {'text': '  ███╗   ███╗ █████╗ ██╗██╗      █████╗ ██╗  ██╗', 'color': (255, 51, 51)},
        {'text': '  ████╗ ████║██╔══██╗██║██║     ██╔══██╗██║ ██╔╝', 'color': (255, 51, 51)},
        {'text': '  ██╔████╔██║███████║██║██║     ███████║█████╔╝ ', 'color': (255, 51, 51)},
        {'text': '  ════════════════════════════════════════════', 'color': (100, 100, 100)},
        {'text': ''},
        {'text': '  Commandes disponibles:', 'color': (255, 255, 255)},
        {'text': ''},
        {'text': '    new              Créer adresse(s) [TEMP: 15min | LONG: 🔒 sécurisé]'},
        {'text': '    inbox            Voir les messages reçus'},
        {'text': '    read             Lire un message'},
        {'text': '    delete           Supprimer messages/inboxes (1,2-4)'},
        {'text': '    attachments      Voir + télécharger pièces jointes'},
        {'text': '    status           Afficher adresse active'},
        {'text': '    inboxes          Lister toutes les inboxes'},
        {'text': '    export           Exporter vers JSON'},
        {'text': '    import           Importer depuis JSON'},
        {'text': '    clear            Effacer l\'écran'},
        {'text': '    exit             Quitter'},
        {'text': ''},
        {'text': '  Commande inconnue = quitte Mailaka', 'color': (150, 150, 150)},
    ]
)

# Screenshot 2: Creating new email
create_terminal_screenshot(
    'screenshots/02-create-email.png',
    'mailaka new',
    [
        {'text': '  ███╗   ███╗ █████╗ ██╗  █████╗ ██╗  ██╗', 'color': (255, 51, 51)},
        {'text': '  ═════════════════════════════════════', 'color': (100, 100, 100)},
        {'text': ''},
        {'text': '  Adresse actuelle: [RED]test@dollicons.com'},
        {'text': '  Provider: mail.tm'},
        {'text': '  Expire dans: 14:58 minutes'},
        {'text': ''},
        {'text': '  ═════════════════════════════════════', 'color': (100, 100, 100)},
        {'text': ''},
        {'text': '  [GREEN]✓ Adresse créée avec succès!'},
        {'text': ''},
        {'text': '  📧 Adresse: test@dollicons.com'},
        {'text': '  🔑 Token: eyJhbGciOi... (chiffré)'},
        {'text': '  ⏱️  Durée: TEMP (15 minutes)'},
        {'text': ''},
        {'text': '  Utilisez [BLUE]inbox pour voir les messages'},
    ]
)

# Screenshot 3: Reading inbox
create_terminal_screenshot(
    'screenshots/03-inbox.png',
    'mailaka inbox',
    [
        {'text': '  📧 Inbox: test@dollicons.com'},
        {'text': '  ════════════════════════════════════════', 'color': (100, 100, 100)},
        {'text': ''},
        {'text': '  1. [RED]Bienvenue sur notre service!'},
        {'text': '     De: noreply@example.com'},
        {'text': '     Il y a 2 minutes'},
        {'text': ''},
        {'text': '  2. [RED]Code de vérification: 123456'},
        {'text': '     De: verify@app.com'},
        {'text': '     Il y a 5 minutes'},
        {'text': ''},
        {'text': '  ════════════════════════════════════════', 'color': (100, 100, 100)},
        {'text': ''},
        {'text': '  📊 Total: 2 messages'},
        {'text': '  📎 Pièces jointes: disponibles'},
        {'text': ''},
        {'text': '  Utilisez [BLUE]read <id> pour lire un message'},
    ]
)

# Screenshot 4: Interactive mode
create_terminal_screenshot(
    'screenshots/04-interactive.png',
    'mailaka (mode interactif)',
    [
        {'text': '  ════════════════════════════════════════', 'color': (100, 100, 100)},
        {'text': '  Mode interactif - tapez une commande'},
        {'text': '  ════════════════════════════════════════', 'color': (100, 100, 100)},
        {'text': ''},
        {'text': '[RED]mailaka> new'},
        {'text': '  🔧 Création adresse mail.tm...'},
        {'text': '  [GREEN]✓ Adresse: user@teihu.com'},
        {'text': ''},
        {'text': '[RED]mailaka> inbox'},
        {'text': '  📥 Vérification messages...'},
        {'text': '  Aucun message reçu'},
        {'text': ''},
        {'text': '[RED]mailaka> status'},
        {'text': '  📧 Adresse active: user@teihu.com'},
        {'text': '  ⏱️  Expiration: 12:34'},
        {'text': '  🔒 Sécurité: Token chiffré'},
        {'text': ''},
        {'text': '[RED]mailaka> exit'},
        {'text': '  👋 Au revoir!'},
    ]
)

print("✅ Tous les screenshots générés dans screenshots/")