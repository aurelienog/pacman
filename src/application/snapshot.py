"""Create renderer-neutral snapshots of the current game state."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .contracts import RenderEntity, Snapshot
from ..domain import Ghost, GhostMode

if TYPE_CHECKING:
    from .game_session import GameSession


def build_snapshot(session: "GameSession") -> Snapshot:
    """Build an immutable snapshot of the current game state.

    Args:
        session: Active game session.

    Returns:
        A renderer-neutral snapshot.
    """
    return Snapshot(
        phase=session.phase,
        maze=session.maze,
        player=session.player,
        player_visual_pos=_player_visual_position(session),
        ghost_visual_positions=tuple(
            _ghost_visual_position(session, ghost)
            for ghost in session.ghosts
        ),
        items=tuple(session.items.items()),
        score=session.score,
        level=session.level_index + 1,
        level_count=len(session._config.levels),
        seconds_remaining=session.seconds_remaining,
        message=session.message,
        invincible=session.invincible,
        freeze_ghosts=session.freeze_ghosts,
        freeze_timer=session.freeze_timer,
        speed_boost=session.speed_boost,
    )


def _player_visual_position(
    session: "GameSession",
) -> tuple[float, float]:
    """Return the interpolated player position.

    Args:
        session: Active game session.

    Returns:
        Player coordinates for smooth rendering.
    """
    if session.player is None:
        return (0.0, 0.0)

    step = (
        session.BASE_PLAYER_STEP_SECONDS / 2
        if session.speed_boost
        else session.BASE_PLAYER_STEP_SECONDS
    )

    progress = min(
        1.0,
        max(
            0.0,
            session._player_elapsed / step,
        ),
    )

    return (
        session.player.prev_position.x
        + (
            session.player.position.x
            - session.player.prev_position.x
        )
        * progress,
        session.player.prev_position.y
        + (
            session.player.position.y
            - session.player.prev_position.y
        )
        * progress,
    )


def _ghost_visual_position(
    session: "GameSession",
    ghost: Ghost,
) -> RenderEntity:
    """Return the interpolated position of one ghost.

    Args:
        session: Active game session.
        ghost: Ghost to interpolate.

    Returns:
        Render information for one ghost.
    """
    if ghost.mode is GhostMode.RESPAWNING:
        progress = 1.0
    else:
        progress = (
            1.0
            if session.freeze_ghosts
            else min(
                1.0,
                max(
                    0.0,
                    session._ghost_elapsed
                    / session.GHOST_STEP_SECONDS,
                ),
            )
        )

    return RenderEntity(
        x=ghost.prev_position.x
        + (
            ghost.position.x
            - ghost.prev_position.x
        )
        * progress,
        y=ghost.prev_position.y
        + (
            ghost.position.y
            - ghost.prev_position.y
        )
        * progress,
        direction=ghost.direction,
        mode=ghost.mode,
    )
