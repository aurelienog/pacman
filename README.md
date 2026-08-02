*This project has been created as part of the 42 curriculum by oshtohri, aunoguei.*

```
pacman/
├── docs/                      # Project Management documentation (Gantt, Risks, etc.)
├── config.json                # Default configuration file
├── pac-man.py                 # Main entry point (python3 pac-man.py config.json)
├── Makefile                   # Mandatory rules: install, run, debug, clean, lint, lint-strict
├── README.md                  # Compliant with required layout (header line, mandatory sections)
├── requirements.txt           # Or pyproject.toml / uv.lock
└── src/
    ├── __init__.py
    ├── core/
    │   ├── engine.py          # Game Loop and State Machine
    │   └── config_loader.py   # JSON parser with comment support and default fallback
    ├── domain/
    │   ├── player.py          # Pac-Man player logic
    │   ├── ghost.py           # Ghost AI logic
    │   ├── maze.py            # Map state and collision handling
    │   └── cheat.py           # Cheat Mode logic
    ├── adapters/
    │   ├── maze_adapter.py    # Integration with external A-Maze-ing package
    │   └── highscore.py       # Highscores persistence
    └── ui/
        ├── renderer.py        # Graphics rendering (MLX / Pygame)
        └── screens.py         # Navigation menus, HUD, and dialogs
```


Transform → gestiona posiciones y operaciones geométricas.
Entity → mantiene el estado del movimiento (speed, direction, next_direction).
Maze → decide si una casilla es transitable.
Level → coordina el flujo del juego (movimiento, giros, colisiones, IA, recogida de objetos...).