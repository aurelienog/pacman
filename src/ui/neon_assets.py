"""Pygame loader for sprite atlas."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.domain import Direction, GhostMode

ATLAS_PATH = Path(__file__).resolve().parents[2] / "assets" / "neon_sprite_atlas.png"


class NeonSpriteAtlas:
    """Slice and draw sprite atlas without exposing it to game rules."""

    def __init__(self, pygame: Any) -> None:
        image = pygame.image.load(str(ATLAS_PATH)).convert_alpha()
        cell_width = image.get_width() // 4
        cell_height = image.get_height() // 2
        self._pygame = pygame
        self._frames = {
            "player_right": self._frame(image, 0, 0, cell_width, cell_height),
            "player_up": self._frame(image, 1, 0, cell_width, cell_height),
            "red": self._frame(image, 2, 0, cell_width, cell_height),
            "pink": self._frame(image, 3, 0, cell_width, cell_height),
            "cyan": self._frame(image, 0, 1, cell_width, cell_height),
            "orange": self._frame(image, 1, 1, cell_width, cell_height),
            "frightened": self._frame(image, 2, 1, cell_width, cell_height),
            "eyes": self._frame(image, 3, 1, cell_width, cell_height),
        }

    @staticmethod
    def available() -> bool:
        """Whether the sprite atlas exists beside the source code."""
        return ATLAS_PATH.is_file()

    def draw_player(self, screen: Any, center: tuple[int, int], cell: int, direction: Direction) -> None:
        """Draw Pac-Man in the requested direction."""
        frame = self._frames["player_right"]
        if direction is Direction.LEFT:
            frame = self._pygame.transform.flip(frame, True, False)
        elif direction is Direction.UP:
            frame = self._frames["player_up"]
        elif direction is Direction.DOWN:
            frame = self._pygame.transform.flip(self._frames["player_up"], False, True)
        self._blit_scaled(screen, frame, center, cell)

    def draw_ghost(self, screen: Any, center: tuple[int, int], cell: int, index: int, mode: GhostMode) -> None:
        """Draw a coloured, frightened, or returning ghost."""
        if mode is GhostMode.RESPAWNING:
            frame = self._frames["eyes"]
        elif mode is GhostMode.FRIGHTENED:
            frame = self._frames["frightened"]
        else:
            frame = self._frames[("red", "pink", "cyan", "orange")[index % 4]]
        self._blit_scaled(screen, frame, center, cell)

    @staticmethod
    def _frame(image: Any, x: int, y: int, width: int, height: int) -> Any:
        return image.subsurface((x * width, y * height, width, height)).copy()

    def _blit_scaled(self, screen: Any, frame: Any, center: tuple[int, int], cell: int) -> None:
        size = max(16, int(cell * 1.15))
        scaled = self._pygame.transform.smoothscale(frame, (size, size))
        screen.blit(scaled, scaled.get_rect(center=center))
