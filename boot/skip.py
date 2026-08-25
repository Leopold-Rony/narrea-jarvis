#!/usr/bin/env python3
"""
Détection non-bloquante de la touche Échap pour sauter les animations de boot.
"""
import sys
import select
import termios
import tty


class RawInput:
    """Contexte qui met le terminal en mode cbreak pour lire les touches sans bloquer."""
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)
        return self

    def __exit__(self, *args):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


def check_skip():
    """Retourne True si Échap a été pressée (vérification instantanée, non bloquante)."""
    if select.select([sys.stdin], [], [], 0)[0]:
        key = sys.stdin.read(1)
        if key == "\x1b":
            return True
    return False