"""Pygame loader for individual ghosts animated sprite atlases."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.domain import Direction, GhostMode

# ⚙️ VERTICAL GHOST OFFSET SETTING (in pixels)
# A negative value (such as -2 or -4) raises the ghost up.
# A positive value (such as 2 or 4) lowers the ghost down.
GHOST_Y_OFFSET = 0


class GhostsSpriteAtlas:
    """Slice and render animated ghosts using individual color atlases
    and utils_sprite_atlas."""

    def __init__(self, pygame: Any) -> None:
        self._pygame = pygame
        self._ghost_atlases: dict[str, list[list[Any]]] = {}
        self._utils_frames: list[list[Any]] = []

        filenames = {
            "red": "red_ghost_sprite_atlas.png",
            "pink": "pink_ghost_sprite_atlas.png",
            "cyan": "blue_ghost_sprite_atlas.png",
            "orange": "orange_ghost_sprite_atlas.png",
        }

        for key, fname in filenames.items():
            frames = self._load_2x4_atlas(fname)
            if frames:
                self._ghost_atlases[key] = frames

        self._utils_frames = self._load_2x4_atlas("utils_sprite_atlas.png")

    def available(self) -> bool:
        """Return True if ghost atlases and utils atlas loaded successfully."""
        return len(self._ghost_atlases) >= 4 and len(self._utils_frames) == 2

    def draw_ghost(
        self,
        screen: Any,
        center: tuple[int, int],
        cell: int,
        index: int,
        mode: GhostMode,
        direction: Direction = Direction.NONE,
    ) -> None:
        """Draw ghost matching color, mode, direction,
        and walking skirt animation."""
        if not self.available():
            return

        ticks = self._pygame.time.get_ticks()

        if mode is GhostMode.RESPAWNING:
            # Eyes (Row 1, Column 0 of utils_sprite_atlas)
            frame = self._utils_frames[1][0]
        elif mode is GhostMode.FRIGHTENED:
            # Scared Ghost (Row 0, Columns 0 and 1 of utils_sprite_atlas)
            col = (ticks // 180) % 2
            frame = self._utils_frames[0][col]
        else:
            # Normal ghosts (0=Red, 1=Pink, 2=Blue, 3=Orange)
            color_keys = ["red", "pink", "cyan", "orange"]
            color_key = color_keys[index % 4]
            atlas = self._ghost_atlases[color_key]

            # Columns by direction: Right=0, Left=1, Up=2, Down=3
            direction_cols = {
                Direction.RIGHT: 0,
                Direction.LEFT: 1,
                Direction.UP: 2,
                Direction.DOWN: 3,
                Direction.NONE: 0,
            }
            col = direction_cols.get(direction, 0)

            # Leg animation (Lines 0 and 1)
            row = (ticks // 150) % 2
            frame = atlas[row][col]

        size = max(16, int(cell * 1.2))
        scaled = self._pygame.transform.smoothscale(frame, (size, size))

        # We apply height shift adjustment
        adjusted_center = (center[0], center[1] + GHOST_Y_OFFSET)
        screen.blit(scaled, scaled.get_rect(center=adjusted_center))

    def _load_2x4_atlas(self, filename: str) -> list[list[Any]]:
        path = self._find_file(filename)
        if path is None:
            return []
        try:
            image = self._pygame.image.load(str(path)).convert_alpha()
            cell_w = image.get_width() // 4
            cell_h = image.get_height() // 2

            frames = []
            for row in range(2):
                row_frames = []
                for col in range(4):
                    sub = image.subsurface(
                        (col * cell_w, row * cell_h, cell_w, cell_h)
                    ).copy()
                    row_frames.append(sub)
                frames.append(row_frames)
            return frames
        except Exception:
            return []

    @staticmethod
    def _find_file(filename: str) -> Path | None:
        possible = [
            Path(__file__).resolve().parents[3] / "assets/sprites" / filename,
            Path(__file__).resolve().parents[3] / "assets" / filename,
            Path("assets/sprites") / filename,
            Path("assets") / filename,
        ]
        for path in possible:
            if path.is_file():
                return path
        return None
