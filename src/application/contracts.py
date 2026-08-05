"""Public, renderer-neutral contracts of the game application."""

from dataclasses import dataclass
from enum import Enum, auto

from src.domain import Item, Maze, Player, GhostMode, Direction, Position


class GamePhase(Enum):
    """Execution states of a game session.

    These values describe the current state of the application and
    allow any user interface to react accordingly.
    """

    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    EXIT = auto()


class InputAction(Enum):
    """Renderer-independent commands accepted by the game.

    These actions represent the player's intent independently of the
    input device or user interface implementation.
    """

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CONFIRM = auto()
    PAUSE = auto()
    QUIT = auto()
    TOGGLE_INVINCIBLE = auto()
    TOGGLE_FREEZE = auto()
    TOGGLE_TIMER = auto()
    TOGGLE_SPEED = auto()
    SKIP_LEVEL = auto()
    ADD_LIFE = auto()
    RETURN_TO_MENU = auto()


@dataclass(frozen=True, slots=True)
class RenderEntity:
    """Interpolated position of a moving entity.

    Attributes:
        x: Horizontal position expressed in maze coordinates.
        y: Vertical position expressed in maze coordinates.
        direction: Current movement direction.
        mode: Optional entity state used during rendering.
    """

    x: float
    y: float
    direction: Direction
    mode: GhostMode | None = None


@dataclass(frozen=True, slots=True)
class Snapshot:
    """Immutable view of the current game state.

    A snapshot contains all information required by a renderer to draw
    one frame without accessing or modifying the internal game state.

    Attributes:
        phase: Current execution state of the game.
        maze: Current maze, or ``None`` before a game starts.
        player: Current player state, or ``None`` before a game starts.
        player_visual_pos: Interpolated player position.
        ghost_visual_positions: Interpolated ghost positions.
        items: Remaining collectible items keyed by position.
        score: Current player score.
        level: Current level number, starting at one.
        level_count: Total number of configured levels.
        seconds_remaining: Remaining time for the current level.
        message: Status message displayed to the player.
        invincible: Whether invincibility mode is enabled.
        freeze_ghosts: Whether ghost movement is frozen.
        freeze_timer: Whether the level timer is frozen.
        speed_boost: Whether player movement is accelerated.
    """

    phase: GamePhase
    maze: Maze | None
    player: Player | None
    player_visual_pos: tuple[float, float]
    ghost_visual_positions: tuple[RenderEntity, ...]
    items: tuple[tuple[Position, Item], ...]
    score: int
    level: int
    level_count: int
    seconds_remaining: float
    message: str
    invincible: bool
    freeze_ghosts: bool
    freeze_timer: bool
    speed_boost: bool
