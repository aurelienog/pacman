"""Generate the collectible items for a level."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_session import GameSession

from ..domain import Item, ItemKind, Position


def place_items(
    session: "GameSession",
    player_spawn: Position,
    ghost_homes: list[Position],
) -> dict[Position, Item]:
    """Create the collectibles for the current level.

    Pac-Gums are placed on random walkable cells. One Super Pac-Gum is
    placed at each ghost home.

    Args:
        session: Active game session.
        player_spawn: Player starting position.
        ghost_homes: Ghost starting positions.

    Returns:
        A mapping from maze positions to collectible items.
    """
    assert session.maze is not None

    candidates: list[Position] = []
    reserved_positions = {player_spawn, *ghost_homes}

    for y in range(session.maze.height):
        for x in range(session.maze.width):
            position = Position(x, y)

            if (
                position in reserved_positions
                or session.maze.is_42_art(position)
            ):
                continue

            candidates.append(position)

    session._random.shuffle(candidates)

    minimum = round(
        len(candidates) * session.MIN_PACGUM_RATIO
    )

    level = session._config.levels[session.level_index]
    count = max(level.pacgum, minimum)

    items = {
        position: Item(
            kind=ItemKind.PACGUM,
            points=session._config.points_per_pacgum,
        )
        for position in candidates[:count]
    }

    for home in ghost_homes:
        items[home] = Item(
            kind=ItemKind.SUPER_PACGUM,
            points=session._config.points_per_super_pacgum,
        )

    return items