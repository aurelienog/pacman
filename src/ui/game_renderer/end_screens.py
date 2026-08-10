"""Renderer for Game Over and Victory end screen overlays."""

from __future__ import annotations

from typing import Any

from src.application.contracts import GamePhase, Snapshot
from src.ui.draw_utils import center_text, draw_menu_card_frame
from .base_game_view import BaseGameView


class EndScreenView(BaseGameView):
    """Render Game Over / Victory modal card."""

    def __init__(self, pygame: Any) -> None:
        super().__init__(pygame)
        self._pacman_icon = self._load_icon("pacman_icon.png")

    def draw(
        self,
        screen: Any,
        snapshot: Snapshot,
        fonts: tuple[Any, Any, Any],
        name: str,
        saved: bool,
    ) -> None:
        """Draw dynamically scaling end game dialog card."""
        sw, sh = screen.get_width(), screen.get_height()

        # Dynamic win/loss card sizes
        card_w = max(420, int(sw * 0.30))
        card_h = max(380, int(sh * 0.50))
        card_rect = self._pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (sw // 2, sh // 2)

        is_over = snapshot.phase is GamePhase.GAME_OVER

        border_color = (255, 50, 70) if is_over else (50, 235, 100)
        draw_menu_card_frame(
            screen,
            card_rect,
            border_color,
            self._pygame,
            pacman_icon=self._pacman_icon,
        )

        # Title
        title_text = "GAME OVER" if is_over else "LEVEL CLEAR!"
        title_color = (255, 60, 75) if is_over else (50, 235, 100)
        title_font = self._get_font(max(24, int(card_h * 0.14)))
        center_text(
            screen,
            title_font,
            title_text,
            title_color,
            card_rect.top + int(card_h * 0.16),
        )

        # "SCORE" Header
        cyan_font = self._get_font(max(20, int(card_h * 0.08)))
        center_text(
            screen,
            cyan_font,
            "SCORE",
            (0, 210, 255),
            card_rect.top + int(card_h * 0.36),
        )

        # Score Value
        score_font = self._get_font(max(22, int(card_h * 0.09)))
        score_str = f"{snapshot.score:06d}"
        center_text(
            screen,
            score_font,
            score_str,
            (245, 245, 245),
            card_rect.top + int(card_h * 0.47),
        )

        # Name Entry Prompt
        prompt_font = self._get_font(max(18, int(card_h * 0.07)))
        input_font = self._get_font(max(18, int(card_h * 0.1)))

        if saved:
            line1 = "SCORE SAVED!"
            line2 = "Press Enter to continue"
            color1 = (50, 235, 100)  # Green
            color2 = (210, 210, 220)
        else:
            line1 = "ENTER NAME (max 10):"
            line2 = f"{name}_" if name else "_"
            color1 = (0, 210, 255)    # Blue
            color2 = (255, 230, 0)    # Yellow highlighted for name

        # Line 1: Hint
        center_text(
            screen,
            prompt_font,
            line1,
            color1,
            card_rect.top + int(card_h * 0.65),
        )

        # Line 2: Name field / Result
        center_text(
            screen,
            input_font,
            line2,
            color2,
            card_rect.top + int(card_h * 0.77),
        )
