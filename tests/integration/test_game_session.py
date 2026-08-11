"""Integration tests for GameSession."""

from unittest.mock import Mock

from src.application.contracts import GamePhase, InputAction
from src.application.game_session import GameSession
from src.domain import (
    Direction,
    GameConfig,
    Ghost,
    GhostMode,
    GhostPersonality,
    LevelConfig,
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


def make_factory(width: int = 10, height: int = 10) -> Mock:
    """Create a deterministic maze factory."""
    factory = Mock()
    factory.generate.return_value = open_maze(width, height)
    return factory


def make_session() -> GameSession:
    """Create a deterministic playing session."""
    factory = make_factory()

    config = GameConfig(
        lives=3,
        levels=(
            LevelConfig(
                width=10,
                height=10,
                pacgum=10,
                seed=42,
                level_max_time=90,
            ),
        ),
    )

    session = GameSession(config, factory)

    session.maze = open_maze(10, 10)

    session.player = Player(
        position=Position(1, 1),
        spawn=Position(1, 1),
        lives=3,
        direction=Direction.RIGHT,
        requested_direction=Direction.RIGHT,
    )

    session.ghosts = [
        Ghost(
            position=Position(5, 5),
            home=Position(5, 5),
            direction=Direction.LEFT,
            personality=GhostPersonality.BLINKY,
        )
    ]

    session.phase = GamePhase.PLAYING
    session.seconds_remaining = 90.0

    return session


# ---------------------------------------------------------------------------
# Session creation
# ---------------------------------------------------------------------------


def test_game_session_starts_in_main_menu() -> None:
    """A new session should start in the main menu."""
    session = GameSession(
        GameConfig(),
        make_factory(),
    )

    assert session.phase is GamePhase.MAIN_MENU
    assert session.message == "Press Enter to start"
    assert session.score == 0
    assert session.level_index == 0
    assert session.maze is None
    assert session.player is None
    assert session.ghosts == []
    assert session.items == {}


def test_game_session_initializes_game_flags() -> None:
    """A new session should initialize gameplay flags disabled."""
    session = GameSession(
        GameConfig(),
        make_factory(),
    )

    assert session.invincible is False
    assert session.freeze_ghosts is False
    assert session.freeze_timer is False
    assert session.speed_boost is False


# ---------------------------------------------------------------------------
# New game / level loading
# ---------------------------------------------------------------------------


def test_confirm_starts_new_game() -> None:
    """CONFIRM from the main menu should start a new game."""
    factory = make_factory()

    config = GameConfig(
        lives=3,
        levels=(
            LevelConfig(
                width=10,
                height=10,
                pacgum=10,
                seed=123,
                level_max_time=90,
            ),
        ),
    )

    session = GameSession(config, factory)

    session.dispatch(InputAction.CONFIRM)

    assert session.phase is GamePhase.PLAYING
    assert session.message == ""
    assert session.score == 0
    assert session.level_index == 0
    assert session.maze is not None
    assert session.player is not None
    assert len(session.ghosts) == 4
    assert session.seconds_remaining == 90.0

    factory.generate.assert_called_once_with(
        10,
        10,
        123,
    )


def test_confirm_resets_score_and_level_index() -> None:
    """Starting a new game should reset score and level index."""
    factory = make_factory()

    config = GameConfig(
        levels=(
            LevelConfig(
                width=10,
                height=10,
                seed=42,
            ),
        ),
    )

    session = GameSession(config, factory)

    session.score = 999
    session.level_index = 5

    session.dispatch(InputAction.CONFIRM)

    assert session.score == 0
    assert session.level_index == 0


def test_start_new_game_resets_cheat_flags() -> None:
    """Starting a new game should disable all gameplay cheats."""
    session = make_session()

    session.invincible = True
    session.freeze_ghosts = True
    session.freeze_timer = True
    session.speed_boost = True

    session.phase = GamePhase.MAIN_MENU

    session.dispatch(InputAction.CONFIRM)

    assert session.invincible is False
    assert session.freeze_ghosts is False
    assert session.freeze_timer is False
    assert session.speed_boost is False


def test_new_level_creates_four_ghosts() -> None:
    """Loading a level should create one ghost for each personality."""
    factory = make_factory()

    config = GameConfig(
        levels=(
            LevelConfig(
                width=10,
                height=10,
                seed=42,
            ),
        ),
    )

    session = GameSession(config, factory)

    session.dispatch(InputAction.CONFIRM)

    personalities = {
        ghost.personality
        for ghost in session.ghosts
    }

    assert len(session.ghosts) == 4

    assert personalities == {
        GhostPersonality.BLINKY,
        GhostPersonality.INKY,
        GhostPersonality.CLYDE,
        GhostPersonality.PINKY,
    }


def test_new_level_initializes_ghosts_at_home() -> None:
    """Each ghost should initially be placed at its home position."""
    session = make_session()
    session.phase = GamePhase.MAIN_MENU

    session.dispatch(InputAction.CONFIRM)

    for ghost in session.ghosts:
        assert ghost.position == ghost.home
        assert ghost.prev_position == ghost.home
        assert ghost.mode is GhostMode.CHASE


def test_new_level_initializes_player() -> None:
    """A new level should initialize the player with configured lives."""
    factory = make_factory()

    config = GameConfig(
        lives=5,
        levels=(
            LevelConfig(
                width=10,
                height=10,
                seed=42,
            ),
        ),
    )

    session = GameSession(config, factory)

    session.dispatch(InputAction.CONFIRM)

    assert session.player is not None
    assert session.player.lives == 5
    assert session.player.position == session.player.spawn
    assert session.player.prev_position == session.player.spawn


def test_new_level_initializes_timer() -> None:
    """A new level should initialize its configured timer."""
    factory = make_factory()

    config = GameConfig(
        levels=(
            LevelConfig(
                width=10,
                height=10,
                seed=42,
                level_max_time=120,
            ),
        ),
    )

    session = GameSession(config, factory)

    session.dispatch(InputAction.CONFIRM)

    assert session.seconds_remaining == 120.0


def test_first_level_without_seed_uses_deterministic_seed() -> None:
    """The first level without a seed should use seed 42."""
    factory = make_factory()

    config = GameConfig(
        levels=(
            LevelConfig(
                width=10,
                height=10,
                seed=None,
            ),
        ),
    )

    session = GameSession(config, factory)

    session.dispatch(InputAction.CONFIRM)

    factory.generate.assert_called_once_with(
        10,
        10,
        42,
    )


# ---------------------------------------------------------------------------
# Input integration
# ---------------------------------------------------------------------------


def test_dispatch_quit_changes_phase_to_exit() -> None:
    """QUIT should move the session to the EXIT phase."""
    session = make_session()

    session.dispatch(InputAction.QUIT)

    assert session.phase is GamePhase.EXIT


def test_dispatch_direction_updates_player_request() -> None:
    """A direction action should update the requested player direction."""
    session = make_session()

    session.dispatch(InputAction.RIGHT)

    assert session.player is not None
    assert session.player.requested_direction is Direction.RIGHT


def test_dispatch_pause_changes_phase_to_paused() -> None:
    """PAUSE should move a playing session to PAUSED."""
    session = make_session()

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PAUSED


def test_dispatch_pause_resumes_game() -> None:
    """PAUSE while paused should resume the game."""
    session = make_session()
    session.phase = GamePhase.PAUSED

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PLAYING


def test_dispatch_return_to_menu_changes_phase() -> None:
    """RETURN_TO_MENU should return the session to the main menu."""
    session = make_session()

    session.dispatch(InputAction.RETURN_TO_MENU)

    assert session.phase is GamePhase.MAIN_MENU
    assert session.message == "Press Enter to start"


def test_dispatch_invincible_toggles_flag() -> None:
    """TOGGLE_INVINCIBLE should toggle invincibility."""
    session = make_session()

    session.dispatch(InputAction.TOGGLE_INVINCIBLE)
    assert session.invincible is True

    session.dispatch(InputAction.TOGGLE_INVINCIBLE)
    assert session.invincible is False


def test_dispatch_freeze_toggles_ghosts() -> None:
    """TOGGLE_FREEZE should toggle ghost freezing."""
    session = make_session()

    session.dispatch(InputAction.TOGGLE_FREEZE)
    assert session.freeze_ghosts is True

    session.dispatch(InputAction.TOGGLE_FREEZE)
    assert session.freeze_ghosts is False


def test_dispatch_timer_toggle() -> None:
    """TOGGLE_TIMER should toggle the level timer."""
    session = make_session()

    session.dispatch(InputAction.TOGGLE_TIMER)
    assert session.freeze_timer is True

    session.dispatch(InputAction.TOGGLE_TIMER)
    assert session.freeze_timer is False


def test_dispatch_speed_toggle() -> None:
    """TOGGLE_SPEED should toggle the player speed boost."""
    session = make_session()

    session.dispatch(InputAction.TOGGLE_SPEED)
    assert session.speed_boost is True

    session.dispatch(InputAction.TOGGLE_SPEED)
    assert session.speed_boost is False


def test_dispatch_add_life_increases_player_lives() -> None:
    """ADD_LIFE should increase the player's lives."""
    session = make_session()

    assert session.player is not None
    assert session.player.lives == 3

    session.dispatch(InputAction.ADD_LIFE)

    assert session.player.lives == 4


# ---------------------------------------------------------------------------
# Update integration
# ---------------------------------------------------------------------------


def test_update_does_nothing_when_not_playing() -> None:
    """Updating a non-playing session should not change game state."""
    session = make_session()
    session.phase = GamePhase.MAIN_MENU

    session.update(0.1)

    assert session.seconds_remaining == 90.0
    assert session.player is not None
    assert session.player.position == Position(1, 1)


def test_update_caps_large_delta() -> None:
    """Update should cap delta_seconds at MAX_DELTA_SECONDS."""
    session = make_session()

    session.update(10.0)

    assert session.seconds_remaining == 89.9


def test_update_ignores_negative_delta() -> None:
    """Negative delta time should not move the simulation backwards."""
    session = make_session()

    session.update(-1.0)

    assert session.seconds_remaining == 90.0


def test_update_decreases_level_timer() -> None:
    """A normal update should decrease the remaining level time."""
    session = make_session()

    session.update(0.1)

    assert session.seconds_remaining == 89.9


def test_update_moves_player_after_player_interval() -> None:
    """The player should move after enough elapsed simulation time."""
    session = make_session()

    session.update(0.1)
    session.update(0.1)
    session.update(0.1)

    assert session.player is not None
    assert session.player.position == Position(2, 1)


def test_update_moves_ghost_after_ghost_interval() -> None:
    """An active ghost should move after its movement interval."""
    session = make_session()

    initial_position = session.ghosts[0].position

    for _ in range(4):
        session.update(0.1)

    assert session.ghosts[0].position != initial_position


# ---------------------------------------------------------------------------
# Gameplay flags
# ---------------------------------------------------------------------------


def test_freeze_timer_prevents_timer_decrease() -> None:
    """freeze_timer should prevent the level timer from decreasing."""
    session = make_session()
    session.freeze_timer = True

    session.update(0.1)

    assert session.seconds_remaining == 90.0


def test_freeze_ghosts_prevents_ghost_movement() -> None:
    """freeze_ghosts should prevent active ghosts from moving."""
    session = make_session()
    session.freeze_ghosts = True

    initial_position = session.ghosts[0].position

    for _ in range(4):
        session.update(0.1)

    assert session.ghosts[0].position == initial_position


def test_speed_boost_reduces_player_step_interval() -> None:
    """Speed boost should allow the player to move sooner."""
    session = make_session()
    session.speed_boost = True

    session.update(0.1)
    session.update(0.1)

    assert session.player is not None
    assert session.player.position == Position(2, 1)


# ---------------------------------------------------------------------------
# Ghost state integration
# ---------------------------------------------------------------------------


def test_frightened_ghost_returns_to_chase_after_timer_expires() -> None:
    """A frightened ghost should return to CHASE."""
    session = make_session()

    ghost = session.ghosts[0]
    ghost.mode = GhostMode.FRIGHTENED
    session._frightened_remaining = 0.05

    session.update(0.1)

    assert ghost.mode is GhostMode.CHASE


def test_respawning_ghost_returns_home_after_timer_expires() -> None:
    """A respawning ghost should return home after its timer expires."""
    session = make_session()

    ghost = session.ghosts[0]
    ghost.position = Position(7, 7)
    ghost.prev_position = Position(7, 7)
    ghost.mode = GhostMode.RESPAWNING
    ghost.respawn_remaining = 0.05

    session.update(0.1)

    assert ghost.position == ghost.home
    assert ghost.prev_position == ghost.home
    assert ghost.mode is GhostMode.CHASE


def test_respawning_ghost_does_not_return_home_before_timer_expires() -> None:
    """A respawning ghost should remain away from home until ready."""
    session = make_session()

    ghost = session.ghosts[0]
    ghost.position = Position(7, 7)
    ghost.prev_position = Position(7, 7)
    ghost.mode = GhostMode.RESPAWNING
    ghost.respawn_remaining = 1.0

    session.update(0.1)

    assert ghost.position == Position(7, 7)
    assert ghost.mode is GhostMode.RESPAWNING


# ---------------------------------------------------------------------------
# Snapshot integration
# ---------------------------------------------------------------------------


def test_snapshot_returns_current_game_state() -> None:
    """snapshot should return the current game representation."""
    session = make_session()

    snapshot = session.snapshot()

    assert snapshot.phase is session.phase
    assert snapshot.score == session.score


def test_snapshot_reflects_score_changes() -> None:
    """snapshot should reflect the current score."""
    session = make_session()
    session.score = 500

    snapshot = session.snapshot()

    assert snapshot.score == 500

