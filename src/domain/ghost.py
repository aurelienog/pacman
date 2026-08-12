from dataclasses import dataclass, field
from enum import Enum, auto


from .geometry import Position, Direction, Hitbox


GHOST_HITBOX_SIZE = 0.8


class GhostPersonality(Enum):
    BLINKY = auto()
    INKY = auto()
    CLYDE = auto()
    PINKY = auto()


class GhostMode(Enum):
    """Behaviour mode of a ghost."""

    CHASE = "chase"
    FRIGHTENED = "frightened"
    RESPAWNING = "respawning"


@dataclass(slots=True)
class Ghost:
    """State for one autonomous ghost."""

    position: Position
    home: Position
    prev_position: Position = field(default_factory=lambda: Position(0, 0))
    direction: Direction = Direction.NONE
    mode: GhostMode = GhostMode.CHASE
    respawn_remaining: float = 0.0
    personality: GhostPersonality = GhostPersonality.BLINKY
    hitbox: Hitbox = Hitbox(
        width=GHOST_HITBOX_SIZE,
        height=GHOST_HITBOX_SIZE,
    )
