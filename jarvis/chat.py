#!/usr/bin/env python3
"""
Chat CLI avec Strys — Naræa/Jarvis
Interroge le serveur llama-server local avec le system prompt chargé depuis un fichier.
"""
import requests
import sys
from pathlib import Path

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from audio.sounds import jingle_strys_ready

API_URL = "http://localhost:8080/v1/chat/completions"

# Dossier contenant les fichiers de prompt
PROMPTS_DIR = Path(__file__).parent / "prompts"
DEFAULT_PROMPT_FILE = PROMPTS_DIR / "strys_default.txt"


def load_system_prompt(path=DEFAULT_PROMPT_FILE):
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        print(f"Erreur : fichier de prompt introuvable ({path})")
        sys.exit(1)


def ask_strys(message, system_prompt, history=None):
    if history is None:
        history = []

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    try:
        response = requests.post(
            API_URL,
            json={"messages": messages, "temperature": 0.7, "max_tokens": 200},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        print("Erreur : impossible de joindre le serveur llama-server.")
        print("Vérifie qu'il tourne bien : ./llama.cpp/build/bin/llama-server -m models/qwen2.5-0.5b-instruct-q4_k_m.gguf --port 8080")
        sys.exit(1)


def main():
    system_prompt = load_system_prompt()

    print("=== Strys — mode test CLI ===")
    print(f"(Prompt chargé : {DEFAULT_PROMPT_FILE.name})")
    print("(Ctrl+C pour quitter)\n")

    jingle_strys_ready()

    history = []
    while True:
        try:
            user_input = input("Vous > ").strip()
            if not user_input:
                continue

            reply = ask_strys(user_input, system_prompt, history)
            print(f"Strys > {reply}\n")

            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": reply})

            if len(history) > 10:
                history = history[-10:]

        except KeyboardInterrupt:
            print("\nÀ votre service, Monsieur. À bientôt.")
            break


if __name__ == "__main__":
    main()