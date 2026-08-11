"""Functional tests for the game-over flow."""

from unittest.mock import patch

from src.application.contracts import GamePhase, InputAction
from src.application.game_session import GameSession
from src.application.collisions import lose_life
from src.domain import (
    GameConfig,
    LevelConfig,
    Maze,
)


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


def create_playing_session() -> GameSession:
    """Create a deterministic session already in PLAYING phase."""
    config = GameConfig(
        lives=1,
        levels=(
            LevelConfig(
                width=5,
                height=5,
                pacgum=1,
                level_max_time=90,
            ),
        ),
    )

    session = GameSession(
        config=config,
        maze_factory=FakeMazeFactory(),
    )

    with patch(
        "src.application.item_placement.place_items",
        return_value={},
    ):
        session.dispatch(InputAction.CONFIRM)

    return session


def test_game_over_when_player_loses_last_life() -> None:
    """Losing the final life should transition the session to GAME_OVER."""
    session = create_playing_session()

    assert session.phase is GamePhase.PLAYING
    assert session.player is not None
    assert session.player.lives == 1

    lose_life(session, "Caught by a ghost!")

    assert session.player.lives == 0
    assert session.phase is GamePhase.GAME_OVER
    assert session.message == (
        "Caught by a ghost! Final score: 0. Press Enter."
    )


def test_game_over_preserves_final_score() -> None:
    """Game Over should preserve the player's final score."""
    session = create_playing_session()

    session.score = 1234

    lose_life(session, "Caught by a ghost!")

    assert session.phase is GamePhase.GAME_OVER
    assert session.score == 1234
    assert session.message == (
        "Caught by a ghost! Final score: 1234. Press Enter."
    )


def test_game_over_can_return_to_main_menu() -> None:
    """Confirming from Game Over should return to the main menu."""
    session = create_playing_session()

    lose_life(session, "Caught by a ghost!")

    assert session.phase is GamePhase.GAME_OVER

    session.dispatch(InputAction.CONFIRM)

    assert session.phase is GamePhase.MAIN_MENU
    assert session.message == "Press Enter to start"
