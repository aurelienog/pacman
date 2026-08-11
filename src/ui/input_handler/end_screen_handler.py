"""Input handler for Game Over and Victory end screen name registration."""

from __future__ import annotations

from typing import Any

from src.application import GameSession, InputAction
from src.scores import ScoreRegistry


class EndScreenInputHandler:
    """Process alphanumeric name entry and highscore saving
    upon game completion."""

    def __init__(
        self,
        session: GameSession,
        score_registry: ScoreRegistry,
        pygame: Any,
    ) -> None:
        """Initialize the end screen input handler.

        Args:
            session: Active GameSession instance.
            score_registry: ScoreRegistry instance for highscores.
            pygame: Pygame module instance.

        Returns:
            None.
        """
        self._session = session
        self._score_registry = score_registry
        self._pygame = pygame
        self.name = ""
        self.saved = False

    def handle_key_event(self, event: Any) -> None:
        """Process name-entry and confirmation keyboard events.

        Backspace removes the last character. Enter saves a non-empty
        name and confirms the result screen. Alphanumeric characters and
        spaces are accepted while the name contains fewer than ten
        characters.

        Args:
            event: Pygame keyboard event to process.

        Returns:
            None.
        """
        if event.key == self._pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif event.key == self._pygame.K_RETURN:
            if not self.saved and self.name.strip():
                try:
                    self._score_registry.add(
                        self.name,
                        self._session.snapshot().score,
                    )
                    self.saved = True
                except (ValueError, OSError):
                    return
            self.name = ""
            self.saved = False
            self._session.dispatch(InputAction.CONFIRM)
        elif event.unicode and (
            event.unicode.isalnum() or event.unicode == " "
        ):
            if len(self.name) < 10:
                self.name += event.unicode
