"""Renderer for maze walls and 42 art cells."""

from __future__ import annotations

from typing import Any

from src.domain import Position
from src.ui.draw_utils import draw_line


class MazeRenderer:
    """Draw maze corridors, walls, and 42 art tiles."""

    def __init__(self, pygame: Any) -> None:
        """Initialize the maze renderer.

        Args:
            pygame: Pygame module instance.

        Returns:
            None.
        """
        self._pygame = pygame

    def draw(
        self,
        screen: Any,
        maze: Any,
        left: int,
        top: int,
        cell: int,
    ) -> None:
        """Draw maze wall bitmasks and reserved 42 tiles.

        Args:
            screen: Pygame display surface.
            maze: Current domain Maze instance.
            left: Left pixel offset of the maze grid.
            top: Top pixel offset of the maze grid.
            cell: Size of a single grid cell in pixels.

        Returns:
            None.
        """
        for y, row in enumerate(maze.cells):
            for x, walls in enumerate(row):
                px, py = left + x * cell, top + y * cell
                is_42 = maze.is_42_art(Position(x, y))
                wall_color = (235, 70, 255) if is_42 else (45, 90, 255)

                if is_42:
                    self._pygame.draw.rect(
                        screen,
                        (74, 16, 95),
                        (px + 2, py + 2, cell - 3, cell - 3),
                    )
                if walls & 1:
                    draw_line(
                        screen,
                        (px, py),
                        (px + cell, py),
                        wall_color,
                        self._pygame,
                    )
                if walls & 2:
                    draw_line(
                        screen,
                        (px + cell, py),
                        (px + cell, py + cell),
                        wall_color,
                        self._pygame,
                    )
                if walls & 4:
                    draw_line(
                        screen,
                        (px, py + cell),
                        (px + cell, py + cell),
                        wall_color,
                        self._pygame,
                    )
                if walls & 8:
                    draw_line(
                        screen,
                        (px, py),
                        (px, py + cell),
                        wall_color,
                        self._pygame,
                    )
