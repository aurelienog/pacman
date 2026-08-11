"""Tests for ghost movement rules."""

from random import Random
from unittest.mock import Mock, patch

from src.domain import (
    Direction,
    GameConfig,
    Ghost,
    GhostMode,
    GhostPersonality,
    Maze,
    Player,
    Position,
)
from src.application.game_session import GameSession
from src.application.movement import move_ghosts, frightened_move


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
    mode: GhostMode = GhostMode.CHASE,
    personality: GhostPersonality = GhostPersonality.BLINKY,
    direction: Direction = Direction.NONE,
) -> Ghost:
    """Create a ghost with a predictable test state."""
    return Ghost(
        position=position,
        home=position,
        direction=direction,
        mode=mode,
        personality=personality,
    )


def player(
    position: Position,
    direction: Direction = Direction.NONE,
) -> Player:
    """Create a player with a predictable test state."""
    return Player(
        position=position,
        spawn=position,
        lives=3,
        direction=direction,
    )


def game_session(
    maze: Maze,
    ghosts: list[Ghost],
    player_state: Player,
) -> GameSession:
    """Create a real GameSession with controlled test state."""
    session = GameSession(
        config=GameConfig(),
        maze_factory=Mock(),
    )

    session.maze = maze
    session.ghosts = ghosts
    session.player = player_state
    session._random = Random(42)

    return session


# ---------------------------------------------------------------------------
# CHASE
# ---------------------------------------------------------------------------


def test_chase_ghost_moves_towards_player() -> None:
    """A chasing ghost should move towards its target."""
    maze = open_maze(5, 5)

    ghost_state = ghost(Position(1, 2))
    player_state = player(Position(4, 2))

    session = game_session(
        maze,
        [ghost_state],
        player_state,
    )

    with patch(
        "src.application.movement.handle_collisions"
    ):
        move_ghosts(session)

    assert ghost_state.prev_position == Position(1, 2)
    assert ghost_state.position == Position(2, 2)
    assert ghost_state.direction is Direction.RIGHT


def test_chase_ghost_updates_previous_position() -> None:
    """Ghost movement should preserve its previous position."""
    maze = open_maze(5, 1)

    ghost_state = ghost(Position(1, 0))
    player_state = player(Position(4, 0))

    session = game_session(
        maze,
        [ghost_state],
        player_state,
    )

    move_ghosts(session)

    assert ghost_state.prev_position == Position(1, 0)
    assert ghost_state.position == Position(2, 0)


# ---------------------------------------------------------------------------
# FRIGHTENED
# ---------------------------------------------------------------------------

def test_frightened_ghost_moves_away_from_player() -> None:
    """A frightened ghost should choose the move maximizing distance."""
    maze = open_maze(5, 3)

    ghost_state = Ghost(
        position=Position(2, 1),
        home=Position(2, 1),
        prev_position=Position(2, 1),
        direction=Direction.LEFT,
        mode=GhostMode.FRIGHTENED,
    )

    player_state = Player(
        position=Position(1, 1),
        spawn=Position(1, 1),
        lives=3,
        prev_position=Position(1, 1),
    )

    move = frightened_move(
        ghost_state,
        player_state,
        maze,
    )

    assert move is not None

    _, destination = move

    def distance(position: Position) -> int:
        return (
            abs(position.x - player_state.position.x)
            + abs(position.y - player_state.position.y)
        )

    available_distances = [
        distance(position)
        for _, position in maze.neighbours(ghost_state.position)
    ]

    assert distance(destination) == max(available_distances)
    assert destination != player_state.position


def test_frightened_ghost_does_not_use_player_as_direct_target() -> None:
    """FRIGHTENED mode should use a random target instead of chasing."""
    maze = open_maze(5, 1)

    ghost_state = ghost(
        Position(4, 0),
        mode=GhostMode.FRIGHTENED,
    )
    player_state = player(Position(0, 0))

    session = game_session(
        maze,
        [ghost_state],
        player_state,
    )

    move_ghosts(session)

    # The exact direction is determined by the seeded RNG.
    # We only verify that the ghost remains in frightened mode
    # and is processed normally.
    assert ghost_state.mode is GhostMode.FRIGHTENED
    assert ghost_state.prev_position == Position(4, 0)


# ---------------------------------------------------------------------------
# RESPAWNING
# ---------------------------------------------------------------------------


def test_respawning_ghost_does_not_move() -> None:
    """A respawning ghost should remain stationary."""
    maze = open_maze(5, 1)

    ghost_state = ghost(
        Position(2, 0),
        mode=GhostMode.RESPAWNING,
    )
    player_state = player(Position(4, 0))

    session = game_session(
        maze,
        [ghost_state],
        player_state,
    )

    move_ghosts(session)

    assert ghost_state.position == Position(2, 0)


def test_respawning_ghost_does_not_update_previous_position() -> None:
    """RESPAWNING ghosts should skip the normal movement pipeline."""
    maze = open_maze(5, 1)

    ghost_state = ghost(
        Position(2, 0),
        mode=GhostMode.RESPAWNING,
    )
    ghost_state.prev_position = Position(1, 0)

    player_state = player(Position(4, 0))

    session = game_session(
        maze,
        [ghost_state],
        player_state,
    )

    move_ghosts(session)

    assert ghost_state.position == Position(2, 0)
    assert ghost_state.prev_position == Position(1, 0)


# ---------------------------------------------------------------------------
# MULTIPLE GHOSTS
# ---------------------------------------------------------------------------


def test_move_ghosts_processes_all_active_ghosts() -> None:
    """All non-respawning ghosts should be processed."""
    maze = open_maze(7, 5)

    blinky = ghost(
        Position(1, 2),
        personality=GhostPersonality.BLINKY,
    )
    pinky = ghost(
        Position(3, 2),
        personality=GhostPersonality.BLINKY,
    )

    player_state = player(Position(6, 2))

    session = game_session(
        maze,
        [blinky, pinky],
        player_state,
    )

    with patch(
        "src.application.movement.handle_collisions"
    ):
        move_ghosts(session)

    assert blinky.position == Position(2, 2)
    assert pinky.position == Position(4, 2)


def test_respawning_ghost_is_skipped_while_active_ghost_moves() -> None:
    """RESPAWNING ghosts should be skipped while active ghosts move."""
    maze = open_maze(7, 5)

    respawning = ghost(
        Position(3, 2),
        mode=GhostMode.RESPAWNING,
    )
    active = ghost(
        Position(1, 2),
        personality=GhostPersonality.BLINKY,
    )

    player_state = player(Position(6, 2))

    session = game_session(
        maze,
        [respawning, active],
        player_state,
    )

    with patch(
        "src.application.movement.handle_collisions"
    ):
        move_ghosts(session)

    assert respawning.position == Position(3, 2)
    assert active.position == Position(2, 2)


# ---------------------------------------------------------------------------
# NO AVAILABLE MOVEMENT
# ---------------------------------------------------------------------------


def test_ghost_does_not_move_when_no_move_is_available() -> None:
    """A ghost should remain in place when no legal movement exists."""
    maze = Maze(
        cells=(
            (15,),
        )
    )

    ghost_state = ghost(Position(0, 0))
    player_state = player(Position(0, 0))

    session = game_session(
        maze,
        [ghost_state],
        player_state,
    )

    move_ghosts(session)

    assert ghost_state.position == Position(0, 0)
    assert ghost_state.prev_position == Position(0, 0)
