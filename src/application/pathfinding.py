"""Path-finding algorithms used by the game."""

from __future__ import annotations

from collections import deque

from ..domain import Direction, Ghost, Maze, Position
import random


def nearest_walkable(
    maze: Maze,
    start: Position,
) -> Position:
    """Return the nearest traversable position.

    If ``start`` is outside the maze, it is first clamped to the
    nearest position inside the maze. A breadth-first search is then
    performed until a position with at least one accessible neighbour
    is found.

    Args:
        maze: Maze to search.
        start: Initial search position.

    Returns:
        The nearest traversable position.
    """
    if maze.width == 0 or maze.height == 0:
        return start

    clamped = Position(
        max(0, min(start.x, maze.width - 1)),
        max(0, min(start.y, maze.height - 1)),
    )

    queue: deque[Position] = deque([clamped])
    visited: set[Position] = {clamped}

    while queue:
        position = queue.popleft()

        if maze.neighbours(position):
            return position

        for direction in (
            Direction.UP,
            Direction.DOWN,
            Direction.LEFT,
            Direction.RIGHT,
        ):
            next_position = position.moved(direction)

            if (
                maze.contains(next_position)
                and next_position not in visited
            ):
                visited.add(next_position)
                queue.append(next_position)

    return clamped


def find_next_move(
    ghost: Ghost,
    target: Position,
    maze: Maze,
) -> tuple[Direction, Position] | None:
    """Return the first step of the shortest path to a target.

    Args:
        ghost: Ghost to move.
        target: Desired destination.
        maze: Current maze.

    Returns:
        Selected direction and destination, or ``None`` if no movement is
        possible.
    """
    move = bfs_next_move(
        ghost,
        target,
        maze,
    )

    if move is not None:
        return move

    choices = _available_moves(
        ghost,
        maze,
    )

    if not choices:
        return None

    return min(
        choices,
        key=lambda move: manhattan_distance(
            move[1],
            target,
        ),
    )


def bfs_next_move(
    ghost: Ghost,
    target: Position,
    maze: Maze,
) -> tuple[Direction, Position] | None:
    """Return the first movement along the shortest path.

    Breadth-first search is used to compute the shortest path between the
    ghost and its target.

    Args:
        ghost: Ghost to move.
        target: Destination.
        maze: Current maze.

    Returns:
        First direction and position of the shortest path, or ``None`` if
        no path exists.
    """
    start = ghost.position

    if start == target:
        return None

    queue: deque[Position] = deque([start])
    visited: set[Position] = {start}

    parents: dict[
        Position,
        tuple[Position, Direction],
    ] = {}

    while queue:
        current = queue.popleft()

        if current == target:
            break

        for direction, neighbour in maze.neighbours(current):
            if neighbour in visited:
                continue

            visited.add(neighbour)
            parents[neighbour] = (
                current,
                direction,
            )
            queue.append(neighbour)

    if target not in parents:
        return None

    current = target

    while parents[current][0] != start:
        current = parents[current][0]

    _, direction = parents[current]

    return (
        direction,
        current,
    )


def _available_moves(
    ghost: Ghost,
    maze: Maze,
) -> list[tuple[Direction, Position]]:
    """Return the legal movements for a ghost."""
    moves = maze.neighbours(ghost.position)

    non_reverse = [
        (direction, position)
        for direction, position in moves
        if direction is not ghost.direction.opposite
    ]

    return non_reverse or moves


def manhattan_distance(
    first: Position,
    second: Position,
) -> int:
    """Return the Manhattan distance between two positions.

    Args:
        first: First position.
        second: Second position.

    Returns:
        Manhattan distance between both positions.
    """
    return (
        abs(first.x - second.x)
        + abs(first.y - second.y)
    )


def random_walkable(
    maze: Maze,
    random_generator: random.Random,
) -> Position:
    """Return a random walkable position."""

    walkable = []

    for y in range(maze.height):
        for x in range(maze.width):
            position = Position(x, y)

            if maze.neighbours(position):
                walkable.append(position)

    return random_generator.choice(walkable)
