"""Movement rules for players and ghosts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .collisions import handle_collisions
from .level_loader import complete_level
from .pathfinding import manhattan_distance
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

    # ------------------------------------------------------------------
    # Move player
    # ------------------------------------------------------------------

    session.player.prev_position = session.player.position

    if session.maze.can_move(
        session.player.position,
        session.player.requested_direction,
    ):
        session.player.direction = session.player.requested_direction

    if session.maze.can_move(
        session.player.position,
        session.player.direction,
    ):
        session.player.position = session.player.position.moved(
            session.player.direction,
        )

    # ------------------------------------------------------------------
    # Collect item
    # ------------------------------------------------------------------

    item = session.items.pop(session.player.position, None)

    if item is not None:
        session.score += item.points

        if item.kind is ItemKind.SUPER_PACGUM:
            session._frightened_remaining = session.FRIGHTENED_DURATION_SECONDS

            for ghost in session.ghosts:
                if ghost.mode is GhostMode.CHASE:
                    ghost.mode = GhostMode.FRIGHTENED

        if not session.items:
            complete_level(session)
            return

    # ------------------------------------------------------------------
    # Resolve collisions
    # ------------------------------------------------------------------

    handle_collisions(session)


def move_ghosts(session: GameSession) -> None:
    """Move all ghosts by one step.

    Args:
        session: Active game session.

    Returns:
        None.
    """
    assert session.maze is not None
    assert session.player is not None

    for ghost in session.ghosts:

        ghost.prev_position = ghost.position

        # --------------------------------------------------------------
        # Respawning ghosts
        # --------------------------------------------------------------

        if ghost.mode is GhostMode.RESPAWNING:
            ghost.respawn_remaining -= session.GHOST_STEP_SECONDS

            if ghost.respawn_remaining <= 0:
                ghost.position = ghost.home
                ghost.prev_position = ghost.home
                ghost.mode = GhostMode.CHASE

            continue

        # --------------------------------------------------------------
        # Choose target
        # --------------------------------------------------------------

        target = (
            ghost.home
            if ghost.mode is GhostMode.FRIGHTENED
            else session.player.position
        )

        # --------------------------------------------------------------
        # Choose movement
        # --------------------------------------------------------------

        moves = session.maze.neighbours(ghost.position)

        non_reverse = [
            (direction, position)
            for direction, position in moves
            if direction is not ghost.direction.opposite
        ]

        choices = non_reverse or moves

        if not choices:
            continue

        selector = (
            max
            if ghost.mode is GhostMode.FRIGHTENED
            else min
        )

        ghost.direction, ghost.position = selector(
            choices,
            key=lambda move: manhattan_distance(
                move[1],
                target,
            ),
        )

    # ------------------------------------------------------------------
    # Resolve collisions
    # ------------------------------------------------------------------

    handle_collisions(session)