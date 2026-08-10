"""Renderer for the Pause Menu overlay view."""

from __future__ import annotations

from typing import Any

from src.ui.draw_utils import (
    center_text,
    draw_button_box,
    draw_menu_card_frame,
    )
from .base_menu import BaseMenuView


class PauseMenuView(BaseMenuView):
    """Render pause overlay card and calculate pause menu hitboxes."""

    def __init__(self, pygame: Any) -> None:
        super().__init__(pygame)
        self._pacman_icon = self._load_icon("pacman_icon.png")
        self.pause_menu_rects: list[Any] = []

    def draw(self, screen: Any, pause_index: int) -> None:
        """Draw dynamically scaling pause card frame and choices."""
        sw, sh = screen.get_width(), screen.get_height()

        # Dynamic pause card dimensions
        # (50% width and 60% height of the window)
        card_w = max(420, int(sw * 0.30))
        card_h = max(380, int(sh * 0.50))
        card_rect = self._pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (sw // 2, sh // 2)

        purple_color = (180, 50, 240)
        draw_menu_card_frame(
            screen,
            card_rect,
            purple_color,
            self._pygame,
            pacman_icon=self._pacman_icon,
        )

        title_font = self._get_font(max(24, int(card_h * 0.14)))
        center_text(
            screen,
            title_font,
            "PAUSED",
            (255, 100, 220),
            card_rect.top + int(card_h * 0.16),
        )

        menu_font = self._get_font(max(18, int(card_h * 0.08)))
        items = ("Resume", "Return to main menu", "Quit game")
        start_y = card_rect.top + int(card_h * 0.42)
        spacing = int(card_h * 0.16)

        self.pause_menu_rects.clear()

        for index, label in enumerate(items):
            y_pos = start_y + index * spacing
            is_selected = index == pause_index

            text_val = f"> {label}" if is_selected else label
            color = (255, 230, 0) if is_selected else (235, 235, 240)

            text_surf = menu_font.render(text_val, True, color)
            text_rect = text_surf.get_rect(center=(sw // 2, y_pos))

            box_w = max(int(card_w * 0.8), text_rect.width + 30)
            box_h = max(40, int(text_rect.height * 2))
            hit_rect = self._pygame.Rect(0, 0, box_w, box_h)
            hit_rect.center = (sw // 2, y_pos)
            self.pause_menu_rects.append(hit_rect)

            if is_selected:
                draw_button_box(
                    screen,
                    hit_rect,
                    self._pygame,
                    color=purple_color,
                )

            screen.blit(text_surf, text_rect)
