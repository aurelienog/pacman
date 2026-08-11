"""Tests for high-score validation and score registry."""

from src.scores.highscore import Highscore
from src.scores.score_registry import ScoreRegistry


class FakeHighscoreRepository:
    """In-memory repository for testing."""

    def __init__(
        self,
        scores: list[Highscore] | None = None,
    ) -> None:
        self.scores = scores or []
        self.saved_scores: list[Highscore] | None = None

    def load(self) -> list[Highscore]:
        """Return stored scores."""
        return self.scores.copy()

    def save(self, scores: list[Highscore]) -> None:
        """Record saved scores."""
        self.saved_scores = scores.copy()


def test_registry_loads_existing_scores() -> None:
    """Registry should load scores from the repository."""
    existing = [
        Highscore("AAA", 500),
        Highscore("BBB", 300),
    ]
    repository = FakeHighscoreRepository(existing)

    registry = ScoreRegistry(repository)

    assert registry.scores == existing


def test_scores_returns_copy() -> None:
    """scores property should not expose the internal list."""
    repository = FakeHighscoreRepository(
        [Highscore("AAA", 500)]
    )
    registry = ScoreRegistry(repository)

    scores = registry.scores
    scores.clear()

    assert registry.scores == [Highscore("AAA", 500)]


def test_add_valid_score() -> None:
    """A valid score should be added and persisted."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("PACMAN", 500)

    assert registry.scores == [
        Highscore("PACMAN", 500),
    ]
    assert repository.saved_scores == [
        Highscore("PACMAN", 500),
    ]


def test_add_strips_name_whitespace() -> None:
    """Leading and trailing whitespace should be removed."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("  PACMAN  ", 500)

    assert registry.scores == [
        Highscore("PACMAN", 500),
    ]


def test_scores_are_sorted_descending() -> None:
    """Scores should always be ordered from highest to lowest."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("AAA", 100)
    registry.add("BBB", 500)
    registry.add("CCC", 300)

    assert registry.scores == [
        Highscore("BBB", 500),
        Highscore("CCC", 300),
        Highscore("AAA", 100),
    ]


def test_registry_keeps_only_top_ten_scores() -> None:
    """Registry should keep at most ten scores."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    for score in range(11):
        registry.add(
            f"P{score}",
            score * 100,
        )

    assert len(registry.scores) == 10
    assert registry.scores[0] == Highscore("P10", 1000)
    assert registry.scores[-1] == Highscore("P1", 100)


def test_eleventh_low_score_is_discarded() -> None:
    """A score below the top ten should not remain in the table."""
    repository = FakeHighscoreRepository()

    existing = [
        Highscore(f"P{score}", score)
        for score in range(10, 20)
    ]

    repository = FakeHighscoreRepository(existing)
    registry = ScoreRegistry(repository)

    registry.add("LOW", 1)

    assert len(registry.scores) == 10
    assert Highscore("LOW", 1) not in registry.scores


def test_zero_score_is_valid() -> None:
    """A score of zero should be accepted."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("ZERO", 0)

    assert registry.scores == [
        Highscore("ZERO", 0),
    ]


def test_maximum_score_is_valid() -> None:
    """The maximum allowed score should be accepted."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("MAX", 999_999)

    assert registry.scores == [
        Highscore("MAX", 999_999),
    ]


def test_empty_name_is_rejected() -> None:
    """Empty names should be ignored."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("   ", 500)

    assert registry.scores == []
    assert repository.saved_scores is None


def test_name_longer_than_ten_characters_is_rejected() -> None:
    """Names longer than ten characters should be ignored."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("ABCDEFGHIJK", 500)

    assert registry.scores == []
    assert repository.saved_scores is None


def test_name_with_invalid_characters_is_rejected() -> None:
    """Names may only contain letters, digits and spaces."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("PAC-MAN", 500)

    assert registry.scores == []
    assert repository.saved_scores is None


def test_non_string_name_is_rejected() -> None:
    """Non-string names should be ignored."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add(123, 500)  # type: ignore[arg-type]

    assert registry.scores == []
    assert repository.saved_scores is None


def test_negative_score_is_rejected() -> None:
    """Negative scores should be ignored."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("PACMAN", -1)

    assert registry.scores == []
    assert repository.saved_scores is None


def test_score_above_maximum_is_rejected() -> None:
    """Scores above the maximum should be ignored."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("PACMAN", 1_000_000)

    assert registry.scores == []
    assert repository.saved_scores is None


def test_non_integer_score_is_rejected() -> None:
    """Non-integer scores should be ignored."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("PACMAN", 500.5)  # type: ignore[arg-type]

    assert registry.scores == []
    assert repository.saved_scores is None


def test_boolean_score_is_rejected() -> None:
    """Boolean values should not be accepted as integer scores."""
    repository = FakeHighscoreRepository()
    registry = ScoreRegistry(repository)

    registry.add("PACMAN", True)  # type: ignore[arg-type]

    assert registry.scores == []
    assert repository.saved_scores is None
