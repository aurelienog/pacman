"""Facade coordinator for game session renderers."""

from __future__ import annotations

from typing import Any

from src.application.contracts import Snapshot
from src.ui.draw_utils import center_text
from src.ui.neon_assets import (
    GhostsSpriteAtlas,
    PacgumsSpriteAtlas,
    PacmanSpriteAtlas,
)

from .base_game_view import BaseGameView
from .end_screens import EndScreenView
from .entities_renderer import EntitiesRenderer
from .hud import HudView
from .items_renderer import ItemsRenderer
from .maze_renderer import MazeRenderer


class GameRenderer(BaseGameView):
    """Delegate gameplay rendering to specific component renderers."""

    def __init__(
        self,
        pygame: Any,
        pacman_atlas: PacmanSpriteAtlas | None,
        ghosts_atlas: GhostsSpriteAtlas | None,
        pacgums_atlas: PacgumsSpriteAtlas | None = None,
    ) -> None:
        super().__init__(pygame)
        self._game_bg = self._load_game_bg()
        self._hud_view = HudView(pygame)
        self._maze_renderer = MazeRenderer(pygame)
        self._items_renderer = ItemsRenderer(pygame, pacgums_atlas)
        self._entities_renderer = EntitiesRenderer(
            pygame,
            pacman_atlas,
            ghosts_atlas,
        )
        self._end_screen_view = EndScreenView(pygame)

    def draw_game(
        self,
        screen: Any,
        snapshot: Snapshot,
        fonts: tuple[Any, Any, Any],
    ) -> None:
        """Draw complete gameplay view."""
        if snapshot.maze is None or snapshot.player is None:
            return

        sw, sh = screen.get_width(), screen.get_height()

        # Background
        if self._game_bg is not None:
            scaled_bg = self._pygame.transform.smoothscale(
                self._game_bg,
                (sw, sh),
            )
            screen.blit(scaled_bg, (0, 0))
        else:
            screen.fill((8, 8, 19))

        y_label = 40
        y_val = y_label + max(18, int(sh * 0.024))
        top = y_val + max(35, int(sh * 0.045))

        maze = snapshot.maze
        cell = max(
            8,
            min((sw - 100) // maze.width, (sh - top - 100) // maze.height),
        )
        left = (sw - maze.width * cell) // 2

        self._hud_view.draw(screen, snapshot)
        self._maze_renderer.draw(screen, maze, left, top, cell)
        self._items_renderer.draw(screen, snapshot, left, top, cell)
        self._entities_renderer.draw_player(screen, snapshot, left, top, cell)
        self._entities_renderer.draw_ghosts(screen, snapshot, left, top, cell)

        if snapshot.message:
            msg_font_size = max(20, int(sh * 0.032))
            msg_font = self._get_font(msg_font_size)
            center_text(screen, msg_font, snapshot.message, (255, 230, 0), 65)

    def draw_end_screen(
        self,
        screen: Any,
        snapshot: Snapshot,
        fonts: tuple[Any, Any, Any],
        name: str,
        saved: bool,
    ) -> None:
        """Draw GAME OVER or VICTORY modal card."""
        self._end_screen_view.draw(screen, snapshot, fonts, name, saved)


__all__ = [
    "GameRenderer",
    "HudView",
    "MazeRenderer",
    "ItemsRenderer",
    "EntitiesRenderer",
    "EndScreenView",
]
