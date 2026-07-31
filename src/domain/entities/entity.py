from dataclasses import dataclass
from abc import ABC

from .. import Direction, Transform


@dataclass
class Entity(ABC):
    speed: float

    transform: Transform

    direction: Direction = Direction.NONE
    next_direction: Direction = Direction.NONE

    def update(self, dt: float) -> None:
        """Advance the entity one frame."""

        dx, dy = self.direction.delta

        self.transform.pixel.x += dx * self.speed * dt
        self.transform.pixel.y += dy * self.speed * dt
