#!/bin/bash
# Script de lancement de Mailaka

# Se déplacer dans le répertoire du script
cd "$(dirname "$0")"

# Activer l'environnement virtuel
source venv/bin/activate

# Lancer Mailaka avec tous les arguments passés
mailaka "$@"
