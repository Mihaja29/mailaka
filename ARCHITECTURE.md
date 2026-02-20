# Architecture Mailaka

## Vue d'ensemble

Mailaka a été restructuré selon une architecture modulaire et professionnelle pour faciliter la maintenance et l'évolution du projet.

## Structure du projet

```
mailaka/
├── mailaka/                     # Package principal
│   ├── __init__.py              # Init du package
│   ├── __main__.py              # Point d'entrée (python -m mailaka)
│   ├── cli.py                   # Logique principale CLI
│   ├── commands/                # Sous-commandes organisées
│   │   ├── __init__.py
│   │   ├── base.py              # Classe de base pour les commandes
│   │   ├── email.py             # Commandes liées aux emails (inbox)
│   │   ├── config.py            # Commandes de configuration
│   │   └── status.py            # Commandes status/info/hello
│   ├── core/                    # Cœur métier
│   │   ├── __init__.py
│   │   ├── models.py            # Modèles de données (Inbox, Message)
│   │   ├── storage.py           # Sauvegarde locale (JSON)
│   │   └── provider.py          # Gestion des APIs providers
│   ├── utils/                   # Utilitaires
│   │   ├── __init__.py
│   │   ├── display.py           # Affichage (couleurs, bannière)
│   │   ├── errors.py            # Exceptions personnalisées
│   │   └── config.py            # Gestion configuration
│   └── assets/                  # (optionnel) ASCII art, etc.
├── tests/                       # Tests unitaires
│   └── __init__.py
├── README.md                    # Documentation
├── LICENSE                      # Licence MIT
├── pyproject.toml               # Configuration du projet
└── .gitignore                   # Fichiers ignorés par git
```

## Modules

### 1. `cli.py` - Point d'entrée principal
- Définit le groupe de commandes principal `main()`
- Gère l'affichage de la bannière et du menu
- Enregistre toutes les sous-commandes

### 2. `commands/` - Commandes simplifiées
- **`new.py`**: Commande `mailaka new` - créer une adresse
- **`inbox.py`**: Commande `mailaka inbox` - lister les messages
- **`read.py`**: Commande `mailaka read <id>` - lire un message
- **`delete.py`**: Commande `mailaka delete <id>` - supprimer (non supporté)
- **`attachments.py`**: Commande `mailaka attachments <id>` - lister PJ
- **`download.py`**: Commande `mailaka download <id>` - télécharger PJ
- **`status.py`**: Commande `mailaka status` - afficher statut

### 3. `core/` - Logique métier
- **`models.py`**: Classes de données `Inbox` et `Message` avec dataclasses
- **`storage.py`**: `InboxStorage` pour gérer la persistance JSON
- **`provider.py`**: 
  - Classe abstraite `Provider`
  - Implémentations: `OneSecMailProvider`, `MailTmProvider`, `GuerrillaMailProvider`
  - `ProviderFactory` pour instancier les providers

### 4. `utils/` - Utilitaires
- **`display.py`**: Fonctions d'affichage stylé (couleurs, bannière)
- **`errors.py`**: Exceptions personnalisées (`MailakaError`, `ProviderError`, `StorageError`)
- **`config.py`**: Classe `Config` pour gérer la configuration utilisateur

## Flux de données

### Création d'une inbox
```
CLI (email.py) 
  → ProviderFactory.get_provider() 
  → Provider.create_inbox() 
  → InboxStorage.add() 
  → Affichage (display.py)
```

### Lecture de messages
```
CLI (email.py) 
  → CommandBase.get_inbox_for_command() 
  → Provider.get_messages() 
  → Affichage (display.py)
```

## Avantages de cette architecture

1. **Séparation des responsabilités**: Chaque module a un rôle clair
2. **Facilité de maintenance**: Code organisé et modulaire
3. **Extensibilité**: Facile d'ajouter de nouveaux providers ou commandes
4. **Testabilité**: Modules indépendants faciles à tester
5. **Réutilisabilité**: Les composants core peuvent être utilisés indépendamment du CLI
6. **Type safety**: Utilisation de dataclasses pour les modèles

## Statistiques

- **Total de lignes**: ~1100 lignes de code Python
- **Modules**: 16 fichiers Python
- **Providers supportés**: 3 (1secmail, mail.tm, guerrillamail)
- **Commandes**: 8 commandes principales (simplifiées)
- **Support pièces jointes**: Oui (1secmail)

## Commandes disponibles

| Commande | Description | Status |
|----------|-------------|--------|
| `mailaka new` | Créer une adresse email | ✅ |
| `mailaka inbox` | Lister les messages | ✅ |
| `mailaka read <id>` | Lire un message | ✅ |
| `mailaka delete <id>` | Supprimer un message | ⚠️ Non supporté |
| `mailaka attachments <id>` | Lister pièces jointes | ✅ (1secmail) |
| `mailaka download <id>` | Télécharger PJ | 🚧 En cours |
| `mailaka status` | Afficher statut | ✅ |
| `mailaka version` | Afficher version | ✅ |

## Prochaines étapes possibles

1. Ajouter des tests unitaires dans `tests/`
2. Implémenter téléchargement complet des pièces jointes
3. Ajouter support pièces jointes pour mail.tm
4. Implémenter de nouveaux providers
5. Ajouter une commande pour lister toutes les inboxes sauvegardées
6. Implémenter un système de cache pour les messages
7. Ajouter un mode interactif/TUI avec rich ou textual
8. Ajouter auto-refresh des messages

## Conventions de code

- **Docstrings**: Format Google-style pour toutes les fonctions publiques
- **Type hints**: Utilisés partout où c'est possible
- **Nommage**: 
  - Classes: PascalCase
  - Fonctions/méthodes: snake_case
  - Constantes: UPPER_SNAKE_CASE
- **Imports**: Organisés par catégorie (stdlib, third-party, local)
