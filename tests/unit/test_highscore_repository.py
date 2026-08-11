"""Tests for JSON high-score persistence."""

import json

from src.scores.highscore import Highscore
from src.adapters.json_highscore_repository import JsonHighscoreRepository


def test_load_returns_empty_list_when_file_does_not_exist(
    tmp_path,
) -> None:
    """Missing high-score files should return an empty list."""
    repository = JsonHighscoreRepository(
        str(tmp_path / "highscores.json")
    )

    assert repository.load() == []


def test_save_and_load_scores(tmp_path) -> None:
    """Saved scores should be correctly restored."""
    path = tmp_path / "highscores.json"
    repository = JsonHighscoreRepository(str(path))

    scores = [
        Highscore("AAA", 900),
        Highscore("BBB", 500),
    ]

    repository.save(scores)

    assert repository.load() == scores


def test_save_creates_parent_directories(tmp_path) -> None:
    """Saving should create missing parent directories."""
    path = tmp_path / "data" / "scores" / "highscores.json"
    repository = JsonHighscoreRepository(str(path))

    scores = [Highscore("AAA", 500)]

    repository.save(scores)

    assert path.exists()
    assert repository.load() == scores


def test_saved_file_contains_expected_json(tmp_path) -> None:
    """Saved JSON should contain name and score fields."""
    path = tmp_path / "highscores.json"
    repository = JsonHighscoreRepository(str(path))

    repository.save([
        Highscore("PACMAN", 1234),
    ])

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == [
        {
            "name": "PACMAN",
            "score": 1234,
        }
    ]


def test_load_returns_empty_list_for_invalid_json(tmp_path) -> None:
    """Invalid JSON should result in an empty score list."""
    path = tmp_path / "highscores.json"
    path.write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    repository = JsonHighscoreRepository(str(path))

    assert repository.load() == []


def test_load_returns_empty_list_when_root_is_not_list(
    tmp_path,
) -> None:
    """The JSON root must be an array."""
    path = tmp_path / "highscores.json"
    path.write_text(
        '{"name": "AAA", "score": 500}',
        encoding="utf-8",
    )

    repository = JsonHighscoreRepository(str(path))

    assert repository.load() == []


def test_load_ignores_non_dictionary_entries(tmp_path) -> None:
    """Invalid array entries should be ignored."""
    path = tmp_path / "highscores.json"
    path.write_text(
        json.dumps([
            {"name": "AAA", "score": 500},
            "invalid",
            123,
            None,
        ]),
        encoding="utf-8",
    )

    repository = JsonHighscoreRepository(str(path))

    assert repository.load() == [
        Highscore("AAA", 500),
    ]


def test_load_ignores_entries_with_invalid_names(tmp_path) -> None:
    """Entries with non-string names should be ignored."""
    path = tmp_path / "highscores.json"
    path.write_text(
        json.dumps([
            {"name": "AAA", "score": 500},
            {"name": 123, "score": 400},
            {"score": 300},
        ]),
        encoding="utf-8",
    )

    repository = JsonHighscoreRepository(str(path))

    assert repository.load() == [
        Highscore("AAA", 500),
    ]


def test_load_ignores_entries_with_invalid_scores(tmp_path) -> None:
    """Entries with non-integer scores should be ignored."""
    path = tmp_path / "highscores.json"
    path.write_text(
        json.dumps([
            {"name": "AAA", "score": 500},
            {"name": "BBB", "score": 10.5},
            {"name": "CCC", "score": True},
            {"name": "DDD", "score": "300"},
        ]),
        encoding="utf-8",
    )

    repository = JsonHighscoreRepository(str(path))

    assert repository.load() == [
        Highscore("AAA", 500),
    ]


def test_load_strips_name_whitespace(tmp_path) -> None:
    """Loaded names should have surrounding whitespace removed."""
    path = tmp_path / "highscores.json"
    path.write_text(
        json.dumps([
            {"name": "  PACMAN  ", "score": 500},
        ]),
        encoding="utf-8",
    )

    repository = JsonHighscoreRepository(str(path))

    assert repository.load() == [
        Highscore("PACMAN", 500),
    ]
