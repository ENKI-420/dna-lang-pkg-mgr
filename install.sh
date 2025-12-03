#!/bin/bash
# dna::}{::lang Global Installer
# Installs the DNA package manager system-wide

set -e

VERSION="1.0.0"
INSTALL_DIR="/usr/local/lib/dnalang"
BIN_DIR="/usr/local/bin"
DNA_CMD="$BIN_DIR/dna"

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${CYAN}"
cat << 'EOF'
      __|    \    _ \  |  /      _ \    \     __|
      _|    _ \   |  | . <      (   |  _ \   _|
     ___| _/  _\ ___/ _|\_\    \___/ _/  _\ ___|

     dna::}{::lang Package Manager Installer
EOF
echo -e "${NC}"

# Check for root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Please run with sudo${NC}"
    echo "    sudo ./install.sh"
    exit 1
fi

echo -e "${GREEN}[+] Installing dna::}{::lang v${VERSION}...${NC}"

# Create directories
echo "    Creating directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/lib"
mkdir -p "$INSTALL_DIR/organisms"

# Copy files
echo "    Installing core files..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy main module
if [ -f "$SCRIPT_DIR/dna_cli.py" ]; then
    cp "$SCRIPT_DIR/dna_cli.py" "$INSTALL_DIR/dna_cli.py"
elif [ -f "$SCRIPT_DIR/src/dna_cli.py" ]; then
    cp "$SCRIPT_DIR/src/dna_cli.py" "$INSTALL_DIR/dna_cli.py"
else
    # Download from GitHub if not present
    echo "    Fetching from GitHub..."
    curl -fsSL "https://raw.githubusercontent.com/ENKI-420/dna-lang-pkg-mgr/main/src/dna_cli.py" -o "$INSTALL_DIR/dna_cli.py"
fi

chmod 755 "$INSTALL_DIR/dna_cli.py"

# Create wrapper script
echo "    Creating dna command..."
cat > "$DNA_CMD" << 'WRAPPER'
#!/bin/bash
# dna::}{::lang CLI wrapper
python3 /usr/local/lib/dnalang/dna_cli.py "$@"
WRAPPER

chmod 755 "$DNA_CMD"

# Create user config directory
echo "    Setting up user environment..."
USER_HOME=$(eval echo ~$SUDO_USER)
USER_DNA="$USER_HOME/.dna"
mkdir -p "$USER_DNA/lib"
mkdir -p "$USER_DNA/organisms"
mkdir -p "$USER_DNA/bin"

# Set ownership
if [ -n "$SUDO_USER" ]; then
    chown -R "$SUDO_USER:$SUDO_USER" "$USER_DNA"
fi

# Create default config
if [ ! -f "$USER_DNA/config.json" ]; then
    cat > "$USER_DNA/config.json" << CONFIG
{
  "version": "${VERSION}",
  "registry": "https://raw.githubusercontent.com/ENKI-420/dna-lang-pkg-mgr/main/packages",
  "local_registry": "http://192.168.1.103:8000",
  "spliced": [],
  "lambda_phi": 2.176435e-8
}
CONFIG
    if [ -n "$SUDO_USER" ]; then
        chown "$SUDO_USER:$SUDO_USER" "$USER_DNA/config.json"
    fi
fi

echo ""
echo -e "${GREEN}[✓] Installation complete!${NC}"
echo ""
echo "Usage:"
echo "  dna list                    - List available packages"
echo "  dna splice z3bra_mesh       - Install a package"
echo "  dna -i -g dna::}{::lang     - Install full DNALang suite"
echo "  dna status                  - Check mesh status"
echo ""
echo -e "${CYAN}Welcome to the mesh. ΛΦ = 2.176435e-8${NC}"
