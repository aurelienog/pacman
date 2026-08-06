"""Update routines for the game simulation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .collisions import lose_life
from .contracts import GamePhase
from .movement import move_ghosts, move_player
from ..domain import GhostMode

if TYPE_CHECKING:
    from .game_session import GameSession


def update_world(
    session: GameSession,
    delta_seconds: float,
) -> None:
    """Advance the game simulation.

    Args:
        session: Current game session.
        delta_seconds: Elapsed real time since the previous update.

    Returns:
        None.
    """
    if (
        session.phase is not GamePhase.PLAYING
        or session.maze is None
        or session.player is None
    ):
        return

    delta = min(
        max(delta_seconds, 0.0),
        session.MAX_DELTA_SECONDS,
    )

    _update_timer(session, delta)

    if session.phase is not GamePhase.PLAYING:
        return

    _update_ghost_states(session, delta)
    _update_player(session, delta)
    _update_ghosts(session, delta)


def _update_timer(
    session: GameSession,
    delta: float,
) -> None:
    """Update the remaining level time.

    Args:
        session: Current game session.
        delta: Elapsed simulation time.

    Returns:
        None.
    """
    if not session.freeze_timer:
        session.seconds_remaining -= delta

    if session.seconds_remaining <= 0:
        lose_life(session, "Time is up!")


def _update_ghost_states(
    session: GameSession,
    delta: float,
) -> None:
    """Update frightened and respawning ghost states.

    Args:
        session: Current game session.
        delta: Elapsed simulation time.

    Returns:
        None.
    """
    session._frightened_remaining = max(
        0.0,
        session._frightened_remaining - delta,
    )

    if session._frightened_remaining == 0:
        for ghost in session.ghosts:
            if ghost.mode is GhostMode.FRIGHTENED:
                ghost.mode = GhostMode.CHASE

    for ghost in session.ghosts:
        if ghost.mode is not GhostMode.RESPAWNING:
            continue

        ghost.respawn_remaining -= delta

        if ghost.respawn_remaining <= 0:
            ghost.position = ghost.home
            ghost.prev_position = ghost.home
            ghost.mode = GhostMode.CHASE


def _update_player(
    session: GameSession,
    delta: float,
) -> None:
    """Advance the player according to elapsed time.

    Args:
        session: Current game session.
        delta: Elapsed simulation time.

    Returns:
        None.
    """
    player_step = player_step_seconds(session)

    session._player_elapsed += delta

    while (
        session._player_elapsed >= player_step
        and session.phase is GamePhase.PLAYING
    ):
        session._player_elapsed -= player_step
        move_player(session)


def _update_ghosts(
    session: GameSession,
    delta
) -> None:
    """Advance all ghosts according to elapsed time.

    Args:
        session: Current game session.

    Returns:
        None.
    """
    session._ghost_elapsed += delta

    while (
        session._ghost_elapsed >= session.GHOST_STEP_SECONDS
        and session.phase is GamePhase.PLAYING
    ):
        session._ghost_elapsed -= session.GHOST_STEP_SECONDS

        if not session.freeze_ghosts:
            move_ghosts(session)


def player_step_seconds(
    session: GameSession,
) -> float:
    """Return the current player movement interval.

    Args:
        session: Current game session.

    Returns:
        Seconds between player movements.
    """
    if session.speed_boost:
        return session.BASE_PLAYER_STEP_SECONDS / 2

    return session.BASE_PLAYER_STEP_SECONDS
