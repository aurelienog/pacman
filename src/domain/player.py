from dataclasses import dataclass, field


from .geometry import Direction, Position


@dataclass(slots=True)
class Player:
    """Player state owned exclusively by the game session."""

    position: Position
    spawn: Position
    lives: int
    prev_position: Position = field(default_factory=lambda: Position(0, 0))
    requested_direction: Direction = Direction.NONE
    direction: Direction = Direction.NONE
