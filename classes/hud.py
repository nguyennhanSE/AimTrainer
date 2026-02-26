from __future__ import annotations
from typing import TYPE_CHECKING
import math
import pygame

if TYPE_CHECKING:
    from classes.score_manager import ScoreManager

WHITE        = (255, 255, 255)
BLACK        = (0,   0,   0)
SHADOW       = (30,  30,  30)
YELLOW       = (255, 230, 0)
HUD_BG       = (0,   0,   0, 160)   # used only when blitting onto a temp surface

# Padding from screen edges
_MARGIN = 14


class HUD:
    """
    Renders in-game statistics at the top of the screen.

    The HUD displays three zones:
    - Top-left  → time remaining
    - Top-centre → current score
    - Top-right  → hit / miss counters
    """

    def __init__(self, font: pygame.font.Font, score_manager: ScoreManager) -> None:
        """
        Args:
            font:          A pygame.font.Font used for all HUD text.
            score_manager: The shared ScoreManager instance to read stats from.
        """
        self._font  = font
        self._sm    = score_manager

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------

    def _render_shadowed(
        self,
        surface: pygame.Surface,
        text: str,
        pos: tuple[int, int],
        color: tuple[int, int, int] = WHITE,
        anchor: str = "topleft",
    ) -> None:
        """
        Blit *text* onto *surface* with a 2-px dark drop-shadow.

        Args:
            surface: Destination surface.
            text:    String to render.
            pos:     (x, y) reference point; interpretation depends on *anchor*.
            color:   Foreground colour.
            anchor:  One of ``"topleft"``, ``"midtop"``, or ``"topright"``.
        """
        shadow_surf = self._font.render(text, True, SHADOW)
        text_surf   = self._font.render(text, True, color)

        shadow_rect = shadow_surf.get_rect()
        text_rect   = text_surf.get_rect()

        setattr(shadow_rect, anchor, pos)
        setattr(text_rect,   anchor, pos)

        # shift shadow by 2 px
        shadow_rect.x += 2
        shadow_rect.y += 2

        surface.blit(shadow_surf, shadow_rect)
        surface.blit(text_surf,   text_rect)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def _draw_combo(self, surface: pygame.Surface) -> None:
        """Vẽ chữ Combo chớp giật siêu đẹp ở giữa cạnh dưới màn hình"""
        combo = self._sm.current_combo
        if combo < 2:
            return  # Chỉ hiện khi Combo từ 2 trở lên
        
        # Thiết lập hiệu ứng dựa trên cấp độ Combo
        if combo >= 30:
            color, scale, text = (255, 50, 50), 1.6, f"GODLIKE! {combo}x"
        elif combo >= 20:
            color, scale, text = (255, 120, 0), 1.4, f"INSANE! {combo}x"
        elif combo >= 10:
            color, scale, text = (255, 230, 0), 1.2, f"GREAT! {combo}x"
        elif combo >= 5:
            color, scale, text = (50, 200, 255), 1.1, f"COMBO: {combo}x"
        else:
            color, scale, text = (200, 200, 200), 1.0, f"COMBO: {combo}x"

        # Thêm thông báo hệ số điểm
        multi = self._sm.multiplier
        if multi > 1.0:
            text += f" (x{multi:.1f} Pts)"

        # Tạo chữ nền màu (Glow)
        color_surf = self._font.render(text, True, color)
        if scale > 1.0:
            new_w, new_h = int(color_surf.get_width() * scale), int(color_surf.get_height() * scale)
            color_surf = pygame.transform.smoothscale(color_surf, (new_w, new_h))

        # Hiệu ứng rung lắc (Camera Shake) cho Combo cao
        offset_x, offset_y = 0, 0
        if combo >= 10:
            time_ms = pygame.time.get_ticks()
            intensity = min(6, combo // 4)
            offset_x = int(math.sin(time_ms * 0.08) * intensity)
            offset_y = int(math.cos(time_ms * 0.06) * intensity)

        # Toạ độ giữa màn hình phía dưới
        cx = surface.get_width() // 2 + offset_x
        cy = surface.get_height() - 50 + offset_y
        rect = color_surf.get_rect(center=(cx, cy))

        # Vẽ viền màu siêu dày (Hiệu ứng phát sáng / Arcade style)
        for dx, dy in [(-3,-3), (3,-3), (-3,3), (3,3), (-4,0), (4,0), (0,-4), (0,4)]:
            rect_glow = rect.copy()
            rect_glow.x += dx
            rect_glow.y += dy
            surface.blit(color_surf, rect_glow)

        # Vẽ lõi chữ màu Trắng để chữ nổi bật lên
        white_surf = self._font.render(text, True, WHITE)
        if scale > 1.0:
            white_surf = pygame.transform.smoothscale(white_surf, (new_w, new_h))
        surface.blit(white_surf, rect)
        
    def draw(self, surface: pygame.Surface, time_left_seconds: float) -> None:
        """
        Render the HUD bar across the top of *surface*.

        Args:
            surface:            The main game surface.
            time_left_seconds:  Remaining game time in seconds (integer display).
        """
        w = surface.get_width()

        time_str  = f"Time: {int(time_left_seconds)}s"
        score_str = f"Score: {self._sm.score}"
        hm_str    = f"Hits: {self._sm.hits}   Misses: {self._sm.misses}"

        # Top-left — time
        self._render_shadowed(surface, time_str,  (_MARGIN, _MARGIN), anchor="topleft")

        # Top-centre — score
        self._render_shadowed(surface, score_str, (w // 2, _MARGIN),  anchor="midtop")

        # Top-right — hits / misses
        self._render_shadowed(surface, hm_str, (w - _MARGIN, _MARGIN), anchor="topright")
        
        # Combo
        self._draw_combo(surface)

    def draw_hit_feedback(
        self,
        surface: pygame.Surface,
        pos: tuple[int, int],
        points: int,
    ) -> None:
        """
        Render a static ``+{points}`` label at *pos* in yellow.

        For animated floating feedback (timer-based) use
        :class:`~classes.feedback_manager.FeedbackManager` instead; this
        method provides a lightweight single-frame alternative when no
        feedback manager is available.

        Args:
            surface: Destination surface.
            pos:     (x, y) pixel position of the click.
            points:  Points awarded for the hit.
        """
        self._render_shadowed(surface, f"+{points}", pos, color=YELLOW, anchor="midbottom")
