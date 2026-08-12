"""Collision handling for the Pac-Man game."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .contracts import GamePhase
from .interpolation import (
    ghost_progress,
    player_progress,
)
from ..domain import (
    Direction,
    Ghost,
    GhostMode,
    Position,
)

if TYPE_CHECKING:
    from .game_session import GameSession


def intersects(
    x1: float,
    y1: float,
    width1: float,
    height1: float,
    x2: float,
    y2: float,
    width2: float,
    height2: float,
) -> bool:
    """Check whether two axis-aligned hitboxes overlap.

    Args:
        x1: Center x-coordinate of the first hitbox.
        y1: Center y-coordinate of the first hitbox.
        width1: Width of the first hitbox.
        height1: Height of the first hitbox.
        x2: Center x-coordinate of the second hitbox.
        y2: Center y-coordinate of the second hitbox.
        width2: Width of the second hitbox.
        height2: Height of the second hitbox.

    Returns:
        True if the hitboxes overlap, otherwise False.
    """
    half_width1 = width1 / 2
    half_height1 = height1 / 2
    half_width2 = width2 / 2
    half_height2 = height2 / 2

    return (
        abs(x1 - x2) < half_width1 + half_width2
        and abs(y1 - y2) < half_height1 + half_height2
    )


def interpolated_position(
    previous: Position,
    current: Position,
    progress: float,
) -> tuple[float, float]:
    """Calculate an entity's interpolated center position.

    Args:
        previous: Previous logical cell position.
        current: Current logical cell position.
        progress: Movement progress between 0.0 and 1.0.

    Returns:
        Interpolated x and y coordinates.
    """
    progress = min(1.0, max(0.0, progress))

    x = previous.x + (
        current.x - previous.x
    ) * progress

    y = previous.y + (
        current.y - previous.y
    ) * progress

    return x, y


def handle_collisions(
    session: "GameSession",
) -> None:
    """Resolve collisions between the player and ghosts.

    Collision detection uses the interpolated center position of each
    entity and its hitbox dimensions. This allows collisions to be
    detected while entities are moving between logical maze cells.

    Args:
        session: Active game session.

    Returns:
        None.
    """
    assert session.player is not None

    player_x, player_y = interpolated_position(
        session.player.prev_position,
        session.player.position,
        player_progress(session),
    )

    player_hitbox = session.player.hitbox

    for ghost in session.ghosts:
        if ghost.mode is GhostMode.RESPAWNING:
            continue

        ghost_x, ghost_y = interpolated_position(
            ghost.prev_position,
            ghost.position,
            ghost_progress(session),
        )

        ghost_hitbox = ghost.hitbox

        if not intersects(
            player_x,
            player_y,
            player_hitbox.width,
            player_hitbox.height,
            ghost_x,
            ghost_y,
            ghost_hitbox.width,
            ghost_hitbox.height,
        ):
            continue

        if ghost.mode is GhostMode.FRIGHTENED:
            _eat_ghost(session, ghost)
            continue

        if not session.invincible:
            lose_life(
                session,
                "Caught by a ghost!",
            )

        return


def _eat_ghost(
    session: "GameSession",
    ghost: Ghost,
) -> None:
    """Handle a collision where the player eats a frightened ghost.

    Args:
        session: Active game session.
        ghost: Frightened ghost that was collided with.

    Returns:
        None.
    """
    session.score += session._config.points_per_ghost

    ghost.prev_position = ghost.position
    ghost.direction = Direction.NONE
    ghost.mode = GhostMode.RESPAWNING
    ghost.respawn_remaining = (
        session.GHOST_RESPAWN_SECONDS
    )


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
