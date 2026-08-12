"""Interpolation helpers for smooth entity movement."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_session import GameSession
    from ..domain import Position


def player_progress(session: "GameSession") -> float:
    """Return the player's interpolation progress.

    The progress represents how far the player has moved from its
    previous logical cell towards its current logical cell.

    Args:
        session: Active game session.

    Returns:
        A value between 0.0 and 1.0 representing movement progress.
    """
    step = (
        session.BASE_PLAYER_STEP_SECONDS / 2
        if session.speed_boost
        else session.BASE_PLAYER_STEP_SECONDS
    )

    return min(
        1.0,
        max(
            0.0,
            session._player_elapsed / step,
        ),
    )


def ghost_progress(session: "GameSession") -> float:
    """Return the ghosts' interpolation progress.

    Args:
        session: Active game session.

    Returns:
        A value between 0.0 and 1.0 representing movement progress.
    """
    if session.freeze_ghosts:
        return 1.0

    return min(
        1.0,
        max(
            0.0,
            session._ghost_elapsed / session.GHOST_STEP_SECONDS,
        ),
    )


def interpolate_position(
    previous: "Position",
    current: "Position",
    progress: float,
    tile_size: float,
) -> tuple[float, float]:
    """Calculate an interpolated pixel position between two cells.

    Args:
        previous: Previous logical grid position.
        current: Current logical grid position.
        progress: Movement progress between 0.0 and 1.0.
        tile_size: Size of one maze cell in pixels.

    Returns:
        The interpolated ``(x, y)`` pixel coordinates.
    """
    progress = min(1.0, max(0.0, progress))

    x = (
        previous.x
        + (current.x - previous.x) * progress
    ) * tile_size

    y = (
        previous.y
        + (current.y - previous.y) * progress
    ) * tile_size

    return x, y
