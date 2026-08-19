#!/usr/bin/env python3
"""
Chat CLI avec Jarvis — Naræa/Jarvis
Interroge le serveur llama-server local avec le system prompt Jarvis.
"""
import requests
import sys

API_URL = "http://localhost:8080/v1/chat/completions"

SYSTEM_PROMPT = """Tu es Jarvis, l'assistant IA personnel du système Naræa. Tu es poli, déférent et élégant dans tes formulations, à la manière d'un majordome britannique — mais tu restes concis et utile, jamais bavard inutilement.

Règles :
- Adresse-toi à l'utilisateur avec respect (ex: "Monsieur", "à votre service").
- Réponds dans la même langue que la question posée (français ou anglais).
- Reste bref : 1 à 3 phrases sauf si on te demande plus de détails.
- Tu n'es ni Qwen, ni un assistant Alibaba Cloud : tu es Jarvis, et uniquement Jarvis."""


def ask_jarvis(message, history=None):
    if history is None:
        history = []

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
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
    print("=== Jarvis — mode test CLI ===")
    print("(Ctrl+C pour quitter)\n")

    history = []
    while True:
        try:
            user_input = input("Vous > ").strip()
            if not user_input:
                continue

            reply = ask_jarvis(user_input, history)
            print(f"Jarvis > {reply}\n")

            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": reply})

            # on garde un historique court pour ne pas surcharger le contexte
            # (important vu la taille limitée du modèle et la RAM disponible)
            if len(history) > 10:
                history = history[-10:]

        except KeyboardInterrupt:
            print("\nÀ votre service, Monsieur. À bientôt.")
            break


if __name__ == "__main__":
    main()