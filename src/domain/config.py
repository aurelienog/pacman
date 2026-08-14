from dataclasses import dataclass, field


class Defaults:
    """Define default values for game configuration settings.

    These values are used by the configuration loader when settings
    are missing, invalid, or otherwise cannot be safely parsed.

    Attributes:
        WIDTH: Default maze width in cells.
        HEIGHT: Default maze height in cells.
        LIVES: Default number of player lives.
        PACGUM: Default number of Pac-Gums in a level.
        POINTS_PER_PACGUM: Points awarded for collecting a Pac-Gum.
        POINTS_PER_SUPER: Points awarded for collecting a Super Pac-Gum.
        POINTS_PER_GHOST: Points awarded for eating a frightened ghost.
        MAX_TIME: Default maximum time allowed for a level.
        HIGHSCORE_FILENAME: Default file used to store high scores.
        MIN_LEVEL_COUNT: Minimum number of levels required by the game.
    """
    WIDTH = 15
    HEIGHT = 15

    LIVES = 3
    PACGUM = 42
    POINTS_PER_PACGUM = 10
    POINTS_PER_SUPER = 50
    POINTS_PER_GHOST = 200
    MAX_TIME = 150

    HIGHSCORE_FILENAME = "highscores.json"

    MIN_LEVEL_COUNT = 10


class Limits:
    """Define validation limits for game configuration settings.

    Values outside these ranges are clamped by the configuration
    loader before being stored in the validated configuration objects.

    Attributes:
        WIDTH_RANGE: Minimum and maximum maze width in cells.
        HEIGHT_RANGE: Minimum and maximum maze height in cells.
        LIVES_RANGE: Minimum and maximum number of player lives.
        PACGUM_POINTS_RANGE: Valid range for Pac-Gum points.
        SUPER_POINTS_RANGE: Valid range for Super Pac-Gum points.
        GHOST_POINTS_RANGE: Valid range for ghost points.
        LEVEL_TIME_RANGE: Minimum and maximum level duration in seconds.
        SEED_RANGE: Minimum and maximum accepted random seed values.
    """
    WIDTH_RANGE = (15, 21)
    HEIGHT_RANGE = (15, 21)

    LIVES_RANGE = (1, 99)

    PACGUM_POINTS_RANGE = (0, 10_000)
    SUPER_POINTS_RANGE = (0, 10_000)
    GHOST_POINTS_RANGE = (0, 100_000)

    LEVEL_TIME_RANGE = (10, 3_600)
    SEED_RANGE = (0, 2**31 - 1)


@dataclass(frozen=True, slots=True)
class LevelConfig:
    """Store validated configuration values for one game level.

    Attributes:
        width: Maze width in cells.
        height: Maze height in cells.
        pacgum: Number of Pac-Gums placed in the level.
        seed: Optional random seed used to generate the maze.
        level_max_time: Maximum time allowed to complete the level,
            in seconds.
    """
    width: int = Defaults.WIDTH
    height: int = Defaults.HEIGHT
    pacgum: int = Defaults.PACGUM
    seed: int | None = None
    level_max_time: int = Defaults.MAX_TIME


@dataclass(frozen=True, slots=True)
class GameConfig:
    """Store validated configuration values used by the game.

    Attributes:
        highscore_filename: File used to persist the top scores.
        lives: Number of lives granted to the player.
        points_per_pacgum: Points awarded for collecting a Pac-Gum.
        points_per_super_pacgum: Points awarded for collecting a Super
            Pac-Gum.
        points_per_ghost: Points awarded for eating a frightened ghost.
        levels: Immutable sequence containing the configuration of every
            game level.
    """
    highscore_filename: str = Defaults.HIGHSCORE_FILENAME
    lives: int = Defaults.LIVES
    points_per_pacgum: int = Defaults.POINTS_PER_PACGUM
    points_per_super_pacgum: int = Defaults.POINTS_PER_SUPER
    points_per_ghost: int = Defaults.POINTS_PER_GHOST
    levels: tuple[LevelConfig, ...] = field(default_factory=tuple)
