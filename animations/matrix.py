#!/usr/bin/env python3
"""
Effet Matrix (pluie de caractères) — Naræa/Jarvis
Conçu pour rester léger en CPU/RAM (pas de dépendance lourde, juste Rich).
"""
import random
import time
import shutil
from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()

# --- Paramètres ajustables ---
DURATION = 5.0          # durée totale de l'animation en secondes
FPS = 12                # images par seconde (12-15 suffit pour l'illusion, économise le CPU)
DENSITY = 0.08          # probabilité qu'une nouvelle goutte démarre sur une colonne à chaque frame
TRAIL_LENGTH = 10        # longueur de la traînée lumineuse par colonne
CHARSET = "アイウエオカキクケコサシスセソ0123456789ABCDEFｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ"


class Column:
    """Représente une colonne de chute de caractères."""
    def __init__(self, height):
        self.height = height
        self.active = False
        self.pos = 0
        self.speed = random.choice([1, 1, 2])  # variation légère de vitesse

    def maybe_start(self):
        if not self.active and random.random() < DENSITY:
            self.active = True
            self.pos = 0

    def step(self):
        if self.active:
            self.pos += self.speed
            if self.pos - TRAIL_LENGTH > self.height:
                self.active = False


def render_frame(columns, width, height):
    grid = [[" " for _ in range(width)] for _ in range(height)]
    styles = [[None for _ in range(width)] for _ in range(height)]

    for x, col in enumerate(columns):
        if not col.active:
            continue
        for offset in range(TRAIL_LENGTH):
            y = col.pos - offset
            if 0 <= y < height:
                char = random.choice(CHARSET)
                grid[y][x] = char
                if offset == 0:
                    styles[y][x] = "bold white"       # tête de la traînée, très lumineuse
                elif offset < 3:
                    styles[y][x] = "bold green"
                else:
                    styles[y][x] = "green"

    text = Text()
    for y in range(height):
        for x in range(width):
            char = grid[y][x]
            style = styles[y][x]
            text.append(char, style=style if style else "")
        text.append("\n")
    return text


def run(duration=DURATION):
    term_size = shutil.get_terminal_size(fallback=(80, 24))
    width, height = term_size.columns, term_size.lines - 1

    columns = [Column(height) for _ in range(width)]
    frame_delay = 1 / FPS
    start = time.time()

    with Live(console=console, screen=True, auto_refresh=False) as live:
        while time.time() - start < duration:
            for col in columns:
                col.maybe_start()
                col.step()
            frame = render_frame(columns, width, height)
            live.update(frame, refresh=True)
            time.sleep(frame_delay)


if __name__ == "__main__":
    run()