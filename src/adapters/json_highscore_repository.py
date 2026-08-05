from ..scores import Highscore, HighscoreRepository

from pathlib import Path
import json
import logging


LOGGER = logging.getLogger(__name__)


class JsonHighscoreRepository(HighscoreRepository):
    """Store and retrieve high scores from a JSON file."""

    def __init__(self, filename: str) -> None:
        """Create a repository backed by a JSON file.

        Args:
            filename: Path to the JSON high-score file.
        """
        self._path = Path(filename)

    def load(self) -> list[Highscore]:
        """Load high scores from disk.

        Returns:
            A list of ``Highscore`` objects. If the file does not exist,
            cannot be read, or contains invalid JSON, an empty list is
            returned.
        """
        try:
            with self._path.open("r", encoding="utf-8") as file:
                raw = json.load(file)

        except (OSError, json.JSONDecodeError) as error:
            LOGGER.warning("Could not load high scores (%s)."
                           " Using empty list.", error)
            return []

        if not isinstance(raw, list):
            LOGGER.warning(
                "High-score file must contain a JSON array."
            )
            return []

        scores: list[Highscore] = []

        for entry in raw:
            if not isinstance(entry, dict):
                LOGGER.warning(
                    "Ignoring invalid high-score entry."
                )
                continue

            name = entry.get("name")
            score = entry.get("score")

            if not isinstance(name, str):
                LOGGER.warning("Ignoring entry with invalid name.")
                continue

            if isinstance(score, bool) or not isinstance(score, int):
                LOGGER.warning("Ignoring entry with invalid score.")
                continue

            scores.append(Highscore(
                name=name.strip(),
                score=score)
            )

        return scores

    def save(self, scores: list[Highscore]) -> None:
        """Write high scores to disk.

        Args:
            scores: High scores to persist.
        """

        try:
            self._path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with self._path.open("w", encoding="utf-8") as file:
                json.dump(
                    [
                        {
                            "name": score.name,
                            "score": score.score
                        }
                        for score in scores
                    ],
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except (OSError, TypeError) as error:
            LOGGER.warning("Could not save high scores (%s).",
                           error,
                           )
