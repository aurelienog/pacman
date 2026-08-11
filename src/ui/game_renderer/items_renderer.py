"""Renderer for collectible pacgums and super-pacgums."""

from __future__ import annotations

from typing import Any

from src.application.contracts import Snapshot
from src.domain import ItemKind
from src.ui.draw_utils import center_float, draw_circle
from src.ui.neon_assets import PacgumsSpriteAtlas


class ItemsRenderer:
    """Draw dots and power pellets using atlas or fallback vector circles."""

    def __init__(
        self,
        pygame: Any,
        pacgums_atlas: PacgumsSpriteAtlas | None,
    ) -> None:
        """Initialize the items renderer.

        Args:
            pygame: Pygame module instance.
            pacgums_atlas: Loaded Pacgums sprite atlas or None.

        Returns:
            None.
        """
        self._pygame = pygame
        self._pacgums_atlas = pacgums_atlas

    def draw(
        self,
        screen: Any,
        snapshot: Snapshot,
        left: int,
        top: int,
        cell: int,
    ) -> None:
        """Draw remaining collectible items on the screen.

        Args:
            screen: Pygame display surface.
            snapshot: Current game state snapshot.
            left: Left pixel offset of the maze grid.
            top: Top pixel offset of the maze grid.
            cell: Size of a single grid cell in pixels.

        Returns:
            None.
        """
        assert snapshot.maze is not None
        maze_w, maze_h = snapshot.maze.width, snapshot.maze.height

        for position, item in snapshot.items:
            center = center_float(position.x, position.y, left, top, cell)
            if (
                self._pacgums_atlas is not None
                and self._pacgums_atlas.available()
            ):
                self._pacgums_atlas.draw_item(
                    screen, center, cell, item.kind, position, maze_w, maze_h
                )
            else:
                radius = max(
                    2,
                    cell // (4 if item.kind is ItemKind.SUPER_PACGUM else 7),
                )
                draw_circle(
                    screen,
                    center,
                    radius,
                    (255, 226, 140),
                    self._pygame,
                )
