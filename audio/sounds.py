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

SAMPLE_RATE = 8000  # basse résolution volontaire pour le grain "8-bit"


def generate_square_wave(frequency, duration, volume=0.3, sample_rate=SAMPLE_RATE):
    """Génère une onde carrée (son typique chiptune)."""
    n_samples = int(sample_rate * duration)
    samples = []
    period = sample_rate / frequency
    for i in range(n_samples):
        # onde carrée : alterne entre +volume et -volume
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


if __name__ == "__main__":
    print("Test des sons rétro 8-bit...")
    print("→ Boot ready")
    sound_boot_ready()
    print("→ Notification")
    sound_notification()
    print("→ Confirm")
    sound_confirm()
    print("→ Error")
    sound_error()