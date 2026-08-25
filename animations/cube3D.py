#!/usr/bin/env python3
"""
Rotation 3D — cube filaire ASCII — Naræa/Jarvis
Léger : projection + rotation de 8 points, pas de dépendance externe (juste math + Rich).
"""
import math
import time
import shutil
from rich.console import Console
from rich.live import Live
from rich.text import Text
from boot.skip import check_skip
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))
from audio.sounds import jingle_cube3d

console = Console()

# --- Paramètres ajustables ---
DURATION = 6.0
FPS = 15
ROTATION_SPEED = 1.2      # radians/seconde
SCALE = 10                # taille du cube (en caractères)
CHAR = "@"                 # caractère utilisé pour tracer les arêtes
STYLE = "bold green"

# Les 8 sommets d'un cube centré à l'origine
VERTICES = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1),  (1, -1, 1),  (1, 1, 1),  (-1, 1, 1),
]

# Les 12 arêtes reliant les sommets (par index)
EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # face arrière
    (4, 5), (5, 6), (6, 7), (7, 4),  # face avant
    (0, 4), (1, 5), (2, 6), (3, 7),  # arêtes reliant les deux faces
]


def rotate(point, angle_x, angle_y):
    x, y, z = point

    # rotation autour de l'axe X
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    # rotation autour de l'axe Y
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y

    return x, y, z


def project(point, width, height, distance=4):
    x, y, z = point
    factor = distance / (distance + z)
    px = int(width / 2 + x * factor * SCALE)
    py = int(height / 2 + y * factor * SCALE * 0.5)  # 0.5 corrige le ratio largeur/hauteur des caractères
    return px, py


def draw_line(grid, x0, y0, x1, y1, width, height):
    """Tracé de segment via l'algorithme de Bresenham."""
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


def render_frame(angle_x, angle_y, width, height):
    grid = [[" " for _ in range(width)] for _ in range(height)]
    projected = [
        project(rotate(v, angle_x, angle_y), width, height)
        for v in VERTICES
    ]
    for edge in EDGES:
        p0, p1 = projected[edge[0]], projected[edge[1]]
        draw_line(grid, p0[0], p0[1], p1[0], p1[1], width, height)

    text = Text()
    for row in grid:
        text.append("".join(row) + "\n", style=STYLE)
    return text


def run(duration=DURATION):
    term_size = shutil.get_terminal_size(fallback=(80, 24))
    width, height = term_size.columns, term_size.lines - 1

    frame_delay = 1 / FPS
    start = time.time()
    angle_x, angle_y = 0.0, 0.0

    jingle_cube3d()

    with Live(console=console, screen=True, auto_refresh=False) as live:
        while time.time() - start < duration:
            if check_skip():
                break
            frame = render_frame(angle_x, angle_y, width, height)
            live.update(frame, refresh=True)
            angle_x += ROTATION_SPEED * frame_delay
            angle_y += ROTATION_SPEED * 0.7 * frame_delay
            time.sleep(frame_delay)


if __name__ == "__main__":
    run()