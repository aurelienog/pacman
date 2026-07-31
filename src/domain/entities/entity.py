from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Entity (ABC):
    position:
    direction:
    speed:

    @abstractmethod
    def move():

    @abstractmethod
    def update():

    @abstractmethod
    def draw():