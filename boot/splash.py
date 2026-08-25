#!/usr/bin/env python3
"""
Séquence complète de démarrage Naræa — jouée AVANT le login.
Enchaîne boot.py, cube3d.py, matrix.py. Échap pour sauter à tout moment.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from boot import boot as boot_mod
from animations import cube3d, matrix
from boot.skip import RawInput, check_skip


def main():
    try:
        with RawInput():
            if check_skip():
                return
            boot_mod.main()
            if check_skip():
                return
            cube3d.run()
            if check_skip():
                return
            matrix.run()
    except Exception as e:
        # En cas d'erreur quelconque, on n'empêche jamais le login de s'afficher
        print(f"[Naræa splash] Erreur ignorée : {e}", file=sys.stderr)


if __name__ == "__main__":
    main()