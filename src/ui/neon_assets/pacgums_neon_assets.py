"""Pygame loader for pacgums and static colored super-pacgums."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.domain import ItemKind, Position
from src.ui.draw_utils import scale_image


class PacgumsSpriteAtlas:
    """Slice and render pacgums and static corner-matched super-pacgums."""

    def __init__(self, pygame: Any) -> None:
        """Initialize pacgum atlas loader and slice subsurface frames.

        Args:
            pygame: Pygame module instance.

        Returns:
            None.
        """
        self._pygame = pygame
        self._path = self._find_atlas_path()
        self._frames: list[list[Any]] = []

        if self._path is not None:
            try:
                image = self._pygame.image.load(
                    str(self._path)
                ).convert_alpha()
                cell_w = image.get_width() // 4
                cell_h = image.get_height() // 2

                for row in range(2):
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
        """Check if utils atlas image file exists and loaded successfully.

        Returns:
            True if atlas frames are available, else False.
        """
        return self._path is not None and len(self._frames) == 2

    def draw_item(
        self,
        screen: Any,
        center: tuple[int, int],
        cell: int,
        kind: ItemKind,
        position: Position,
        maze_w: int,
        maze_h: int,
    ) -> None:
        """Draw pacgum or static colored super-pacgum.

        Normal pacgums use the fixed pacgum frame. Super-pacgums use a
        static color selected according to the item's maze quadrant.

        Args:
            screen: Pygame display surface.
            center: (x, y) center pixel coordinate.
            cell: Size of a single grid cell in pixels.
            kind: ItemKind enum (PACGUM or SUPER_PACGUM).
            position: Position object for corner color matching.
            maze_w: Total maze width in cells.
            maze_h: Total maze height in cells.

        Returns:
            None.
        """
        if not self.available():
            return

        if kind is ItemKind.PACGUM:
            # Small yellow pacgam (Row 1, Column 1)
            frame = self._frames[1][1]
            size = max(8, int(cell * 0.40))
        else:
            # Static colored super-pacgam without animation
            # Top-Left (Red) -> Row 0, Column 2
            # Top-Right (Pink) -> Row 1, Column 3
            # Bottom-Left (Blue) -> Row 0, Column 3
            # Bottom-Right (Orange) -> Row 1, Column 2
            is_left = position.x < maze_w / 2.0
            is_top = position.y < maze_h / 2.0

            if is_top and is_left:
                frame = self._frames[0][2]  # Red
            elif is_top and not is_left:
                frame = self._frames[1][3]  # Pink
            elif not is_top and is_left:
                frame = self._frames[0][3]  # Blue
            else:
                frame = self._frames[1][2]  # Orange

            size = max(14, int(cell * 0.85))

        scaled = scale_image(frame, (size, size), self._pygame)
        screen.blit(scaled, scaled.get_rect(center=center))

    @staticmethod
    def _find_atlas_path() -> Path | None:
        """Search for utils_sprite_atlas.png in assets subdirectories.

        Returns:
            Path object if found, otherwise None.
        """
        possible = [
            Path(__file__).resolve().parents[3]
            / "assets"
            / "sprites"
            / "utils_sprite_atlas.png",
            Path(__file__).resolve().parents[3]
            / "assets"
            / "utils_sprite_atlas.png",
            Path("assets/sprites/utils_sprite_atlas.png"),
            Path("assets/utils_sprite_atlas.png"),
        ]
        for path in possible:
            if path.is_file():
                return path
        return None
