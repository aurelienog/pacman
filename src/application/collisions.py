"""Collision handling for the Pac-Man game."""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_session import GameSession

from .contracts import GamePhase
from ..domain import Direction, GhostMode


def handle_collisions(session: "GameSession") -> None:
    """Resolve collisions between the player and ghosts.

    Args:
        session: Active game session.

    Returns:
        None.
    """
    assert session.player is not None

    for ghost in session.ghosts:

        if (
            ghost.position != session.player.position
            or ghost.mode is GhostMode.RESPAWNING
        ):
            continue

        if ghost.mode is GhostMode.FRIGHTENED:
            session.score += session._config.points_per_ghost

            ghost.prev_position = ghost.position
            ghost.mode = GhostMode.RESPAWNING
            ghost.respawn_remaining = session.GHOST_RESPAWN_SECONDS

        elif not session.invincible:
            lose_life(session, "Caught by a ghost!")

        return


def lose_life(session: "GameSession", message: str) -> None:
    """Remove one player life and update the game state.

    Args:
        session: Active game session.
        message: Message shown to the player.

    Returns:
        None.
    """
    assert session.player is not None

    session.player.lives -= 1

    if session.player.lives <= 0:
        session.phase = GamePhase.GAME_OVER
        session.message = (
            f"{message} Final score: {session.score}. Press Enter."
        )
        return

    session.player.position = session.player.spawn
    session.player.prev_position = session.player.spawn
    session.player.direction = Direction.NONE

    for ghost in session.ghosts:
        ghost.position = ghost.home
        ghost.prev_position = ghost.home
        ghost.direction = Direction.NONE
        ghost.mode = GhostMode.CHASE

    session.message = message
