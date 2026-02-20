# Mailaka Installation Script for Windows
# Run with PowerShell: powershell -ExecutionPolicy Bypass -File install.ps1

$Repo = "Mihaja29/mailaka"
$InstallDir = "$env:LOCALAPPDATA\Mailaka"
$BinaryName = "mailaka-windows.exe"
$TargetName = "mailaka.exe"

Write-Host "📥 Installation de Mailaka..." -ForegroundColor Cyan

# Create install directory
if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

# Get latest release URL
$LatestUrl = "https://api.github.com/repos/$Repo/releases/latest"
try {
    $Release = Invoke-RestMethod -Uri $LatestUrl
    $Asset = $Release.assets | Where-Object { $_.name -eq $BinaryName }
    if (!$Asset) {
        Write-Host "❌ Binaire non trouvé dans la release" -ForegroundColor Red
        exit 1
    }
    $DownloadUrl = $Asset.browser_download_url
} catch {
    Write-Host "❌ Erreur lors de la récupération de la release: $_" -ForegroundColor Red
    exit 1
}

Write-Host "📥 Téléchargement depuis: $DownloadUrl" -ForegroundColor Cyan

# Download binary
try {
    $OutputPath = Join-Path $InstallDir $TargetName
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $OutputPath -UseBasicParsing
    Write-Host "✅ Binaire téléchargé: $OutputPath" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur lors du téléchargement: $_" -ForegroundColor Red
    exit 1
}

# Add to PATH
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$InstallDir", "User")
    Write-Host "✅ Ajouté au PATH utilisateur" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Déjà dans le PATH" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Mailaka installé avec succès!" -ForegroundColor Green
Write-Host ""
Write-Host "📧 Utilisation rapide:" -ForegroundColor Cyan
Write-Host "   mailaka --help     # Afficher l'aide"
Write-Host "   mailaka new        # Créer une adresse"
Write-Host "   mailaka inbox      # Voir les messages"
Write-Host ""
Write-Host "⚠️ Redémarrez votre terminal pour utiliser 'mailaka'"
