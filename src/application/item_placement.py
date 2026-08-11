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

    Pac-Gums are placed on random walkable cells. The player spawn
    is reserved, while each ghost home receives a Super Pac-Gum.
    Decorative ``42`` cells are never used.

    Args:
        session: Active game session.
        player_spawn: Player starting position.
        ghost_homes: Ghost starting positions.

    Returns:
        A mapping from maze positions to collectible items.
    """
    assert session.maze is not None

    maze = session.maze

    reserved_positions = {
        player_spawn,
        *ghost_homes,
    }

    candidates: list[Position] = []

    for y in range(maze.height):
        for x in range(maze.width):
            position = Position(x, y)

            if position in reserved_positions:
                continue

            if maze.is_42_art(position):
                continue

            if not maze.neighbours(position):
                continue

            candidates.append(position)

    session._random.shuffle(candidates)

    minimum = round(
        len(candidates) * session.MIN_PACGUM_RATIO
    )

    level = session._config.levels[session.level_index]

    count = min(
        max(level.pacgum, minimum),
        len(candidates),
    )

    items = {
        position: Item(
            kind=ItemKind.PACGUM,
            points=session._config.points_per_pacgum,
        )
        for position in candidates[:count]
    }

    for home in ghost_homes:
        if (
            maze.contains(home)
            and not maze.is_42_art(home)
        ):
            items[home] = Item(
                kind=ItemKind.SUPER_PACGUM,
                points=session._config.points_per_super_pacgum,
            )

    return items
