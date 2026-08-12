from dataclasses import dataclass, field


from .geometry import Direction, Position, Hitbox


PLAYER_HITBOX_SIZE = 0.8


@dataclass(slots=True)
class Player:
    """Player state owned exclusively by the game session."""

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
