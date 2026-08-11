"""Facade coordinator for UI input handlers across Pac-Man game states."""

from __future__ import annotations

from typing import Any

from src.application import GamePhase, GameSession, InputAction
from src.scores import ScoreRegistry
from src.ui.menu_renderer import MenuRenderer

from .end_screen_handler import EndScreenInputHandler
from .menu_handler import MenuInputHandler
from .pause_handler import PauseInputHandler
from .playing_handler import PlayingInputHandler


class InputHandler:
    """Coordinate state-specific input handlers
    while maintaining unified API."""

    def __init__(
        self,
        session: GameSession,
        score_registry: ScoreRegistry,
        pygame: Any,
        menu_renderer: MenuRenderer,
    ) -> None:
        """Initialize state input handlers and dependencies.

        Args:
            session: Active game session used to dispatch input actions.
            score_registry: Registry used by the end-screen handler to
                save high scores.
            pygame: Pygame module instance.
            menu_renderer: Menu renderer providing menu hitboxes.

        Returns:
            None.
        """
        self._session = session
        self._pygame = pygame
        self._menu_handler = MenuInputHandler(session, pygame, menu_renderer)
        self._pause_handler = PauseInputHandler(session, pygame, menu_renderer)
        self._playing_handler = PlayingInputHandler(session, pygame)
        self._end_screen_handler = EndScreenInputHandler(
            session,
            score_registry,
            pygame,
        )

    @property
    def menu_index(self) -> int:
        """Selected main menu button index."""
        return self._menu_handler.menu_index

    @menu_index.setter
    def menu_index(self, value: int) -> None:
        self._menu_handler.menu_index = value

    @property
    def show_scores(self) -> bool:
        """Whether the highscores screen is displayed."""
        return self._menu_handler.show_scores

    @show_scores.setter
    def show_scores(self, value: bool) -> None:
        self._menu_handler.show_scores = value

    @property
    def show_instructions(self) -> bool:
        """Whether the instructions screen is displayed."""
        return self._menu_handler.show_instructions

    @show_instructions.setter
    def show_instructions(self, value: bool) -> None:
        self._menu_handler.show_instructions = value

    @property
    def pause_index(self) -> int:
        """Selected pause menu button index."""
        return self._pause_handler.pause_index

    @pause_index.setter
    def pause_index(self, value: int) -> None:
        self._pause_handler.pause_index = value

    @property
    def name(self) -> str:
        """Player name input string."""
        return self._end_screen_handler.name

    @name.setter
    def name(self, value: str) -> None:
        self._end_screen_handler.name = value

    @property
    def saved(self) -> bool:
        """Whether the highscore entry has been saved."""
        return self._end_screen_handler.saved

    @saved.setter
    def saved(self, value: bool) -> None:
        self._end_screen_handler.saved = value

    def handle_event(self, event: Any) -> None:
        """Route pygame event to corresponding sub-handler based on phase.

        Quit, mouse movement, mouse clicks, and keyboard events are
        dispatched according to the current game phase.

        Args:
            event: Pygame event object.

        Returns:
            None.
        """
        if event.type == self._pygame.QUIT:
            self._session.dispatch(InputAction.QUIT)
            return

        # Mouse movement processing
        if event.type == self._pygame.MOUSEMOTION:
            snapshot = self._session.snapshot()
            if snapshot.phase is GamePhase.MAIN_MENU:
                self._menu_handler.handle_mouse_move(event.pos)
            elif snapshot.phase is GamePhase.PAUSED:
                self._pause_handler.handle_mouse_move(event.pos)
            return

        # Left mouse click handling
        if event.type == self._pygame.MOUSEBUTTONDOWN and event.button == 1:
            snapshot = self._session.snapshot()
            if snapshot.phase is GamePhase.MAIN_MENU:
                self._menu_handler.handle_mouse_click(event.pos)
            elif snapshot.phase is GamePhase.PAUSED:
                self._pause_handler.handle_mouse_click(event.pos)
            return

        if event.type != self._pygame.KEYDOWN:
            return

        snapshot = self._session.snapshot()
        if snapshot.phase is GamePhase.MAIN_MENU:
            self._menu_handler.handle_key(event.key)
        elif snapshot.phase in (GamePhase.GAME_OVER, GamePhase.VICTORY):
            self._end_screen_handler.handle_key_event(event)
        elif snapshot.phase is GamePhase.PAUSED:
            self._pause_handler.handle_key(event.key)
        elif snapshot.phase is GamePhase.PLAYING:
            self._playing_handler.handle_key(event.key)


__all__ = [
    "InputHandler",
    "MenuInputHandler",
    "PauseInputHandler",
    "PlayingInputHandler",
    "EndScreenInputHandler",
]
