from .geometry import Direction, Position

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Maze:
    """Represent the maze walls and traversable cells.

    Each cell stores wall bits supplied by A-Maze-ing using the
    convention N=1, E=2, S=4 and W=8.

    Attributes:
        cells: Two-dimensional tuple containing the wall bitmask of
            every maze cell.
    """

    cells: tuple[tuple[int, ...], ...]

    @property
    def width(self) -> int:
        """Return the maze width in cells.

        Returns:
            Number of columns in the maze.
        """
        return len(self.cells[0])

    @property
    def height(self) -> int:
        """Return the maze height in cells.

        Returns:
            Number of rows in the maze.
        """
        return len(self.cells)

    def contains(self, position: Position) -> bool:
        """Check whether a position is inside the maze.

        Args:
            position: Maze position to check.

        Returns:
            ``True`` if the position is inside the maze boundaries,
            otherwise ``False``.
        """
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def can_move(self, position: Position, direction: Direction) -> bool:
        """Check whether movement is possible from a maze cell.

        A movement is possible when the destination is inside the maze
        and the corresponding wall bit is not set. ``Direction.NONE``
        is always considered valid because it represents no movement.

        Args:
            position: Current maze position.
            direction: Direction in which movement is requested.

        Returns:
            ``True`` if movement is allowed, otherwise ``False``.
        """
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
        """Return all traversable neighbouring cells.

        Args:
            position: Current maze position.

        Returns:
            A list containing the direction and position of every
            adjacent cell that can be reached from ``position``.
        """
        return [
            (direction, position.moved(direction)) for direction in Direction
            if (direction is not Direction.NONE
                and self.can_move(position, direction))]

    def is_42_art(self, position: Position) -> bool:
        """Check whether a cell belongs to the immutable ``42`` artwork.

        The A-Maze-ing generator reserves these cells by setting all
        four wall bits, resulting in a value of ``15``. Such cells are
        decorative rather than traversable game space and therefore
        cannot contain game items.

        Args:
            position: Maze position to check.

        Returns:
            ``True`` if the position belongs to the immutable ``42``
            artwork, otherwise ``False``.
        """
        return (self.contains(position)
                and self.cells[position.y][position.x] == 15)
