"""Input handler for the Main Menu phase."""

from __future__ import annotations

from typing import Any

from src.application import GameSession, InputAction
from src.ui.menu_renderer import MenuRenderer
from .base_handler import BaseInputHandler


class MenuInputHandler(BaseInputHandler):
    """Process key and mouse inputs while in the Main Menu."""

    def __init__(
        self,
        session: GameSession,
        pygame: Any,
        menu_renderer: MenuRenderer,
    ) -> None:
        """Initialize main menu input handler.

        Args:
            session: Active game session used to dispatch menu actions.
            pygame: Pygame module instance.
            menu_renderer: Menu renderer providing menu item hitboxes.

        Returns:
            None.
        """
        self._session = session
        self._pygame = pygame
        self._menu_renderer = menu_renderer
        self.menu_index = 0
        self.show_scores = False
        self.show_instructions = False

    def handle_mouse_move(self, pos: tuple[int, int]) -> None:
        """Update the selected menu item based on mouse position.

        Hovering over a menu item changes ``menu_index``. Selection is
        not changed while a scores or instructions screen is displayed.

        Args:
            pos: Mouse (x, y) coordinate tuple.

        Returns:
            None.
        """
        if self.show_scores or self.show_instructions:
            return
        for index, rect in enumerate(self._menu_renderer.main_menu_rects):
            if self.is_inside(pos, rect):
                self.menu_index = index
                break

    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        """Handle a left-click on a main menu item.

        Clicking a menu item starts the game, opens the scores or
        instructions screen, or quits the application. Clicking while
        a submenu is open closes that submenu.

        Args:
            pos: Mouse (x, y) coordinate tuple.

        Returns:
            None.
        """
        if self.show_scores or self.show_instructions:
            self.show_scores = self.show_instructions = False
            return
        for index, rect in enumerate(self._menu_renderer.main_menu_rects):
            if self.is_inside(pos, rect):
                self.menu_index = index
                if index == 0:
                    self._session.dispatch(InputAction.CONFIRM)
                elif index == 1:
                    self.show_scores = True
                elif index == 2:
                    self.show_instructions = True
                elif index == 3:
                    self._session.dispatch(InputAction.QUIT)
                break

    def handle_key(self, key: int) -> None:
        """Process keyboard navigation and selection in the main menu.

        Arrow keys and WASD move the selection. Enter and Space activate
        the selected item, while Escape closes an open submenu.

        Args:
            key: Pygame keyboard constant to process.

        Returns:
            None.
        """
        entries = 4
        if key in (self._pygame.K_UP, self._pygame.K_w):
            self.menu_index = (self.menu_index - 1) % entries
        elif key in (self._pygame.K_DOWN, self._pygame.K_s):
            self.menu_index = (self.menu_index + 1) % entries
        elif key == self._pygame.K_ESCAPE:
            self.show_scores = self.show_instructions = False
        elif key in (self._pygame.K_RETURN, self._pygame.K_SPACE):
            if self.show_scores or self.show_instructions:
                self.show_scores = self.show_instructions = False
            elif self.menu_index == 0:
                self._session.dispatch(InputAction.CONFIRM)
            elif self.menu_index == 1:
                self.show_scores = True
            elif self.menu_index == 2:
                self.show_instructions = True
            else:
                self._session.dispatch(InputAction.QUIT)
