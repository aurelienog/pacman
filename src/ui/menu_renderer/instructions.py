"""Renderer for the Game Instructions view."""

from __future__ import annotations

from typing import Any

from src.ui.draw_utils import center_text, draw_menu_card_frame
from .base_menu import BG_DIR, BaseMenuView

INSTRUCTIONS_BG_PATH = BG_DIR / "background_instructions.png"


class InstructionsView(BaseMenuView):
    """Render game instructions and cheat keys panel."""

    def __init__(self, pygame: Any) -> None:
        super().__init__(pygame)
        self._instructions_bg = self._load_image(
            INSTRUCTIONS_BG_PATH,
            alpha=False
        )
        self._logo_instructions = self._load_icon("game_instructions_logo.png")

        self._pacman_icon = self._load_icon("pacman_icon.png")
        self._dots_icon = self._load_icon("dots_icons.png")
        self._ghosts_icon = self._load_icon("ghosts_icons.png")
        self._super_pacgum_icon = self._load_icon("super_pacgum_icons.png")
        self._timer_icon = self._load_icon("timer_icon.png")
        self._cheats_logo = self._load_icon("cheats_logo.png")

    def draw(self, screen: Any) -> None:
        """Draw instructions card frame, icons, rules text, and cheat codes."""
        sw, sh = screen.get_width(), screen.get_height()

        self._render_bg(screen, self._instructions_bg)
        top_y = self._draw_logo(
            screen,
            self._logo_instructions,
            "GAME INSTRUCTIONS",
            height_ratio=0.16,  # <--- Size
            y_ratio=0.135,       # <--- Position
        )

        # Dynamic card sizes (78% width and 68% height of the window)
        card_w = max(550, int(sw * 0.5))
        card_h = max(420, int(sh * 0.6))
        card_rect = self._pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (sw // 2, top_y + card_h // 2 + int(sh * 0.045))

        # Blue instruction panel frame
        draw_menu_card_frame(
            screen, card_rect,
            (0, 140, 255),
            self._pygame,
            pacman_icon=self._pacman_icon
        )

        col_icon_x = card_rect.left + int(card_w * 0.18)
        col_text_x = card_rect.left + int(card_w * 0.35)

        text_font = self._get_font(max(14, int(card_h * 0.05)))
        cheat_font = self._get_font(max(15, int(card_h * 0.05)))
        text_color = (240, 240, 245)

        start_y = card_rect.top + int(card_h * 0.1)
        row_step = int(card_h * 0.14)

        # Line 1: CONTROL PAC-MAN
        r1_y = start_y
        if self._pacman_icon and self._dots_icon:
            pm_sz = int(card_h * 0.08)
            dt_w, dt_h = int(card_w * 0.16), int(card_h * 0.08)
            ic_pm = self._pygame.transform.smoothscale(
                self._pacman_icon,
                (pm_sz, pm_sz)
            )
            ic_dt = self._pygame.transform.smoothscale(
                self._dots_icon,
                (dt_w, dt_h)
            )
            screen.blit(
                ic_pm,
                (col_icon_x - int(card_w * 0.11), r1_y - int(card_h * 0.02))
            )
            screen.blit(
                ic_dt,
                (col_icon_x - int(card_w * 0.06), r1_y - int(card_h * 0.02))
            )

        t1_1 = text_font.render(
            "CONTROL PAC-MAN AND EAT ALL THE DOTS.",
            True,
            text_color
        )
        t1_2 = text_font.render(
            "FINISH THE LEVEL TO MOVE TO THE NEXT ONE.",
            True,
            text_color
        )
        screen.blit(t1_1, (col_text_x, r1_y - int(card_h * 0.025)))
        screen.blit(t1_2, (col_text_x, r1_y + int(card_h * 0.025)))

        # Line 2: AVOID THE GHOSTS
        r2_y = start_y + row_step
        if self._ghosts_icon:
            gh_w, gh_h = int(card_w * 0.2), int(card_h * 0.10)
            ic_gh = self._pygame.transform.smoothscale(
                self._ghosts_icon,
                (gh_w, gh_h)
            )
            screen.blit(ic_gh, ic_gh.get_rect(center=(col_icon_x - 10, r2_y)))

        t2_1 = text_font.render(
            "AVOID THE GHOSTS! THEY WILL CHASE YOU.",
            True,
            text_color
        )
        t2_2 = text_font.render("YOU HAVE LIMITED LIVES.", True, text_color)
        screen.blit(t2_1, (col_text_x, r2_y - int(card_h * 0.025)))
        screen.blit(t2_2, (col_text_x, r2_y + int(card_h * 0.025)))

        # Line 3: EAT POWER PELLETS
        r3_y = start_y + row_step * 2
        if self._super_pacgum_icon:
            sp_w, sp_h = int(card_w * 0.2), int(card_h * 0.10)
            ic_sp = self._pygame.transform.smoothscale(
                self._super_pacgum_icon,
                (sp_w, sp_h)
            )
            screen.blit(ic_sp, ic_sp.get_rect(center=(col_icon_x - 10, r3_y)))

        t3_1 = text_font.render(
            "EAT POWER PELLETS TO MAKE GHOSTS BLUE",
            True,
            text_color
        )
        t3_2 = text_font.render(
            "AND EAT THEM FOR BONUS POINTS!",
            True,
            text_color
        )
        screen.blit(t3_1, (col_text_x, r3_y - int(card_h * 0.025)))
        screen.blit(t3_2, (col_text_x, r3_y + int(card_h * 0.025)))

        # Line 4: WATCH THE TIMER
        r4_y = start_y + row_step * 3
        if self._timer_icon:
            tm_sz = int(card_h * 0.08)
            ic_tm = self._pygame.transform.smoothscale(
                self._timer_icon,
                (tm_sz, tm_sz)
            )
            screen.blit(ic_tm, ic_tm.get_rect(center=(col_icon_x - 10, r4_y)))

        t4_1 = text_font.render(
            "WATCH THE TIMER! TIME IS LIMITED.",
            True,
            text_color
        )
        screen.blit(t4_1, (col_text_x, r4_y - int(card_h * 0.012)))

        # Separator line
        sep_y = card_rect.top + int(card_h * 0.66)
        self._pygame.draw.line(
            screen, (40, 80, 160),
            (card_rect.left + 30, sep_y),
            (card_rect.right - 30, sep_y), 1
        )

        # Line 5: CHEATS SECTION
        cheats_y = card_rect.top + int(card_h * 0.72)

        if self._cheats_logo:
            ch_w, ch_h = int(card_w * 0.22), int(card_h * 0.12)
            ic_ch = self._pygame.transform.smoothscale(
                self._cheats_logo,
                (ch_w, ch_h)
            )
            screen.blit(
                ic_ch,
                ic_ch.get_rect(
                    center=(col_icon_x - 10, cheats_y + int(card_h * 0.05))
                )
            )

        c_col1_x = card_rect.left + int(card_w * 0.35)
        c_col2_x = card_rect.left + int(card_w * 0.67)

        cheat_spacing = int(card_h * 0.055)

        # Column 1 cheats
        c1_1 = cheat_font.render("I - INVINCIBLE", True, text_color)
        c1_2 = cheat_font.render("L - EXTRA LIVES", True, text_color)
        c1_3 = cheat_font.render("N - LEVEL SKIP", True, text_color)

        screen.blit(c1_1, (c_col1_x, cheats_y))
        screen.blit(c1_2, (c_col1_x, cheats_y + cheat_spacing))
        screen.blit(c1_3, (c_col1_x, cheats_y + cheat_spacing * 2))

        # Column 2 cheats
        c2_1 = cheat_font.render("F - GHOST FREEZE", True, text_color)
        c2_2 = cheat_font.render("T - STOP TIME", True, text_color)
        c2_3 = cheat_font.render("B - BOOST SPEED x2", True, text_color)

        screen.blit(c2_1, (c_col2_x, cheats_y))
        screen.blit(c2_2, (c_col2_x, cheats_y + cheat_spacing))
        screen.blit(c2_3, (c_col2_x, cheats_y + cheat_spacing * 2))

        # Bottom hint
        hint_font = self._get_font(max(16, int(card_h * 0.08)))
        center_text(
            screen,
            hint_font,
            "Enter / Esc to go back",
            (200, 200, 210),
            card_rect.bottom + int(sh * 0.07)
        )
