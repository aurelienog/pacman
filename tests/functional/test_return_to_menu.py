"""Functional tests for returning to the main menu."""

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
    """Create a deterministic playing game session."""
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


def test_return_to_menu_from_playing() -> None:
    """Returning to the menu from PLAYING should change the phase."""
    session = create_session()

    assert session.phase is GamePhase.PLAYING

    session.dispatch(InputAction.RETURN_TO_MENU)

    assert session.phase is GamePhase.MAIN_MENU
    assert session.message == "Press Enter to start"


def test_return_to_menu_from_paused() -> None:
    """Returning to the menu from PAUSED should change the phase."""
    session = create_session()

    session.dispatch(InputAction.PAUSE)

    assert session.phase is GamePhase.PAUSED

    session.dispatch(InputAction.RETURN_TO_MENU)

    assert session.phase is GamePhase.MAIN_MENU
    assert session.message == "Press Enter to start"


def test_return_to_menu_preserves_score_and_level() -> None:
    """Returning to the menu should not reset score or level immediately."""
    session = create_session()

    session.score = 500
    session.level_index = 0

    session.dispatch(InputAction.RETURN_TO_MENU)

    assert session.phase is GamePhase.MAIN_MENU
    assert session.score == 500
    assert session.level_index == 0


def test_return_to_menu_from_main_menu_has_no_effect() -> None:
    """RETURN_TO_MENU from the main menu should leave it unchanged."""
    session = GameSession(
        config=GameConfig(),
        maze_factory=FakeMazeFactory(),
    )

    assert session.phase is GamePhase.MAIN_MENU

    session.dispatch(InputAction.RETURN_TO_MENU)

    assert session.phase is GamePhase.MAIN_MENU
    assert session.message == "Press Enter to start"
