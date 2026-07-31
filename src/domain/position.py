from dataclasses import dataclass


@dataclass
class Position():
  x: int
  y: int

  def moved(self, dx: int, dy: int) -> "Position":
    return Position(self.x + dx, self.y + dy)