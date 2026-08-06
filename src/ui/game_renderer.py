"""Renderer for active gameplay, maze walls, entities, HUD, and end screens."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.application.contracts import GamePhase, Snapshot
from src.domain import GhostMode, ItemKind, Position
from src.ui.draw_utils import (
    center_float,
    center_text,
    draw_circle,
    draw_line,
    draw_menu_card_frame,
)
from src.ui.neon_assets import NeonSpriteAtlas

ICONS_DIR = Path(__file__).resolve().parents[2] / "assets" / "icons"
LOGOS_DIR = Path(__file__).resolve().parents[2] / "assets" / "logos"


class GameRenderer:
    """Draw maze, entities, HUD, cheats status, and victory/game over screens."""

    def __init__(self, pygame: Any, atlas: NeonSpriteAtlas | None) -> None:
        self._pygame = pygame
        self._atlas = atlas
        self._font_cache: dict[int, Any] = {}
        self._pacman_icon = self._load_pacman_icon()

    def _load_pacman_icon(self) -> Any:
        possible = [
            ICONS_DIR / "pacman_icon1.png",
            LOGOS_DIR / "pacman_icon1.png",
            Path(__file__).resolve().parents[2] / "assets" / "pacman_icon1.png",
        ]
        for p in possible:
            if p.is_file():
                try:
                    return self._pygame.image.load(str(p)).convert_alpha()
                except Exception:
                    pass
        return None

    def _get_font(self, size: int) -> Any:
        if size not in self._font_cache:
            self._font_cache[size] = self._pygame.font.Font(None, size)
        return self._font_cache[size]

    def draw_game(self, screen: Any, snapshot: Snapshot, fonts: tuple[Any, Any, Any]) -> None:
        """Draw complete gameplay view."""
        if snapshot.maze is None or snapshot.player is None:
            return

        maze = snapshot.maze
        cell = max(8, min((screen.get_width() - 40) // maze.width, (screen.get_height() - 120) // maze.height))
        left = (screen.get_width() - maze.width * cell) // 2
        top = 80

        self._draw_hud(screen, snapshot, fonts)
        self._draw_maze(screen, maze, left, top, cell)
        self._draw_items(screen, snapshot, left, top, cell)
        self._draw_player(screen, snapshot, left, top, cell)
        self._draw_ghosts(screen, snapshot, left, top, cell)

        if snapshot.message:
            center_text(screen, fonts[0], snapshot.message, (255, 230, 0), screen.get_height() - 25)

    def draw_end_screen(
        self,
        screen: Any,
        snapshot: Snapshot,
        fonts: tuple[Any, Any, Any],
        name: str,
        saved: bool,
    ) -> None:
        """Draw GAME OVER or VICTORY dialog card."""
        sw, sh = screen.get_width(), screen.get_height()

        card_w = min(int(sw * 0.45), 600)
        card_h = min(int(sh * 0.62), 620)
        card_rect = self._pygame.Rect(0, 0, card_w, card_h)
        card_rect.center = (sw // 2, sh // 2)

        is_over = snapshot.phase is GamePhase.GAME_OVER

        border_color = (255, 50, 70) if is_over else (50, 235, 100)
        draw_menu_card_frame(screen, card_rect, border_color, self._pygame, pacman_icon=self._pacman_icon)

        # Title
        title_text = "GAME OVER" if is_over else "LEVEL CLEAR!"
        title_color = (255, 60, 75) if is_over else (50, 235, 100)
        title_font = self._get_font(int(card_h * 0.09))
        center_text(screen, title_font, title_text, title_color, card_rect.top + int(card_h * 0.16))

        # "SCORE" Header
        cyan_font = self._get_font(int(card_h * 0.045))
        center_text(screen, cyan_font, "SCORE", (0, 210, 255), card_rect.top + int(card_h * 0.36))

        # Score Value
        score_font = self._get_font(int(card_h * 0.07))
        score_str = f"{snapshot.score:06d}"
        center_text(screen, score_font, score_str, (245, 245, 245), card_rect.top + int(card_h * 0.47))

        # Name Entry Prompt
        prompt_font = self._get_font(int(card_h * 0.05))
        prompt_text = "Saved. Press Enter" if saved else f"Name (max 10): {name}_"
        center_text(screen, prompt_font, prompt_text, (230, 230, 240), card_rect.top + int(card_h * 0.72))

    def _draw_hud(self, screen: Any, snapshot: Snapshot, fonts: tuple[Any, Any, Any]) -> None:
        """Draw text HUD."""
        hud = (
            f"Score {snapshot.score}    Lives {snapshot.player.lives if snapshot.player else 0}    "
            f"Level {snapshot.level}/{snapshot.level_count}    Time {max(0, snapshot.seconds_remaining):.0f}"
        )
        screen.blit(fonts[0].render(hud, True, (240, 240, 240)), (20, 20))

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
            surface = fonts[0].render("  |  ".join(cheats), True, (255, 215, 90))
            screen.blit(surface, (20, 48))

    def _draw_maze(self, screen: Any, maze: Any, left: int, top: int, cell: int) -> None:
        for y, row in enumerate(maze.cells):
            for x, walls in enumerate(row):
                px, py = left + x * cell, top + y * cell
                is_42 = maze.is_42_art(Position(x, y))
                wall_color = (235, 70, 255) if is_42 else (45, 90, 255)

                if is_42:
                    self._pygame.draw.rect(screen, (74, 16, 95), (px + 2, py + 2, cell - 3, cell - 3))
                if walls & 1:
                    draw_line(screen, (px, py), (px + cell, py), wall_color, self._pygame)
                if walls & 2:
                    draw_line(screen, (px + cell, py), (px + cell, py + cell), wall_color, self._pygame)
                if walls & 4:
                    draw_line(screen, (px, py + cell), (px + cell, py + cell), wall_color, self._pygame)
                if walls & 8:
                    draw_line(screen, (px, py), (px, py + cell), wall_color, self._pygame)

    def _draw_items(self, screen: Any, snapshot: Snapshot, left: int, top: int, cell: int) -> None:
        for position, item in snapshot.items:
            radius = max(2, cell // (4 if item.kind is ItemKind.SUPER_PACGUM else 7))
            center = center_float(position.x, position.y, left, top, cell)
            draw_circle(screen, center, radius, (255, 226, 140), self._pygame)

    def _draw_player(self, screen: Any, snapshot: Snapshot, left: int, top: int, cell: int) -> None:
        if snapshot.player is None:
            return
        px_vis, py_vis = snapshot.player_visual_pos
        player_center = center_float(px_vis, py_vis, left, top, cell)
        if self._atlas is not None:
            self._atlas.draw_player(screen, player_center, cell, snapshot.player.direction)
        else:
            draw_circle(screen, player_center, max(4, cell // 2 - 2), (255, 222, 0), self._pygame)

    def _draw_ghosts(self, screen: Any, snapshot: Snapshot, left: int, top: int, cell: int) -> None:
        colors = [(255, 60, 60), (255, 140, 255), (70, 230, 255), (255, 150, 50)]
        for index, g_ent in enumerate(snapshot.ghost_visual_positions):
            center = center_float(g_ent.x, g_ent.y, left, top, cell)
            if self._atlas is not None:
                self._atlas.draw_ghost(screen, center, cell, index, g_ent.mode)
            else:
                color = (50, 90, 255) if g_ent.mode is GhostMode.FRIGHTENED else colors[index % 4]
                if g_ent.mode is not GhostMode.RESPAWNING:
                    draw_circle(screen, center, max(4, cell // 2 - 2), color, self._pygame)
