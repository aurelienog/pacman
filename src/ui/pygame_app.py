"""Pygame driving coordinator adapter."""

from __future__ import annotations

from src.application import GamePhase, GameSession
from src.scores import ScoreRegistry
from src.ui.game_renderer import GameRenderer
from src.ui.input_handler import InputHandler
from src.ui.menu_renderer import MenuRenderer
from src.ui.neon_assets import NeonSpriteAtlas


class PygameApplication:
    """Coordinate input handler, game loop, and menu/game renderers."""

    def __init__(self, session: GameSession, score_registry: ScoreRegistry) -> None:
        self._session = session
        self._score_registry = score_registry

    def run(self) -> int:
        try:
            import pygame
        except ImportError:
            print("Missing dependency: pygame. Run `python -m pip install pygame`.")
            return 1

        pygame.init()
        screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
        pygame.display.set_caption("Pac-Man")

        atlas = NeonSpriteAtlas(pygame) if NeonSpriteAtlas.available() else None
        menu_renderer = MenuRenderer(pygame, self._score_registry)
        game_renderer = GameRenderer(pygame, atlas)
        input_handler = InputHandler(self._session, self._score_registry, pygame)

        clock = pygame.time.Clock()
        fonts = (pygame.font.Font(None, 30), pygame.font.Font(None, 48), pygame.font.Font(None, 72))

        try:
            while self._session.phase is not GamePhase.EXIT:
                for event in pygame.event.get():
                    input_handler.handle_event(event)

                self._session.update(clock.tick(60) / 1000.0)

                snapshot = self._session.snapshot()
                if snapshot.phase is GamePhase.MAIN_MENU:
                    menu_renderer.draw_main_menu(
                        screen,
                        fonts,
                        input_handler.menu_index,
                        input_handler.show_scores,
                        input_handler.show_instructions,
                    )
                else:
                    screen.fill((8, 8, 19))
                    game_renderer.draw_game(screen, snapshot, fonts)

                if snapshot.phase is GamePhase.PAUSED:
                    menu_renderer.draw_pause_menu(screen, fonts, input_handler.pause_index)

                if snapshot.phase in (GamePhase.GAME_OVER, GamePhase.VICTORY):
                    game_renderer.draw_end_screen(
                        screen,
                        snapshot,
                        fonts,
                        input_handler.name,
                        input_handler.saved,
                    )

                pygame.display.flip()
        finally:
            pygame.quit()

        return 0
