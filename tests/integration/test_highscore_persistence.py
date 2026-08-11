"""Integration tests for high-score persistence."""

import json

from src.adapters.json_highscore_repository import (
    JsonHighscoreRepository,
)
from src.scores.score_registry import ScoreRegistry


def test_highscore_is_persisted_and_loaded(tmp_path) -> None:
    """A score added through the registry should survive a reload."""

    path = tmp_path / "highscores.json"

    repository = JsonHighscoreRepository(str(path))
    registry = ScoreRegistry(repository)

    registry.add("PACMAN", 5000)

    new_repository = JsonHighscoreRepository(str(path))
    new_registry = ScoreRegistry(new_repository)

    assert new_registry.scores == [
        registry.scores[0],
    ]


def test_highscores_are_persisted_in_score_order(tmp_path) -> None:
    """Persisted scores should be restored in descending score order."""

    path = tmp_path / "highscores.json"

    repository = JsonHighscoreRepository(str(path))
    registry = ScoreRegistry(repository)

    registry.add("PLAYER1", 1000)
    registry.add("PLAYER2", 5000)
    registry.add("PLAYER3", 2500)

    new_repository = JsonHighscoreRepository(str(path))
    new_registry = ScoreRegistry(new_repository)

    assert [
        score.score
        for score in new_registry.scores
    ] == [5000, 2500, 1000]


def test_highscore_file_contains_expected_json_format(tmp_path) -> None:
    """Persisted scores should use the expected JSON structure."""

    path = tmp_path / "highscores.json"

    repository = JsonHighscoreRepository(str(path))
    registry = ScoreRegistry(repository)

    registry.add("PACMAN", 1234)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == [
        {
            "name": "PACMAN",
            "score": 1234,
        }
    ]


def test_top_ten_scores_are_persisted(tmp_path) -> None:
    """Only the ten highest scores should be persisted."""

    path = tmp_path / "highscores.json"

    repository = JsonHighscoreRepository(str(path))
    registry = ScoreRegistry(repository)

    for score in range(12):
        registry.add(
            f"PLAYER{score}",
            score * 100,
        )

    new_repository = JsonHighscoreRepository(str(path))
    new_registry = ScoreRegistry(new_repository)

    assert len(new_registry.scores) == 10

    assert [
        score.score
        for score in new_registry.scores
    ] == [
        1100,
        1000,
        900,
        800,
        700,
        600,
        500,
        400,
        300,
        200,
    ]
