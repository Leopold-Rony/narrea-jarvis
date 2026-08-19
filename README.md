# Naræa / Jarvis

Un assistant IA local, esthétique rétro (boot DOS/90s, phosphore vert), tournant entièrement sur un HP ProBook 450 G7 recyclé.

Pas de cloud, pas de GPU, pas d'environnement graphique — juste un CPU i3, 4 Go de RAM, et un LLM local qui tient dans cette contrainte.

---

## Contexte matériel

| | |
|---|---|
| **Machine** | HP ProBook 450 G7 (hostname `melinda`) |
| **CPU** | Intel Core i3-10110U (AVX2) |
| **RAM** | 4 Go DDR4 — contrainte principale du projet |
| **Stockage** | ~500 Go HDD |
| **GPU** | Intel UHD (aucun calcul GPU utilisé, tout tourne sur CPU) |
| **OS** | Debian Trixie, mode texte pur (pas de DE, pour préserver la RAM) |
| **Utilisateur système** | `qsnoopy` |

## Stack technique

- **Interface** : Python, [Textual](https://github.com/Textualize/textual) / [Rich](https://github.com/Textualize/rich)
- **Moteur IA** : [llama.cpp](https://github.com/ggerganov/llama.cpp), compilé avec `-DGGML_NATIVE=ON` (AVX2)
- **Modèle** : Qwen2.5-0.5B-Instruct, quantification Q4_K_M (~400 Mo)
- **API locale** : serveur HTTP compatible OpenAI (`llama-server`, `/v1/chat/completions`)

---

## Structure du repo

```
narrea-jarvis/
├── boot/         # Séquence de démarrage scénarisée (esthétique DOS/90s)
├── ui/           # Interface TUI principale (Textual/Rich)
├── jarvis/       # Personnalité Jarvis, system prompt, logique de conversation
├── animations/   # Animations ASCII (Matrix, rotation 3D, etc.)
├── audio/        # Sons de notification rétro 8-bit
└── mobile/       # Nœud mobile Android/Termux (Phase 5)
```

---

## Roadmap

| Phase | Contenu | Statut |
|---|---|---|
| 0 | Fondations système | ✅ Terminé |
| 1 | Mise à jour et préparation | ✅ Terminé |
| 2 | Stack TUI | ✅ Terminé |
| 3 | Moteur IA local | ✅ Terminé |
| 4 | Boot & esthétique rétro | 🚧 En cours |
| 5 | Nœud mobile (Android/Termux) | À venir |
| 6 | Architecture distribuée | À venir |
| 7 | Fonctionnalités avancées | À venir |
| 8 | Évolutions matérielles (RAM/SSD) | À évaluer plus tard |

### Détail Phase 4 — en cours

- [x] Script de démarrage scénarisé (`boot/boot.py`)
- [ ] Animations ASCII (rotation 3D, effet Matrix)
- [ ] Intégration de la personnalité Jarvis via system prompt
- [ ] Sons de notification rétro 8-bit
- [ ] Lancement automatique au démarrage (autologin + auto-start)

---

## Notes de développement

- Développement principal sur PC (VS Code + GitHub Desktop), test et exécution exclusivement sur le ProBook (`git pull` + venv)
- `venv/`, `models/*.gguf` et `llama.cpp/` sont exclus du repo (voir `.gitignore`) — trop volumineux et regénérables localement
- Toutes les décisions d'architecture découlent de la contrainte RAM (4 Go) : mode texte pur, modèle 0.5B, quantification agressive