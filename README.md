# Mailaka

Generateur d'emails ephemeres en ligne de commande pour proteger votre vie privee.

![Version](https://img.shields.io/badge/version-1.0.0-red)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Fonctionnalites

- Securise - Chiffrement des tokens API
- Multi-providers - mail.tm, mail.gw, GuerrillaMail, tempmail.io
- Cross-platform - Linux, macOS, Windows
- Mode interactif - Interface utilisateur elegante
- Pieces jointes - Telechargement supporte
- Export/Import - JSON pour portabilite

## Installation

### Linux / macOS

```bash
curl -sSL https://raw.githubusercontent.com/Mihaja29/mailaka/main/install.sh | bash
```

Ou manuellement :
```bash
wget https://github.com/Mihaja29/mailaka/releases/latest/download/mailaka-linux
chmod +x mailaka-linux
sudo mv mailaka-linux /usr/local/bin/mailaka
```

### Windows

```powershell
powershell -ExecutionPolicy Bypass -Command "Invoke-Expression (Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Mihaja29/mailaka/main/install.ps1').Content"
```

Ou manuellement :
1. Telecharger `mailaka-windows.exe` depuis les [releases](https://github.com/Mihaja29/mailaka/releases)
2. Renommer en `mailaka.exe`
3. Ajouter au PATH

### Via pip

```bash
pip install mailaka
```

### Via npm / pnpm (depuis GitHub)

```bash
# Avec npm
npm install -g Mihaja29/mailaka

# Avec pnpm (plus rapide, moins d'espace disque)
pnpm install -g Mihaja29/mailaka

# Ou avec npx (sans installation globale)
npx Mihaja29/mailaka
```

**Note:** Le paquet n'est pas encore publié sur npm registry. L'installation se fait directement depuis GitHub.

### Via Git

```bash
git clone https://github.com/Mihaja29/mailaka.git
cd mailaka
pip install -e .
```

## Utilisation rapide

```bash
mailaka new           # Creer une adresse
mailaka inbox         # Voir les messages
mailaka read id       # Lire un message
mailaka               # Mode interactif
```

## Commandes disponibles

| Commande | Description |
|----------|-------------|
| `mailaka new` | Creer une adresse temporaire |
| `mailaka inbox` | Lister les messages recus |
| `mailaka inboxes` | Lister toutes les inboxes |
| `mailaka read id` | Lire un message |
| `mailaka delete id` | Supprimer un message |
| `mailaka attachments id` | Voir les pieces jointes |
| `mailaka status` | Statut de l'adresse active |
| `mailaka export` | Exporter vers JSON |
| `mailaka import fichier` | Importer depuis JSON |
| `mailaka version` | Afficher la version |

## Architecture

```
mailaka/
├── mailaka/
│   ├── commands/
│   ├── core/
│   ├── interactive.py
│   └── utils/
├── tests/
├── install.sh
├── install.ps1
└── pyproject.toml
```

## Development

```bash
git clone https://github.com/Mihaja29/mailaka.git
cd mailaka
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

pytest
ruff check .
```

## Providers supportes

| Provider | Domaines | PJ | Notes |
|----------|----------|-----|-------|
| mail.tm | @dollicons.com | Oui | Personnalisable |
| mail.gw | @oakon.com | Oui | Personnalisable |
| GuerrillaMail | @guerrillamailblock.com | Oui | Fiable |
| tempmail.io | 10+ domaines | Non | Simple |

## License

MIT License - voir [LICENSE](LICENSE)

## Avertissement

Ne pas utiliser pour services sensibles (banques, gouvernement).  
Destine a la protection anti-spam et vie privee temporaire.
