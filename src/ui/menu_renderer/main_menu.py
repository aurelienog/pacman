"""Renderer for the Main Menu view."""

from __future__ import annotations

from typing import Any

from src.ui.draw_utils import draw_button_box
from .base_menu import BG_DIR, BaseMenuView

MENU_BG_PATH = BG_DIR / "background_menu.png"


class MainMenuView(BaseMenuView):
    """Render the main menu and maintain its mouse hitboxes."""

    def __init__(self, pygame: Any) -> None:
        """Initialize main menu view and load background and logo assets.

        Args:
            pygame: Pygame module instance.

        Returns:
            None.
        """
        super().__init__(pygame)
        self._menu_bg = self._load_image(MENU_BG_PATH, alpha=False)
        self._logo_main = self._load_icon("logo.png")
        self.main_menu_rects: list[Any] = []

    def draw(self, screen: Any, menu_index: int) -> None:
        """Draw main menu choices
        and store button rects for mouse interaction.

        The selected item is highlighted, and the corresponding
        rectangles are stored for mouse interaction.

        Args:
            screen: Pygame surface on which the menu is drawn.
            menu_index: Index of the currently selected menu item.

        Returns:
            None.
        """
        sw, sh = screen.get_width(), screen.get_height()

        self._render_bg(screen, self._menu_bg)
        logo_bottom = self._draw_logo(screen, self._logo_main, "PAC-MAN")

        menu_font = self._get_font(int(sh * 0.055))
        start_y = max(logo_bottom + int(sh * 0.08), int(sh * 0.38))
        item_spacing = int(sh * 0.095)

        items = ("START GAME", "HIGHSCORES", "INSTRUCTIONS", "EXIT")
        self.main_menu_rects.clear()

        for index, label in enumerate(items):
            y_pos = start_y + index * item_spacing
            is_selected = index == menu_index

            text_val = f"> {label}" if is_selected else label
            color = (255, 230, 0) if is_selected else (235, 235, 240)

            text_surf = menu_font.render(text_val, True, color)
            text_rect = text_surf.get_rect(center=(sw // 2, y_pos))

            box_w = max(int(sw * 0.28), text_rect.width + int(sw * 0.06))
            box_h = max(44, int(text_rect.height * 2))
            hit_rect = self._pygame.Rect(0, 0, box_w, box_h)
            hit_rect.center = (sw // 2, y_pos)
            self.main_menu_rects.append(hit_rect)

            if is_selected:
                draw_button_box(screen, hit_rect, self._pygame)

            screen.blit(text_surf, text_rect)
