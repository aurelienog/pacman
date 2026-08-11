"""Renderer for in-game HUD and active cheat indicators."""

from __future__ import annotations

from typing import Any

from src.application.contracts import Snapshot
from src.ui.draw_utils import draw_line
from .base_game_view import BaseGameView


class HudView(BaseGameView):
    """Render top HUD columns and active cheat code tape."""

    def __init__(self, pygame: Any) -> None:
        """Initialize HUD view and load icons.

        Args:
            pygame: Pygame module instance.

        Returns:
            None.
        """
        super().__init__(pygame)
        self._pacman_icon = self._load_icon("pacman_icon.png")
        self._level_icon = self._load_icon("level_icon.png")
        self._timer_icon = self._load_icon("timer_icon.png")

    def draw(self, screen: Any, snapshot: Snapshot) -> None:
        """Draw SCORE, LIVES, LEVEL, TIME columns and cheat indicators.

        Args:
            screen: Pygame display surface.
            snapshot: Current game state snapshot.

        Returns:
            None.
        """
        sw, sh = screen.get_width(), screen.get_height()

        header_font_size = max(14, int(sh * 0.022))
        value_font_size = max(16, int(sh * 0.028))

        header_font = self._get_font(header_font_size)
        value_font = self._get_font(value_font_size)

        cyan_color = (0, 210, 255)
        white_color = (245, 245, 245)
        sep_color = (180, 50, 240)

        col_w = max(85, int(sw * 0.075))
        icon_sz = max(16, int(sh * 0.028))
        line_w = max(1, int(sw * 0.0015))

        start_x = 10
        y_label = 30
        y_val = y_label + max(18, int(sh * 0.024))

        # 1. SCORE
        cx1 = start_x + col_w // 2
        lbl_score = header_font.render("SCORE", True, cyan_color)
        screen.blit(lbl_score, lbl_score.get_rect(center=(cx1, y_label)))

        val_score = value_font.render(
            f"{snapshot.score:06d}",
            True,
            white_color,
        )
        screen.blit(val_score, val_score.get_rect(center=(cx1, y_val)))

        # Separator 1
        sep1_x = start_x + col_w
        draw_line(
            screen,
            (sep1_x, y_label - 2),
            (sep1_x, y_val + icon_sz // 2 + 2),
            sep_color,
            self._pygame,
            width=line_w,
        )

        # 2. LIVES
        cx2 = sep1_x + col_w // 2
        lbl_lives = header_font.render("LIVES", True, cyan_color)
        screen.blit(lbl_lives, lbl_lives.get_rect(center=(cx2, y_label)))

        lives_count = snapshot.player.lives if snapshot.player else 0
        txt_lives = value_font.render(f" x {lives_count}", True, white_color)

        if self._pacman_icon:
            ic_pm = self._pygame.transform.smoothscale(
                self._pacman_icon,
                (icon_sz, icon_sz),
            )
            total_w = icon_sz + txt_lives.get_width()
            start_icon_x = cx2 - total_w // 2
            screen.blit(ic_pm, (start_icon_x, y_val - icon_sz // 2))
            screen.blit(
                txt_lives,
                (start_icon_x + icon_sz, y_val - txt_lives.get_height() // 2),
            )
        else:
            screen.blit(txt_lives, txt_lives.get_rect(center=(cx2, y_val)))

        # Separator 2
        sep2_x = sep1_x + col_w
        draw_line(
            screen,
            (sep2_x, y_label - 2),
            (sep2_x, y_val + icon_sz // 2 + 2),
            sep_color,
            self._pygame,
            width=line_w,
        )

        # 3. LEVEL
        cx3 = sep2_x + col_w // 2
        lbl_level = header_font.render("LEVEL", True, cyan_color)
        screen.blit(lbl_level, lbl_level.get_rect(center=(cx3, y_label)))

        txt_lvl = value_font.render(
            f" {snapshot.level}/{snapshot.level_count}",
            True,
            white_color,
        )
        if self._level_icon:
            ic_lvl = self._pygame.transform.smoothscale(
                self._level_icon,
                (icon_sz, icon_sz),
            )
            total_w = icon_sz + txt_lvl.get_width()
            start_icon_x = cx3 - total_w // 2
            screen.blit(ic_lvl, (start_icon_x, y_val - icon_sz // 2))
            screen.blit(
                txt_lvl,
                (start_icon_x + icon_sz, y_val - txt_lvl.get_height() // 2),
            )
        else:
            screen.blit(txt_lvl, txt_lvl.get_rect(center=(cx3, y_val)))

        # Separator 3
        sep3_x = sep2_x + col_w
        draw_line(
            screen,
            (sep3_x, y_label - 2),
            (sep3_x, y_val + icon_sz // 2 + 2),
            sep_color,
            self._pygame,
            width=line_w,
        )

        # 4. TIME
        cx4 = sep3_x + col_w // 2
        lbl_time = header_font.render("TIME", True, cyan_color)
        screen.blit(lbl_time, lbl_time.get_rect(center=(cx4, y_label)))

        sec = max(0, int(snapshot.seconds_remaining))
        txt_time = value_font.render(f" {sec}", True, white_color)
        if self._timer_icon:
            ic_tm = self._pygame.transform.smoothscale(
                self._timer_icon,
                (icon_sz, icon_sz),
            )
            total_w = icon_sz + txt_time.get_width()
            start_icon_x = cx4 - total_w // 2
            screen.blit(ic_tm, (start_icon_x, y_val - icon_sz // 2))
            screen.blit(
                txt_time,
                (start_icon_x + icon_sz, y_val - txt_time.get_height() // 2),
            )
        else:
            screen.blit(txt_time, txt_time.get_rect(center=(cx4, y_val)))

        # 5. CHEAT TAPE
        cheats = [
            label
            for enabled, label in (
                (snapshot.invincible, "INVINCIBLE [I]"),
                (snapshot.freeze_ghosts, "GHOSTS FROZEN [F]"),
                (snapshot.freeze_timer, "TIMER FROZEN [T]"),
                (snapshot.speed_boost, "SPEED BOOST [B]"),
            )
            if enabled
        ]
        if cheats:
            surface = header_font.render(
                "  |  ".join(cheats),
                True,
                (255, 215, 90),
            )
            screen.blit(
                surface,
                (start_x + 30, y_val + max(20, int(sh * 0.03))),
            )
