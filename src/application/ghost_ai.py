"""Ghost chase algorithms."""

from __future__ import annotations

from ..domain import (
    Ghost,
    GhostPersonality,
    Maze,
    Player,
    Position,
)

from .pathfinding import manhattan_distance, nearest_walkable


class GhostAI:
    """Compute chase targets for ghost personalities."""

    @staticmethod
    def target(
        ghost: Ghost,
        player: Player,
        ghosts: list[Ghost],
        maze: Maze,
    ) -> Position:
        """Return the current chase target for a ghost.

        Args:
            ghost: Ghost whose target will be computed.
            player: Current player state.
            ghosts: All ghosts in the current level.
            maze: Current maze.

        Returns:
            Target position selected by the ghost personality.
        """
        match ghost.personality:
            case GhostPersonality.BLINKY:
                return GhostAI._blinky_target(player)

            case GhostPersonality.PINKY:
                return GhostAI._pinky_target(
                    maze,
                    player,
                )

            case GhostPersonality.INKY:
                return GhostAI._inky_target(
                    maze,
                    player,
                    ghosts,
                )

            case GhostPersonality.CLYDE:
                return GhostAI._clyde_target(
                    maze,
                    ghost,
                    player,
                )

        return player.position

    @staticmethod
    def _blinky_target(
        player: Player,
    ) -> Position:
        """Return Blinky's chase target.

        Blinky always targets the player's current position.

        Args:
            player: Current player state.

        Returns:
            Player position.
        """
        return player.position

    @staticmethod
    def _pinky_target(
        maze: Maze,
        player: Player,
    ) -> Position:
        """Return Pinky's chase target.

        Pinky aims four tiles ahead of the player's current direction.

        Args:
            maze: Current maze.
            player: Current player state.

        Returns:
            Target position.
        """
        return GhostAI._advance(
            maze,
            player.position,
            player.direction,
            4,
        )

    @staticmethod
    def _inky_target(
        maze: Maze,
        player: Player,
        ghosts: list[Ghost],
    ) -> Position:
        """Return Inky's chase target.

        Inky projects a point two tiles in front of the player and mirrors
        it relative to Blinky's current position.

        Args:
            maze: Current maze.
            player: Current player state.
            ghosts: Active ghosts.

        Returns:
            Target position.
        """
        blinky = next(
            (
                ghost
                for ghost in ghosts
                if ghost.personality is GhostPersonality.BLINKY
            ),
            None,
        )

        if blinky is None:
            return player.position

        pivot = GhostAI._advance(
            maze,
            player.position,
            player.direction,
            2,
        )

        dx = pivot.x - blinky.position.x
        dy = pivot.y - blinky.position.y

        target = Position(
            pivot.x + dx,
            pivot.y + dy,
        )

        if (
            not maze.contains(target)
            or not maze.neighbours(target)
        ):
            target = nearest_walkable(
                maze,
                target,
            )

        return target

    @staticmethod
    def _clyde_target(
        maze: Maze,
        ghost: Ghost,
        player: Player,
    ) -> Position:
        """Return Clyde's chase target.

        Clyde chases the player while far away. Once he gets close,
        he retreats towards the lower-left corner.

        Args:
            maze: Current maze.
            ghost: Clyde.
            player: Current player state.

        Returns:
            Target position.
        """
        if manhattan_distance(
            ghost.position,
            player.position,
        ) > 8:
            return player.position

        target = Position(
            0,
            maze.height - 1,
        )
        if (
            not maze.contains(target)
            or not maze.neighbours(target)
        ):
            target = nearest_walkable(
                maze,
                target,
            )

        return target

    @staticmethod
    def _advance(
        maze: Maze,
        start: Position,
        direction,
        steps: int,
    ) -> Position:
        """Advance a position while movement is possible.

        Args:
            maze: Current maze.
            start: Starting position.
            direction: Direction of movement.
            steps: Maximum number of cells to advance.

        Returns:
            Final reachable position.
        """
        position = start

        for _ in range(steps):
            if not maze.can_move(position, direction):
                break

            position = position.moved(direction)

        return position
