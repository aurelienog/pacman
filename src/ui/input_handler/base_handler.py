"""Base helper class for input handling."""

from __future__ import annotations

from typing import Any


class BaseInputHandler:
    """Base class providing shared input utility functions."""

    @staticmethod
    def is_inside(pos: tuple[int, int], rect: Any) -> bool:
        """Pure math point-in-bounds check
        (100% MLX compatible, no rect.collidepoint)."""
        px, py = pos
        return rect.left <= px <= rect.right and rect.top <= py <= rect.bottom
