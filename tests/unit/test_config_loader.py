import logging

from src.adapters import ConfigLoader
from src.domain.config import Defaults, Limits, LevelConfig


# ============================================================================
# JSON LOADING
# ============================================================================

def test_load_valid_configuration(tmp_path):
    """Load a valid configuration file successfully.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """

    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "highscore_filename": "scores.json",
            "lives": 5,
            "points_per_pacgum": 25,
            "points_per_super_pacgum": 100,
            "points_per_ghost": 500,
            "levels": [
                {
                    "width": 25,
                    "height": 31,
                    "pacgum": 80,
                    "seed": 42,
                    "level_max_time": 120
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    config = ConfigLoader.load(config_file)

    assert config.highscore_filename == "scores.json"
    assert config.lives == 5
    assert config.points_per_pacgum == 25
    assert config.points_per_super_pacgum == 100
    assert config.points_per_ghost == 500

    assert len(config.levels) == Defaults.MIN_LEVEL_COUNT

    level = config.levels[0]

    assert level.width == 25
    assert level.height == 31
    assert level.pacgum == 80
    assert level.seed == 42
    assert level.level_max_time == 120


# def test_missing_file_uses_defaults(tmp_path, caplog):
#     """Use default values when the configuration file is missing.

#     Args:
#         tmp_path: Temporary directory provided by pytest.
#         caplog: Pytest fixture used to capture log messages.

#     Returns:
#         None.
#     """
#     config_file = tmp_path / "config.json"

#     caplog.set_level(logging.WARNING)

#     config = ConfigLoader.load(config_file)

#     assert config.highscore_filename == Defaults.HIGHSCORE_FILENAME
#     assert config.lives == Defaults.LIVES
#     assert config.points_per_pacgum == Defaults.POINTS_PER_PACGUM
#     assert config.points_per_super_pacgum == Defaults.POINTS_PER_SUPER
#     assert config.points_per_ghost == Defaults.POINTS_PER_GHOST

#     assert "Could not read configuration" in caplog.text


# def test_empty_file_uses_defaults(tmp_path, caplog):
#     config_file = tmp_path / "config.json"
#     config_file.write_text("", encoding="utf-8")

#     caplog.set_level(logging.WARNING)

#     config = ConfigLoader.load(config_file)

#     assert config.lives == Defaults.LIVES
#     assert "Could not read configuration" in caplog.text


def test_invalid_json_uses_defaults(tmp_path, caplog):
    """Use default values when the JSON document is malformed.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """

    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "lives": 5,
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.highscore_filename == Defaults.HIGHSCORE_FILENAME
    assert config.lives == Defaults.LIVES
    assert config.points_per_pacgum == Defaults.POINTS_PER_PACGUM
    assert config.points_per_super_pacgum == Defaults.POINTS_PER_SUPER
    assert config.points_per_ghost == Defaults.POINTS_PER_GHOST

    assert "Using defaults." in caplog.text


def test_root_must_be_dictionary(tmp_path, caplog):
    """Reject configuration files whose root element is not an object.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"
    config_file.write_text(
        """
        [
            1,
            2,
            3
        ]
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.lives == Defaults.LIVES
    assert config.highscore_filename == Defaults.HIGHSCORE_FILENAME
    assert "Configuration root must be an object" in caplog.text


# ============================================================================
# COMMENTS
# ============================================================================

def test_comments_are_ignored(tmp_path):
    """Ignore line comments while parsing the configuration file.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"
    config_file.write_text(
        """
        {
            # This is a comment
            "lives": 5,

            // Another comment
            "points_per_pacgum": 25
        }
        """,
        encoding="utf-8",
    )

    config = ConfigLoader.load(config_file)

    assert config.lives == 5
    assert config.points_per_pacgum == 25


# ============================================================================
# UNKNOWN KEYS
# ============================================================================

def test_unknown_keys_are_ignored(tmp_path, caplog):
    """Ignore unsupported configuration keys.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"
    config_file.write_text(
        """
        {
            "lives": 4,
            "unknown_key": 12345,
            "another_one": true
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.lives == 4

    assert "Ignoring unknown configuration key 'unknown_key'" in caplog.text
    assert "Ignoring unknown configuration key 'another_one'" in caplog.text


# def test_missing_key_uses_default(tmp_path):
#     config_file = tmp_path / "config.json"
#     config_file.write_text(
#         """
#         {
#             "lives": 8
#         }
#         """,
#         encoding="utf-8",
#     )

#     config = ConfigLoader.load(config_file)

#     assert config.lives == 8
#     assert config.points_per_pacgum == Defaults.POINTS_PER_PACGUM
#     assert config.points_per_super_pacgum == Defaults.POINTS_PER_SUPER
#     assert config.points_per_ghost == Defaults.POINTS_PER_GHOST
#     assert config.highscore_filename == Defaults.HIGHSCORE_FILENAME

# ============================================================================
# NUMERIC VALIDATION
# ============================================================================

def test_values_below_minimum_are_clamped(tmp_path, caplog):
    """Clamp numeric values below the allowed minimum.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "lives": -5,
            "levels": [
                {
                    "width": 5,
                    "height": 7,
                    "level_max_time": 1
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.lives == Limits.LIVES_RANGE[0]
    assert config.levels[0].width == Limits.WIDTH_RANGE[0]
    assert config.levels[0].height == Limits.HEIGHT_RANGE[0]
    assert config.levels[0].level_max_time == Limits.LEVEL_TIME_RANGE[0]

    assert "Clamped" in caplog.text


def test_values_above_maximum_are_clamped(tmp_path, caplog):
    """Clamp numeric values above the allowed maximum.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "points_per_ghost": 999999999,
            "levels": [
                {
                    "width": 100,
                    "height": 100,
                    "level_max_time": 999999
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.points_per_ghost == Limits.GHOST_POINTS_RANGE[1]
    assert config.levels[0].width == Limits.WIDTH_RANGE[1]
    assert config.levels[0].height == Limits.HEIGHT_RANGE[1]
    assert config.levels[0].level_max_time == Limits.LEVEL_TIME_RANGE[1]

    assert "Clamped" in caplog.text


def test_invalid_integer_uses_default(tmp_path, caplog):
    """Replace invalid integer values with their defaults.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "lives": "three"
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.lives == Defaults.LIVES
    assert "must be an integer" in caplog.text


def test_boolean_is_not_integer(tmp_path, caplog):
    """Reject boolean values where integers are expected.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "lives": true
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.lives == Defaults.LIVES
    assert "must be an integer" in caplog.text

# ============================================================================
# TEXT VALIDATION
# ============================================================================


def test_empty_filename_uses_default(tmp_path, caplog):
    """Replace an empty filename with the default value.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "highscore_filename": "     "
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.highscore_filename == Defaults.HIGHSCORE_FILENAME
    assert "is empty" in caplog.text


def test_non_string_filename_uses_default(tmp_path, caplog):
    """Replace a non-string filename with the default value.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "highscore_filename": 123
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.highscore_filename == Defaults.HIGHSCORE_FILENAME
    assert "must be a string" in caplog.text


# ============================================================================
# LEVEL PARSING
# ============================================================================

def test_missing_levels_creates_default_levels(tmp_path, caplog):
    """Create default levels when the 'levels' key is missing.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        "{}",
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert len(config.levels) == Defaults.MIN_LEVEL_COUNT
    assert all(level == LevelConfig() for level in config.levels)

    assert "Missing or invalid 'levels'" in caplog.text


def test_invalid_levels_creates_default_levels(tmp_path, caplog):
    """Create default levels when the 'levels' value is invalid.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "levels": 123
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert len(config.levels) == Defaults.MIN_LEVEL_COUNT
    assert all(level == LevelConfig() for level in config.levels)

    assert "Missing or invalid 'levels'" in caplog.text


def test_invalid_level_entry_uses_default(tmp_path, caplog):
    """Replace an invalid level entry with default values.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "levels": [
                123
            ]
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    config = ConfigLoader.load(config_file)

    assert config.levels[0] == LevelConfig()

    assert "Level 0 is invalid" in caplog.text


def test_even_width_is_converted_to_odd(tmp_path):
    """Convert an even level width to the next odd value.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "levels": [
                {
                    "width": 20
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    config = ConfigLoader.load(config_file)

    assert config.levels[0].width == 21


def test_even_height_is_converted_to_odd(tmp_path):
    """Convert an even level height to the next odd value.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "levels": [
                {
                    "height": 18
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    config = ConfigLoader.load(config_file)

    assert config.levels[0].height == 19


# def test_width_is_clamped_before_becoming_odd(tmp_path):
#     config_file = tmp_path / "config.json"

#     config_file.write_text(
#         """
#         {
#             "levels": [
#                 {
#                     "width": 100
#                 }
#             ]
#         }
#         """,
#         encoding="utf-8",
#     )

#     config = ConfigLoader.load(config_file)

#     # 100 -> clamp 40 -> odd 41
#     assert config.levels[0].width == 41


def test_level_values_are_clamped(tmp_path):
    """Clamp all numeric values inside a level configuration.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "levels": [
                {
                    "width": 1,
                    "height": 100,
                    "pacgum": 999999,
                    "seed": 999999999999,
                    "level_max_time": 1
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    config = ConfigLoader.load(config_file)

    level = config.levels[0]

    assert level.width == Limits.WIDTH_RANGE[0]
    assert level.height == Limits.HEIGHT_RANGE[1]
    assert level.pacgum == Limits.WIDTH_RANGE[0] * Limits.HEIGHT_RANGE[1]
    assert level.seed == Limits.SEED_RANGE[1]
    assert level.level_max_time == Limits.LEVEL_TIME_RANGE[0]


def test_extra_levels_are_preserved(tmp_path):
    """Load every level provided in the configuration file.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    levels = ",".join(
        '{"width": 21, "height": 21}'
        for _ in range(30)
    )

    config_file.write_text(
        f'{{"levels":[{levels}]}}',
        encoding="utf-8",
    )

    config = ConfigLoader.load(config_file)

    assert len(config.levels) == 30


def test_missing_levels_are_completed(tmp_path):
    """Append default levels until the minimum level count is reached.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "levels": [
                {
                    "width": 31,
                    "height": 31
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    config = ConfigLoader.load(config_file)

    assert len(config.levels) == Defaults.MIN_LEVEL_COUNT

    assert config.levels[0].width == 31
    assert config.levels[0].height == 31

    for level in config.levels[1:]:
        assert level == LevelConfig()


# ============================================================================
# LOGGING
# ============================================================================

def test_warning_is_logged_for_unknown_key(tmp_path, caplog):
    """Log a warning for unknown configuration keys.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "foo": 123
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    ConfigLoader.load(config_file)

    assert "Ignoring unknown configuration key" in caplog.text


def test_warning_is_logged_for_invalid_value(tmp_path, caplog):
    """Log a warning for invalid configuration values.

    Args:
        tmp_path: Temporary directory provided by pytest.
        caplog: Pytest fixture used to capture log messages.

    Returns:
        None.
    """
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "lives": "three"
        }
        """,
        encoding="utf-8",
    )

    caplog.set_level(logging.WARNING)

    ConfigLoader.load(config_file)

    assert "'lives' must be an integer" in caplog.text


# def test_warning_is_logged_for_missing_file(tmp_path, caplog):
#     """Log a warning when the configuration file cannot be read.

#     Args:
#         tmp_path: Temporary directory provided by pytest.
#         caplog: Pytest fixture used to capture log messages.

#     Returns:
#         None.
#     """
#     config_file = tmp_path / "missing.json"

#     caplog.set_level(logging.WARNING)

#     ConfigLoader.load(config_file)

#     assert "Could not read configuration" in caplog.text


# ============================================================================
# SUMMARY
# ============================================================================

# | Group                | Tests |
# | -------------------- | -----:|
# | JSON loading         |      3 |
# | Comments             |      1 |
# | Unknown keys         |      1 |
# | Numeric validation   |      4 |
# | Text validation      |      2 |
# | Level parsing        |      8 |
# | Logging              |      2 |
# | **Total**            | **21** |
