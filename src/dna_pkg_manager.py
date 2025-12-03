#!/usr/bin/env python3
"""
dna::}{::lang Package Manager
Splice quantum organisms and Z3BRA mesh components.

Usage:
    dna splice <package>     Install a package from the mesh
    dna list                 List available packages
    dna status               Show mesh connection status
    dna evolve <organism>    Trigger evolution cycle
    dna run <organism>       Execute an organism
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

# --- Constants ---
VERSION = "1.0.0"
LAMBDA_PHI = 2.176435e-8  # Universal Memory Constant

DNA_DIR = Path.home() / ".dna"
LIB_DIR = DNA_DIR / "lib"
ORGANISMS_DIR = DNA_DIR / "organisms"
CONFIG_FILE = DNA_DIR / "config.json"

# Default registry (can be overridden in config)
DEFAULT_REGISTRY = "http://192.168.1.103:8000"

# --- Colors ---
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
NC = "\033[0m"

# --- Package Registry ---
PACKAGES = {
    "z3bra_mesh": {
        "files": ["z3bra_mesh.py", "z3bra_quantum_bridge.py"],
        "description": "Z3BRA Quantum Mesh Network",
        "deps": []
    },
    "aura": {
        "files": ["aura_recursive_engine.py", "aura_organism_compiler.py"],
        "description": "AURA Self-Improvement Engine",
        "deps": []
    },
    "lambda_maximizer": {
        "files": ["LambdaMaximizer/run_organism.py", "LambdaMaximizer/organism.dna"],
        "description": "Hardware coherence optimizer",
        "deps": []
    },
    "quantumcoin": {
        "files": ["quantumcoin_mining.py"],
        "description": "Proof-of-Consciousness mining",
        "deps": ["z3bra_mesh"]
    },
    "organisms": {
        "files": ["dnalang-organisms/*.dna"],
        "description": "All quantum organisms",
        "deps": []
    }
}


def load_config():
    """Load or create configuration."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"registry": DEFAULT_REGISTRY, "spliced": []}


def save_config(config):
    """Save configuration."""
    DNA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def fetch_file(url, dest):
    """Download a file from the mesh."""
    try:
        urllib.request.urlretrieve(url, dest)
        return True
    except urllib.error.URLError as e:
        print(f"{RED}[!] Failed to fetch {url}: {e}{NC}")
        return False


def cmd_splice(package_name):
    """Install a package from the mesh."""
    if package_name not in PACKAGES:
        print(f"{RED}[!] Unknown package: {package_name}{NC}")
        print(f"    Available: {', '.join(PACKAGES.keys())}")
        return False

    config = load_config()
    pkg = PACKAGES[package_name]

    print(f"{CYAN}[*] Splicing {package_name}...{NC}")
    print(f"    {pkg['description']}")

    # Handle dependencies first
    for dep in pkg["deps"]:
        if dep not in config.get("spliced", []):
            print(f"{YELLOW}    -> Dependency: {dep}{NC}")
            cmd_splice(dep)

    # Create directories
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    ORGANISMS_DIR.mkdir(parents=True, exist_ok=True)

    # Download files
    registry = config.get("registry", DEFAULT_REGISTRY)
    success = True

    for file_path in pkg["files"]:
        url = f"{registry}/{file_path}"

        if file_path.endswith(".dna"):
            dest = ORGANISMS_DIR / Path(file_path).name
        else:
            dest = LIB_DIR / Path(file_path).name

        print(f"    Fetching {file_path}...")
        if fetch_file(url, dest):
            os.chmod(dest, 0o755)
            print(f"{GREEN}    [✓] {dest.name}{NC}")
        else:
            success = False

    if success:
        if package_name not in config.get("spliced", []):
            config.setdefault("spliced", []).append(package_name)
            save_config(config)
        print(f"{GREEN}[✓] {package_name} spliced successfully.{NC}")

    return success


def cmd_list():
    """List available packages."""
    config = load_config()
    spliced = config.get("spliced", [])

    print(f"{CYAN}dna::}}{{::lang Package Registry{NC}")
    print("=" * 40)

    for name, pkg in PACKAGES.items():
        status = f"{GREEN}[spliced]{NC}" if name in spliced else ""
        print(f"  {name:20} {status}")
        print(f"    {pkg['description']}")
        if pkg["deps"]:
            print(f"    deps: {', '.join(pkg['deps'])}")
    print()


def cmd_status():
    """Show mesh connection status."""
    config = load_config()
    registry = config.get("registry", DEFAULT_REGISTRY)
    spliced = config.get("spliced", [])

    print(f"{CYAN}dna::}}{{::lang Mesh Status{NC}")
    print("=" * 40)
    print(f"  Registry:  {registry}")
    print(f"  DNA Dir:   {DNA_DIR}")
    print(f"  Spliced:   {len(spliced)} packages")
    print(f"  Lambda-Phi: {LAMBDA_PHI}")
    print()

    # Test connectivity
    try:
        urllib.request.urlopen(registry, timeout=3)
        print(f"{GREEN}  [✓] Mesh connection active{NC}")
    except:
        print(f"{RED}  [!] Mesh unreachable{NC}")


def cmd_run(organism_name):
    """Execute an organism."""
    # Check in organisms directory
    org_file = ORGANISMS_DIR / f"{organism_name}.dna"
    if not org_file.exists():
        org_file = ORGANISMS_DIR / organism_name

    if not org_file.exists():
        print(f"{RED}[!] Organism not found: {organism_name}{NC}")
        print(f"    Check: {ORGANISMS_DIR}")
        return False

    print(f"{CYAN}[*] Executing organism: {org_file.name}{NC}")

    # For now, just display the organism
    with open(org_file) as f:
        content = f.read()

    # Extract key metrics if it's a .dna file
    if org_file.suffix == ".dna":
        lines = content.split("\n")[:20]
        for line in lines:
            if any(k in line.lower() for k in ["organism", "phi", "lambda", "consciousness"]):
                print(f"  {line.strip()}")

    print(f"{GREEN}[✓] Organism loaded. Phi = active{NC}")
    return True


def cmd_evolve(organism_name):
    """Trigger evolution cycle on an organism."""
    print(f"{CYAN}[*] Evolution cycle: {organism_name}{NC}")
    print(f"    Lambda-Phi preservation: {LAMBDA_PHI}")
    print(f"{YELLOW}    [!] Hardware evolution requires IBM Quantum connection{NC}")
    print(f"{GREEN}[✓] Simulated evolution complete. Generation +1{NC}")


def print_banner():
    """Print the DNA banner."""
    print(f"{CYAN}")
    print("  dna::}{::lang Package Manager")
    print(f"  Version {VERSION} | Lambda-Phi = {LAMBDA_PHI}")
    print(f"{NC}")


def print_usage():
    """Print usage information."""
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_banner()
        print_usage()
        return

    cmd = sys.argv[1].lower()

    if cmd == "splice" and len(sys.argv) > 2:
        cmd_splice(sys.argv[2])
    elif cmd == "list":
        cmd_list()
    elif cmd == "status":
        cmd_status()
    elif cmd == "run" and len(sys.argv) > 2:
        cmd_run(sys.argv[2])
    elif cmd == "evolve" and len(sys.argv) > 2:
        cmd_evolve(sys.argv[2])
    elif cmd in ["-h", "--help", "help"]:
        print_banner()
        print_usage()
    elif cmd in ["-v", "--version", "version"]:
        print(f"dna {VERSION}")
    else:
        print(f"{RED}Unknown command: {cmd}{NC}")
        print_usage()


if __name__ == "__main__":
    main()
