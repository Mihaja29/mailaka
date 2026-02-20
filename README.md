# Mailaka

**Générateur d'emails éphémères en ligne de commande pour protéger votre vie privée.**

![Version](https://img.shields.io/badge/version-1.0.0-red)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Fonctionnalités

- 🔒 **Sécurisé** - Chiffrement des tokens API
- 📧 **Multi-providers** - mail.tm, mail.gw, GuerrillaMail, tempmail.io
- 🖥️ **Cross-platform** - Linux, macOS, Windows
- 💻 **Mode interactif** - Interface utilisateur élégante
- 📎 **Pièces jointes** - Téléchargement supporté
- 🔄 **Export/Import** - JSON pour portabilité

## 📦 Installation

### 🐧 Linux / 🍎 macOS (via script)

```bash
curl -sSL https://raw.githubusercontent.com/Mihaja29/mailaka/main/install.sh | bash
```

Ou manuellement :
```bash
# Télécharger le binaire
wget https://github.com/Mihaja29/mailaka/releases/latest/download/mailaka-linux
chmod +x mailaka-linux
sudo mv mailaka-linux /usr/local/bin/mailaka
```

### 🪟 Windows (via PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -Command "Invoke-Expression (Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Mihaja29/mailaka/main/install.ps1').Content"
```

Ou manuellement :
1. Télécharger `mailaka-windows.exe` depuis les [releases](https://github.com/Mihaja29/mailaka/releases)
2. Renommer en `mailaka.exe`
3. Ajouter au PATH

### 🐍 Via pip (toutes plateformes)

```bash
pip install mailaka
```

### 📦 Via Git (développement)

```bash
git clone https://github.com/Mihaja29/mailaka.git
cd mailaka
pip install -e .
```

## 🚀 Utilisation rapide

```bash
# Créer une adresse
mailaka new

# Voir les messages
mailaka inbox

# Lire un message
mailaka read <message-id>

# Mode interactif (recommandé)
mailaka
```

## 📚 Commandes disponibles

| Commande | Description |
|----------|-------------|
| `mailaka new` | Créer une adresse temporaire |
| `mailaka inbox` | Lister les messages reçus |
| `mailaka inboxes` | Lister toutes les inboxes |
| `mailaka read <id>` | Lire un message |
| `mailaka delete <id>` | Supprimer un message |
| `mailaka attachments <id>` | Voir les pièces jointes |
| `mailaka status` | Statut de l'adresse active |
| `mailaka export` | Exporter vers JSON |
| `mailaka import <fichier>` | Importer depuis JSON |
| `mailaka version` | Afficher la version |

## 🏗️ Architecture

```
mailaka/
├── mailaka/              # Package principal
│   ├── commands/         # Commandes CLI
│   ├── core/             # Logique métier
│   │   ├── provider.py   # Gestion providers
│   │   ├── storage.py    # Stockage local
│   │   └── models.py     # Modèles
│   ├── interactive.py    # Mode interactif
│   └── utils/            # Utilitaires
├── tests/                # Tests
├── install.sh            # Install Linux/macOS
├── install.ps1           # Install Windows
└── pyproject.toml        # Configuration
```

## 🔧 Développement

```bash
# Setup
git clone https://github.com/Mihaja29/mailaka.git
cd mailaka
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Tests
pytest

# Lint
ruff check .

# Build binaires
pyinstaller --onefile mailaka/cli.py
```

## 🌐 Providers supportés

| Provider | Domaines | PJ | Notes |
|----------|----------|-----|-------|
| mail.tm | @dollicons.com, etc. | ✅ | Personnalisable |
| mail.gw | @oakon.com, etc. | ✅ | Personnalisable |
| GuerrillaMail | @guerrillamailblock.com | ✅ | Fiable |
| tempmail.io | 10+ domaines | ❌ | Simple |

## 🤝 Contribution

```bash
# Fork → Clone → Branch → Commit → PR
git checkout -b feature/ma-feature
git commit -m "Add ma feature"
git push origin feature/ma-feature
```

## 📄 License

MIT License - voir [LICENSE](LICENSE)

## ⚠️ Avertissement

**Ne pas utiliser** pour services sensibles (banques, gouvernement, etc.).  
Destiné à la protection anti-spam et vie privée temporaire.

---

**Made with 🦞 by Mihaja**
