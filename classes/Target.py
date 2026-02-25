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

    def __init__(self, x: int, y: int, radius: int, ttl_ms: int, vx: float = 0.0, vy: float = 0.0) -> None:
        self.x              = x
        self.y              = y
        self.radius         = radius
        self.ttl_ms         = ttl_ms
        self.initial_radius = radius
        self.alive          = True
        self.vx = vx
        self.vy = vy
        
        self.spawn_time     = pygame.time.get_ticks()
        self.last_update    = self.spawn_time
        self._elapsed       = 0

    def update(self, current_time_ms: int, screen_width: int, screen_height: int):
        self._elapsed = current_time_ms - self.spawn_time
        if self._elapsed >= self.ttl_ms:
            self.alive = False
            return "timeout"
        dt = current_time_ms - self.last_update
        self.last_update = current_time_ms
        if self.vx != 0 or self.vy != 0:
            self.x += self.vx * dt
            self.y += self.vy * dt

            # Va chạm với viền màn hình (Bouncing)
            if self.x - self.radius < 0:
                self.x = self.radius
                self.vx *= -1
            elif self.x + self.radius > screen_width:
                self.x = screen_width - self.radius
                self.vx *= -1

            if self.y - self.radius < 0:
                self.y = self.radius
                self.vy *= -1
            elif self.y + self.radius > screen_height:
                self.y = screen_height - self.radius
                self.vy *= -1

        return None

    def draw(self, surface: pygame.Surface) -> None:
        life_ratio = min(1.0, self._elapsed / self.ttl_ms) if self.ttl_ms > 0 else 0.0

        outer_color = _lerp_color(_GREEN, _RED, life_ratio)
        r = self.radius

        dx, dy = int(self.x), int(self.y)
        
        pygame.draw.circle(surface, (20, 20, 20),     (dx, dy), r + 2)
        pygame.draw.circle(surface, outer_color,      (dx, dy), r)
        pygame.draw.circle(surface, WHITE,            (dx, dy), max(1, int(r * 0.55)))
        pygame.draw.circle(surface, outer_color,      (dx, dy), max(1, int(r * 0.35)))
        pygame.draw.circle(surface, WHITE,            (dx, dy), max(1, int(r * 0.15)))

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
    def spawn(width: int, height: int, radius: int, ttl_ms: int = INITIAL_TTL, mode: str = "basic") -> "Target":
        x = randint(radius + 1, width  - radius - 1)
        y = randint(radius + 1, height - radius - 1)
        vx, vy = 0.0, 0.0
        if mode == "dynamic":
            speed = randint(20, 60) / 100.0  # Tốc độ ngẫu nhiên từ 0.2 đến 0.6 pixel/ms
            angle = math.radians(randint(0, 359))
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
        return Target(float(x), float(y), radius, ttl_ms, vx, vy)
