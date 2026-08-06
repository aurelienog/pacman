"""Rendering utilities and neon graphical primitives for Pygame."""

from __future__ import annotations

from typing import Any


def center_text(screen: Any, font: Any, value: str, color: tuple[int, int, int], y: int, pygame: Any) -> Any:
    """Render and draw centered text horizontally at height y. Returns text rect."""
    text = font.render(value, True, color)
    rect = text.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(text, rect)
    return rect


def center_float(x: float, y: float, left: int, top: int, cell: int) -> tuple[int, int]:
    """Convert grid float coordinates to screen pixel coordinates."""
    return int(left + x * cell + cell / 2.0), int(top + y * cell + cell / 2.0)


def draw_neon_line(
    screen: Any,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int],
    pygame: Any,
) -> None:
    """Draw a dark outer tube and a bright inner neon line."""
    pygame.draw.line(screen, (10, 20, 80), start, end, 7)
    pygame.draw.line(screen, color, start, end, 3)
    highlight = (190, 235, 255) if color[2] > 200 else (255, 190, 255)
    pygame.draw.line(screen, highlight, start, end, 1)


def draw_neon_circle(
    screen: Any,
    center: tuple[int, int],
    radius: int,
    color: tuple[int, int, int],
    pygame: Any,
) -> None:
    """Draw a compact glow that remains readable on small maze cells."""
    glow = pygame.Surface((radius * 4 + 2, radius * 4 + 2), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*color, 35), (radius * 2 + 1, radius * 2 + 1), radius * 2)
    screen.blit(glow, (center[0] - radius * 2 - 1, center[1] - radius * 2 - 1))
    pygame.draw.circle(screen, color, center, radius)


def draw_neon_button_box(
    screen: Any,
    rect: Any,
    pygame: Any,
    color: tuple[int, int, int] = (45, 130, 255),
    border_radius: int = 22,
) -> None:
    """Draw an interactive neon glowing rounded button box around selected item."""
    glow_rect = rect.inflate(6, 6)
    pygame.draw.rect(screen, (10, 30, 90), glow_rect, width=6, border_radius=border_radius + 2)
    pygame.draw.rect(screen, color, rect, width=3, border_radius=border_radius)
    pygame.draw.rect(screen, (190, 235, 255), rect.inflate(-2, -2), width=1, border_radius=border_radius - 1)


def draw_neon_text(
    screen: Any,
    font: Any,
    value: str,
    color: tuple[int, int, int],
    y: int,
    pygame: Any,
    glow_color: tuple[int, int, int] = (10, 80, 220),
) -> Any:
    """Render centered text with a multi-layer glowing neon sign effect."""
    sw = screen.get_width()
    glow_surf = font.render(value, True, glow_color)
    glow_rect = glow_surf.get_rect(center=(sw // 2, y))

    for dx in (-3, -2, 0, 2, 3):
        for dy in (-3, -2, 0, 2, 3):
            if dx != 0 or dy != 0:
                screen.blit(glow_surf, glow_rect.move(dx, dy))

    main_surf = font.render(value, True, color)
    main_rect = main_surf.get_rect(center=(sw // 2, y))
    screen.blit(main_surf, main_rect)

    core_surf = font.render(value, True, (225, 248, 255))
    core_rect = core_surf.get_rect(center=(sw // 2, y))
    screen.blit(core_surf, core_rect)

    return main_rect


def draw_neon_menu_card_frame(
    screen: Any,
    rect: Any,
    border_color: tuple[int, int, int],
    pygame: Any,
    glow_color: tuple[int, int, int] | None = None,
    pacman_icon: Any = None,
) -> None:
    """Draw a tech rounded panel frame with glowing 3-layer neon effect and bottom Pac-Man notch."""
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill((8, 10, 24, 235))
    screen.blit(overlay, rect.topleft)

    if glow_color is None:
        # Автоматично створюємо темніший колір сяйва
        glow_color = (max(10, border_color[0] // 3), max(10, border_color[1] // 3), max(10, border_color[2] // 3))

    core_color = (235, 248, 255)  # Яскраво-біле ядро неону

    # ==============================================================================
    # 📌 1. ОСНОВНА ЗОВНІШНЯ НЕОНОВА РАМКА (3 шари сяйва)
    # ==============================================================================
    # Шар 1: Розмите зовнішнє сяйво
    glow_rect = rect.inflate(6, 6)
    pygame.draw.rect(screen, glow_color, glow_rect, width=7, border_radius=26)

    # Шар 2: Яскрава неонова трубка
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=22)

    # Шар 3: Внутрішнє біле ядро
    pygame.draw.rect(screen, core_color, rect.inflate(-2, -2), width=1, border_radius=21)

    # ==============================================================================
    # 📌 2. МАКЕНЬКІ ЗАКРУГЛЕНІ НЕОНОВІ КУТИКИ (3 шари сяйва)
    # ==============================================================================
    corner_inset = 14   # Відступ усередину від основної рамки
    corner_radius = 12  # Радіус заокруглення кутиків
    corner_len = 22     # Довжина дуг кутика

    inner_rect = rect.inflate(-corner_inset * 2, -corner_inset * 2)

    # Кутики - Шар 1: Сяйво
    pygame.draw.rect(screen, glow_color, inner_rect.inflate(4, 4), width=5, border_radius=corner_radius + 2)

    # Кутики - Шар 2: Основний колір
    pygame.draw.rect(screen, border_color, inner_rect, width=2, border_radius=corner_radius)

    # Кутики - Шар 3: Біле ядро
    pygame.draw.rect(screen, core_color, inner_rect.inflate(-2, -2), width=1, border_radius=max(1, corner_radius - 1))

    # Вирізаємо середні прямі ділянки, залишаючи 4 сяючих кутики
    bg_color = (8, 10, 24)
    if inner_rect.width > corner_len * 2:
        # Верхня середина
        pygame.draw.rect(screen, bg_color, (inner_rect.left + corner_len, inner_rect.top - 6, inner_rect.width - corner_len * 2, 12))
        # Нижня середина
        pygame.draw.rect(screen, bg_color, (inner_rect.left + corner_len, inner_rect.bottom - 6, inner_rect.width - corner_len * 2, 12))

    if inner_rect.height > corner_len * 2:
        # Ліва середина
        pygame.draw.rect(screen, bg_color, (inner_rect.left - 6, inner_rect.top + corner_len, 12, inner_rect.height - corner_len * 2))
        # Права середина
        pygame.draw.rect(screen, bg_color, (inner_rect.right - 6, inner_rect.top + corner_len, 12, inner_rect.height - corner_len * 2))

    # ==============================================================================
    # 📌 3. НИЖНІЙ ВИРІЗ З ПАКМАНОМ ТА НЕОНОВИМИ ЛІНІЯМИ
    # ==============================================================================
    cx, cy = rect.centerx, rect.bottom

    cutout = pygame.Rect(cx - 32, cy - 6, 64, 12)
    pygame.draw.rect(screen, bg_color, cutout)

    if pacman_icon is not None:
        icon_size = 38
        scaled_icon = pygame.transform.smoothscale(pacman_icon, (icon_size, icon_size))
        icon_rect = scaled_icon.get_rect(center=(cx, cy-5))
        screen.blit(scaled_icon, icon_rect)
    else:
        r = 11
        yellow = (255, 230, 0)
        pygame.draw.circle(screen, yellow, (cx, cy), r, width=2)
        p1 = (cx, cy)
        p2 = (cx + r + 2, cy - r // 2)
        p3 = (cx + r + 2, cy + r // 2)
        pygame.draw.polygon(screen, bg_color, [p1, p2, p3])

"""     # Неонові бокові лінієчки біля Пакмана (3 шари)
    # Ліва лінія
    pygame.draw.line(screen, glow_color, (cx - 36, cy), (cx - 16, cy), 5)
    pygame.draw.line(screen, border_color, (cx - 34, cy), (cx - 18, cy), 2)
    pygame.draw.line(screen, core_color, (cx - 32, cy), (cx - 20, cy), 1)

    # Права лінія
    pygame.draw.line(screen, glow_color, (cx + 16, cy), (cx + 36, cy), 5)
    pygame.draw.line(screen, border_color, (cx + 18, cy), (cx + 34, cy), 2)
    pygame.draw.line(screen, core_color, (cx + 20, cy), (cx + 32, cy), 1) """
