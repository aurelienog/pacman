"""Path-finding algorithms used by the game."""

from __future__ import annotations

from collections import deque

from ..domain import Direction, Maze, Position


def nearest_walkable(
    maze: Maze,
    start: Position,
) -> Position:
    """Return the nearest traversable position.

    Starting from ``start``, perform a breadth-first search until a
    position with at least one accessible neighbour is found.

    Args:
        maze: Maze to search.
        start: Initial search position.

    Returns:
        The nearest traversable position.
    """
    queue: deque[Position] = deque([start])
    visited: set[Position] = {start}

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

    return start


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
    return abs(first.x - second.x) + abs(first.y - second.y)