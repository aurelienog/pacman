from abc import ABC

from .entities import GhostState

class GhostAI(ABC):

    def choose_direction(self, ghost, level):
        if ghost.state == GhostState.CHASE:
            return self._chase(ghost, level)

        if ghost.state == GhostState.FRIGHTENED:
            return self._run_away(ghost, level)

        if ghost.state == GhostState.RESPAWN:
            return self._return_home(ghost, level)

    def _chase(...):
        ...

    def _run_away(...):
        ...

    def _return_home(...):
        ...