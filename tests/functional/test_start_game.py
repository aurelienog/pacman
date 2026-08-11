"""Functional tests for starting a new game session."""

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
        """Return a simple fully walkable maze."""
        return Maze(
            cells=tuple(
                tuple(0 for _ in range(width))
                for _ in range(height)
            )
        )


def test_start_game_from_main_menu() -> None:
    """Confirming from the main menu should start the first level."""
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

    assert session.phase is GamePhase.MAIN_MENU
    assert session.maze is None
    assert session.player is None
    assert session.score == 0
    assert session.level_index == 0

    session.dispatch(InputAction.CONFIRM)

    assert session.phase is GamePhase.PLAYING
    assert session.maze is not None
    assert session.player is not None

    assert session.level_index == 0
    assert session.score == 0

    assert session.player.lives == config.lives

    assert len(session.ghosts) == 4
    assert session.items

    assert session.seconds_remaining == 90.0
    assert session.message == ""
