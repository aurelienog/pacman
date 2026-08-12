"""Renderer for the Highscores Leaderboard view."""

from __future__ import annotations

from typing import Any

from src.scores import ScoreRegistry
from src.ui.draw_utils import center_text, draw_menu_card_frame, scale_image
from .base_menu import BG_DIR, BaseMenuView

SCORES_BG_PATH = BG_DIR / "background_scores.png"


class HighscoresView(BaseMenuView):
    """Render the Top 10 highscore screen."""

    def __init__(self, pygame: Any, score_registry: ScoreRegistry) -> None:
        """Initialize the highscore view and load its visual assets.

        Args:
            pygame: Pygame module instance.
            score_registry: Registry providing the stored high scores.

        Returns:
            None.
        """
        super().__init__(pygame)
        self._score_registry = score_registry
        self._scores_bg = self._load_image(SCORES_BG_PATH, alpha=False)
        self._logo_scores = self._load_icon("top10_highscores_logo.png")
        self._pacman_icon = self._load_icon("pacman_icon.png")
        self._crown_icon = self._load_icon("crown_icon.png")

    def draw(self, screen: Any) -> None:
        """Draw background, logo, and the Top 10 highscore leaderboard card.

        The view renders the background, title, leaderboard card,
        score entries, and the navigation hint.

        Args:
            screen: Pygame surface on which the leaderboard is drawn.

        Returns:
            None.
        """
        sw, sh = screen.get_width(), screen.get_height()

        self._render_bg(screen, self._scores_bg)
        top_y = self._draw_logo(
            screen,
            self._logo_scores,
            "TOP 10 HIGHSCORES",
            height_ratio=0.16,
            y_ratio=0.12,
        )

        # Dynamic card sizes
        card_w = max(520, int(sw * 0.50))
        card_h = max(420, int(sh * 0.60))
        card_rect = self._pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (sw // 2, top_y + card_h // 2 + int(sh * 0.05))

        draw_menu_card_frame(
            screen, card_rect,
            (45, 160, 255),
            self._pygame,
            pacman_icon=self._pacman_icon
        )

        pad_x = int(card_w * 0.15)
        col_num_x = card_rect.left + pad_x
        col_name_x = card_rect.left + int(card_w * 0.25)
        col_score_x = card_rect.right - pad_x

        header_y = card_rect.top + int(card_h * 0.08)
        header_font = self._get_font(max(16, int(card_h * 0.052)))
        row_font = self._get_font(max(18, int(card_h * 0.058)))

        t_hash = header_font.render("#", True, (90, 210, 255))
        screen.blit(t_hash, (col_num_x, header_y))

        t_name_h = header_font.render("NAME", True, (90, 210, 255))
        screen.blit(t_name_h, (col_name_x, header_y))

        t_score_h = header_font.render("SCORE", True, (90, 210, 255))
        screen.blit(
            t_score_h,
            t_score_h.get_rect(topright=(col_score_x, header_y))
        )

        header_sep_y = header_y + int(card_h * 0.06)
        self._pygame.draw.line(
            screen, (60, 120, 200),
            (card_rect.left + pad_x // 2, header_sep_y),
            (card_rect.right - pad_x // 2, header_sep_y), 1
        )

        scores = self._score_registry.scores
        rows_y = header_sep_y + int(card_h * 0.05)
        row_h = int((card_rect.bottom - rows_y - int(card_h * 0.08)) / 10)

        for idx in range(10):
            cur_y = rows_y + idx * row_h
            has_entry = scores is not None and idx < len(scores)

            name_str = scores[idx].name.upper() if has_entry else "---"
            score_str = f"{scores[idx].score}" if has_entry else "0"
            is_top = idx == 0

            color = (255, 230, 0) if is_top else (220, 150, 255)

            if is_top and self._crown_icon is not None:
                icon_sz = max(18, int(row_h * 0.8))
                scaled_icon = scale_image(
                    self._crown_icon,
                    (icon_sz, icon_sz),
                    self._pygame,
                )
                icon_rect = scaled_icon.get_rect(
                    center=(col_num_x - icon_sz // 2 - 8, cur_y + row_h // 4.5)
                )
                screen.blit(scaled_icon, icon_rect)

            t_num = row_font.render(f"{idx + 1}.", True, color)
            screen.blit(t_num, (col_num_x, cur_y))

            t_name = row_font.render(name_str, True, color)
            screen.blit(t_name, (col_name_x, cur_y))

            t_score = row_font.render(score_str, True, color)
            s_rect = t_score.get_rect(topright=(col_score_x, cur_y))
            screen.blit(t_score, s_rect)

            dot_start_x = col_name_x + t_name.get_width() + 15
            dot_end_x = s_rect.left - 15
            dot_y = cur_y + t_name.get_height() // 2 + 1

            if dot_end_x > dot_start_x:
                dot_color = (255, 230, 0) if is_top else (180, 100, 220)
                for dx in range(dot_start_x, dot_end_x, 14):
                    self._pygame.draw.circle(screen, dot_color, (dx, dot_y), 2)

            if idx < 9:
                sep_y = cur_y + row_h - 1
                self._pygame.draw.line(
                    screen, (35, 25, 65),
                    (card_rect.left + pad_x // 2, sep_y),
                    (card_rect.right - pad_x // 2, sep_y), 1
                )

        hint_font = self._get_font(max(16, int(card_h * 0.08)))
        center_text(
            screen, hint_font,
            "Enter / Esc to go back",
            (200, 200, 210),
            card_rect.bottom + int(sh * 0.07)
        )
