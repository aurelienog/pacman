"""Functional tests for pausing and resuming the game."""

from src.application.contracts import GamePhase, InputAction
from src.application.game_session import GameSession
from src.domain import GameConfig, LevelConfig, Maze


class FakeMazeFactory:
    """Deterministic maze factory for functional tests."""

    def generate(
        self,
        width: int,
        height: int,
        seed: int,
    ) -> Maze:
        """Return a fully walkable maze."""
        return Maze(
            cells=tuple(
                tuple(0 for _ in range(width))
                for _ in range(height)
            )
        )


def create_session() -> GameSession:
    """Create a deterministic playable game session."""
    config = GameConfig(
        levels=(
            LevelConfig(
                width=5,
                height=5,
                pacgum=1,
                level_max_time=90,
            ),
        )
    )

    session = GameSession(
        config=config,
        maze_factory=FakeMazeFactory(),
    )

    session.dispatch(InputAction.CONFIRM)

    return session


def test_player_can_pause_game() -> None:
    """Pausing a playing game should enter the PAUSED phase."""
    session = create_session()

    assert session.phase is GamePhase.PLAYING

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PAUSED


def test_paused_game_does_not_update() -> None:
    """The simulation should not advance while the game is paused."""
    session = create_session()

    assert session.phase is GamePhase.PLAYING
    assert session.player is not None

    initial_position = session.player.position
    initial_time = session.seconds_remaining

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PAUSED

    session.update(0.1)

    assert session.player.position == initial_position
    assert session.seconds_remaining == initial_time


def test_player_can_resume_paused_game() -> None:
    """Pressing pause again should resume a paused game."""
    session = create_session()

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PAUSED

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PLAYING


def test_pause_and_resume_preserve_game_state() -> None:
    """Pausing and resuming should not reset score, level or timer."""
    session = create_session()

    session.score = 150
    session.level_index = 0
    session.seconds_remaining = 75.0

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PAUSED
    assert session.score == 150
    assert session.level_index == 0
    assert session.seconds_remaining == 75.0

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PLAYING
    assert session.score == 150
    assert session.level_index == 0
    assert session.seconds_remaining == 75.0


def test_return_to_menu_from_paused_game() -> None:
    """A paused player should be able to return to the main menu."""
    session = create_session()

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PAUSED

    session.dispatch(InputAction.RETURN_TO_MENU)

    assert session.phase is GamePhase.MAIN_MENU
    assert session.message == "Press Enter to start"
