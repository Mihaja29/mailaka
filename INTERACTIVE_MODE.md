# Mode Interactif Mailaka

## Lancement

Quand vous tapez simplement `mailaka`, une interface interactive s'ouvre automatiquement:

```bash
source venv/bin/activate
mailaka
```

## Interface

```
     __  __       _ _       _         
    |  \/  | __ _(_) | __ _| | ____ _ 
    | |\/| |/ _` | | |/ _` | |/ / _` |
    | |  | | (_| | | | (_| |   < (_| |
    |_|  |_|\__,_|_|_|\__,_|_|\_\__,_|
                                       
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  v0.1 - Mode interactif
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Adresse active: exemple@1secmail.com
  Provider: 1secmail

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

mailaka> _
```

## Commandes Disponibles

Dans le mode interactif, vous tapez directement les commandes sans préfixe `mailaka`:

| Commande | Description | Exemple |
|----------|-------------|---------|
| `new` | Créer une nouvelle adresse | `new` ou `new 1secmail` |
| `inbox` | Lister les messages | `inbox` |
| `read <id>` | Lire un message | `read 12345` |
| `status` | Afficher l'adresse active | `status` |
| `version` | Afficher la version | `version` |
| `clear` | Effacer l'écran | `clear` |
| `help` | Afficher l'aide | `help` |
| `exit` | Quitter | `exit` ou `quit` ou `q` |

## Exemple de Session

```
mailaka> help

  Commandes disponibles:

    new                  Créer une nouvelle adresse email
    inbox                Lister les messages reçus
    read <id>            Lire un message
    status               Afficher l'adresse active
    version              Afficher la version
    clear                Effacer l'écran
    help                 Afficher cette aide
    exit                 Quitter

mailaka> new

  Création d'une nouvelle adresse avec auto...

  Adresse créée: test123@1secmail.com
  Provider: 1secmail
  Token: test123

mailaka> status

  Adresse active:

    Email: test123@1secmail.com
    Provider: 1secmail
    Token: test123
    Créée le: 2026-02-17 07:30:00

mailaka> inbox

  Récupération des messages pour test123@1secmail.com...

  Aucun message reçu

mailaka> exit

  Au revoir!
```

## Raccourcis Clavier

- `Ctrl+C` ou `Ctrl+D` : Quitter le mode interactif
- `Entrée vide` : Ignorer (reste dans le prompt)

## Mode Non-Interactif

Si vous préférez utiliser les commandes classiques:

```bash
mailaka --no-interactive
mailaka new
mailaka inbox
mailaka status
```

## Différences avec le Mode Classique

| Aspect | Mode Interactif | Mode Classique |
|--------|----------------|----------------|
| Prompt | Continu avec `mailaka>` | Une commande à la fois |
| Commandes | Sans préfixe | Avec préfixe `mailaka` |
| Session | Reste ouvert | Se ferme après exécution |
| Contexte | Conservé (adresse active) | Rechargé à chaque fois |
| Sortie | `exit`, `quit`, `q` | Automatique |

## Avantages du Mode Interactif

- Interface type conversationnelle comme RovoDev
- Pas besoin de retaper `mailaka` à chaque fois
- Contexte conservé entre les commandes
- Plus rapide pour enchaîner plusieurs actions
- Expérience utilisateur fluide

## Désactiver le Mode Interactif par Défaut

Si vous préférez le mode classique par défaut, utilisez toujours:

```bash
alias mailaka='mailaka --no-interactive'
```

Ou modifiez `cli.py` pour inverser le comportement par défaut.
