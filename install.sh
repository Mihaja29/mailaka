#!/bin/bash
# Mailaka Installation Script for Linux/macOS

set -e

REPO="Mihaja29/mailaka"
INSTALL_DIR="/usr/local/bin"
BINARY_NAME="mailaka"

# Detect OS and Architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case "$ARCH" in
    x86_64)
        ARCH="amd64"
        ;;
    arm64|aarch64)
        ARCH="arm64"
        ;;
    *)
        echo "Architecture non supportée: $ARCH"
        exit 1
        ;;
esac

# Map OS to binary name
case "$OS" in
    linux)
        ASSET_NAME="mailaka-linux"
        ;;
    darwin)
        ASSET_NAME="mailaka-macos"
        ;;
    *)
        echo "OS non supporté: $OS"
        exit 1
        ;;
esac

echo "📥 Installation de Mailaka..."
echo "   OS: $OS"
echo "   Arch: $ARCH"

# Get latest release
LATEST_URL=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep "browser_download_url.*$ASSET_NAME" | cut -d '"' -f 4)

if [ -z "$LATEST_URL" ]; then
    echo "❌ Impossible de trouver la dernière release"
    exit 1
fi

echo "📥 Téléchargement depuis: $LATEST_URL"

# Download binary
TMP_DIR=$(mktemp -d)
curl -L -o "$TMP_DIR/$BINARY_NAME" "$LATEST_URL"

# Make executable
chmod +x "$TMP_DIR/$BINARY_NAME"

# Check if sudo is needed
if [ -w "$INSTALL_DIR" ]; then
    mv "$TMP_DIR/$BINARY_NAME" "$INSTALL_DIR/"
else
    echo "🔒 Sudo requis pour l'installation"
    sudo mv "$TMP_DIR/$BINARY_NAME" "$INSTALL_DIR/"
fi

# Cleanup
rm -rf "$TMP_DIR"

echo ""
echo "✅ Mailaka installé avec succès!"
echo ""
echo "📧 Utilisation rapide:"
echo "   mailaka --help     # Afficher l'aide"
echo "   mailaka new        # Créer une adresse"
echo "   mailaka inbox      # Voir les messages"
echo ""
