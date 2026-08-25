#!/usr/bin/env python3
import time
import random
import sys
from rich.console import Console
from rich.text import Text
from boot.skip import check_skip


sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))
from audio.sounds import jingle_boot

console = Console()

# Palette rétro phosphore vert (classique terminal DOS-like)
GREEN = "bold green"
DIM_GREEN = "green"
AMBER = "bold yellow"

def typewriter(text, style=GREEN, delay=0.015, end="\n"):
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(delay)
    console.print("", end=end)

def fake_check(label, duration=0.4, ok=True):
    from boot.skip import check_skip
    console.print(f"[{DIM_GREEN}]{label}...[/{DIM_GREEN}]", end=" ")
    elapsed = 0
    while elapsed < duration:
        if check_skip():
            console.print(f"[{GREEN}][SKIP][/{GREEN}]")
            return
        time.sleep(0.05)
        elapsed += 0.05
    status = "[OK]" if ok else "[FAIL]"
    style = GREEN if ok else "bold red"
    console.print(f"[{style}]{status}[/{style}]")

def print_logo():
    logo = r"""
     _   _                     
    | \ | | __ _ _ __ _ __ ___  __ _ 
    |  \| |/ _` | '__| '__/ _ \/ _` |
    | |\  | (_| | |  | | |  __/ (_| |
    |_| \_|\__,_|_|  |_|  \___|\__,_|
    """
    console.print(logo, style=GREEN)

def main():
    console.clear()
    jingle_boot()
    print_logo()
    time.sleep(0.5)
    typewriter("NARÆA SYSTEM v0.1 — HP ProBook 450 G7", style=AMBER, delay=0.01)
    typewriter("Copyright (c) 2026 qsnoopy Industries", delay=0.01)
    console.print()
    time.sleep(0.3)

    checks = [
        ("Vérification CPU (i3-10110U, AVX2)", 0.5),
        ("Test mémoire 4096 Ko... [dim](mode texte, RAM préservée)[/dim]", 0.6),
        ("Montage /home/qsnoopy/narrea", 0.3),
        ("Initialisation environnement Python (venv)", 0.4),
        ("Chargement moteur IA (llama.cpp)", 0.7),
        ("Recherche du modèle Qwen2.5-0.5B-Instruct...", 0.5),
        ("Connexion réseau (enp1s0 / wlp0s20f3)", 0.4),
    ]
    for label, dur in checks:
        fake_check(label, dur)

    console.print()
    time.sleep(0.3)
    typewriter("Démarrage de JARVIS...", style=AMBER, delay=0.02)
    time.sleep(0.5)
    console.print()
    console.print("[bold green]Système prêt.[/bold green]")
    time.sleep(0.8)

if __name__ == "__main__":
    main()