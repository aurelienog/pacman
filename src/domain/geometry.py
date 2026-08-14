from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """Represent a cardinal movement direction in maze coordinates.

    Each direction contains its corresponding ``(x, y)`` coordinate
    delta. ``NONE`` represents no movement.

    Attributes:
        UP: Movement towards the previous row.
        DOWN: Movement towards the next row.
        LEFT: Movement towards the previous column.
        RIGHT: Movement towards the next column.
        NONE: No movement.
    """

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)

    @property
    def delta(self) -> tuple[int, int]:
        """Return the coordinate delta for this direction.

        Returns:
            A tuple containing the ``(x, y)`` coordinate delta.
        """
        return self.value

    @property
    def opposite(self) -> "Direction":
        """Return the opposite direction.

        Returns:
            The direction representing the reverse movement.
        """
        return {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.NONE: Direction.NONE,
        }[self]


@dataclass(frozen=True, slots=True)
class Position:
    """Represent an immutable maze-cell coordinate.

    Attributes:
        x: Horizontal cell coordinate.
        y: Vertical cell coordinate.
    """

    x: int
    y: int

    def moved(self, direction: Direction) -> "Position":
        """Return a new position moved in the given direction.

        The current position is not modified because ``Position`` is
        immutable.

        Args:
            direction: Direction in which to move.

        Returns:
            A new position one cell away in ``direction``.
        """
        dx, dy = direction.delta
        return Position(self.x + dx, self.y + dy)


@dataclass(frozen=True, slots=True)
class Hitbox:
    """Represent the collision bounds of an entity.

    Hitbox dimensions are expressed in maze-cell units and describe
    the rectangular collision area centred on the entity position.

    Attributes:
        width: Width of the hitbox in maze-cell units.
        height: Height of the hitbox in maze-cell units.
    """

    width: float
    height: float
