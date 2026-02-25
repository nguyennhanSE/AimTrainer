"""
Screen classes for each non-gameplay state: Start, Pause, and Results.

Each class owns its own layout/rendering and returns a string action token
from ``handle_event()`` so the caller never needs to inspect pygame internals.
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from classes.score_manager import ScoreManager

# ---------------------------------------------------------------------------
# Shared colour palette
# ---------------------------------------------------------------------------
WHITE        = (255, 255, 255)
BLACK        = (0,   0,   0)
GRAY         = (180, 180, 180)
DARK_GRAY    = (40,  40,  40)
YELLOW       = (255, 215, 0)
RED          = (200, 50,  50)
GREEN        = (60,  180, 60)
BLUE         = (50,  120, 200)

DARK_OVERLAY = (0,   0,   0, 160)   # semi-transparent black for pause overlay

BTN_NORMAL   = (55,  55,  70)
BTN_HOVER    = (90,  90,  120)
BTN_BORDER   = (120, 120, 160)
BTN_TEXT     = (230, 230, 255)

TITLE_COLOR  = (255, 220, 60)
SUBTITLE_COLOR = (200, 200, 200)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _make_font(size: int) -> pygame.font.Font:
    """Return the default system font at *size* px."""
    return pygame.font.SysFont("segoeui", size, bold=False)


def _make_bold_font(size: int) -> pygame.font.Font:
    """Return a bold system font at *size* px."""
    return pygame.font.SysFont("segoeui", size, bold=True)


def _draw_button(
    surface: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    font: pygame.font.Font,
    hovered: bool = False,
) -> None:
    """
    Draw a rounded button with optional hover highlight.

    Args:
        surface: Destination surface.
        rect:    Button bounding rectangle.
        label:   Button text.
        font:    Font used for the label.
        hovered: When ``True`` use the brighter hover colour.
    """
    bg_color = BTN_HOVER if hovered else BTN_NORMAL
    pygame.draw.rect(surface, bg_color,   rect, border_radius=8)
    pygame.draw.rect(surface, BTN_BORDER, rect, width=2, border_radius=8)

    text_surf = font.render(label, True, BTN_TEXT)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def _render_shadow(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    center: tuple[int, int],
    color: tuple[int, int, int] = WHITE,
    shadow_color: tuple[int, int, int] = (20, 20, 20),
    shadow_offset: int = 3,
) -> None:
    """Render *text* centred at *center* with a drop-shadow."""
    shadow_surf = font.render(text, True, shadow_color)
    text_surf   = font.render(text, True, color)

    sx, sy = center[0] + shadow_offset, center[1] + shadow_offset
    surface.blit(shadow_surf, shadow_surf.get_rect(center=(sx, sy)))
    surface.blit(text_surf,   text_surf.get_rect(center=center))


# ---------------------------------------------------------------------------
# StartScreen
# ---------------------------------------------------------------------------

class StartScreen:
    """
    Title / main-menu screen rendered when the game is in the START state.

    Buttons and their action tokens:
    - ``"start"``        → begin a new game
    - ``"instructions"`` → show how-to-play info
    - ``"settings"``     → open settings
    - ``"exit"``         → quit the application
    """

    _BUTTON_W = 260
    _BUTTON_H = 52
    _BUTTON_GAP = 18

    def __init__(self, width: int, height: int) -> None:
        """
        Args:
            width:  Screen width in pixels.
            height: Screen height in pixels.
        """
        self._w = width
        self._h = height

        self._title_font    = _make_bold_font(72)
        self._subtitle_font = _make_font(22)
        self._btn_font      = _make_font(24)

        # Build button rects centred horizontally
        cx = width // 2
        labels_actions = [
            ("Start Game",    "start"),
            ("Instructions",  "instructions"),
            ("Settings",      "settings"),
            ("Exit Game",     "exit"),
        ]

        # Vertical starting point — roughly centred in the lower half
        total_h  = len(labels_actions) * (self._BUTTON_H + self._BUTTON_GAP) - self._BUTTON_GAP
        start_y  = height // 2 + 40

        self._buttons: list[tuple[pygame.Rect, str]] = []
        for i, (label, action) in enumerate(labels_actions):
            y = start_y + i * (self._BUTTON_H + self._BUTTON_GAP)
            rect = pygame.Rect(0, 0, self._BUTTON_W, self._BUTTON_H)
            rect.centerx = cx
            rect.y = y
            self._buttons.append((rect, action))

    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """
        Process a single pygame event and return an action string if a button
        was clicked, otherwise return ``None``.

        Args:
            event: A pygame event object (e.g. from ``pygame.event.get()``).

        Returns:
            One of ``"start"``, ``"instructions"``, ``"settings"``, ``"exit"``,
            or ``None``.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for rect, action in self._buttons:
                if rect.collidepoint(pos):
                    return action
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the start screen onto *surface*.

        Args:
            surface: The main display surface.
        """
        # Background gradient-like fill
        surface.fill(DARK_GRAY)

        # Decorative top stripe
        pygame.draw.rect(surface, (30, 30, 50), pygame.Rect(0, 0, self._w, 8))

        # Title
        _render_shadow(
            surface, "AIM TRAINER",
            self._title_font,
            (self._w // 2, self._h // 2 - 80),
            color=TITLE_COLOR,
        )

        # Subtitle
        sub_surf = self._subtitle_font.render("Test your reflexes", True, SUBTITLE_COLOR)
        surface.blit(sub_surf, sub_surf.get_rect(center=(self._w // 2, self._h // 2 - 20)))

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for rect, _ in self._buttons:
            label_index = [r for r, _ in self._buttons].index(rect)
            label = ["Start Game", "Instructions", "Settings", "Exit Game"][label_index]
            _draw_button(surface, rect, label, self._btn_font, hovered=rect.collidepoint(mouse_pos))


# ---------------------------------------------------------------------------
# PauseScreen
# ---------------------------------------------------------------------------

class PauseScreen:
    """
    Semi-transparent pause overlay rendered on top of the frozen game view.

    Buttons and their action tokens:
    - ``"resume"``  → continue the current game
    - ``"restart"`` → restart the round from scratch
    - ``"menu"``    → return to the main menu
    """

    _BUTTON_W = 240
    _BUTTON_H = 50
    _BUTTON_GAP = 16

    def __init__(self, width: int, height: int) -> None:
        """
        Args:
            width:  Screen width in pixels.
            height: Screen height in pixels.
        """
        self._w = width
        self._h = height

        self._title_font = _make_bold_font(64)
        self._btn_font   = _make_font(24)

        cx = width // 2
        labels_actions = [
            ("Resume",       "resume"),
            ("Restart",      "restart"),
            ("Quit to Menu", "menu"),
        ]

        total_h = len(labels_actions) * (self._BUTTON_H + self._BUTTON_GAP) - self._BUTTON_GAP
        start_y = height // 2 + 20

        self._buttons: list[tuple[pygame.Rect, str]] = []
        for i, (label, action) in enumerate(labels_actions):
            y = start_y + i * (self._BUTTON_H + self._BUTTON_GAP)
            rect = pygame.Rect(0, 0, self._BUTTON_W, self._BUTTON_H)
            rect.centerx = cx
            rect.y = y
            self._buttons.append((rect, action))

        # Pre-build the overlay surface (alpha)
        self._overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self._overlay.fill(DARK_OVERLAY)

    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """
        Process a single pygame event.

        Returns:
            One of ``"resume"``, ``"restart"``, ``"menu"``, or ``None``.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for rect, action in self._buttons:
                if rect.collidepoint(pos):
                    return action
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the pause overlay onto *surface*.

        Args:
            surface: The main display surface (game frame should already be drawn).
        """
        # Dim the game behind us
        surface.blit(self._overlay, (0, 0))

        # "PAUSED" title
        _render_shadow(
            surface, "PAUSED",
            self._title_font,
            (self._w // 2, self._h // 2 - 60),
            color=WHITE,
        )

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        labels = ["Resume", "Restart", "Quit to Menu"]
        for (rect, _), label in zip(self._buttons, labels):
            _draw_button(surface, rect, label, self._btn_font, hovered=rect.collidepoint(mouse_pos))


# ---------------------------------------------------------------------------
# ResultsScreen
# ---------------------------------------------------------------------------

class ResultsScreen:
    """
    End-of-round results screen showing performance metrics.

    Buttons and their action tokens:
    - ``"restart"`` → play another round
    - ``"menu"``    → return to main menu
    - ``"exit"``    → quit the application
    """

    _BUTTON_W = 200
    _BUTTON_H = 48
    _BUTTON_GAP = 14

    def __init__(self, width: int, height: int, score_manager: ScoreManager) -> None:
        """
        Args:
            width:         Screen width in pixels.
            height:        Screen height in pixels.
            score_manager: ScoreManager instance whose data will be displayed.
        """
        self._w  = width
        self._h  = height
        self._sm = score_manager

        self._title_font  = _make_bold_font(52)
        self._stat_font   = _make_font(26)
        self._label_font  = _make_bold_font(26)
        self._btn_font    = _make_font(22)

        cx = width // 2
        labels_actions = [
            ("Play Again", "restart"),
            ("Main Menu",  "menu"),
            ("Exit",       "exit"),
        ]

        btn_block_w = (
            len(labels_actions) * self._BUTTON_W
            + (len(labels_actions) - 1) * self._BUTTON_GAP
        )
        start_x = cx - btn_block_w // 2
        btn_y   = height - 90

        self._buttons: list[tuple[pygame.Rect, str]] = []
        for i, (label, action) in enumerate(labels_actions):
            x = start_x + i * (self._BUTTON_W + self._BUTTON_GAP)
            rect = pygame.Rect(x, btn_y, self._BUTTON_W, self._BUTTON_H)
            self._buttons.append((rect, action))

    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """
        Process a single pygame event.

        Returns:
            One of ``"restart"``, ``"menu"``, ``"exit"``, or ``None``.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for rect, action in self._buttons:
                if rect.collidepoint(pos):
                    return action
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the results screen onto *surface*.

        Args:
            surface: The main display surface.
        """
        surface.fill(DARK_GRAY)

        cx = self._w // 2

        # Title
        _render_shadow(
            surface, "RESULTS",
            self._title_font,
            (cx, 60),
            color=TITLE_COLOR,
        )

        # Horizontal divider
        pygame.draw.line(surface, BTN_BORDER, (cx - 200, 100), (cx + 200, 100), 2)

        # Stat rows  ────────────────────────────────────────────────────
        stats = [
            ("Score",              f"{self._sm.score}",                         YELLOW),
            ("Hits",               f"{self._sm.hits}",                          GREEN),
            ("Misses",             f"{self._sm.misses}",                         RED),
            ("Accuracy",           f"{self._sm.accuracy:.1f}%",                 WHITE),
            ("Avg Reaction Time",  f"{self._sm.avg_reaction_time:.0f} ms",      WHITE),
            ("Best Reaction Time", f"{self._sm.best_reaction_time:.0f} ms",     YELLOW),
        ]

        row_h   = 44
        start_y = 130
        col_w   = 220   # width of each column

        for i, (label, value, color) in enumerate(stats):
            y = start_y + i * row_h

            # Label  (right-aligned in the left column)
            label_surf = self._label_font.render(label + ":", True, GRAY)
            label_rect = label_surf.get_rect(midright=(cx - 10, y + row_h // 2))
            surface.blit(label_surf, label_rect)

            # Value  (left-aligned in the right column)
            value_surf = self._stat_font.render(value, True, color)
            value_rect = value_surf.get_rect(midleft=(cx + 10, y + row_h // 2))
            surface.blit(value_surf, value_rect)

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        labels = ["Play Again", "Main Menu", "Exit"]
        for (rect, _), label in zip(self._buttons, labels):
            _draw_button(surface, rect, label, self._btn_font, hovered=rect.collidepoint(mouse_pos))
