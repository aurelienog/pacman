"""Input handler for the Pause Menu phase."""

from __future__ import annotations

from typing import Any

from src.application import GameSession, InputAction
from src.ui.menu_renderer import MenuRenderer
from .base_handler import BaseInputHandler


class PauseInputHandler(BaseInputHandler):
    """Process key and mouse inputs while the game is paused."""

    def __init__(
        self,
        session: GameSession,
        pygame: Any,
        menu_renderer: MenuRenderer,
    ) -> None:
        self._session = session
        self._pygame = pygame
        self._menu_renderer = menu_renderer
        self.pause_index = 0

    def handle_mouse_move(self, pos: tuple[int, int]) -> None:
        """Update selected pause item index on mouse hover."""
        for index, rect in enumerate(self._menu_renderer.pause_menu_rects):
            if self.is_inside(pos, rect):
                self.pause_index = index
                break

    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        """Trigger selected action on mouse left-click."""
        for index, rect in enumerate(self._menu_renderer.pause_menu_rects):
            if self.is_inside(pos, rect):
                self.pause_index = index
                if index == 0:
                    self._session.dispatch(InputAction.PAUSE)
                elif index == 1:
                    self._session.dispatch(InputAction.RETURN_TO_MENU)
                elif index == 2:
                    self._session.dispatch(InputAction.QUIT)
                break

    def handle_key(self, key: int) -> None:
        """Process keyboard navigation for the pause overlay."""
        if key in (self._pygame.K_ESCAPE, self._pygame.K_p):
            self._session.dispatch(InputAction.PAUSE)
        elif key in (self._pygame.K_UP, self._pygame.K_w):
            self.pause_index = (self.pause_index - 1) % 3
        elif key in (self._pygame.K_DOWN, self._pygame.K_s):
            self.pause_index = (self.pause_index + 1) % 3
        elif key in (self._pygame.K_RETURN, self._pygame.K_SPACE):
            if self.pause_index == 0:
                self._session.dispatch(InputAction.PAUSE)
            elif self.pause_index == 1:
                self._session.dispatch(InputAction.RETURN_TO_MENU)
            else:
                self._session.dispatch(InputAction.QUIT)
