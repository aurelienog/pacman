from ..domain import Player, Ghost
from ..domain import Item
from ..domain import Maze
from .score_registry import ScoreRegistry

class Level:

    maze: Maze
    player: Player
    ghosts: list[Ghost]
    items: list[Item]
    score: ScoreRegistry

    def update(self, dt):
        self.player.update(dt)

        for ghost in self.ghosts:
            ghost.update(dt)

        self._handle_turns()

        self._handle_items()

        self._handle_collisions()

        self._check_level_completed()
    
        draw()


timer_remaining

LOGICA DEL GIRO