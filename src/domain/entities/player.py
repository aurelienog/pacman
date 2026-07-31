from dataclasses import dataclass
from .entity import Entity

@dataclass
class Player(Entity):
    lives: int = 3
    is_empowered: bool = False

    def choose_next_direction(self, maze):
        return self.requested_direction



puntuación
inputs