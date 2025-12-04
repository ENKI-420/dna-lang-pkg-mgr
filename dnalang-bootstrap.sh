#!/bin/bash
# dna::}{::lang Auto-Configuration Sequence
# Run this on a new machine to splice into the Z3BRA mesh.

# --- Configuration ---
# The IP of your main "Mother" node hosting the files
REGISTRY_URL="http://192.168.1.103:8000"
DNA_DIR="$HOME/.dna"
BIN_DIR="$DNA_DIR/bin"
LIB_DIR="$DNA_DIR/lib"
EXECUTABLE="$BIN_DIR/dna"

# --- Colors ---
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "      __|    \    _ \  |  /      _ \    \     __| "
echo "     _|    _ \   |  | . <      (   |  _ \   _|   "
echo "     ___| _/  _\ ___/ _|\_\    \___/ _/  _\ ___|  "
echo "     dna::}{::lang Bootstrap v1.0"
echo -e "${NC}"

echo -e "${GREEN}[+] Initializing DNA Environment...${NC}"

# 1. Prepare Directories
mkdir -p "$BIN_DIR"
mkdir -p "$LIB_DIR"

# 2. Download the Package Manager Core
echo "    Fetching dna_pkg_manager.py from $REGISTRY_URL..."
# Note: We save it as 'dna' (no extension) to look like a binary
if curl -s "$REGISTRY_URL/dna_pkg_manager.py" -o "$EXECUTABLE"; then
    echo -e "${GREEN}[✓] Core spliced successfully.${NC}"
else
    echo -e "${RED}[!] Failed to connect to Mesh Registry ($REGISTRY_URL).${NC}"
    echo "    Ensure the server is running: python3 -m http.server 8000"
    exit 1
fi

# 3. Make Executable
chmod +x "$EXECUTABLE"

# 4. Configure Shell Path (Idempotent)
SHELL_RC="$HOME/.bashrc"
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

if ! grep -q "$BIN_DIR" "$SHELL_RC"; then
    echo "" >> "$SHELL_RC"
    echo "# dna::}{::lang Package Manager" >> "$SHELL_RC"
    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_RC"
    echo "    Added $BIN_DIR to $SHELL_RC"
fi

# 5. Environment Activation
export PATH="$PATH:$BIN_DIR"

echo -e "${CYAN}[*] System configured.${NC}"
echo "    You can now use 'dna' to splice packages."
echo "    Example: dna splice z3bra_mesh"
echo ""
echo -e "${GREEN}Run 'source $SHELL_RC' to activate in this window.${NC}"
