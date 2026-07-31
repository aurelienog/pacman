from .entities import Entity
from .geometry import Direction, Transform

class Maze:

    def is_walkable(self, transform: Transform) -> bool:
        ...

    def can_move(self, entity: Entity, direction: Direction) -> bool:
        ...

    