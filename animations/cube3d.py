#!/usr/bin/env python3
"""
Rotation 3D — cube filaire ASCII — Naræa/Jarvis
Léger : projection + rotation de 8 points, pas de dépendance externe (juste math + Rich).
"""
import math
import time
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from audio.sounds import jingle_cube3d
from boot.skip import check_skip

from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()

# --- Paramètres ajustables ---
DURATION = 6.0
FPS = 15
ROTATION_SPEED = 1.2
SCALE = 10
CHAR = "@"
STYLE = "bold green"

VERTICES = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1),  (1, -1, 1),  (1, 1, 1),  (-1, 1, 1),
]

EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]


def rotate(point, angle_x, angle_y):
    x, y, z = point
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
    return x, y, z


def project(point, width, height, distance=4):
    x, y, z = point
    factor = distance / (distance + z)
    px = int(width / 2 + x * factor * SCALE)
    py = int(height / 2 + y * factor * SCALE * 0.5)
    return px, py


def draw_line(grid, x0, y0, x1, y1, width, height):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        if 0 <= x0 < width and 0 <= y0 < height:
            grid[y0][x0] = CHAR
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def render_frame(angle_x, angle_y, width, height, progress=None):
    bar_height = 2 if progress is not None else 0
    grid_height = height - bar_height
    grid = [[" " for _ in range(width)] for _ in range(grid_height)]

    projected = [
        project(rotate(v, angle_x, angle_y), width, grid_height)
        for v in VERTICES
    ]
    for edge in EDGES:
        p0, p1 = projected[edge[0]], projected[edge[1]]
        draw_line(grid, p0[0], p0[1], p1[0], p1[1], width, grid_height)

    text = Text()
    for row in grid:
        text.append("".join(row) + "\n", style=STYLE)

    if progress is not None:
        bar_width = min(40, max(10, width - 20))
        filled = int(bar_width * min(progress, 1.0))
        bar = "▓" * filled + "░" * (bar_width - filled)
        pct = int(min(progress, 1.0) * 100)
        label = f"Chargement du noyau Naræa... [{bar}] {pct}%"
        pad = max(0, (width - len(label)) // 2)
        text.append("\n" + " " * pad + label, style="bold yellow")

    return text


def run(duration=DURATION, live=None, show_progress=True):
    term_size = shutil.get_terminal_size(fallback=(80, 24))
    width, height = term_size.columns, term_size.lines - 1

    jingle_cube3d()

    frame_delay = 1 / FPS
    start = time.time()
    angle_x, angle_y = 0.0, 0.0

    def loop(live_obj):
        nonlocal angle_x, angle_y
        while True:
            elapsed = time.time() - start
            if elapsed >= duration or check_skip():
                break
            progress = elapsed / duration if show_progress else None
            frame = render_frame(angle_x, angle_y, width, height, progress=progress)
            live_obj.update(frame, refresh=True)
            angle_x += ROTATION_SPEED * frame_delay
            angle_y += ROTATION_SPEED * 0.7 * frame_delay
            time.sleep(frame_delay)

    if live is not None:
        loop(live)
    else:
        with Live(console=console, screen=True, auto_refresh=False) as live_obj:
            loop(live_obj)


if __name__ == "__main__":
    run()