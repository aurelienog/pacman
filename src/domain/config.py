from dataclasses import dataclass, field


class Defaults:
    """Default configuration values used when settings are missing or invalid.

    These constants define the safe fallback values applied by the
    configuration loader whenever a configuration entry cannot be
    read or validated.
    """
    WIDTH = 21
    HEIGHT = 21

    LIVES = 3
    PACGUM = 42
    POINTS_PER_PACGUM = 10
    POINTS_PER_SUPER = 50
    POINTS_PER_GHOST = 200
    MAX_TIME = 90

    HIGHSCORE_FILENAME = "highscores.json"

    MIN_LEVEL_COUNT = 10


class Limits:
    """Validation limits for configurable game settings.

    These constants define the minimum and maximum accepted values
    for configuration entries. Values outside these ranges are
    clamped by the configuration loader.
    """
    WIDTH_RANGE = (14, 41)
    HEIGHT_RANGE = (14, 41)

    LIVES_RANGE = (1, 99)

    PACGUM_POINTS_RANGE = (0, 10_000)
    SUPER_POINTS_RANGE = (0, 10_000)
    GHOST_POINTS_RANGE = (0, 100_000)

    LEVEL_TIME_RANGE = (10, 3_600)
    SEED_RANGE = (0, 2**31 - 1)


@dataclass(frozen=True, slots=True)
class LevelConfig:
    """Validated configuration values for a single game level."""
    width: int = Defaults.WIDTH
    height: int = Defaults.HEIGHT
    pacgum: int = Defaults.PACGUM
    seed: int | None = None
    level_max_time: int = Defaults.MAX_TIME


@dataclass(frozen=True, slots=True)
class GameConfig:
    """Validated configuration values used by the game."""
    highscore_filename: str = Defaults.HIGHSCORE_FILENAME
    lives: int = Defaults.LIVES
    points_per_pacgum: int = Defaults.POINTS_PER_PACGUM
    points_per_super_pacgum: int = Defaults.POINTS_PER_SUPER
    points_per_ghost: int = Defaults.POINTS_PER_GHOST
    levels: tuple[LevelConfig, ...] = field(default_factory=tuple)
