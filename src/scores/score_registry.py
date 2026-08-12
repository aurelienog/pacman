"""High-score registry and validation rules."""

import logging

from .highscore import Highscore
from .highscore_repository import HighscoreRepository


LOGGER = logging.getLogger(__name__)

MAX_SCORE: int = 999_999
MAX_HIGHSCORES: int = 10


class ScoreRegistry:
    """Manage the game's high-score table.

    The registry validates new scores, keeps only the highest entries,
    and delegates persistence to a high-score repository.
    """

    def __init__(self, repository: HighscoreRepository) -> None:
        """Initialize a score registry.

        Previously stored scores are loaded from the repository,
        sorted by descending score, and limited to the top entries.

        Args:
            repository: Object responsible for loading and saving
                high scores.
        """
        self._repository = repository
        self._scores = sorted(
            repository.load(),
            key=lambda item: item.score,
            reverse=True,
        )[:MAX_HIGHSCORES]

    @property
    def scores(self) -> list[Highscore]:
        """Return a copy of the current high-score table.

        Returns:
            A shallow copy of the stored high-score list.
        """
        return self._scores.copy()

    def add(self, name: str, score: int) -> None:
        """Validate and add a new high-score entry.

        Invalid scores are ignored. Valid scores are inserted,
        ordered by descending score, limited to the maximum number
        of entries, and persisted through the repository.

        Args:
            name: Player name associated with the score.
            score: Player score to add.

        Returns:
            None.
        """
        current_score = self._validate(name, score)

        if current_score is None:
            return

        self._scores.append(current_score)

        self._scores.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        self._scores = self._scores[:MAX_HIGHSCORES]

        self._repository.save(self._scores)

    @staticmethod
    def _validate(
        name: object,
        score: object,
    ) -> Highscore | None:
        """Validate a high-score entry.

        The name must be a non-empty string of at most ten characters
        containing only letters, digits, and whitespace. The score must
        be an integer between zero and ``MAX_SCORE`` inclusive.

        Args:
            name: Candidate player name.
            score: Candidate player score.

        Returns:
            A validated ``Highscore`` object if the input is valid;
            otherwise, ``None``.
        """
        if not isinstance(name, str):
            LOGGER.warning("Name must be a string.")
            return None

        name = name.strip()

        if not name:
            LOGGER.warning("Name cannot be empty.")
            return None

        if len(name) > 10:
            LOGGER.warning(
                "Name must contain at most 10 characters."
            )
            return None

        for char in name:
            if not char.isalnum() and not char.isspace():
                LOGGER.warning(
                    "Name may contain only letters, digits and spaces."
                )
                return None

        if isinstance(score, bool) or not isinstance(score, int):
            LOGGER.warning("Score must be an integer.")
            return None

        if score < 0:
            LOGGER.warning("Score cannot be negative.")
            return None

        if score > MAX_SCORE:
            LOGGER.warning(
                "Score exceeds the maximum allowed value."
            )
            return None

        return Highscore(name, score)
