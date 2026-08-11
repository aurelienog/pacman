"""Input handler for the Pause Menu phase."""

from __future__ import annotations

from typing import Any

from src.application import GameSession, InputAction
from src.ui.menu_renderer import MenuRenderer
from .base_handler import BaseInputHandler


class PauseInputHandler(BaseInputHandler):
    """Process keyboard and mouse input in the pause menu."""

    def __init__(
        self,
        session: GameSession,
        pygame: Any,
        menu_renderer: MenuRenderer,
    ) -> None:
        """Initialize pause menu input handler.

        Args:
            session: Active game session used to dispatch pause actions.
            pygame: Pygame module instance.
            menu_renderer: Menu renderer providing pause menu hitboxes.

        Returns:
            None.
        """
        self._session = session
        self._pygame = pygame
        self._menu_renderer = menu_renderer
        self.pause_index = 0

    def handle_mouse_move(self, pos: tuple[int, int]) -> None:
        """Update the selected pause item based on mouse position.

        Args:
            pos: Mouse (x, y) coordinate tuple.

        Returns:
            None.
        """
        for index, rect in enumerate(self._menu_renderer.pause_menu_rects):
            if self.is_inside(pos, rect):
                self.pause_index = index
                break

    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        """Handle a left-click on a pause menu item.

        The selected action can resume the game, return to the main menu,
        or quit the application.

        Args:
            pos: Mouse (x, y) coordinate tuple.

        Returns:
            None.
        """
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
        """Process keyboard navigation and pause menu selection.

        Escape and P toggle the pause state. Arrow keys and WASD move
        the selection, while Enter and Space activate the selected item.

        Args:
            key: Pygame keyboard constant to process.

        Returns:
            None.
        """
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
