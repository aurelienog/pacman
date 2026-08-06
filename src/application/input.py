"""Input handling for the game session."""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_session import GameSession

from .contracts import GamePhase, InputAction
from .level_loader import start_new_game, complete_level
from ..domain import Direction


DIRECTION_ACTIONS = {
    InputAction.UP: Direction.UP,
    InputAction.DOWN: Direction.DOWN,
    InputAction.LEFT: Direction.LEFT,
    InputAction.RIGHT: Direction.RIGHT,
}


MAIN_MENU_MESSAGE = "Press Enter to start"


def dispatch_action(session: "GameSession", action: InputAction) -> None:
    """Dispatch one input action to the appropriate state handler.

    Args:
        session: Active game session.
        action: Input command received from the user interface.

    Returns:
        None.
    """
    if action is InputAction.QUIT:
        session.phase = GamePhase.EXIT
        return

    if session.phase is GamePhase.MAIN_MENU:
        _handle_menu(session, action)
        return

    if session.phase is GamePhase.PLAYING:
        _handle_playing(session, action)
        return

    if session.phase is GamePhase.PAUSED:
        _handle_paused(session, action)
        return

    if session.phase in (GamePhase.GAME_OVER, GamePhase.VICTORY):
        _handle_finished(session, action)


def _handle_menu(session: "GameSession", action: InputAction) -> None:
    """Process input while the main menu is visible.

    Args:
        session: Active game session.
        action: Input command.

    Returns:
        None.
    """
    if action is InputAction.CONFIRM:
        start_new_game(session)


def _handle_playing(session: "GameSession", action: InputAction) -> None:
    """Process input while a game is in progress.

    Args:
        session: Active game session.
        action: Input command.

    Returns:
        None.
    """
    assert session.player is not None

    if action in DIRECTION_ACTIONS:
        session.player.requested_direction = DIRECTION_ACTIONS[action]
        return

    if action is InputAction.PAUSE:
        session.phase = GamePhase.PAUSED
        return

    if action is InputAction.RETURN_TO_MENU:
        session.phase = GamePhase.MAIN_MENU
        session.message = MAIN_MENU_MESSAGE
        return

    if action is InputAction.TOGGLE_INVINCIBLE:
        session.invincible = not session.invincible
        return

    if action is InputAction.TOGGLE_FREEZE:
        session.freeze_ghosts = not session.freeze_ghosts
        return

    if action is InputAction.TOGGLE_TIMER:
        session.freeze_timer = not session.freeze_timer
        return

    if action is InputAction.TOGGLE_SPEED:
        session.speed_boost = not session.speed_boost
        return

    if action is InputAction.SKIP_LEVEL:
        complete_level(session)
        return

    if action is InputAction.ADD_LIFE:
        session.player.lives += 1


def _handle_paused(session: "GameSession", action: InputAction) -> None:
    """Process input while the game is paused.

    Args:
        session: Active game session.
        action: Input command.

    Returns:
        None.
    """
    if action is InputAction.PAUSE:
        session.phase = GamePhase.PLAYING
        return

    if action is InputAction.RETURN_TO_MENU:
        session.phase = GamePhase.MAIN_MENU
        session.message = MAIN_MENU_MESSAGE


def _handle_finished(session: "GameSession", action: InputAction) -> None:
    """Process input after victory or game over.

    Args:
        session: Active game session.
        action: Input command.

    Returns:
        None.
    """
    if action is InputAction.CONFIRM:
        session.phase = GamePhase.MAIN_MENU
        session.message = MAIN_MENU_MESSAGE
