from ..domain import GameConfig, Maze, Player, Ghost, Item, Position
from ..adapters import AmazingMazeFactory

from .contracts import GamePhase, InputAction, Snapshot
from .input import dispatch_action
from .update import update_world
from .snapshot import build_snapshot

import random


class GameSession:

    BASE_PLAYER_STEP_SECONDS = 0.25
    GHOST_STEP_SECONDS = 0.35

    FRIGHTENED_DURATION_SECONDS = 7.0
    GHOST_RESPAWN_SECONDS = 5.0

    MAX_DELTA_SECONDS = 0.1
    MIN_PACGUM_RATIO = 0.50

    def __init__(self,
                 config: GameConfig,
                 maze_factory: AmazingMazeFactory
                 ) -> None:
        """Create a new game session.

        Args:
            config: Validated game configuration.
            maze_factory: Maze generator implementation.
        """
        self._config = config
        self._factory = maze_factory
        self._random = random.Random()

        self.phase = GamePhase.MAIN_MENU
        self.message = "Press Enter to start"

        self.score = 0
        self.level_index = 0

        self.maze: Maze | None = None
        self.player: Player | None = None
        self.ghosts: list[Ghost] = []
        self.items: dict[Position, Item] = {}

        self.seconds_remaining = 0.0

        self.invincible = False
        self.freeze_ghosts = False
        self.freeze_timer = False
        self.speed_boost = False

        self._player_elapsed = 0.0
        self._ghost_elapsed = 0.0
        self._frightened_remaining = 0.0

    def dispatch(self, action: InputAction) -> None:
        """Apply one user action.

        Args:
            action: Renderer-independent input command.

        Returns:
            None.
        """
        dispatch_action(self, action)

    def update(self, delta_seconds: float) -> None:
        """Advance the simulation.

        Args:
            delta_seconds: Real elapsed time.

        Returns:
            None.
        """
        update_world(self, delta_seconds)

    def snapshot(self) -> Snapshot:
        """Return a renderer-safe representation of the game.

        Returns:
            Immutable game snapshot.
        """
        return build_snapshot(self)
