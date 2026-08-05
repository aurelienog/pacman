from .geometry import Direction, Position

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Maze:
    """Maze wall bits supplied by A-Maze-ing (N=1, E=2, S=4, W=8)."""

    cells: tuple[tuple[int, ...], ...]

    @property
    def width(self) -> int:
        """Maze width in cells."""
        return len(self.cells[0])

    @property
    def height(self) -> int:
        """Maze height in cells."""
        return len(self.cells)

    def contains(self, position: Position) -> bool:
        """Whether the position is inside the maze."""
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def can_move(self, position: Position, direction: Direction) -> bool:
        """Whether a corridor allows a move from this cell."""
        bits = {Direction.UP: 1, Direction.RIGHT: 2, Direction.DOWN: 4,
                Direction.LEFT: 8, Direction.NONE: 0}[direction]
        target = position.moved(direction)
        return direction is Direction.NONE or (
            self.contains(target)
            and (self.cells[position.y][position.x] & bits) == 0
        )

    def neighbours(
            self, position: Position
            ) -> list[tuple[Direction, Position]]:
        """Return all reachable adjacent cells."""
        return [
            (direction, position.moved(direction)) for direction in Direction
            if (direction is not Direction.NONE
                and self.can_move(position, direction))]

    def is_42_art(self, position: Position) -> bool:
        """Whether this cell belongs to the immutable ``42`` mark from
        A-Maze-ing.

        The assigned generator reserves those cells with all four wall bits
        set (15).
        They are decorative, not traversable game space, so no item may be
        placed there.
        """
        return self.contains(position) and self.cells[position.y][position.x] == 15
