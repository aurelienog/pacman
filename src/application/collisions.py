"""Collision handling for the Pac-Man game."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_session import GameSession

from .interpolation import (
    ghost_progress,
    player_progress,
)
from .contracts import GamePhase
from ..domain import (
    Direction,
    GhostMode,
    Position,
)

SWITCH_THRESHOLD = 0.2


def occupied_position(
    previous: Position,
    current: Position,
    progress: float,
) -> Position:
    """Return the cell currently occupied by an entity."""

    if progress < SWITCH_THRESHOLD:
        return previous

    return current


def handle_collisions(
    session: "GameSession",
) -> None:
    """Resolve collisions between the player and ghosts.

    Args:
        session: Active game session.

    Returns:
        None.
    """
    assert session.player is not None

    occupied_player = occupied_position(
        session.player.prev_position,
        session.player.position,
        player_progress(session),
    )

    for ghost in session.ghosts:

        if ghost.mode is GhostMode.RESPAWNING:
            continue

        # Favour the player when eating frightened ghosts.
        if (
            ghost.mode is GhostMode.FRIGHTENED
            and session.player.position == ghost.position
        ):
            session.score += session._config.points_per_ghost
            ghost.prev_position = ghost.position
            ghost.mode = GhostMode.RESPAWNING
            ghost.respawn_remaining = (
                session.GHOST_RESPAWN_SECONDS
            )
            continue

        occupied_ghost = occupied_position(
            ghost.prev_position,
            ghost.position,
            ghost_progress(session),
        )

        if occupied_ghost != occupied_player:
            continue

        if not session.invincible:
            lose_life(
                session,
                "Caught by a ghost!",
            )

        return


def lose_life(
    session: "GameSession",
    message: str,
) -> None:
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
            f"{message} Final score: "
            f"{session.score}. Press Enter."
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
