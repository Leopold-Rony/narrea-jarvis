#!/usr/bin/env python3
"""
Séquence complète de démarrage Naræa — jouée AVANT le login.
Enchaîne boot.py, cube3d.py, matrix.py dans une session d'écran partagée
pour des transitions fluides. Échap pour sauter à tout moment.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from boot import boot as boot_mod
from animations import cube3d, matrix
from boot.skip import RawInput, check_skip

from rich.console import Console
from rich.live import Live


def main():
    try:
        with RawInput():
            if check_skip():
                return

            # Boot : impression classique (pas d'écran alternatif)
            boot_mod.main()
            if check_skip():
                return

            # Cube 3D + Matrix : une seule session Live partagée = transition fluide
            shared_console = Console()
            with Live(console=shared_console, screen=True, auto_refresh=False) as live:
                cube3d.run(live=live)
                if check_skip():
                    return
                matrix.run(live=live)

    except Exception as e:
        print(f"[Naræa splash] Erreur ignorée : {e}", file=sys.stderr)


if __name__ == "__main__":
    main()