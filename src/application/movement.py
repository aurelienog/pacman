"""Movement rules for players and ghosts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .collisions import handle_collisions
from .ghost_ai import GhostAI
from .level_loader import complete_level
from .pathfinding import find_next_move, random_walkable
from ..domain import GhostMode, ItemKind

if TYPE_CHECKING:
    from .game_session import GameSession


def move_player(session: GameSession) -> None:
    """Move the player by one cell.

    Args:
        session: Active game session.

    Returns:
        None.
    """
    assert session.maze is not None
    assert session.player is not None

    session.player.prev_position = session.player.position

    if session.maze.can_move(
        session.player.position,
        session.player.requested_direction,
    ):
        session.player.direction = (
            session.player.requested_direction
        )

    if session.maze.can_move(
        session.player.position,
        session.player.direction,
    ):
        session.player.position = (
            session.player.position.moved(
                session.player.direction,
            )
        )

    item = session.items.pop(
        session.player.position,
        None,
    )

    if item is not None:
        session.score += item.points

        if item.kind is ItemKind.SUPER_PACGUM:
            session._frightened_remaining = (
                session.FRIGHTENED_DURATION_SECONDS
            )

            for ghost in session.ghosts:
                if ghost.mode is GhostMode.CHASE:
                    ghost.mode = GhostMode.FRIGHTENED

        if not session.items:
            complete_level(session)
            return

    handle_collisions(session)


def move_ghosts(session: GameSession) -> None:
    """Move every ghost one simulation step.

    Args:
        session: Active game session.

    Returns:
        None.
    """
    assert session.maze is not None
    assert session.player is not None

    for ghost in session.ghosts:

        if ghost.mode is GhostMode.RESPAWNING:
            continue

        ghost.prev_position = ghost.position

        if ghost.mode is GhostMode.FRIGHTENED:
            random_target = random_walkable(
                session.maze,
                session._random,
            )

            next_move = find_next_move(
                ghost,
                random_target,
                session.maze,
            )
        else:
            target = GhostAI.target(
                ghost,
                session.player,
                session.ghosts,
                session.maze,
            )
            next_move = find_next_move(
                ghost,
                target,
                session.maze,
            )

        if next_move is None:
            continue

        ghost.direction, ghost.position = next_move

    handle_collisions(session)
