import math
from random import randint

import pygame

from constants import (
    GREEN, RED, WHITE, YELLOW,
    INITIAL_RADIUS, INITIAL_TTL,
)

_GREEN = GREEN
_RED   = RED


def _lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


class Target:

    def __init__(self, x: int, y: int, radius: int, ttl_ms: int) -> None:
        self.x              = x
        self.y              = y
        self.radius         = radius
        self.ttl_ms         = ttl_ms
        self.initial_radius = radius
        self.alive          = True
        self.spawn_time     = pygame.time.get_ticks()
        self._elapsed       = 0

    def update(self, current_time_ms: int):
        self._elapsed = current_time_ms - self.spawn_time
        if self._elapsed >= self.ttl_ms:
            self.alive = False
            return "timeout"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        life_ratio = min(1.0, self._elapsed / self.ttl_ms) if self.ttl_ms > 0 else 0.0

        outer_color = _lerp_color(_GREEN, _RED, life_ratio)
        r = self.radius

        pygame.draw.circle(surface, (20, 20, 20),     (self.x, self.y), r + 2)
        pygame.draw.circle(surface, outer_color,      (self.x, self.y), r)
        pygame.draw.circle(surface, WHITE,            (self.x, self.y), max(1, int(r * 0.55)))
        pygame.draw.circle(surface, outer_color,      (self.x, self.y), max(1, int(r * 0.35)))
        pygame.draw.circle(surface, WHITE,            (self.x, self.y), max(1, int(r * 0.15)))

        arc_ratio = max(0.0, 1.0 - life_ratio)
        if arc_ratio > 0.01:
            arc_angle = arc_ratio * 2 * math.pi
            arc_rect  = pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)
            pygame.draw.arc(surface, YELLOW, arc_rect,
                            -math.pi / 2,
                            -math.pi / 2 + arc_angle,
                            3)

    def is_hit(self, mouse_x: int, mouse_y: int) -> bool:
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        return math.hypot(dx, dy) <= self.radius

    def get_reaction_time(self, hit_time_ms: int) -> int:
        return hit_time_ms - self.spawn_time

    @staticmethod
    def spawn(width: int, height: int, radius: int, ttl_ms: int = INITIAL_TTL) -> "Target":
        x = randint(radius + 1, width  - radius - 1)
        y = randint(radius + 1, height - radius - 1)
        return Target(x, y, radius, ttl_ms)
