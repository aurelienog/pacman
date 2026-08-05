from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Highscore:
    """Manage the game's high-score table.

    The registry validates new scores, keeps only the highest
    entries and delegates persistence to a repository.
    """

    name: str
    score: int
