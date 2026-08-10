"""Pygame loader for the Pac-Man animated sprite atlas."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.domain import Direction


class PacmanSpriteAtlas:
    """Slice and render animated 4x3 Pac-Man sprite atlas."""

    def __init__(self, pygame: Any) -> None:
        self._pygame = pygame
        self._path = self._find_atlas_path()
        self._frames: list[list[Any]] = []

        if self._path is not None:
            try:
                image = self._pygame.image.load(
                    str(self._path)
                ).convert_alpha()
                cell_w = image.get_width() // 4
                cell_h = image.get_height() // 3

                for row in range(3):
                    row_frames = []
                    for col in range(4):
                        sub = image.subsurface(
                            (col * cell_w, row * cell_h, cell_w, cell_h)
                        ).copy()
                        row_frames.append(sub)
                    self._frames.append(row_frames)
            except Exception:
                self._frames = []

    def available(self) -> bool:
        """Return True if atlas image file exists and loaded successfully."""
        return self._path is not None and len(self._frames) == 3

    def draw_player(
        self,
        screen: Any,
        center: tuple[int, int],
        cell: int,
        direction: Direction,
    ) -> None:
        """Draw animated Pac-Man frame matching direction and time."""
        if not self.available():
            return

        direction_cols = {
            Direction.RIGHT: 0,
            Direction.LEFT: 1,
            Direction.DOWN: 2,
            Direction.UP: 3,
            Direction.NONE: 0,
        }
        col = direction_cols.get(direction, 0)

        # Smooth mouth opening/closing animation (0 -> 1 -> 2 -> 1)
        ticks = self._pygame.time.get_ticks()
        anim_sequence = [0, 1, 2, 1]
        row = anim_sequence[(ticks // 90) % 4]

        frame = self._frames[row][col]
        size = max(16, int(cell * 1.2))
        scaled = self._pygame.transform.smoothscale(frame, (size, size))
        screen.blit(scaled, scaled.get_rect(center=center))

    @staticmethod
    def _find_atlas_path() -> Path | None:
        possible = [
            Path(__file__).resolve().parents[3]
            / "assets"
            / "sprites"
            / "pacman_sprite_atlas.png",
            Path(__file__).resolve().parents[3]
            / "assets"
            / "pacman_sprite_atlas.png",
            Path("assets/sprites/pacman_sprite_atlas.png"),
            Path("assets/pacman_sprite_atlas.png"),
        ]
        for path in possible:
            if path.is_file():
                return path
        return None
