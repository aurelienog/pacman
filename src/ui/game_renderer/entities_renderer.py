"""Renderer for moving entities (Player and Ghosts)."""

from __future__ import annotations

from typing import Any

from src.application.contracts import Snapshot
from src.domain import GhostMode
from src.ui.draw_utils import center_float, draw_circle
from src.ui.neon_assets import GhostsSpriteAtlas, PacmanSpriteAtlas


class EntitiesRenderer:
    """Draw player and ghost entities using sprite atlases
    or vector fallback."""

    def __init__(
        self,
        pygame: Any,
        pacman_atlas: PacmanSpriteAtlas | None,
        ghosts_atlas: GhostsSpriteAtlas | None,
    ) -> None:
        """Initialize the entities renderer with sprite atlases.

        Args:
            pygame: Pygame module instance.
            pacman_atlas: Loaded Pac-Man sprite atlas or None.
            ghosts_atlas: Loaded Ghosts sprite atlas or None.

        Returns:
            None.
        """
        self._pygame = pygame
        self._pacman_atlas = pacman_atlas
        self._ghosts_atlas = ghosts_atlas

    def draw_player(
        self,
        screen: Any,
        snapshot: Snapshot,
        left: int,
        top: int,
        cell: int,
    ) -> None:
        """Draw interpolated player position using atlas or vector circle.

        Args:
            screen: Pygame display surface.
            snapshot: Current game state snapshot.
            left: Left pixel offset of the maze grid.
            top: Top pixel offset of the maze grid.
            cell: Size of a single grid cell in pixels.

        Returns:
            None.
        """
        if snapshot.player is None:
            return
        px_vis, py_vis = snapshot.player_visual_pos
        player_center = center_float(px_vis, py_vis, left, top, cell)
        if self._pacman_atlas is not None and self._pacman_atlas.available():
            self._pacman_atlas.draw_player(
                screen,
                player_center,
                cell,
                snapshot.player.direction,
            )
        else:
            draw_circle(
                screen,
                player_center,
                max(4, cell // 2 - 2),
                (255, 222, 0),
                self._pygame,
            )

    def draw_ghosts(
        self,
        screen: Any,
        snapshot: Snapshot,
        left: int,
        top: int,
        cell: int,
    ) -> None:
        """Draw interpolated ghost positions using atlas or vector fallback.

        Args:
            screen: Pygame display surface.
            snapshot: Current game state snapshot.
            left: Left pixel offset of the maze grid.
            top: Top pixel offset of the maze grid.
            cell: Size of a single grid cell in pixels.

        Returns:
            None.
        """
        colors = [
            (255, 60, 60),
            (255, 140, 255),
            (70, 230, 255),
            (255, 150, 50),
        ]
        for index, g_ent in enumerate(snapshot.ghost_visual_positions):
            center = center_float(g_ent.x, g_ent.y, left, top, cell)
            ghost_mode = (
                g_ent.mode if g_ent.mode is not None else GhostMode.CHASE
            )
            if (
                self._ghosts_atlas is not None
                and self._ghosts_atlas.available()
            ):
                self._ghosts_atlas.draw_ghost(
                    screen,
                    center,
                    cell,
                    index,
                    ghost_mode,
                    g_ent.direction,
                )
            else:
                color = (
                    (50, 90, 255)
                    if ghost_mode is GhostMode.FRIGHTENED
                    else colors[index % 4]
                )
                if ghost_mode is not GhostMode.RESPAWNING:
                    draw_circle(
                        screen,
                        center,
                        max(4, cell // 2 - 2),
                        color,
                        self._pygame,
                    )
