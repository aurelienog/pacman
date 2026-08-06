"""Responsive renderer for Main Menu, Highscores, Instructions, and Pause overlays."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.scores import ScoreRegistry
from src.ui.draw_utils import (
    center_text,
    draw_button_box,
    draw_menu_card_frame,
)

BG_DIR = Path(__file__).resolve().parents[2] / "assets" / "backgrounds"
LOGOS_DIR = Path(__file__).resolve().parents[2] / "assets" / "logos"
ICONS_DIR = Path(__file__).resolve().parents[2] / "assets" / "icons"

MENU_BG_PATH = BG_DIR / "background_menu.png"
SCORES_BG_PATH = BG_DIR / "background_scores.png"
INSTRUCTIONS_BG_PATH = BG_DIR / "background_instructions.png"


class MenuRenderer:
    """Render non-gameplay menu overlays with dynamic scaling and interactive buttons."""

    def __init__(self, pygame: Any, score_registry: ScoreRegistry) -> None:
        self._pygame = pygame
        self._score_registry = score_registry
        self._menu_bg = self._load_image(MENU_BG_PATH, alpha=False)
        self._scores_bg = self._load_image(SCORES_BG_PATH, alpha=False)
        self._instructions_bg = self._load_image(INSTRUCTIONS_BG_PATH, alpha=False)

        self._logo_main = self._load_image_fallback("logo.png", alpha=True)
        self._logo_instructions = self._load_image_fallback("game_instructions_logo.png", alpha=True)
        self._logo_scores = self._load_image_fallback("top10_highscores_logo.png", alpha=True)
        self._pacman_icon = self._load_image_fallback("pacman_icon1.png", alpha=True)

        self._font_cache: dict[int, Any] = {}

        # Hitboxes for mouse interaction
        self.main_menu_rects: list[Any] = []
        self.pause_menu_rects: list[Any] = []

    def _load_image(self, path: Path, alpha: bool = False) -> Any:
        if path.is_file():
            try:
                img = self._pygame.image.load(str(path))
                return img.convert_alpha() if alpha else img.convert()
            except Exception:
                return None
        return None

    def _load_image_fallback(self, filename: str, alpha: bool = True) -> Any:
        possible = [
            LOGOS_DIR / filename,
            ICONS_DIR / filename,
            Path(__file__).resolve().parents[2] / "assets" / filename,
        ]
        for p in possible:
            if p.is_file():
                try:
                    img = self._pygame.image.load(str(p))
                    return img.convert_alpha() if alpha else img.convert()
                except Exception:
                    pass
        return None

    def _get_font(self, size: int) -> Any:
        if size not in self._font_cache:
            self._font_cache[size] = self._pygame.font.Font(None, size)
        return self._font_cache[size]

    def _render_bg(self, screen: Any, bg_image: Any) -> None:
        target_bg = bg_image if bg_image is not None else self._menu_bg
        if target_bg is not None:
            scaled_bg = self._pygame.transform.smoothscale(
                target_bg, (screen.get_width(), screen.get_height())
            )
            screen.blit(scaled_bg, (0, 0))
        else:
            screen.fill((8, 8, 19))

    def _draw_logo(self, screen: Any, logo_img: Any = None, fallback_text: str = "PAC-MAN") -> int:
        sw, sh = screen.get_width(), screen.get_height()
        center_y = int(sh * 0.15)
        target_logo = logo_img if logo_img is not None else self._logo_main

        if target_logo is not None:
            aspect = target_logo.get_width() / target_logo.get_height()
            target_h = int(sh * 0.22)
            target_w = int(target_h * aspect)

            if target_w > int(sw * 0.85):
                target_w = int(sw * 0.85)
                target_h = int(target_w / aspect)

            scaled_logo = self._pygame.transform.smoothscale(target_logo, (target_w, target_h))
            rect = scaled_logo.get_rect(center=(sw // 2, center_y))
            screen.blit(scaled_logo, rect)
            return rect.bottom

        title_font = self._get_font(int(sh * 0.09))
        rect = center_text(screen, title_font, fallback_text, (255, 230, 0), center_y)
        return rect.bottom

    def draw_main_menu(
        self,
        screen: Any,
        fonts: tuple[Any, Any, Any],
        menu_index: int,
        show_scores: bool,
        show_instructions: bool,
    ) -> None:
        sw, sh = screen.get_width(), screen.get_height()

        if show_scores:
            self._render_bg(screen, self._scores_bg)
            logo_bottom = self._draw_logo(screen, self._logo_scores, "TOP 10 HIGHSCORES")
            self._draw_highscores(screen, logo_bottom)
            return

        if show_instructions:
            self._render_bg(screen, self._instructions_bg)
            logo_bottom = self._draw_logo(screen, self._logo_instructions, "GAME INSTRUCTIONS")
            self._draw_instructions(screen, logo_bottom)
            return

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
            box_h = max(44, int(text_rect.height * 1.5))
            hit_rect = self._pygame.Rect(0, 0, box_w, box_h)
            hit_rect.center = (sw // 2, y_pos)
            self.main_menu_rects.append(hit_rect)

            if is_selected:
                draw_button_box(screen, hit_rect, self._pygame)

            screen.blit(text_surf, text_rect)

    def draw_pause_menu(self, screen: Any, fonts: tuple[Any, Any, Any], pause_index: int) -> None:
        """Draw responsive pause menu overlay."""
        sw, sh = screen.get_width(), screen.get_height()

        card_w = min(int(sw * 0.45), 600)
        card_h = min(int(sh * 0.62), 620)
        card_rect = self._pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (sw // 2, sh // 2)

        purple_color = (180, 50, 240)
        draw_menu_card_frame(screen, card_rect, purple_color, self._pygame, pacman_icon=self._pacman_icon)

        title_font = self._get_font(int(card_h * 0.14))
        center_text(screen, title_font, "PAUSED", (255, 100, 220), card_rect.top + int(card_h * 0.16))

        menu_font = self._get_font(int(card_h * 0.08))
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
            box_h = max(40, int(text_rect.height * 1.4))
            hit_rect = self._pygame.Rect(0, 0, box_w, box_h)
            hit_rect.center = (sw // 2, y_pos)
            self.pause_menu_rects.append(hit_rect)

            if is_selected:
                draw_button_box(screen, hit_rect, self._pygame, color=purple_color)

            screen.blit(text_surf, text_rect)

    def _draw_highscores(self, screen: Any, top_y: int) -> None:
        """Draw leaderboard frame."""
        sw, sh = screen.get_width(), screen.get_height()

        card_w = min(int(sw * 0.7), 900)
        card_h = min(int(sh * 0.6), 750)
        card_rect = self._pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (sw // 2, top_y + card_h // 2 + int(sh * 0.02))

        draw_menu_card_frame(screen, card_rect, (45, 160, 255), self._pygame, pacman_icon=self._pacman_icon)

        pad_x = int(card_w * 0.15)
        col_num_x = card_rect.left + pad_x
        col_name_x = card_rect.left + int(card_w * 0.25)
        col_score_x = card_rect.right - pad_x

        header_y = card_rect.top + int(card_h * 0.08)
        header_font = self._get_font(int(card_h * 0.052))
        row_font = self._get_font(int(card_h * 0.058))

        t_hash = header_font.render("#", True, (90, 210, 255))
        screen.blit(t_hash, (col_num_x, header_y))

        t_name_h = header_font.render("NAME", True, (90, 210, 255))
        screen.blit(t_name_h, (col_name_x, header_y))

        t_score_h = header_font.render("SCORE", True, (90, 210, 255))
        screen.blit(t_score_h, t_score_h.get_rect(topright=(col_score_x, header_y)))

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

            if is_top and self._pacman_icon is not None:
                icon_sz = max(18, int(row_h * 0.8))
                scaled_icon = self._pygame.transform.smoothscale(self._pacman_icon, (icon_sz, icon_sz))
                icon_rect = scaled_icon.get_rect(center=(col_num_x - icon_sz // 2 - 8, cur_y + row_h // 4.5))
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

        hint_font = self._get_font(int(card_h * 0.08))
        center_text(screen, hint_font, "Enter / Esc to go back", (200, 200, 210), card_rect.bottom + int(sh * 0.05))

    def _draw_instructions(self, screen: Any, top_y: int) -> None:
        sw, sh = screen.get_width(), screen.get_height()

        text = [
            "Move: arrows or WASD",
            "Pause: P / Esc",
            "Cheats: I invincible, F ghosts, T timer, B speed boost, N next level, L life",
        ]
        start_y = top_y + int(sh * 0.08)
        spacing = int(sh * 0.06)

        item_font = self._get_font(int(sh * 0.038))
        for index, line in enumerate(text):
            center_text(screen, item_font, line, (230, 230, 235), start_y + index * spacing)

        hint_font = self._get_font(int(sh * 0.048))
        center_text(screen, hint_font, "Enter / Esc to go back", (200, 200, 210), int(sh * 0.90))
