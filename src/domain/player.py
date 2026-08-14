from dataclasses import dataclass, field


from .geometry import Direction, Position, Hitbox


PLAYER_HITBOX_SIZE = 0.8


@dataclass(slots=True)
class Player:
    """Represent the current state of the player.

    The player state is owned and updated exclusively by the game
    session.

    Attributes:
        position: Current logical position of the player in the maze.
        spawn: Position where the player is restored after losing a life.
        lives: Number of lives currently remaining.
        prev_position: Previous logical position used for interpolation.
        requested_direction: Direction requested by the player's input.
        direction: Direction currently used for movement.
        hitbox: Collision bounds used when checking entity overlap.
    """

    position: Position
    spawn: Position
    lives: int
    prev_position: Position = field(default_factory=lambda: Position(0, 0))
    requested_direction: Direction = Direction.NONE
    direction: Direction = Direction.NONE
    hitbox: Hitbox = Hitbox(
        width=PLAYER_HITBOX_SIZE,
        height=PLAYER_HITBOX_SIZE,
    )
