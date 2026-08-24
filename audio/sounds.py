#!/usr/bin/env python3
"""
Génération de sons rétro 8-bit — Naræa/Jarvis
Ondes carrées générées à la volée (module wave, aucune dépendance externe).
"""
import wave
import struct
import subprocess
import tempfile
import os
import time

SAMPLE_RATE = 8000  # basse résolution volontaire pour le grain "8-bit"


def generate_square_wave(frequency, duration, volume=0.3, sample_rate=SAMPLE_RATE):
    """Génère une onde carrée (son typique chiptune)."""
    n_samples = int(sample_rate * duration)
    samples = []
    period = sample_rate / frequency
    for i in range(n_samples):
        value = volume if (i % period) < (period / 2) else -volume
        samples.append(int(value * 32767))
    return samples


def save_wav(samples, path, sample_rate=SAMPLE_RATE):
    with wave.open(path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        for s in samples:
            f.writeframes(struct.pack("<h", s))


def play_wav(path):
    try:
        subprocess.run(["aplay", "-q", path], check=True)
    except FileNotFoundError:
        print("Erreur : 'aplay' introuvable. Installe alsa-utils : sudo apt install alsa-utils")
    except subprocess.CalledProcessError:
        print("Erreur lors de la lecture du son.")


def play_tone(frequency, duration, volume=0.3):
    """Génère et joue un son immédiatement (fichier temporaire nettoyé après)."""
    samples = generate_square_wave(frequency, duration, volume)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        path = tmp.name
    save_wav(samples, path)
    play_wav(path)
    os.remove(path)


# --- Table de fréquences (notes de musique) ---
NOTES = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
    "G4": 392.00, "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "F5": 698.46,
    "G5": 783.99, "A5": 880.00, "B5": 987.77,
    "C6": 1046.50,
}


def play_melody(sequence, volume=0.3):
    """
    Joue une séquence de notes.
    sequence : liste de tuples (nom_note, durée_en_secondes)
    Utilise None comme nom de note pour un silence.
    """
    for note, duration in sequence:
        if note is None:
            time.sleep(duration)
        else:
            play_tone(NOTES[note], duration, volume)


# --- Sons prédéfinis pour les notifications système ---

def sound_boot_ready():
    """Petit carillon ascendant : système prêt."""
    for freq in [440, 554, 659]:
        play_tone(freq, 0.1)


def sound_notification():
    """Bip simple : notification standard."""
    play_tone(880, 0.08)


def sound_error():
    """Bip grave : erreur."""
    play_tone(220, 0.25)


def sound_confirm():
    """Double bip : confirmation d'action."""
    play_tone(660, 0.06)
    play_tone(880, 0.06)


# --- Jingles pour les animations ---

def jingle_boot():
    """Montée triomphante — lancement du système."""
    play_melody([
        ("C4", 0.08), ("E4", 0.08), ("G4", 0.08),
        ("C5", 0.15),
    ])


def jingle_matrix():
    """Descente mystérieuse — entrée dans le Matrix."""
    play_melody([
        ("C5", 0.06), ("B4", 0.06), ("A4", 0.06),
        ("G4", 0.06), ("F4", 0.06), ("E4", 0.10),
        (None, 0.05),
        ("C4", 0.15),
    ])


def jingle_cube3d():
    """Arpège rapide — entrée dans la rotation 3D."""
    play_melody([
        ("C4", 0.05), ("E4", 0.05), ("G4", 0.05),
        ("C5", 0.05), ("G4", 0.05), ("C5", 0.12),
    ])


def jingle_strys_ready():
    """Deux notes douces — Strys prêt à discuter."""
    play_melody([
        ("E5", 0.08), ("C5", 0.12),
    ])


if __name__ == "__main__":
    print("Test des sons rétro 8-bit...")
    print("→ Boot ready"); sound_boot_ready()
    print("→ Notification"); sound_notification()
    print("→ Confirm"); sound_confirm()
    print("→ Error"); sound_error()
    print("→ Jingle boot"); jingle_boot()
    print("→ Jingle matrix"); jingle_matrix()
    print("→ Jingle cube3d"); jingle_cube3d()
    print("→ Jingle strys ready"); jingle_strys_ready()