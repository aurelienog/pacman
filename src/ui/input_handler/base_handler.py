"""Base helper class for input handling."""

from __future__ import annotations

from typing import Any


class BaseInputHandler:
    """Base class providing shared input utility functions."""

    @staticmethod
    def is_inside(pos: tuple[int, int], rect: Any) -> bool:
        """Check whether a point lies within a rectangular boundary.

        Args:
            pos: Mouse (x, y) coordinate tuple.
            rect: Pygame Rect defining boundary bounds.

        Returns:
            True if position is within bounds, otherwise False.
        """
        px, py = pos
        return bool(
            rect.left <= px <= rect.right and rect.top <= py <= rect.bottom
        )
