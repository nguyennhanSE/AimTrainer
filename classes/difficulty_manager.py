import constants
from constants import (
    INITIAL_RADIUS, MIN_RADIUS,
    INITIAL_TTL,    MIN_TTL,
    TTL_DECREASE_INTERVAL,    TTL_DECREASE_AMOUNT,
    RADIUS_DECREASE_INTERVAL, RADIUS_DECREASE_AMOUNT,
)


class DifficultyManager:

    def __init__(self) -> None:
        self.current_ttl    = constants.INITIAL_TTL
        self.current_radius = constants.INITIAL_RADIUS
        self._last_seconds  = 0

    def update(self, elapsed_seconds: int) -> None:
        if elapsed_seconds == self._last_seconds:
            return
        self._last_seconds = elapsed_seconds

        ttl_steps    = elapsed_seconds // TTL_DECREASE_INTERVAL
        radius_steps = elapsed_seconds // RADIUS_DECREASE_INTERVAL

        self.current_ttl = max(
            MIN_TTL,
            constants.INITIAL_TTL - ttl_steps * TTL_DECREASE_AMOUNT,
        )
        self.current_radius = max(
            MIN_RADIUS,
            constants.INITIAL_RADIUS - radius_steps * RADIUS_DECREASE_AMOUNT,
        )

    def reset(self) -> None:
        self.current_ttl    = constants.INITIAL_TTL
        self.current_radius = constants.INITIAL_RADIUS
        self._last_seconds  = 0
