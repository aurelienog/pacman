from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """A cardinal movement direction in maze coordinates."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)

    @property
    def delta(self) -> tuple[int, int]:
        """Return the coordinate delta for this direction."""
        return self.value

    @property
    def opposite(self) -> "Direction":
        """Return the reverse direction."""
        return {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.NONE: Direction.NONE,
        }[self]


@dataclass(frozen=True, slots=True)
class Position:
    """An immutable cell coordinate."""

    x: int
    y: int

    def moved(self, direction: Direction) -> "Position":
        """Return the adjacent position in ``direction``."""
        dx, dy = direction.delta
        return Position(self.x + dx, self.y + dy)


@dataclass(frozen=True)
class Hitbox:
    """Represent the collision bounds of an entity.

    Attributes:
        width: Width of the hitbox in maze-cell units.
        height: Height of the hitbox in maze-cell units.
    """

    width: float
    height: float
