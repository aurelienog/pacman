from dataclasses import dataclass
from enum import Enum, auto

from .entity import Entity
from ..ghost_ai import GhostAI


class GhostState(Enum):
    CHASE = auto()
    FRIGHTENED = auto()
    RESPAWN = auto()

@dataclass
class Ghost(Entity, GhostAI):
    ai: GhostAI

estados frightened/chase


