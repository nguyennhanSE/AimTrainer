import pygame


def draw_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple,
    center_pos: tuple[int, int],
    shadow: bool = True,
) -> None:
    if shadow:
        shadow_surf = font.render(text, True, (20, 20, 20))
        shadow_rect = shadow_surf.get_rect(center=(center_pos[0] + 2, center_pos[1] + 2))
        surface.blit(shadow_surf, shadow_rect)

    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=center_pos)
    surface.blit(text_surf, text_rect)


def draw_button(
    surface: pygame.Surface,
    rect: pygame.Rect,
    text: str,
    font: pygame.font.Font,
    base_color: tuple,
    hover_color: tuple,
    text_color: tuple,
    mouse_pos: tuple[int, int],
) -> bool:
    hovered  = rect.collidepoint(mouse_pos)
    bg_color = hover_color if hovered else base_color

    pygame.draw.rect(surface, bg_color, rect, border_radius=12)

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

    return hovered


def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))


def format_time(seconds: float) -> str:
    total   = max(0, int(seconds))
    minutes = total // 60
    secs    = total % 60
    return f"{minutes}:{secs:02d}"
