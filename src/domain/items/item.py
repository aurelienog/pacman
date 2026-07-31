from dataclasses import dataclass
from abc import ABC, abstractmethod
from .. import GridPosition


@dataclass
class CollectResult:
    score: int
    frightened_mode: bool = False


@dataclass
class Item(ABC):
    position: GridPosition
    value: int
    eaten: bool = False

    @abstractmethod
    def collect(self) -> CollectResult:
        ...