from __future__ import annotations

from pathlib import Path
import json
import logging
import re

from ..domain import Defaults, Limits, LevelConfig, GameConfig

LOGGER = logging.getLogger(__name__)


class ConfigLoader:
    """Load, validate and normalize the game configuration.

    The loader reads a JSON configuration file, ignores comments,
    replaces invalid or missing values with safe defaults, clamps
    values to allowed ranges and returns a validated GameConfig.
    """

    KNOWN_KEYS = {
        "highscore_filename",
        "lives",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "levels",
    }

    @classmethod
    def load(cls, path: Path) -> GameConfig:
        """Load a validated game configuration from a JSON file.

        Args:
            path: Path to the configuration file.

        Returns:
            A validated GameConfig instance.
        """
        raw = cls._load_json(path)
        return cls._build(raw)

    @classmethod
    def _load_json(cls, path: Path) -> dict[str, object]:
        """Read and parse a JSON configuration file.

        Comments are removed before parsing. If the file cannot be
        parsed or the root element is not a JSON object, an empty
        dictionary is returned.

        Args:
            path: Path to the configuration file.

        Returns:
            The parsed configuration dictionary, or an empty dictionary.
        """

        try:
            content = path.read_text(encoding="utf-8")
            raw = json.loads(cls._strip_comments(content))

        except (json.JSONDecodeError) as error:
            LOGGER.warning(
                "Could not parse configuration (%s). Using defaults.",
                error,
            )
            return {}

        if not isinstance(raw, dict):
            LOGGER.warning(
                "Configuration root must be an object. Using defaults."
            )
            return {}

        return raw

    @classmethod
    def _build(cls, raw: dict[str, object]) -> GameConfig:
        """Build a validated GameConfig from raw configuration data.

        Args:
            raw: Raw configuration dictionary.

        Returns:
            A fully validated GameConfig instance.
        """
        cls._warn_unknown_keys(raw)

        return GameConfig(
            highscore_filename=cls._normalize_text(
                raw.get("highscore_filename"),
                Defaults.HIGHSCORE_FILENAME,
                "highscore_filename",
            ),
            lives=cls._normalize_int(
                raw.get("lives"),
                Defaults.LIVES,
                *Limits.LIVES_RANGE,
                "lives",
            ),
            points_per_pacgum=cls._normalize_int(
                raw.get("points_per_pacgum"),
                Defaults.POINTS_PER_PACGUM,
                *Limits.PACGUM_POINTS_RANGE,
                "points_per_pacgum",
            ),
            points_per_super_pacgum=cls._normalize_int(
                raw.get("points_per_super_pacgum"),
                Defaults.POINTS_PER_SUPER,
                *Limits.SUPER_POINTS_RANGE,
                "points_per_super_pacgum",
            ),
            points_per_ghost=cls._normalize_int(
                raw.get("points_per_ghost"),
                Defaults.POINTS_PER_GHOST,
                *Limits.GHOST_POINTS_RANGE,
                "points_per_ghost",
            ),
            levels=cls._parse_levels(raw.get("levels")),
        )

    @classmethod
    def _warn_unknown_keys(cls, raw: dict[str, object]) -> None:
        """Log warnings for unsupported configuration keys.

        Args:
            raw: Raw configuration dictionary.

        Returns:
            None.
        """
        for key in raw:
            if key not in cls.KNOWN_KEYS:
                LOGGER.warning(
                    "Ignoring unknown configuration key '%s'.",
                    key,
                )

    @classmethod
    def _parse_levels(
        cls,
        value: object,
    ) -> tuple[LevelConfig, ...]:
        """Validate and build the list of level configurations.

        Missing, invalid or incomplete levels are replaced with
        default values until the configured number of levels is
        reached.

        Args:
            value: Raw value associated with the "levels" key.

        Returns:
            A tuple containing validated LevelConfig objects.
        """
        if not isinstance(value, list):
            LOGGER.warning(
                "Missing or invalid 'levels'. Using default levels."
            )
            return tuple(LevelConfig()
                         for _ in range(Defaults.MIN_LEVEL_COUNT))

        levels: list[LevelConfig] = []

        for index, entry in enumerate(value):

            if not isinstance(entry, dict):
                LOGGER.warning(
                    "Level %d is invalid. Using defaults.",
                    index,
                )
                entry = {}

            width = cls._normalize_int(
                entry.get("width"),
                Defaults.WIDTH,
                *Limits.WIDTH_RANGE,
                "width",
            )

            height = cls._normalize_int(
                entry.get("height"),
                Defaults.HEIGHT,
                *Limits.HEIGHT_RANGE,
                "height",
            )

            if width % 2 == 0:
                width += 1

            if height % 2 == 0:
                height += 1

            levels.append(
                LevelConfig(
                    width=width,
                    height=height,
                    pacgum=cls._normalize_int(
                        entry.get("pacgum"),
                        Defaults.PACGUM,
                        1,
                        width * height,
                        "pacgum",
                    ),
                    seed=cls._normalize_seed(entry.get("seed")),
                    level_max_time=cls._normalize_int(
                        entry.get("level_max_time"),
                        Defaults.MAX_TIME,
                        *Limits.LEVEL_TIME_RANGE,
                        "level_max_time",
                    ),
                )
            )

        while len(levels) < Defaults.MIN_LEVEL_COUNT:
            levels.append(LevelConfig())

        return tuple(levels)

    @staticmethod
    def _normalize_int(
        value: object,
        default: int,
        minimum: int,
        maximum: int,
        key: str,
    ) -> int:
        """Validate and clamp an integer configuration value.

        Args:
            value: Value to validate.
            default: Value used when the input is missing or invalid.
            minimum: Minimum accepted value.
            maximum: Maximum accepted value.
            key: Configuration key used for logging.

        Returns:
            A validated integer within the allowed range.
        """
        if value is None:
            LOGGER.warning(
                "Missing '%s'. Using default %d.",
                key,
                default,
            )
            return default

        if isinstance(value, bool) or not isinstance(value, int):
            LOGGER.warning(
                "'%s' must be an integer. Using default %d.",
                key,
                default,
            )
            return default

        if value < minimum:
            LOGGER.warning(
                "'%s' below minimum (%d). Clamped to %d.",
                key,
                value,
                minimum,
            )
            return minimum

        if value > maximum:
            LOGGER.warning(
                "'%s' above maximum (%d). Clamped to %d.",
                key,
                value,
                maximum,
            )
            return maximum

        return value

    @classmethod
    def _normalize_seed(cls, value: object) -> int | None:
        """Validate an optional seed value.

        Args:
            value: Raw seed value.

        Returns:
            The validated seed, or None if no seed was provided.
        """
        if value is None:
            return None

        return cls._normalize_int(
            value,
            0,
            *Limits.SEED_RANGE,
            "seed",
        )

    @staticmethod
    def _normalize_text(
        value: object,
        default: str,
        key: str,
    ) -> str:
        """Validate a string configuration value.

        Args:
            value: Value to validate.
            default: Value used when the input is missing or invalid.
            key: Configuration key used for logging.

        Returns:
            A non-empty validated string.
        """
        if value is None:
            LOGGER.warning(
                "Missing '%s'. Using default '%s'.",
                key,
                default,
            )
            return default

        if not isinstance(value, str):
            LOGGER.warning(
                "'%s' must be a string. Using default '%s'.",
                key,
                default,
            )
            return default

        value = value.strip()

        if not value:
            LOGGER.warning(
                "'%s' is empty. Using default '%s'.",
                key,
                default,
            )
            return default

        return value

    @staticmethod
    def _strip_comments(content: str) -> str:
        """Remove line comments from a JSON-with-comments document.

        Both '#' and '//' comments are removed before parsing.

        Args:
            content: Raw configuration file contents.

        Returns:
            The configuration text without comments.
        """
        lines: list[str] = []

        for line in content.splitlines():
            line = re.sub(r"\s*(//|#).*", "", line)

            if line.strip():
                lines.append(line)

        return "\n".join(lines)
