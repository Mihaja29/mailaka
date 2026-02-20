/**
 * Post-install script for Mailaka npm package
 * Sets up Python environment and dependencies
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const colors = {
  red: '\x1b[31m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

function log(msg, color = 'blue') {
  console.log(`${colors[color]}[mailaka]${colors.reset} ${msg}`);
}

function checkPython() {
  try {
    execSync('python3 --version', { stdio: 'pipe' });
    return 'python3';
  } catch {
    try {
      execSync('python --version', { stdio: 'pipe' });
      return 'python';
    } catch {
      return null;
    }
  }
}

async function install() {
  log('Installation de Mailaka...');
  
  const python = checkPython();
  if (!python) {
    log('Python non trouvé. Veuillez installer Python 3.8+', 'red');
    console.log('  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv');
    console.log('  macOS: brew install python3');
    console.log('  Windows: https://python.org/downloads');
    process.exit(1);
  }
  
  log(`Python trouvé: ${python}`);
  
  const rootDir = path.join(__dirname, '..');
  const venvPath = path.join(rootDir, 'venv');
  
  // Check if already installed via pip
  try {
    execSync('pip show mailaka', { stdio: 'pipe' });
    log('Mailaka déjà installé via pip!', 'green');
    return;
  } catch {
    // Continue with venv setup
  }
  
  // Create virtual environment
  if (!fs.existsSync(venvPath)) {
    log('Création de l\'environnement virtuel...');
    try {
      execSync(`${python} -m venv venv`, { cwd: rootDir, stdio: 'inherit' });
    } catch (err) {
      log('Erreur lors de la création du venv', 'red');
      process.exit(1);
    }
  }
  
  // Install mailaka in venv
  log('Installation des dépendances...');
  const pipPath = process.platform === 'win32' 
    ? path.join(venvPath, 'Scripts', 'pip.exe')
    : path.join(venvPath, 'bin', 'pip');
  
  try {
    execSync(`${pipPath} install -e .`, { cwd: rootDir, stdio: 'inherit' });
    log('Installation terminée!', 'green');
    log('Utilisation: mailaka --help');
  } catch (err) {
    log('Erreur lors de l\'installation des dépendances', 'red');
    process.exit(1);
  }
}

install().catch(err => {
  console.error(err);
  process.exit(1);
});
