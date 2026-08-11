"""Functional tests for the game victory condition."""

from unittest.mock import Mock

from src.application.contracts import GamePhase
from src.application.game_session import GameSession
from src.application.level_loader import complete_level
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


def create_session() -> GameSession:
    """Create a session with a small deterministic configuration."""
    config = GameConfig(
        levels=(
            LevelConfig(
                width=5,
                height=5,
                pacgum=1,
                level_max_time=90,
            ),
        ),
    )

    return GameSession(
        config=config,
        maze_factory=FakeMazeFactory(),
    )


def test_completing_last_level_triggers_victory() -> None:
    """Completing the final configured level should end the game in victory."""
    session = create_session()

    session.phase = GamePhase.PLAYING
    session.score = 1234
    session.player = Mock()
    session.player.lives = session._config.lives

    complete_level(session)

    assert session.phase is GamePhase.VICTORY
    assert session.level_index == 0
    assert session.score == 1234


def test_victory_message_contains_final_score() -> None:
    """The victory message should contain the final score."""
    session = create_session()

    session.phase = GamePhase.PLAYING
    session.score = 2500
    session.player = Mock()
    session.player.lives = session._config.lives

    complete_level(session)

    assert session.phase is GamePhase.VICTORY
    assert session.message == (
        "You won! Final score: 2500. Press Enter."
    )


def test_victory_can_return_to_main_menu() -> None:
    """Confirming after victory should return the player to the main menu."""
    session = create_session()

    session.phase = GamePhase.PLAYING
    session.score = 500
    session.player = Mock()
    session.player.lives = session._config.lives

    complete_level(session)

    assert session.phase is GamePhase.VICTORY

    # Import locally to keep this test focused on the user flow.
    from src.application.contracts import InputAction

    session.dispatch(InputAction.CONFIRM)

    assert session.phase is GamePhase.MAIN_MENU
    assert session.message == "Press Enter to start"