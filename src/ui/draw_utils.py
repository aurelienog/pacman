"""Basic rendering utilities for Pygame (MLX-compatible primitives)."""

from __future__ import annotations

from typing import Any


def center_text(
    screen: Any,
    font: Any,
    value: str,
    color: tuple[int, int, int],
    y: int,
) -> Any:
    """Render and draw centered text horizontally at a given height.

    Args:
        screen: Pygame display surface.
        font: Loaded font object used for rendering.
        value: Text string to display.
        color: RGB color tuple for the text.
        y: Vertical center coordinate for the text.

    Returns:
        The rectangle bounding the rendered text.
    """
    text = font.render(value, True, color)
    rect = text.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(text, rect)
    return rect


def center_float(
    x: float,
    y: float,
    left: int,
    top: int,
    cell: int,
) -> tuple[int, int]:
    """Convert grid float coordinates to screen pixel coordinates.

    Args:
        x: Horizontal grid position.
        y: Vertical grid position.
        left: Left offset of the grid on screen in pixels.
        top: Top offset of the grid on screen in pixels.
        cell: Size of a single grid cell in pixels.

    Returns:
        Tuple of (x, y) screen pixel coordinates for the cell center.
    """
    return int(left + x * cell + cell / 2.0), int(top + y * cell + cell / 2.0)


def draw_line(
    screen: Any,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int],
    pygame: Any,
    width: int = 3,
) -> None:
    """Draw a simple straight line on the screen.

    Args:
        screen: Pygame display surface.
        start: Starting (x, y) pixel coordinate.
        end: Ending (x, y) pixel coordinate.
        color: RGB color tuple for the line.
        pygame: Pygame module instance.
        width: Line thickness in pixels.

    Returns:
        None.
    """
    pygame.draw.line(screen, color, start, end, width)


def draw_circle(
    screen: Any,
    center: tuple[int, int],
    radius: int,
    color: tuple[int, int, int],
    pygame: Any,
) -> None:
    """Draw a simple filled circle on the screen.

    Args:
        screen: Pygame display surface.
        center: Center (x, y) pixel coordinate.
        radius: Radius of the circle in pixels.
        color: RGB color tuple for the circle.
        pygame: Pygame module instance.

    Returns:
        None.
    """
    pygame.draw.circle(screen, color, center, radius)


def draw_button_box(
    screen: Any,
    rect: Any,
    pygame: Any,
    color: tuple[int, int, int] = (45, 130, 255),
) -> None:
    """Draw a clean selection box around a selected menu item.

    Args:
        screen: Pygame display surface.
        rect: Pygame Rect object defining the button boundary.
        pygame: Pygame module instance.
        color: RGB color tuple for the border box.

    Returns:
        None.
    """
    pygame.draw.rect(screen, color, rect, width=2)


def draw_menu_card_frame(
    screen: Any,
    rect: Any,
    border_color: tuple[int, int, int],
    pygame: Any,
    pacman_icon: Any = None,
) -> None:
    """Draw a clean menu panel frame with a simple border and icon notch.

    Args:
        screen: Pygame display surface.
        rect: Pygame Rect object defining the panel area.
        border_color: RGB color tuple for the frame border.
        pygame: Pygame module instance.
        pacman_icon: Optional loaded icon surface drawn in the bottom notch.

    Returns:
        None.
    """
    # Panel background
    pygame.draw.rect(screen, (8, 10, 24), rect)
    # Simple frame
    pygame.draw.rect(screen, border_color, rect, width=2)

    # Bottom cutout for the Pacman icon
    cx, cy = rect.centerx, rect.bottom
    cutout = pygame.Rect(cx - 24, cy - 6, 48, 12)
    pygame.draw.rect(screen, (8, 10, 24), cutout)

    if pacman_icon is not None:
        icon_size = 38
        scaled_icon = pygame.transform.smoothscale(
            pacman_icon,
            (icon_size, icon_size)
        )
        icon_rect = scaled_icon.get_rect(center=(cx, cy - 2))
        screen.blit(scaled_icon, icon_rect)
