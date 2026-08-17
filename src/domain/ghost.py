from dataclasses import dataclass, field
from enum import Enum, auto


from .geometry import Position, Direction, Hitbox


GHOST_HITBOX_SIZE = 0.9


class GhostPersonality(Enum):
    """Identify the targeting strategy assigned to each ghost.

    Attributes:
        BLINKY: Personality used by the red ghost.
        INKY: Personality used by the cyan ghost.
        CLYDE: Personality used by the orange ghost.
        PINKY: Personality used by the pink ghost.
    """
    BLINKY = auto()
    INKY = auto()
    CLYDE = auto()
    PINKY = auto()


class GhostMode(Enum):
    """Define the current behavioural state of a ghost.

    Attributes:
        CHASE: Ghost actively pursues its target.
        FRIGHTENED: Ghost attempts to move away from the player.
        RESPAWNING: Ghost is temporarily inactive after being eaten.
    """

    CHASE = "chase"
    FRIGHTENED = "frightened"
    RESPAWNING = "respawning"


@dataclass(slots=True)
class Ghost:
    """Store the runtime state of one autonomous ghost.

    Attributes:
        position: Current logical maze position.
        home: Position where the ghost returns after being eaten or
            when the player loses a life.
        prev_position: Previous logical maze position used for smooth
            movement interpolation.
        direction: Current movement direction of the ghost.
        mode: Current behavioural state of the ghost.
        respawn_remaining: Remaining respawn time in seconds.
        personality: Targeting strategy assigned to the ghost.
        hitbox: Rectangular collision bounds of the ghost in maze-cell
            units.
    """

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
