from enum import Enum
from dataclasses import dataclass


class ItemKind(Enum):
    """Collectible types."""

    PACGUM = "pacgum"
    SUPER_PACGUM = "super_pacgum"


@dataclass(frozen=True, slots=True)
class Item:
    """A collectible, keyed by position in a session."""

    kind: ItemKind
    points: int
