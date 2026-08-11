"""Integration tests for the A-Maze-ing maze adapter."""

import pytest

from src.adapters import AmazingMazeFactory, MazeGenerationError
from src.domain import Maze


def test_amazing_maze_factory_generates_domain_maze() -> None:
    """The adapter should convert an external maze into a domain Maze."""
    factory = AmazingMazeFactory()

    maze = factory.generate(
        width=21,
        height=21,
        seed=42,
    )

    assert isinstance(maze, Maze)
    assert maze.width == 21
    assert maze.height == 21


def test_amazing_maze_factory_is_deterministic_for_same_seed() -> None:
    """The same dimensions and seed should generate the same maze."""
    factory = AmazingMazeFactory()

    first = factory.generate(
        width=21,
        height=21,
        seed=42,
    )
    second = factory.generate(
        width=21,
        height=21,
        seed=42,
    )

    assert first.cells == second.cells


def test_amazing_maze_factory_produces_valid_wall_encoding() -> None:
    """Generated cells should use the expected 0..15 wall encoding."""
    factory = AmazingMazeFactory()

    maze = factory.generate(
        width=21,
        height=21,
        seed=42,
    )

    assert all(
        isinstance(cell, int) and 0 <= cell <= 15
        for row in maze.cells
        for cell in row
    )


def test_amazing_maze_factory_generates_solvable_maze() -> None:
    """The adapter should only return a maze accepted as solvable."""
    factory = AmazingMazeFactory()

    maze = factory.generate(
        width=21,
        height=21,
        seed=42,
    )

    assert maze.width == 21
    assert maze.height == 21

    # A generated maze should contain walkable cells.
    assert any(
        cell != 15
        for row in maze.cells
        for cell in row
    )


def test_amazing_maze_factory_rejects_invalid_dimensions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Invalid external maze dimensions should raise MazeGenerationError."""

    class FakeGenerator:
        maze = ((0, 0),)
        shortest_path = [(0, 0)]

    monkeypatch.setattr(
        "src.adapters.amazing_maze_factory.MazeGenerator",
        lambda **_: FakeGenerator(),
    )

    factory = AmazingMazeFactory()

    with pytest.raises(MazeGenerationError, match="invalid maze size"):
        factory.generate(
            width=5,
            height=5,
            seed=42,
        )


def test_amazing_maze_factory_rejects_invalid_wall_data(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Invalid wall values from the external library should be rejected."""

    class FakeGenerator:
        maze = (
            (0, 16),
            (0, 0),
        )
        shortest_path = [(0, 0), (1, 0)]

    monkeypatch.setattr(
        "src.adapters.amazing_maze_factory.MazeGenerator",
        lambda **_: FakeGenerator(),
    )

    factory = AmazingMazeFactory()

    with pytest.raises(
        MazeGenerationError,
        match="invalid wall data",
    ):
        factory.generate(
            width=2,
            height=2,
            seed=42,
        )


def test_amazing_maze_factory_rejects_unsolvable_maze(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An external maze without a path should be rejected."""

    class FakeGenerator:
        maze = (
            (0, 0),
            (0, 0),
        )
        shortest_path = []

    monkeypatch.setattr(
        "src.adapters.amazing_maze_factory.MazeGenerator",
        lambda **_: FakeGenerator(),
    )

    factory = AmazingMazeFactory()

    with pytest.raises(
        MazeGenerationError,
        match="not solvable",
    ):
        factory.generate(
            width=2,
            height=2,
            seed=42,
        )


def test_amazing_maze_factory_wraps_generator_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Errors from A-Maze-ing should become MazeGenerationError."""

    def failing_generator(**_: object) -> None:
        raise RuntimeError("generator failure")

    monkeypatch.setattr(
        "src.adapters.amazing_maze_factory.MazeGenerator",
        failing_generator,
    )

    factory = AmazingMazeFactory()

    with pytest.raises(
        MazeGenerationError,
        match="A-Maze-ing failed to generate the maze",
    ):
        factory.generate(
            width=21,
            height=21,
            seed=42,
        )
