"""JSON-backed persistence for high scores."""

from ..scores import Highscore, HighscoreRepository

from pathlib import Path
import json
import re
import logging
from src.scores import MAX_SCORE

LOGGER = logging.getLogger(__name__)
NAME_PATTERN = re.compile(r"[A-Za-z0-9 ]{1,10}")


class JsonHighscoreRepository(HighscoreRepository):
    """Store and retrieve high scores from a JSON file."""

    def __init__(self, filename: str) -> None:
        """Create a repository backed by a JSON file.

        Args:
            filename: Path to the JSON high-score file.
        """
        self._path = Path(filename)

    def load(self) -> list[Highscore]:
        """Load valid high scores from the JSON file.

        Invalid or malformed entries are ignored and logged. If the
        file cannot be read or contains invalid JSON, an empty list
        is returned.

        Returns:
            A list of valid high scores sorted by descending score.
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

            if not self._is_valid_entry(name, score):
                LOGGER.warning("Ignoring invalid high-score entry.")
                continue

            assert isinstance(name, str)
            assert isinstance(score, int)

            scores.append(Highscore(
                name=name.strip(),
                score=score)
            )

        return sorted(
            scores,
            key=lambda highscore: highscore.score,
            reverse=True)

    def save(self, scores: list[Highscore]) -> None:
        """Persist high scores to the JSON file.

        The parent directory is created automatically when necessary.
        If the file cannot be written, a warning is logged and the
        application continues without raising the filesystem error.

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

    @staticmethod
    def _is_valid_entry(name: object, score: object) -> bool:
        """Validate an entry loaded from external JSON data.

        This validation protects the application from malformed or
        manually modified high-score files before creating domain
        objects.

        Args:
            name: Candidate player name loaded from JSON.
            score: Candidate score loaded from JSON.

        Returns:
            ``True`` if both the name and score satisfy the repository
            input constraints, otherwise ``False``.
        """
        if not isinstance(name, str):
            return False
        if not NAME_PATTERN.fullmatch(name.strip()):
            return False
        return (
            not isinstance(score, bool)
            and isinstance(score, int)
            and score >= 0
            and score <= MAX_SCORE
        )
