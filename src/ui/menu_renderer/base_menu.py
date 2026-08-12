"""Base helper class for menu rendering and asset management."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.ui.draw_utils import center_text, scale_image

BG_DIR = Path(__file__).resolve().parents[3] / "assets" / "backgrounds"
LOGOS_DIR = Path(__file__).resolve().parents[3] / "assets" / "logos"
ICONS_DIR = Path(__file__).resolve().parents[3] / "assets" / "icons"


class BaseMenuView:
    """Base class for menu views containing shared font
    and asset loading logic."""

    def __init__(self, pygame: Any) -> None:
        """Initialize base menu view and font cache.

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

    def _load_image(self, path: Path, alpha: bool = False) -> Any:
        """Safely load an image file from a Path object.

        Args:
            path: Path to the image file.
            alpha: Whether to enable per-pixel alpha transparency.

        Returns:
            Pygame Surface if loaded successfully, otherwise None.
        """
        if path.is_file():
            try:
                img = self._pygame.image.load(str(path))
                return img.convert_alpha() if alpha else img.convert()
            except Exception:
                return None
        return None

    def _load_icon(self, filename: str) -> Any:
        """Safely load an icon image from assets subdirectories.

        The icon directory, logos directory, and root assets directory
        are checked in that order.

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

    def _render_bg(
        self,
        screen: Any,
        bg_image: Any,
        fallback_bg: Any = None,
    ) -> None:
        """Render and scale background image to fill screen dimensions.

        The selected image is scaled to the current screen dimensions.

        Args:
            screen: Pygame surface on which the background is drawn.
            bg_image: Primary background surface image.
            fallback_bg: Secondary fallback background surface image.

        Returns:
            None.
        """
        target_bg = bg_image if bg_image is not None else fallback_bg
        if target_bg is not None:
            scaled_bg = scale_image(
                target_bg,
                (screen.get_width(), screen.get_height()),
                self._pygame,
            )
            screen.blit(scaled_bg, (0, 0))
        else:
            screen.fill((8, 8, 19))

    def _draw_logo(
        self,
        screen: Any,
        logo_img: Any,
        fallback_text: str = "PAC-MAN",
        height_ratio: float = 0.22,
        y_ratio: float = 0.15,
    ) -> int:
        """Draw scaled header logo image or fallback title text.

        The logo is scaled according to the screen height and limited
        to 85 percent of the screen width.

        Args:
            screen: Pygame surface on which the logo is drawn.
            logo_img: Loaded logo image surface or None.
            fallback_text: Text used if logo image is unavailable.
            height_ratio: Logo height ratio relative to screen height.
            y_ratio: Vertical center ratio relative to screen height.

        Returns:
            Bottom Y pixel coordinate of the rendered logo or text.
        """
        sw, sh = screen.get_width(), screen.get_height()
        center_y = int(sh * y_ratio)

        if logo_img is not None:
            aspect = logo_img.get_width() / logo_img.get_height()
            target_h = int(sh * height_ratio)
            target_w = int(target_h * aspect)

            if target_w > int(sw * 0.85):
                target_w = int(sw * 0.85)
                target_h = int(target_w / aspect)

            scaled_logo = scale_image(
                logo_img,
                (target_w, target_h),
                self._pygame,
            )
            rect = scaled_logo.get_rect(center=(sw // 2, center_y))
            screen.blit(scaled_logo, rect)
            return int(rect.bottom)

        title_font = self._get_font(int(sh * 0.09))
        rect = center_text(
            screen,
            title_font,
            fallback_text,
            (255, 230, 0),
            center_y,
        )
        return int(rect.bottom)
