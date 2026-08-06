"""Level creation and initialization."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_session import GameSession

from .item_placement import place_items
from .pathfinding import nearest_walkable
from ..domain import Ghost, Player, Position, GhostPersonality
from .contracts import GamePhase


def start_new_game(session: "GameSession") -> None:
    """Initialize a new game.

    Args:
        session: Active game session.

    Returns:
        None.
    """
    session.score = 0
    session.level_index = 0

    session.invincible = False
    session.freeze_ghosts = False
    session.freeze_timer = False
    session.speed_boost = False

    load_level(
        session=session,
        lives=session._config.lives,
    )


def load_level(session: "GameSession", lives: int) -> None:
    """Create and initialize the current level.

    Args:
        session: Active game session.
        lives: Number of lives carried into the level.

    Returns:
        None.
    """
    level = session._config.levels[session.level_index]

    if level.seed is not None:
        seed = level.seed
    elif session.level_index == 0:
        seed = 42
    else:
        seed = session._random.randrange(1, 2**31)

    session.maze = session._factory.generate(
        level.width,
        level.height,
        seed,
    )

    center = Position(
        session.maze.width // 2,
        session.maze.height // 2,
    )

    player_spawn = nearest_walkable(session.maze, center)

    corners = [
        Position(0, 0),
        Position(session.maze.width - 1, 0),
        Position(0, session.maze.height - 1),
        Position(session.maze.width - 1, session.maze.height - 1),
    ]

    ghost_homes = [
        nearest_walkable(session.maze, corner)
        for corner in corners
    ]

    session.player = Player(
        position=player_spawn,
        spawn=player_spawn,
        lives=lives,
        prev_position=player_spawn,
    )

    session.ghosts = _create_ghosts(ghost_homes)

    session.items = place_items(
        session=session,
        player_spawn=player_spawn,
        ghost_homes=ghost_homes,
    )
    # Reset timers
    session.seconds_remaining = float(level.level_max_time)
    session._player_elapsed = 0.0
    session._ghost_elapsed = 0.0
    session._frightened_remaining = 0.0

    # Enter gameplay
    session.phase = GamePhase.PLAYING
    session.message = ""


def complete_level(session: "GameSession") -> None:
    """Advance to the next level or finish the game.

    Args:
        session: Active game session.

    Returns:
        None.
    """
    assert session.player is not None

    if session.level_index + 1 >= len(session._config.levels):
        session.phase = GamePhase.VICTORY
        session.message = (
            f"You won! Final score: {session.score}. "
            "Press Enter."
        )
        return

    lives = session.player.lives
    session.level_index += 1

    load_level(
        session=session,
        lives=lives,
    )


def _create_ghosts(
    ghost_homes: list[Position],
) -> list[Ghost]:
    """Create the ghosts for a level."""

    personalities = (
        GhostPersonality.BLINKY,
        GhostPersonality.PINKY,
        GhostPersonality.INKY,
        GhostPersonality.CLYDE,
    )

    return [
        Ghost(
            position=home,
            home=home,
            prev_position=home,
            personality=personality,
        )
        for home, personality in zip(
            ghost_homes,
            personalities,
            strict=True,
        )
    ]
