from enum import Enum
from dataclasses import dataclass

TILE_SIZE = 24 #cell size


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)

    @property
    def delta(self) -> tuple[int, int]:
        return self.value


@dataclass(slots=True)
class GridPosition:
    x: int
    y: int


@dataclass(slots=True)
class PixelPosition:
    x: float
    y: float


@dataclass
class Transform:
    grid: GridPosition
    pixel: PixelPosition

    def next_cell_center(self, direction: Direction, tile_size: int) -> PixelPosition:
            dx, dy = direction.delta

            return PixelPosition(
                (self.grid.x + dx) * tile_size,
                (self.grid.y + dy) * tile_size,
            )
    
    def reached_cell_center(self, direction: Direction, tile_size: int) -> bool:
        target = self.next_cell_center(direction, tile_size)

        dx, dy = direction.delta

        if dx > 0:
            return self.pixel.x >= target.x

        if dx < 0:
            return self.pixel.x <= target.x

        if dy > 0:
            return self.pixel.y >= target.y

        if dy < 0:
            return self.pixel.y <= target.y

        return False

    def advance(self, direction: Direction, tile_size: int) -> None:
        dx, dy = direction.delta

        self.grid.x += dx
        self.grid.y += dy

        self.pixel.x = self.grid.x * tile_size
        self.pixel.y = self.grid.y * tile_size

