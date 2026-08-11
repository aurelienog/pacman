"""Coordinate rendering of the Pac-Man menu views."""

from __future__ import annotations

from typing import Any

from src.scores import ScoreRegistry
from .highscores import HighscoresView
from .instructions import InstructionsView
from .main_menu import MainMenuView
from .pause_menu import PauseMenuView


class MenuRenderer:
    """Delegate menu rendering to specific modular view classes."""

    def __init__(self, pygame: Any, score_registry: ScoreRegistry) -> None:
        """Initialize all sub-views and view dependencies.

        Args:
            pygame: Pygame module instance.
            score_registry: Highscore table registry service.

        Returns:
            None.
        """
        self._main_menu_view = MainMenuView(pygame)
        self._pause_menu_view = PauseMenuView(pygame)
        self._highscores_view = HighscoresView(pygame, score_registry)
        self._instructions_view = InstructionsView(pygame)

    @property
    def main_menu_rects(self) -> list[Any]:
        """Return button hitboxes for main menu mouse interaction."""
        return self._main_menu_view.main_menu_rects

    @property
    def pause_menu_rects(self) -> list[Any]:
        """Return button hitboxes for pause menu mouse interaction."""
        return self._pause_menu_view.pause_menu_rects

    def draw_main_menu(
        self,
        screen: Any,
        fonts: tuple[Any, Any, Any],
        menu_index: int,
        show_scores: bool,
        show_instructions: bool,
    ) -> None:
        """Route drawing to Highscores, Instructions, or Main Menu view.

        The method selects the highscore, instructions, or main menu
        view according to the supplied display flags.

        Args:
            screen: Pygame surface on which the view is drawn.
            fonts: Fonts supplied by the application.
            menu_index: Currently selected menu item index.
            show_scores: Whether highscores overlay is active.
            show_instructions: Whether instructions overlay is active.

        Returns:
            None.
        """
        if show_scores:
            self._highscores_view.draw(screen)
            return

        if show_instructions:
            self._instructions_view.draw(screen)
            return

        self._main_menu_view.draw(screen, menu_index)

    def draw_pause_menu(
        self,
        screen: Any,
        fonts: tuple[Any, Any, Any],
        pause_index: int,
    ) -> None:
        """Route drawing to Pause Menu view.

        Args:
            screen: Pygame surface on which the menu is drawn.
            fonts: Fonts supplied by the application.
            pause_index: Currently selected pause menu item index.

        Returns:
            None.
        """
        self._pause_menu_view.draw(screen, pause_index)


__all__ = [
    "MenuRenderer",
    "MainMenuView",
    "PauseMenuView",
    "HighscoresView",
    "InstructionsView",
]
