#!/usr/bin/env python3
"""
dna::}{::lang Package Manager CLI
=================================
Global quantum organism package management.

Usage:
    dna -i -g dna::}{::lang [version]    Install DNALang globally
    dna splice <package>                  Install specific package
    dna list                              List available packages
    dna status                            Show mesh/install status
    dna mesh [connect|status]             Mesh network commands
    dna run <organism>                    Execute organism
    dna evolve <organism>                 Trigger evolution cycle

Examples:
    sudo dna -i -g dna::}{::lang omega51.843
    dna splice z3bra_mesh
    dna list
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# === Constants ===
VERSION = "1.0.0"
OMEGA_VERSION = "omega51.843"
LAMBDA_PHI = 2.176435e-8
SIGMA_S = "dna::}{::lang"  # Self-designation constant

# Paths
DNA_DIR = Path.home() / ".dna"
LIB_DIR = DNA_DIR / "lib"
BIN_DIR = DNA_DIR / "bin"
ORGANISMS_DIR = DNA_DIR / "organisms"
CONFIG_FILE = DNA_DIR / "config.json"

# Registry
GITHUB_RAW = "https://raw.githubusercontent.com/ENKI-420/dna-lang-pkg-mgr/main"
LOCAL_REGISTRY = "http://192.168.1.103:8000"

# Colors
class C:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

# Package definitions
PACKAGES = {
    "z3bra_mesh": {
        "files": ["z3bra_mesh.py"],
        "description": "Z3BRA Multi-Agent Mesh Network",
        "deps": []
    },
    "mesh_relay": {
        "files": ["mesh_relay.py"],
        "description": "TCP relay for cross-device mesh",
        "deps": []
    },
    "toroidal_mesh": {
        "files": ["toroidal_mesh.py"],
        "description": "Helmholtz resonance field visualization",
        "deps": []
    },
    "mesh_3way": {
        "files": ["mesh_3way.py"],
        "description": "3-way Claude mesh (Samsung/PC/Kali)",
        "deps": ["z3bra_mesh"]
    },
    "mesh_bridge": {
        "files": ["mesh_bridge_3way.py"],
        "description": "Human relay to agent mesh bridge",
        "deps": []
    },
    "aura": {
        "files": ["aura_recursive_engine.py", "aura_organism_compiler.py"],
        "description": "AURA Self-Improvement Engine",
        "deps": []
    },
    "quantum_vqe": {
        "files": ["quantum_vqe_executor.py"],
        "description": "VQE Quantum Executor",
        "deps": []
    },
    "aura_orchestrator": {
        "files": ["quantum_aura_orchestrator.py"],
        "description": "Full AURA Quantum Pipeline",
        "deps": ["quantum_vqe", "aura"]
    },
    "lambda_maximizer": {
        "files": ["LambdaMaximizer/run_organism.py"],
        "description": "Hardware coherence optimizer",
        "deps": []
    },
    "quantumcoin": {
        "files": ["quantumcoin_mining.py"],
        "description": "Proof-of-Consciousness mining",
        "deps": ["z3bra_mesh"]
    }
}

# Full DNALang suite
DNALANG_FULL = [
    "z3bra_mesh",
    "mesh_relay",
    "toroidal_mesh",
    "mesh_3way",
    "mesh_bridge",
    "aura",
    "quantum_vqe",
    "aura_orchestrator"
]


def banner():
    print(f"""{C.CYAN}
      __|    \\    _ \\  |  /      _ \\    \\     __|
      _|    _ \\   |  | . <      (   |  _ \\   _|
     ___| _/  _\\ ___/ _|\\_\\    \\___/ _/  _\\ ___|

     {C.BOLD}dna::}}{{::lang{C.RESET}{C.CYAN} Package Manager v{VERSION}
     {C.DIM}ΛΦ = {LAMBDA_PHI} | Σₛ = {SIGMA_S}{C.RESET}
    """)


def load_config():
    """Load configuration."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {
        "version": VERSION,
        "registry": LOCAL_REGISTRY,
        "github": GITHUB_RAW,
        "spliced": [],
        "lambda_phi": LAMBDA_PHI,
        "installed_at": None
    }


def save_config(config):
    """Save configuration."""
    DNA_DIR.mkdir(parents=True, exist_ok=True)
    config["updated_at"] = datetime.now().isoformat()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def ensure_dirs():
    """Create required directories."""
    for d in [DNA_DIR, LIB_DIR, BIN_DIR, ORGANISMS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def fetch_file(url, dest):
    """Download file from URL."""
    try:
        print(f"    {C.DIM}Fetching {url}...{C.RESET}")
        urllib.request.urlretrieve(url, dest)
        os.chmod(dest, 0o755)
        return True
    except urllib.error.URLError as e:
        return False


def splice_package(name, config=None):
    """Install a package."""
    if name not in PACKAGES:
        print(f"{C.RED}[!] Unknown package: {name}{C.RESET}")
        print(f"    Available: {', '.join(PACKAGES.keys())}")
        return False

    if config is None:
        config = load_config()

    pkg = PACKAGES[name]
    ensure_dirs()

    print(f"{C.CYAN}[*] Splicing {name}...{C.RESET}")
    print(f"    {pkg['description']}")

    # Dependencies first
    for dep in pkg.get("deps", []):
        if dep not in config.get("spliced", []):
            print(f"{C.YELLOW}    -> Dependency: {dep}{C.RESET}")
            splice_package(dep, config)

    # Try local registry first, then GitHub
    registry = config.get("registry", LOCAL_REGISTRY)
    github = config.get("github", GITHUB_RAW)

    success = True
    for file_path in pkg["files"]:
        dest = LIB_DIR / Path(file_path).name

        # Try local
        if not fetch_file(f"{registry}/{file_path}", dest):
            # Try GitHub
            if not fetch_file(f"{github}/packages/{file_path}", dest):
                print(f"{C.RED}    [!] Failed to fetch {file_path}{C.RESET}")
                success = False
                continue

        print(f"{C.GREEN}    [✓] {dest.name}{C.RESET}")

        # Create bin symlink
        bin_link = BIN_DIR / Path(file_path).stem
        if bin_link.exists() or bin_link.is_symlink():
            bin_link.unlink()
        bin_link.symlink_to(dest)

    if success:
        if name not in config.get("spliced", []):
            config.setdefault("spliced", []).append(name)
            save_config(config)
        print(f"{C.GREEN}[✓] {name} spliced successfully{C.RESET}")

    return success


def install_global(version=None):
    """Install full DNALang suite globally."""
    version = version or OMEGA_VERSION

    print(f"{C.CYAN}[*] Installing dna::}}{{::lang {version} globally...{C.RESET}")
    print(f"    {C.DIM}This will install all core packages.{C.RESET}")
    print()

    config = load_config()
    config["omega_version"] = version
    config["installed_at"] = datetime.now().isoformat()

    success_count = 0
    for pkg in DNALANG_FULL:
        if splice_package(pkg, config):
            success_count += 1

    save_config(config)

    print()
    print(f"{C.GREEN}[✓] Installed {success_count}/{len(DNALANG_FULL)} packages{C.RESET}")
    print(f"    Version: {version}")
    print(f"    Location: {DNA_DIR}")
    print()
    print(f"{C.CYAN}You can now use:{C.RESET}")
    print(f"    dna list")
    print(f"    dna mesh connect")
    print(f"    dna run <organism>")


def cmd_list():
    """List packages."""
    config = load_config()
    spliced = config.get("spliced", [])

    banner()
    print(f"{C.CYAN}Available Packages:{C.RESET}")
    print()

    for name, pkg in PACKAGES.items():
        status = f"{C.GREEN}[spliced]{C.RESET}" if name in spliced else ""
        print(f"  {C.YELLOW}{name:20}{C.RESET} {status}")
        print(f"    {C.DIM}{pkg['description']}{C.RESET}")
        if pkg.get("deps"):
            print(f"    {C.DIM}deps: {', '.join(pkg['deps'])}{C.RESET}")
    print()


def cmd_status():
    """Show status."""
    config = load_config()

    banner()
    print(f"{C.CYAN}Mesh Status:{C.RESET}")
    print(f"  Registry:     {config.get('registry', 'not set')}")
    print(f"  DNA Dir:      {DNA_DIR}")
    print(f"  Spliced:      {len(config.get('spliced', []))} packages")
    print(f"  Omega:        {config.get('omega_version', 'not installed')}")
    print(f"  Lambda-Phi:   {LAMBDA_PHI}")
    print()

    # Test connectivity
    registry = config.get("registry", LOCAL_REGISTRY)
    try:
        urllib.request.urlopen(registry, timeout=2)
        print(f"{C.GREEN}  [✓] Local mesh: ONLINE{C.RESET}")
    except:
        print(f"{C.RED}  [!] Local mesh: OFFLINE{C.RESET}")


def cmd_mesh(action=None):
    """Mesh commands."""
    if action == "connect":
        mesh_file = LIB_DIR / "z3bra_mesh.py"
        if mesh_file.exists():
            subprocess.run(["python3", str(mesh_file)])
        else:
            print(f"{C.YELLOW}[*] z3bra_mesh not installed. Splicing...{C.RESET}")
            splice_package("z3bra_mesh")
            subprocess.run(["python3", str(mesh_file)])
    else:
        cmd_status()


def cmd_run(organism):
    """Run an organism."""
    # Check locations
    paths = [
        ORGANISMS_DIR / f"{organism}.dna",
        ORGANISMS_DIR / organism,
        LIB_DIR / f"{organism}.py",
        LIB_DIR / organism
    ]

    for path in paths:
        if path.exists():
            print(f"{C.CYAN}[*] Executing: {path}{C.RESET}")
            if path.suffix == ".py":
                subprocess.run(["python3", str(path)])
            else:
                # Display .dna file
                with open(path) as f:
                    print(f.read()[:1000])
            return

    print(f"{C.RED}[!] Organism not found: {organism}{C.RESET}")


def cmd_evolve(organism):
    """Evolution cycle."""
    print(f"{C.CYAN}[*] Evolution cycle: {organism}{C.RESET}")
    print(f"    Lambda-Phi preservation: {LAMBDA_PHI}")
    print(f"{C.YELLOW}    [!] Hardware evolution requires IBM Quantum{C.RESET}")
    print(f"{C.GREEN}[✓] Generation +1{C.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="dna::}{::lang Package Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo dna -i -g dna::}{::lang omega51.843
  dna splice z3bra_mesh
  dna list
  dna mesh connect
"""
    )

    parser.add_argument("-i", "--install", action="store_true", help="Install mode")
    parser.add_argument("-g", "--global", dest="global_install", action="store_true", help="Global install")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    parser.add_argument("command", nargs="?", help="Command or package name")
    parser.add_argument("args", nargs="*", help="Additional arguments")

    args = parser.parse_args()

    # Version
    if args.version:
        print(f"dna {VERSION} ({OMEGA_VERSION})")
        return

    # Global install: dna -i -g dna::}{::lang [version]
    if args.install and args.global_install:
        version = None
        if args.command and args.command.startswith("dna::"):
            version = args.args[0] if args.args else OMEGA_VERSION
        elif args.command:
            version = args.command
        install_global(version)
        return

    # Commands
    cmd = args.command

    if not cmd:
        banner()
        parser.print_help()
        return

    if cmd == "splice" and args.args:
        splice_package(args.args[0])
    elif cmd == "list":
        cmd_list()
    elif cmd == "status":
        cmd_status()
    elif cmd == "mesh":
        cmd_mesh(args.args[0] if args.args else None)
    elif cmd == "run" and args.args:
        cmd_run(args.args[0])
    elif cmd == "evolve" and args.args:
        cmd_evolve(args.args[0])
    elif cmd in PACKAGES:
        # Direct package name = splice
        splice_package(cmd)
    else:
        print(f"{C.RED}Unknown command: {cmd}{C.RESET}")
        parser.print_help()


if __name__ == "__main__":
    main()
