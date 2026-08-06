"""Basic rendering utilities for Pygame (MLX-compatible primitives)."""

from __future__ import annotations

from typing import Any


def center_text(screen: Any, font: Any, value: str, color: tuple[int, int, int], y: int) -> Any:
    """Render and draw centered text horizontally at height y. Returns text rect."""
    text = font.render(value, True, color)
    rect = text.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(text, rect)
    return rect


def center_float(x: float, y: float, left: int, top: int, cell: int) -> tuple[int, int]:
    """Convert grid float coordinates to screen pixel coordinates."""
    return int(left + x * cell + cell / 2.0), int(top + y * cell + cell / 2.0)


def draw_line(
    screen: Any,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int],
    pygame: Any,
    width: int = 3,
) -> None:
    """Draw a simple wall line."""
    pygame.draw.line(screen, color, start, end, width)


def draw_circle(
    screen: Any,
    center: tuple[int, int],
    radius: int,
    color: tuple[int, int, int],
    pygame: Any,
) -> None:
    """Draw a simple filled circle."""
    pygame.draw.circle(screen, color, center, radius)


def draw_button_box(
    screen: Any,
    rect: Any,
    pygame: Any,
    color: tuple[int, int, int] = (45, 130, 255),
) -> None:
    """Draw a clean selection box around a selected menu item."""
    pygame.draw.rect(screen, color, rect, width=2)


def draw_menu_card_frame(
    screen: Any,
    rect: Any,
    border_color: tuple[int, int, int],
    pygame: Any,
    pacman_icon: Any = None,
) -> None:
    """Draw a clean menu panel frame with a simple border and Pac-Man icon notch."""
    # Тло панелі
    pygame.draw.rect(screen, (8, 10, 24), rect)
    # Проста рамка
    pygame.draw.rect(screen, border_color, rect, width=2)

    # Нижній виріз під іконку Пакмана
    cx, cy = rect.centerx, rect.bottom
    cutout = pygame.Rect(cx - 24, cy - 6, 48, 12)
    pygame.draw.rect(screen, (8, 10, 24), cutout)

    if pacman_icon is not None:
        icon_size = 28
        scaled_icon = pygame.transform.smoothscale(pacman_icon, (icon_size, icon_size))
        icon_rect = scaled_icon.get_rect(center=(cx, cy - 2))
        screen.blit(scaled_icon, icon_rect)
