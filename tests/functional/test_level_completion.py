"""Functional tests for level completion."""

from src.application.contracts import GamePhase
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
        """Return a simple fully walkable maze."""
        return Maze(
            cells=tuple(
                tuple(0 for _ in range(width))
                for _ in range(height)
            )
        )


def create_session(levels: tuple[LevelConfig, ...]) -> GameSession:
    """Create a real game session with a deterministic maze factory."""
    return GameSession(
        config=GameConfig(levels=levels),
        maze_factory=FakeMazeFactory(),
    )


def start_session(session: GameSession) -> None:
    """Put the session into the PLAYING phase."""
    from src.application.contracts import InputAction

    session.dispatch(InputAction.CONFIRM)

    assert session.phase is GamePhase.PLAYING
    assert session.player is not None
    assert session.maze is not None


def test_complete_level_loads_next_level() -> None:
    """Completing a level should advance to the next configured level."""
    levels = (
        LevelConfig(
            width=5,
            height=5,
            pacgum=1,
            level_max_time=90,
        ),
        LevelConfig(
            width=7,
            height=7,
            pacgum=1,
            level_max_time=120,
        ),
    )

    session = create_session(levels)
    start_session(session)

    assert session.level_index == 0
    assert session.player is not None
    assert session.player.lives == session._config.lives

    session.score = 500

    # Complete the current level through the application service.
    from src.application.level_loader import complete_level

    complete_level(session)

    assert session.phase is GamePhase.PLAYING
    assert session.level_index == 1
    assert session.score == 500

    assert session.player is not None
    assert session.player.lives == session._config.lives

    assert session.maze is not None
    assert session.maze.width == 7
    assert session.maze.height == 7

    assert session.seconds_remaining == 120.0
    assert session.message == ""


def test_complete_last_level_enters_victory() -> None:
    """Completing the final level should put the game into VICTORY."""
    levels = (
        LevelConfig(
            width=5,
            height=5,
            pacgum=1,
            level_max_time=90,
        ),
    )

    session = create_session(levels)
    start_session(session)

    session.score = 1000

    from src.application.level_loader import complete_level

    complete_level(session)

    assert session.phase is GamePhase.VICTORY
    assert session.level_index == 0
    assert session.score == 1000
    assert session.player is not None
    assert session.player.lives == session._config.lives

    assert session.message == (
        "You won! Final score: 1000. Press Enter."
    )


def test_victory_can_return_to_main_menu() -> None:
    """Confirming after victory should return to the main menu."""
    levels = (
        LevelConfig(
            width=5,
            height=5,
            pacgum=1,
            level_max_time=90,
        ),
    )

    session = create_session(levels)
    start_session(session)

    from src.application.level_loader import complete_level
    from src.application.contracts import InputAction

    complete_level(session)

    assert session.phase is GamePhase.VICTORY

    session.dispatch(InputAction.CONFIRM)

    assert session.phase is GamePhase.MAIN_MENU
    assert session.message == "Press Enter to start"
