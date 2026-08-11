"""Base helper class for gameplay rendering and asset loading."""

from __future__ import annotations

from pathlib import Path
from typing import Any

BG_DIR = Path(__file__).resolve().parents[3] / "assets" / "backgrounds"
ICONS_DIR = Path(__file__).resolve().parents[3] / "assets" / "icons"
LOGOS_DIR = Path(__file__).resolve().parents[3] / "assets" / "logos"


class BaseGameView:
    """Base class for game rendering views providing icon
    and font utilities."""

    def __init__(self, pygame: Any) -> None:
        """Initialize the base game view and font cache.

        Args:
            pygame: Pygame module instance.

        Returns:
            None.
        """
        self._pygame = pygame
        self._font_cache: dict[int, Any] = {}

    def _get_font(self, size: int) -> Any:
        """Retrieve a cached font of the specified size.

        Args:
            size: Font point size.

        Returns:
            Pygame Font object.
        """
        if size not in self._font_cache:
            self._font_cache[size] = self._pygame.font.Font(None, size)
        return self._font_cache[size]

    def _load_icon(self, filename: str) -> Any:
        """Safely load an icon image from assets subdirectories.

        Args:
            filename: Name of the image file to load.

        Returns:
            Pygame Surface if loaded successfully, otherwise None.
        """
        possible = [
            ICONS_DIR / filename,
            LOGOS_DIR / filename,
            Path(__file__).resolve().parents[3] / "assets" / filename,
        ]
        for p in possible:
            if p.is_file():
                try:
                    return self._pygame.image.load(str(p)).convert_alpha()
                except Exception:
                    pass
        return None

    def _load_game_bg(self) -> Any:
        """Safely load the gameplay background image.

        Returns:
            Pygame Surface if loaded successfully, otherwise None.
        """
        possible = [
            BG_DIR / "game_bg.png",
            BG_DIR / "background_game.png",
            BG_DIR / "game_bg.jpg",
            Path(__file__).resolve().parents[3] / "assets" / "game_bg.png",
        ]
        for path in possible:
            if path.is_file():
                try:
                    return self._pygame.image.load(str(path)).convert()
                except Exception:
                    pass
        return None
