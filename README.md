*This project has been created as part of the 42 curriculum by oshtohri, aunoguei.*


# Pac-Man 🟡👻

A complete, modern, and modular recreation of the classic 1980 Namco arcade game **Pac-Man**, implemented in Python 3.10+ using object-oriented architecture, clean code principles, and Pygame constrained to MLX-equivalent graphical primitives.

---

## Table of Contents

- [Description](#description)
- [Instructions](#instructions)
- [Configuration](#configuration)
- [Highscore System](#highscore-system)
- [Maze Generation](#maze-generation)
- [Implementation](#implementation)
- [General Software Architecture](#general-software-architecture)
- [Project Management](#project-management)
- [Resources & AI Usage](#resources--ai-usage)

---

## Description

The goal of this project is to build a fully functional arcade Pac-Man game with multi-level progression, persistent scoring, intelligent ghost behavior, custom configuration handling, and cheat modes for review purposes.

### Key Features
- **Arcade Gameplay**: Smooth corridor navigation, score tracking, dynamic HUD, power pellets (Super Pacgums), and frightened/respawning ghost mechanics.
- **Distinct Ghost AI**: Four unique ghost personalities (Blinky, Pinky, Inky, Clyde) powered by Breadth-First Search (BFS) pathfinding.
- **Robust Configuration**: Configurable parameters via JSON files supporting comments (`#` and `//`) with graceful fallback handling.
- **Third-Party Maze Adapter**: Seamless integration with assigned `A-Maze-ing` package producing non-perfect Pac-Man corridors.
- **Persistent Highscores**: Top 10 leaderboard saved to disk with player name validation.
- **Interactive & Responsive UI**: Custom sprite atlases, responsive HUD, mouse & keyboard navigation, and scaled game views.
- **Cheat Suite**: Built-in developer hotkeys for peer review evaluation.

---

## Instructions

### Prerequisites
- Python 3.10 or later
- `pip` or any modern Python package manager (`uv`, `venv`)

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd pac-man
   ```

2. **Install dependencies via Makefile**:
   ```bash
   make install
   ```

3. **Execution**:
   Launch the game by providing a valid configuration file:
   ```bash
   python3 pac-man.py config.json
   ```
   or using the Makefile:
   ```bash
   make run
   ```

### Makefile Targets

| Command | Description |
| :--- | :--- |
| `make install` | Install required project dependencies (`pygame`). |
| `make run` | Execute the main game entry point with `config.json`. |
| `make debug` | Run the main script in debug mode using `pdb`. |
| `make clean` | Clean temporary files, bytecode (`__pycache__`), and cache directories. |
| `make lint` | Run static analysis using `flake8 .` and `mypy` with mandatory flags. |
| `make lint-strict` | Execute strict linting checks (`mypy --strict`). |

---

## Configuration

The game is configured via a JSON file provided as the command-line argument. The loader is robust, ignoring comments and clamping out-of-range or missing values to safe defaults without raising uncaught exceptions.

### Comment Handling
Lines starting with `#` or `//` are stripped prior to JSON parsing.

### Configuration Schema (`config.json`)

```json
{
  # Path to persistent leaderboard storage
  "highscore_filename": "highscores.json",

  # Player starting lives and scoring parameters
  "lives": 3,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,

  # Multilevel Array (At least 10 levels enforced automatically)
  "levels": [
    {
      "level_number": 1,
      "width": 21,
      "height": 21,
      "pacgum": 42,
      "seed": 42,
      "level_max_time": 90
    },
    ...
  ]
}
```

### Faulty Config Handling
If keys are missing, invalid, or corrupted, the loader logs a clear warning message (`LOGGER.warning`), clamps numerical values to valid boundaries (`Limits`), and guarantees at least 10 levels using default `LevelConfig` instances.

---

## Highscore System

The persistent highscore system is encapsulated within the `ScoreRegistry` and backed by `JsonHighscoreRepository`.

### System Highlights:
- **Persistence**: Saved to a JSON file specified in the configuration (`highscore_filename`).
- **Validation**:
  - Names are restricted to 1–10 characters containing only alphanumeric characters and spaces (`[A-Za-z0-9 ]{1,10}`).
  - Scores are validated as non-negative integers ($\ge 0$).
- **Top 10 Retention**: Only the top 10 highest scores are retained on disk, sorted in descending order.
- **Error Resiliency**: Unreadable, corrupt, or missing files gracefully return an empty score registry without crashing the application.
- **Design Rationale**: Decoupling persistence from the domain logic ensures that highscore management can be independently unit-tested without disk I/O dependencies.

---

## Maze Generation

Maze generation relies on the assigned external `A-Maze-ing` wheel package without modifying its internal source code.

### Integration Adapter (`AmazingMazeFactory`)
- The game engine interacts with `MazeFactory` via a clean adapter port (`AmazingMazeFactory`).
- **Corridor Compatibility**: Mazes are generated with `perfect=False` to produce Pac-Man-compatible loops and multiple corridors.
- **Reproducibility**: The first level uses a deterministic fixed seed (e.g., `42`), while subsequent levels generate randomized seeds.
- **Decorative 42 Pattern**: Cells belonging to the decorative `42` central mark (wall bitmask `15`) are flagged as un-walkable obstacles; no collectible items spawn inside them.
- **Error Handling**: If the external package fails to generate a grid or produces an unsolvable maze, `MazeGenerationError` is raised and caught cleanly at startup.

---

## Implementation

### Player & Movement
- Player moves strictly through corridors using WASD or Arrow keys.
- Movement coordinates are interpolated smoothly between logical grid cells (`_player_visual_position`) for fluid rendering.

### Ghost AI & Behavioral States
Ghosts move autonomously using Breadth-First Search (BFS) shortest-path pathfinding, operating in three distinct modes:
1. **Chase Mode**: Each ghost follows a distinct targeting strategy:
   - **Blinky (Red)**: Targets Pac-Man's exact tile.
   - **Pinky (Pink)**: Targets 4 tiles ahead of Pac-Man's direction.
   - **Inky (Cyan)**: Uses Blinky's position and Pac-Man's tile to calculate a mirrored vector target.
   - **Clyde (Orange)**: Chases Pac-Man when far away, but retreats to his corner when within 8 tiles.
2. **Frightened Mode**: Triggered by eating a Super Pacgum. Ghosts turn blue, slow down, move randomly, and become edible for bonus points.
3. **Respawning Mode**: When eaten, a ghost turns into eyes and returns to its home corner before re-entering Chase mode.

### Cheat Mode (Peer Review Tools)
Dedicated hotkeys allow reviewers to easily test game mechanics:
- `I`: Toggle Invincibility (ghosts cannot hurt player).
- `F`: Toggle Ghost Freeze (ghosts stop moving).
- `T`: Toggle Timer Freeze (level timer pauses).
- `B`: Toggle Speed Boost (doubles player movement speed).
- `N`: Level Skip (instantly completes current level).
- `L`: Add Extra Life (+1 life).

### MLX Compliance Rules
To comply with 42 evaluation rules regarding MiniLibX equivalence:
- High-level Pygame convenience methods (such as `Rect.collidepoint`) are replaced with pure mathematical boundary checks (`left <= x <= right`).
- Rendering relies on image blitting (`screen.blit`), basic geometric primitives, and pre-rendered static sprite atlases.

---

## General Software Architecture

The project follows a strict **Hexagonal / Clean Architecture** pattern, enforcing a complete separation between the core simulation engine, domain models, adapters, and UI presentation.

```text
pac-man/
├── config.json
├── highscores.json
├── Makefile
├── pac-man.py
└── src/
    ├── domain/               # Pure business models (Maze, Player, Ghost, Position)
    ├── application/          # Use cases & game loop orchestration (GameSession, AI, Collisions)
    ├── adapters/             # External integration (ConfigLoader, AmazingMazeFactory)
    ├── scores/               # Highscore domain and JsonRepository
    └── ui/                   # Modular presentation layer
        ├── draw_utils.py     # Clean drawing primitives
        ├── input_handler/    # Menu, Pause, Gameplay & EndScreen input sub-handlers
        ├── menu_renderer/   # Modular Main, Pause, Highscore & Instruction views
        ├── game_renderer/   # Modular HUD, Maze, Items & Entities renderers
        └── neon_assets/     # Sprite atlas loaders for Pac-Man, Ghosts & Items
```

### Data Flow & Decoupling
- **`InputAction`**: The UI translates keyboard and mouse events into renderer-independent `InputAction` commands dispatched to `GameSession`.
- **`Snapshot`**: The engine exposes an immutable, read-only `Snapshot` of the current world state per frame. The renderer never modifies domain state directly.

---

## Project Management

The development process followed a structured project management methodology divided into 3 iterations (Timeline, Gantt chart, Risk Matrix, and RACI distribution).

### Team RACI Matrix

| Task / Responsibility | `aunoguei` | `oshtohri` |
| :--- | :---: | :---: |
| Architecture & Layer Contracts | **A / R** | **A / R** |
| Engine Logic & BFS Pathfinding | **A / R** | C |
| Configuration Loader & Limits | **A / R** | C |
| Ghost AI Personalities & States | **A / R** | C |
| Maze Adapter (`A-Maze-ing`) | C | **A / R** |
| Pygame UI & Responsive Scaling | C | **A / R** |
| Sprite Atlases & Visual Assets | C | **A / R** |
| Highscore System Persistence | **A / R** | C |
| Documentation & Packaging | C | **A / R** |

*Key: **A** = Accountable, **R** = Responsible, **C** = Consulted*

All project management evidence, Gantt charts, risk mitigation plans, test plans, and retrospective documents are located in the dedicated repository subdirectory:

📁 **[`/docs/project_management/`](./docs/project_management/)**

---

## Resources & AI Usage

### References & Documentation
- [Pac-Man Dossier by Jamey Pittman](https://www.pacmanfoss.com/) — Detailed arcade mechanics, ghost behavioral logic, and timing specs.
- [Python 3.10+ Typing Documentation](https://docs.python.org/3/library/typing.html) — Static type hints and mypy practices.
- [Pygame Community Docs](https://www.pygame.org/docs/) — Windowing and event loop handling.

### AI Usage Description
In accordance with Chapter II (AI Instructions), AI tools (ChatGPT/Claude) were utilized selectively as a learning and productivity aid:
- **Refactoring & Architecture Brainstorming**: Assisted in discussing clean Hexagonal Architecture boundaries, separating renderer modules from engine state, and designing MLX-compliant primitive abstractions.
- **Documentation & Formatting**: Aided in drafting documentation templates, markdown tables, and organizing project management reports.
- **Code Review & Linting**: Used to double-check edge cases for `flake8` compliance (line length limits, PEP 257 docstrings) and type annotations.
- **Verification**: All AI-generated logic was thoroughly walked through, tested, peer-reviewed, and validated by both team members before integration.

---
