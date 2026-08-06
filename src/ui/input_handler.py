"""User input translation and UI state navigation controller."""

from __future__ import annotations

from typing import Any

from src.scores import ScoreRegistry
from src.application import GamePhase, GameSession, InputAction
from src.ui.menu_renderer import MenuRenderer


class InputHandler:
    """Manage keyboard and mouse events, menu selection, and highscore entry state."""

    def __init__(
        self,
        session: GameSession,
        score_registry: ScoreRegistry,
        pygame: Any,
        menu_renderer: MenuRenderer,
    ) -> None:
        self._session = session
        self._score_registry = score_registry
        self._pygame = pygame
        self._menu_renderer = menu_renderer
        self.menu_index = 0
        self.show_scores = False
        self.show_instructions = False
        self.pause_index = 0
        self.name = ""
        self.saved = False

    def handle_event(self, event: Any) -> None:
        """Route pygame event to corresponding UI menu or game action."""
        if event.type == self._pygame.QUIT:
            self._session.dispatch(InputAction.QUIT)
            return

        # Mouse movement processing
        if event.type == self._pygame.MOUSEMOTION:
            self._handle_mouse_move(event.pos)
            return

        # Left mouse click handling
        if event.type == self._pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
            return

        if event.type != self._pygame.KEYDOWN:
            return

        snapshot = self._session.snapshot()
        if snapshot.phase is GamePhase.MAIN_MENU:
            self._handle_menu_key(event.key)
            return
        if snapshot.phase in (GamePhase.GAME_OVER, GamePhase.VICTORY):
            self._handle_end_key(event)
            return
        if snapshot.phase is GamePhase.PAUSED:
            self._handle_pause_key(event.key)
            return

        self._handle_playing_key(event.key)

    @staticmethod
    def _is_inside(pos: tuple[int, int], rect: Any) -> bool:
        """Pure math point-in-bounds check (100% MLX compatible, no rect.collidepoint)."""
        px, py = pos
        return rect.left <= px <= rect.right and rect.top <= py <= rect.bottom

    def _handle_mouse_move(self, pos: tuple[int, int]) -> None:
        snapshot = self._session.snapshot()
        if snapshot.phase is GamePhase.MAIN_MENU and not self.show_scores and not self.show_instructions:
            for index, rect in enumerate(self._menu_renderer.main_menu_rects):
                if self._is_inside(pos, rect):
                    self.menu_index = index
                    break
        elif snapshot.phase is GamePhase.PAUSED:
            for index, rect in enumerate(self._menu_renderer.pause_menu_rects):
                if self._is_inside(pos, rect):
                    self.pause_index = index
                    break

    def _handle_mouse_click(self, pos: tuple[int, int]) -> None:
        snapshot = self._session.snapshot()
        if snapshot.phase is GamePhase.MAIN_MENU:
            if self.show_scores or self.show_instructions:
                self.show_scores = self.show_instructions = False
                return
            for index, rect in enumerate(self._menu_renderer.main_menu_rects):
                if self._is_inside(pos, rect):
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
        elif snapshot.phase is GamePhase.PAUSED:
            for index, rect in enumerate(self._menu_renderer.pause_menu_rects):
                if self._is_inside(pos, rect):
                    self.pause_index = index
                    if index == 0:
                        self._session.dispatch(InputAction.PAUSE)
                    elif index == 1:
                        self._session.dispatch(InputAction.RETURN_TO_MENU)
                    elif index == 2:
                        self._session.dispatch(InputAction.QUIT)
                    break

    def _handle_menu_key(self, key: int) -> None:
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

    def _handle_pause_key(self, key: int) -> None:
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

    def _handle_playing_key(self, key: int) -> None:
        actions = {
            self._pygame.K_UP: InputAction.UP, self._pygame.K_w: InputAction.UP,
            self._pygame.K_DOWN: InputAction.DOWN, self._pygame.K_s: InputAction.DOWN,
            self._pygame.K_LEFT: InputAction.LEFT, self._pygame.K_a: InputAction.LEFT,
            self._pygame.K_RIGHT: InputAction.RIGHT, self._pygame.K_d: InputAction.RIGHT,
            self._pygame.K_ESCAPE: InputAction.PAUSE, self._pygame.K_p: InputAction.PAUSE,
            self._pygame.K_i: InputAction.TOGGLE_INVINCIBLE, self._pygame.K_f: InputAction.TOGGLE_FREEZE,
            self._pygame.K_t: InputAction.TOGGLE_TIMER, self._pygame.K_b: InputAction.TOGGLE_SPEED,
            self._pygame.K_n: InputAction.SKIP_LEVEL, self._pygame.K_l: InputAction.ADD_LIFE,
        }
        action = actions.get(key)
        if action is not None:
            self._session.dispatch(action)

    def _handle_end_key(self, event: Any) -> None:
        if event.key == self._pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif event.key == self._pygame.K_RETURN:
            if not self.saved and self.name.strip():
                try:
                    self._score_registry.add(self.name, self._session.snapshot().score)
                    self.saved = True
                except (ValueError, OSError):
                    return
            self.name = ""
            self.saved = False
            self._session.dispatch(InputAction.CONFIRM)
        elif event.unicode and (event.unicode.isalnum() or event.unicode == " "):
            if len(self.name) < 10:
                self.name += event.unicode
