from __future__ import annotations

from .highscore import Highscore

from typing import Protocol


class HighscoreRepository(Protocol):
    """Persistence interface for high scores."""

    def load(self) -> list[Highscore]:
        """Load all persisted high scores.

        Returns:
            A list of persisted high scores. Returns an empty list if no
            valid data could be loaded.
        """
        ...

    def save(self, scores: list[Highscore]) -> None:
        """Persist the given high scores.

        Args:
            scores: High scores to write to persistent storage.
        """
        ...
