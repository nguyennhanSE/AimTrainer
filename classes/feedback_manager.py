"""
FeedbackManager — animated floating hit / miss labels drawn over the game.

Each feedback entry is a small dict that tracks its screen position, the
text to display, a remaining lifetime, the elapsed time (used to compute
the upward float offset), and a colour.
"""

from __future__ import annotations
from typing import Optional

import pygame

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
YELLOW = (255, 230, 0)
RED    = (220, 60,  60)
WHITE  = (255, 255, 255)
SHADOW = (20,  20,  20)

# ---------------------------------------------------------------------------
# Tuning constants
# ---------------------------------------------------------------------------
_HIT_LIFETIME_MS   = 800    # ms a hit label stays visible
_MISS_LIFETIME_MS  = 600    # ms a miss label stays visible
_FLOAT_SPEED       = 0.06   # pixels of upward travel per ms of elapsed time


class FeedbackManager:
    """
    Maintains a pool of short-lived floating text labels for visual feedback.

    Typical usage inside the game loop::

        # once, after constructing:
        fb = FeedbackManager()

        # on a hit:
        fb.add_hit_feedback(mouse_pos, points)

        # on a miss:
        fb.add_miss_feedback(mouse_pos)

        # every frame (dt is milliseconds since last tick):
        fb.update(dt)
        fb.draw(surface, font)
    """

    def __init__(self) -> None:
        """Initialise with an empty list of active feedback entries."""
        self._entries: list[dict] = []

    # ------------------------------------------------------------------
    # Adding entries
    # ------------------------------------------------------------------

    def add_hit_feedback(self, pos: tuple[int, int], points: int) -> None:
        """
        Spawn a yellow ``+{points}`` label at *pos*.

        Args:
            pos:    (x, y) pixel position — typically the click location.
            points: Points awarded for the hit; displayed after a ``+`` sign.
        """
        self._entries.append({
            "text":    f"+{points}",
            "x":       float(pos[0]),
            "y":       float(pos[1]),
            "timer":   _HIT_LIFETIME_MS,
            "elapsed": 0.0,
            "color":   YELLOW,
        })

    def add_miss_feedback(self, pos: tuple[int, int]) -> None:
        """
        Spawn a red ``MISS`` label at *pos*.

        Args:
            pos: (x, y) pixel position — typically the click location.
        """
        self._entries.append({
            "text":    "MISS",
            "x":       float(pos[0]),
            "y":       float(pos[1]),
            "timer":   _MISS_LIFETIME_MS,
            "elapsed": 0.0,
            "color":   RED,
        })

    # ------------------------------------------------------------------
    # Update & draw
    # ------------------------------------------------------------------

    def update(self, dt: float) -> None:
        """
        Advance all feedback entries by *dt* milliseconds and remove
        any whose lifetime has expired.

        Args:
            dt: Delta time in milliseconds since the last frame.
        """
        for entry in self._entries:
            entry["timer"]   -= dt
            entry["elapsed"] += dt

        self._entries = [e for e in self._entries if e["timer"] > 0]

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Render all active feedback labels onto *surface*.

        Labels float upward over time and fade in opacity as their lifetime
        expires.  A dark drop-shadow is drawn two pixels below-right for
        legibility against any background.

        Args:
            surface: Destination surface.
            font:    Font used to render each label.
        """
        for entry in self._entries:
            # Compute upward offset based on how long the entry has been alive
            y_offset = entry["elapsed"] * _FLOAT_SPEED

            draw_x = int(entry["x"])
            draw_y = int(entry["y"] - y_offset)

            # Determine lifetime fraction remaining (1.0 → fresh, 0.0 → expired)
            lifetime = _HIT_LIFETIME_MS if entry["color"] == YELLOW else _MISS_LIFETIME_MS
            alpha_frac = max(0.0, entry["timer"] / lifetime)
            alpha = int(alpha_frac * 255)

            # Render to a temporary surface so we can apply per-pixel alpha
            shadow_surf = font.render(entry["text"], True, SHADOW)
            text_surf   = font.render(entry["text"], True, entry["color"])

            shadow_surf.set_alpha(alpha)
            text_surf.set_alpha(alpha)

            shadow_rect = shadow_surf.get_rect(midbottom=(draw_x + 2, draw_y + 2))
            text_rect   = text_surf.get_rect(midbottom=(draw_x, draw_y))

            surface.blit(shadow_surf, shadow_rect)
            surface.blit(text_surf,   text_rect)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove all active feedback entries (e.g. on round reset)."""
        self._entries.clear()

    @property
    def active_count(self) -> int:
        """Number of feedback labels currently alive."""
        return len(self._entries)
