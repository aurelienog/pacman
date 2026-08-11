"""Input handler for active gameplay phase."""

from __future__ import annotations

from typing import Any

from src.application import GameSession, InputAction


class PlayingInputHandler:
    """Translate keyboard inputs during active gameplay
    into game session commands."""

    def __init__(self, session: GameSession, pygame: Any) -> None:
        """Initialize playing input handler.

        Args:
            session: Active game session that receives input actions.
            pygame: Pygame module instance.

        Returns:
            None.
        """
        self._session = session
        self._pygame = pygame

    def handle_key(self, key: int) -> None:
        """Dispatch gameplay direction commands, pause toggle, or cheats.

        Direction keys control the player. Escape and P toggle pause,
        while the configured cheat keys toggle gameplay cheats or
        perform level and life actions.

        Args:
            key: Pygame key constant.

        Returns:
            None.
        """
        actions = {
            self._pygame.K_UP: InputAction.UP,
            self._pygame.K_w: InputAction.UP,
            self._pygame.K_DOWN: InputAction.DOWN,
            self._pygame.K_s: InputAction.DOWN,
            self._pygame.K_LEFT: InputAction.LEFT,
            self._pygame.K_a: InputAction.LEFT,
            self._pygame.K_RIGHT: InputAction.RIGHT,
            self._pygame.K_d: InputAction.RIGHT,
            self._pygame.K_ESCAPE: InputAction.PAUSE,
            self._pygame.K_p: InputAction.PAUSE,
            self._pygame.K_i: InputAction.TOGGLE_INVINCIBLE,
            self._pygame.K_f: InputAction.TOGGLE_FREEZE,
            self._pygame.K_t: InputAction.TOGGLE_TIMER,
            self._pygame.K_b: InputAction.TOGGLE_SPEED,
            self._pygame.K_n: InputAction.SKIP_LEVEL,
            self._pygame.K_l: InputAction.ADD_LIFE,
        }
        action = actions.get(key)
        if action is not None:
            self._session.dispatch(action)
