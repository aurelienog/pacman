from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Item(ABC):
    position:
    value: int
    eaten: bool

    @abstractmethod
    def on_collect(player, game):
        ...