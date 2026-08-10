"""Command-line entry point for Pac-Man."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

try:
    from src.adapters import (AmazingMazeFactory,
                              ConfigLoader, MazeGenerationError)
except ImportError:
    print("❌ [ERROR] Missing dependency: mazegenerator")
    sys.exit(1)

try:
    from src.ui.pygame_app import PygameApplication
except ImportError:
    print("❌ [ERROR] Missing dependency: pygame")
    print("Install it with: pip install pygame")
    sys.exit(1)

from src.application import GameSession
from src.adapters import JsonHighscoreRepository
from src.scores import ScoreRegistry


def main(argv: list[str] | None = None) -> int:
    """Build adapters, validate arguments and launch the application."""
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("❌ [ERROR] Usage: python3 pac-man.py <config.json>")
        return 2

    config_path = Path(arguments[0])
    if config_path.suffix.lower() != ".json":
        print("❌ [ERROR] configuration file must have a .json extension.")
        return 2

    if not config_path.is_file():
        print(f"❌ [ERROR] configuration file '{config_path}' not found.")
        return 2

    logging.basicConfig(level=logging.WARNING,
                        format="%(levelname)s: %(message)s")

    config = ConfigLoader.load(config_path)
    repository = JsonHighscoreRepository(config.highscore_filename)
    score_registry = ScoreRegistry(repository)
    session = GameSession(config, AmazingMazeFactory())

    try:
        return PygameApplication(session, score_registry).run()
    except MazeGenerationError as error:
        print(f"❌ [ERROR] Could not start the game: {error}")
        return 1
    except Exception as error:
        print(f"❌ [ERROR] Unexpected error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
