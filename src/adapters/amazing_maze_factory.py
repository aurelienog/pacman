"""Adapter for the assigned, third-party A-Maze-ing wheel."""


from __future__ import annotations

from typing import Protocol

from src.domain.maze import Maze
from mazegenerator import MazeGenerator


class MazeGenerationError(RuntimeError):
    """Raised when an external maze cannot be safely converted."""


class MazeFactory(Protocol):
    """Port used by the application to request a maze."""

    def generate(
            self, width: int, height: int, seed: int
            ) -> Maze:
        """Generate a validated maze.

        Args:
            width: Requested maze width.
            height: Requested maze height.
            seed: Seed used to generate the maze.

        Returns:
            A validated Maze instance.
        """
        ...


class AmazingMazeFactory:
    """Create domain mazes using the A-Maze-ing library."""

    def generate(self, width: int, height: int, seed: int) -> Maze:
        """Generate and validate a maze from the external library.

        The generated maze is checked for the expected dimensions,
        valid wall encoding and the existence of a valid path before
        being converted into the domain ``Maze`` type.

        Args:
            width: Requested maze width.
            height: Requested maze height.
            seed: Seed used to generate the maze.

        Returns:
            A validated Maze instance.

        Raises:
            MazeGenerationError: If the external generator fails or
                produces an invalid or unsolvable maze.
        """

        try:
            generated = MazeGenerator(
                size=(width, height),
                perfect=False,
                seed=seed)
            raw_cells = generated.maze

        except Exception as error:
            raise MazeGenerationError(
                f"A-Maze-ing failed to generate the maze: {error}"
            ) from error

        if len(raw_cells) != height or any(len(row) != width
                                           for row in raw_cells):
            raise MazeGenerationError(
                "A-Maze-ing returned an invalid maze size.")

        if any(not isinstance(cell, int) or not 0 <= cell <= 15
               for row in raw_cells for cell in row):
            raise MazeGenerationError("A-Maze-ing returned invalid wall data.")

        if not generated.shortest_path:
            raise MazeGenerationError(
                "Generated maze is not solvable."
            )
        return Maze(tuple(tuple(row) for row in raw_cells))
