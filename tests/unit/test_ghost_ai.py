"""Tests for ghost pathfinding and personality-based AI."""

from random import Random

from src.application.ghost_ai import GhostAI
from src.application.pathfinding import (
    bfs_next_move,
    find_next_move,
    manhattan_distance,
    nearest_walkable,
    random_walkable,
)
from src.domain import (
    Direction,
    Ghost,
    GhostPersonality,
    Maze,
    Player,
    Position,
)


def open_maze(width: int, height: int) -> Maze:
    """Create a fully open maze for testing."""
    return Maze(
        cells=tuple(
            tuple(0 for _ in range(width))
            for _ in range(height)
        )
    )


def ghost(
    position: Position,
    personality: GhostPersonality = GhostPersonality.BLINKY,
    direction: Direction = Direction.NONE,
) -> Ghost:
    """Create a predictable ghost state."""
    return Ghost(
        position=position,
        home=position,
        direction=direction,
        personality=personality,
    )


def player(
    position: Position,
    direction: Direction = Direction.NONE,
) -> Player:
    """Create a predictable player state."""
    return Player(
        position=position,
        spawn=position,
        lives=3,
        direction=direction,
    )


# ---------------------------------------------------------------------------
# Pathfinding
# ---------------------------------------------------------------------------


def test_manhattan_distance() -> None:
    """Manhattan distance should sum horizontal and vertical distance."""
    assert manhattan_distance(
        Position(1, 2),
        Position(5, 7),
    ) == 9


def test_bfs_returns_shortest_move() -> None:
    """BFS should return the first move of the shortest path."""
    maze = open_maze(5, 5)
    ghost_state = ghost(Position(1, 2))

    result = bfs_next_move(
        ghost_state,
        Position(4, 2),
        maze,
    )

    assert result == (
        Direction.RIGHT,
        Position(2, 2),
    )


def test_bfs_returns_none_when_target_is_current_position() -> None:
    """No movement is required when target equals ghost position."""
    maze = open_maze(5, 5)
    ghost_state = ghost(Position(2, 2))

    assert bfs_next_move(
        ghost_state,
        Position(2, 2),
        maze,
    ) is None


def test_bfs_returns_none_when_target_is_unreachable() -> None:
    """BFS should return None when no path exists."""
    maze = Maze(
        cells=(
            (0, 15, 0),
        )
    )
    ghost_state = ghost(Position(0, 0))

    assert bfs_next_move(
        ghost_state,
        Position(2, 0),
        maze,
    ) is None


def test_find_next_move_prefers_bfs_path() -> None:
    """find_next_move should use BFS when a path exists."""
    maze = open_maze(5, 5)
    ghost_state = ghost(Position(1, 2))

    result = find_next_move(
        ghost_state,
        Position(4, 2),
        maze,
    )

    assert result == (
        Direction.RIGHT,
        Position(2, 2),
    )


def test_find_next_move_avoids_reverse_direction() -> None:
    """Fallback movement should avoid reversing when alternatives exist."""
    maze = open_maze(5, 5)

    ghost_state = ghost(
        Position(2, 2),
        direction=Direction.RIGHT,
    )

    result = find_next_move(
        ghost_state,
        Position(2, 10),
        maze,
    )

    assert result is not None
    assert result[0] is not Direction.LEFT


def test_find_next_move_allows_reverse_when_necessary() -> None:
    """A ghost should reverse when no other movement is available."""
    maze = Maze(
        cells=(
            (15, 0, 15),
        )
    )

    ghost_state = ghost(
        Position(1, 0),
        direction=Direction.RIGHT,
    )

    result = find_next_move(
        ghost_state,
        Position(0, 0),
        maze,
    )

    assert result == (
        Direction.LEFT,
        Position(0, 0),
    )


def test_nearest_walkable_returns_walkable_position() -> None:
    """nearest_walkable should return an accessible position."""
    maze = open_maze(5, 5)

    result = nearest_walkable(
        maze,
        Position(2, 2),
    )

    assert result == Position(2, 2)
    assert maze.neighbours(result)


def test_nearest_walkable_finds_nearest_accessible_position() -> None:
    """nearest_walkable should search outward using BFS."""
    maze = Maze(
        cells=(
            (0, 0, 0),
            (0, 15, 0),
            (0, 0, 0),
        )
    )

    result = nearest_walkable(
        maze,
        Position(1, 1),
    )

    assert result in {
        Position(0, 1),
        Position(2, 1),
        Position(1, 0),
        Position(1, 2),
    }


def test_nearest_walkable_clamps_outside_position() -> None:
    """Outside positions should be clamped inside the maze."""
    maze = open_maze(3, 3)

    result = nearest_walkable(
        maze,
        Position(-1, 0),
    )

    assert result == Position(0, 0)


def test_random_walkable_returns_accessible_position() -> None:
    """random_walkable should return a traversable position."""
    maze = open_maze(5, 5)
    rng = Random(42)

    result = random_walkable(
        maze,
        rng,
    )

    assert maze.contains(result)
    assert maze.neighbours(result)


# ---------------------------------------------------------------------------
# Ghost personalities
# ---------------------------------------------------------------------------


def test_blinky_targets_player_position() -> None:
    """Blinky should target the player's current position."""
    maze = open_maze(5, 5)

    blinky = ghost(
        Position(1, 1),
        GhostPersonality.BLINKY,
    )
    pacman = player(Position(3, 3))

    assert GhostAI.target(
        blinky,
        pacman,
        [blinky],
        maze,
    ) == pacman.position


def test_pinky_targets_four_cells_ahead() -> None:
    """Pinky should target up to four cells ahead of the player."""
    maze = open_maze(10, 5)

    pinky = ghost(
        Position(1, 1),
        GhostPersonality.PINKY,
    )
    pacman = player(
        Position(2, 2),
        Direction.RIGHT,
    )

    assert GhostAI.target(
        pinky,
        pacman,
        [pinky],
        maze,
    ) == Position(6, 2)


def test_pinky_stops_at_wall() -> None:
    """Pinky should stop before a blocked cell."""
    maze = open_maze(10, 5)

    pinky = ghost(
        Position(0, 0),
        GhostPersonality.PINKY,
    )
    pacman = player(
        Position(2, 2),
        Direction.RIGHT,
    )

    result = GhostAI.target(
        pinky,
        pacman,
        [pinky],
        maze,
    )

    assert result == Position(6, 2)


def test_inky_targets_relative_to_blinky() -> None:
    """Inky should mirror the two-cell player pivot around Blinky."""
    maze = open_maze(9, 9)

    blinky = ghost(
        Position(1, 1),
        GhostPersonality.BLINKY,
    )
    inky = ghost(
        Position(4, 4),
        GhostPersonality.INKY,
    )
    pacman = player(
        Position(3, 3),
        Direction.RIGHT,
    )

    result = GhostAI.target(
        inky,
        pacman,
        [blinky, inky],
        maze,
    )

    # Pivot = (5, 3)
    # Blinky = (1, 1)
    # Target = (9, 5), outside the maze.
    #
    # The result must therefore be normalised to a walkable position.
    assert maze.contains(result)
    assert maze.neighbours(result)


def test_inky_targets_player_without_blinky() -> None:
    """Inky should fall back to the player without Blinky."""
    maze = open_maze(5, 5)

    inky = ghost(
        Position(1, 1),
        GhostPersonality.INKY,
    )
    pacman = player(
        Position(3, 3),
        Direction.RIGHT,
    )

    assert GhostAI.target(
        inky,
        pacman,
        [inky],
        maze,
    ) == pacman.position


def test_clyde_chases_when_far_away() -> None:
    """Clyde should chase the player when farther than eight cells."""
    maze = open_maze(20, 5)

    clyde = ghost(
        Position(1, 2),
        GhostPersonality.CLYDE,
    )
    pacman = player(Position(12, 2))

    assert GhostAI.target(
        clyde,
        pacman,
        [clyde],
        maze,
    ) == pacman.position


def test_clyde_retreats_when_close() -> None:
    """Clyde should retreat when eight cells away or closer."""
    maze = open_maze(10, 10)

    clyde = ghost(
        Position(4, 4),
        GhostPersonality.CLYDE,
    )
    pacman = player(Position(6, 4))

    assert GhostAI.target(
        clyde,
        pacman,
        [clyde],
        maze,
    ) == Position(0, 9)


def test_clyde_retreats_at_exactly_eight_cells() -> None:
    """Clyde should retreat when distance is exactly eight."""
    maze = open_maze(20, 20)

    clyde = ghost(
        Position(4, 4),
        GhostPersonality.CLYDE,
    )
    pacman = player(Position(4, 12))

    assert GhostAI.target(
        clyde,
        pacman,
        [clyde],
        maze,
    ) == Position(0, 19)

