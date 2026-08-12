"""Provide the Pygame application adapter for the Pac-Man game."""

from __future__ import annotations

from src.application import GamePhase, GameSession
from src.scores import ScoreRegistry
from src.ui.game_renderer import GameRenderer
from src.ui.input_handler import InputHandler
from src.ui.menu_renderer import MenuRenderer
from src.ui.neon_assets import (
    GhostsSpriteAtlas,
    PacgumsSpriteAtlas,
    PacmanSpriteAtlas,
)


class PygameApplication:
    """Coordinate input handler, game loop, and menu/game renderers."""

    def __init__(
        self,
        session: GameSession,
        score_registry: ScoreRegistry,
    ) -> None:
        """Initialize application dependencies and services.

        Args:
            session: Active Pac-Man game session.
            score_registry: Highscore table registry service.
        """
        self._session = session
        self._score_registry = score_registry

    def run(self) -> int:
        """Run the Pac-Man application until the game exits.

        The method initializes Pygame, creates the rendering and input
        components, processes window events, updates the game session,
        and renders the appropriate screen for the current game phase.
        Pygame is always shut down when the main loop finishes.

        Returns:
            ``0`` when the application exits normally, or ``1`` when
            Pygame cannot be imported.
        """
        try:
            import pygame
        except ImportError:
            print(
                "Missing dependency: pygame."
                " Run `python -m pip install pygame`."
            )
            return 1

        pygame.init()
        # Initial window size 16:9 (1920x1080)
        screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Pac-Man")

        # Initializing sprite atlas loaders
        pacman_atlas = PacmanSpriteAtlas(pygame)
        ghosts_atlas = GhostsSpriteAtlas(pygame)
        pacgums_atlas = PacgumsSpriteAtlas(pygame)

        menu_renderer = MenuRenderer(pygame, self._score_registry)
        game_renderer = GameRenderer(
            pygame,
            pacman_atlas=pacman_atlas if pacman_atlas.available() else None,
            ghosts_atlas=ghosts_atlas if ghosts_atlas.available() else None,
            pacgums_atlas=pacgums_atlas if pacgums_atlas.available() else None,
        )

        input_handler = InputHandler(
            self._session,
            self._score_registry,
            pygame,
            menu_renderer,
        )

        clock = pygame.time.Clock()
        fonts = (
            pygame.font.Font(None, 30),
            pygame.font.Font(None, 48),
            pygame.font.Font(None, 72),
        )

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
                    menu_renderer.draw_pause_menu(
                        screen,
                        fonts,
                        input_handler.pause_index,
                    )

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
