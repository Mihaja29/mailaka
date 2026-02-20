# Mailaka

**Générateur d'emails éphémères en ligne de commande pour protéger votre vie privée.**

![Version](https://img.shields.io/badge/version-1.0.0-red)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Fonctionnalités

- Création rapide d'adresses email temporaires
- Protection de la vie privée
- Multi-providers (1secmail, mail.tm, GuerrillaMail)
- Stockage local automatique
- Interface élégante avec couleurs
- Léger et rapide

## Installation

```bash
# Cloner le repository
git clone <your-repo-url>
cd mailaka

# Installer en mode développement
pip install -e .
```

## Utilisation

### Commandes principales

```bash
# Afficher l'aide
mailaka --help

# Créer une nouvelle adresse email temporaire
mailaka new                           # Mode auto (essaye tous les providers)
mailaka new --provider 1secmail       # Provider spécifique
mailaka new --provider mailtm
mailaka new --provider guerrillamail

# Afficher le statut de l'adresse active
mailaka status

# Lister toutes les inboxes sauvegardées
mailaka inboxes

# Lister les emails reçus
mailaka inbox

# Lire un email spécifique
mailaka read <message-id>

# Lister les pièces jointes d'un email
mailaka attachments <message-id>

# Télécharger une pièce jointe (si supporté)
mailaka download <attachment-id> -o fichier.pdf

# Supprimer un email (non supporté par la plupart des providers)
mailaka delete <message-id>

# Afficher la version
mailaka version
```

### Exemples d'utilisation

```bash
# Workflow typique
mailaka new                    # 1. Créer une adresse
mailaka status                 # 2. Voir l'adresse active
mailaka inbox                  # 3. Lister les messages reçus
mailaka read 12345             # 4. Lire un message spécifique
mailaka attachments 12345      # 5. Voir les pièces jointes (si disponibles)
```

## Architecture

```
mailaka/
├── mailaka/                     # Package principal
│   ├── __init__.py
│   ├── __main__.py              # Point d'entrée (python -m mailaka)
│   ├── cli.py                   # Logique principale CLI
│   ├── commands/                # Commandes simplifiées
│   │   ├── __init__.py
│   │   ├── new.py               # Créer une nouvelle adresse
│   │   ├── inbox.py             # Lister les messages
│   │   ├── read.py              # Lire un message
│   │   ├── delete.py            # Supprimer un message
│   │   ├── attachments.py       # Lister les pièces jointes
│   │   ├── download.py          # Télécharger une pièce jointe
│   │   └── status.py            # Afficher le statut
│   ├── core/                    # Cœur métier
│   │   ├── __init__.py
│   │   ├── provider.py          # Gestion des APIs (providers)
│   │   ├── storage.py           # Sauvegarde locale
│   │   └── models.py            # Modèles de données (Inbox, Message)
│   └── utils/                   # Utilitaires
│       ├── __init__.py
│       ├── display.py           # Fonctions d'affichage
│       ├── errors.py            # Gestion des erreurs
│       └── config.py            # Configuration
├── tests/                       # Tests unitaires
├── README.md
├── LICENSE
└── pyproject.toml
```

## Commandes disponibles

| Commande | Description |
|----------|-------------|
| `mailaka new` | Crée une nouvelle adresse email temporaire |
| `mailaka inbox` | Liste les emails reçus dans la boîte active |
| `mailaka inboxes` | Liste toutes les inboxes sauvegardées |
| `mailaka read <id>` | Affiche le contenu d'un email |
| `mailaka delete <id>` | Supprime un email (non supporté) |
| `mailaka attachments <id>` | Liste les pièces jointes d'un email |
| `mailaka download <id>` | Télécharge une pièce jointe |
| `mailaka status` | Affiche l'adresse active et infos |
| `mailaka version` | Affiche la version de Mailaka |

## Providers supportés

### 1secmail
- Simple, rapide, pas de mot de passe
- URL: https://www.1secmail.com

### mail.tm
- Plus sécurisé avec authentification
- URL: https://mail.tm

### GuerrillaMail
- Fiable, bien établi
- URL: https://www.guerrillamail.com

## Développement

```bash
# Installer en mode développement
pip install -e .

# Structure du projet
# - Ajoutez de nouveaux providers dans mailaka/core/provider.py
# - Ajoutez de nouvelles commandes dans mailaka/commands/
# - Les tests vont dans tests/
```

## License

MIT License - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir une issue ou une pull request.

## Avertissement

Les emails éphémères ne doivent **PAS** être utilisés pour des services importants (banques, services gouvernementaux, etc.). Ils sont destinés à éviter le spam et protéger votre vie privée pour des inscriptions temporaires.
