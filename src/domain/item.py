from enum import Enum
from dataclasses import dataclass


class ItemKind(Enum):
    """Define the types of collectible items available in the game.

    Attributes:
        PACGUM: Standard collectible that awards regular points.
        SUPER_PACGUM: Special collectible that awards additional points.
    """
    PACGUM = "pacgum"
    SUPER_PACGUM = "super_pacgum"


@dataclass(frozen=True, slots=True)
class Item:
    """Represent a collectible item located at a maze position.

    Item positions are managed externally by the game session, while
    each item stores its type and the number of points it awards.

    Attributes:
        kind: Type of collectible item.
        points: Number of points awarded when the item is collected.
    """

    kind: ItemKind
    points: int
