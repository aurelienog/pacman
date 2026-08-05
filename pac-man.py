from src.adapters import ConfigLoader, JsonHighscoreRepository
from src.scores import ScoreRegistry
from src.domain import GameConfig

import sys
from pathlib import Path


# try:
#     import pygame
# except ImportError:
#     print("❌ [ERROR] Missing dependency: pygame")
#     print("Install it with: pip install pygame")
#     sys.exit(1)

# try:
#     import src.adapters.amazing_maze_factory
# except ImportError:
#     print("❌ [ERROR] Missing dependency: mazegenerator")
#     sys.exit(1)


def main() -> None:
    if len(sys.argv) != 2:
        print("❌ [ERROR] Usage: python3 pac-man.py <config.json>")
        return

    config_path = Path(sys.argv[1])
    if config_path.suffix.lower() != ".json":
        print("❌ [ERROR] configuration file must have a .json extension.")
        return

    if not config_path.is_file():
        print(f"❌ [ERROR] configuration file '{config_path}' not found.")
        return

    config: GameConfig = ConfigLoader.load(config_path)
    repository: JsonHighscoreRepository = JsonHighscoreRepository(
        config.highscore_filename)
    score_registry = ScoreRegistry(repository)
    print(score_registry.scores)


if __name__ == "__main__":
    main()
