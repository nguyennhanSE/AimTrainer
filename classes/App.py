import sys
import pygame

from constants import (
    WIDTH, HEIGHT, FPS, TITLE,
    DARK_GRAY, YELLOW, RED, WHITE,
    GAME_DURATION,
)
from classes.asset_loader import AssetLoader
from classes.target import Target
from classes.score_manager import ScoreManager
from classes.difficulty_manager import DifficultyManager
from classes.state_manager import GameState, GameStateManager
from classes.feedback_manager import FeedbackManager
from classes.hud import HUD
from classes.screens import (
    StartScreen, PauseScreen, ResultsScreen,
    InstructionsScreen, SettingsScreen,
)

_BG_COLOR        = (18, 18, 28)
_CROSSHAIR_COLOR = (220, 220, 220)
_CROSSHAIR_SIZE  = 16
_CROSSHAIR_GAP   = 5
_SPAWN_DELAY_MS  = 150


class App:

    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self._clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        assets        = AssetLoader()
        self._fonts   = assets.load_fonts()
        self._sounds  = assets.load_sounds()

        self._state    = GameStateManager(GameState.START)
        self._score    = ScoreManager()
        self._diff     = DifficultyManager()
        self._feedback = FeedbackManager()
        self._hud      = HUD(self._fonts["medium"], self._score)

        self._start_screen    = StartScreen(WIDTH, HEIGHT)
        self._pause_screen    = PauseScreen(WIDTH, HEIGHT)
        self._results_screen  = ResultsScreen(WIDTH, HEIGHT, self._score)
        self._instr_screen    = InstructionsScreen(WIDTH, HEIGHT)
        self._settings_screen = SettingsScreen(WIDTH, HEIGHT)

        self._game_timer    = 0
        self._target        = None
        self._spawn_timer   = 0
        self._waiting_spawn = False

        self._game_frame = pygame.Surface((WIDTH, HEIGHT))

    def run(self) -> None:
        while True:
            dt     = self._clock.tick(FPS)
            events = pygame.event.get()
            self._handle_events(events)
            self._update(dt)
            self._draw()

    def _play(self, name: str) -> None:
        snd = self._sounds.get(name)
        if snd:
            snd.play()

    def _start_round(self) -> None:
        self._score.reset()
        self._diff.reset()
        self._feedback.clear()
        self._game_timer    = 0
        self._target        = None
        self._waiting_spawn = True
        self._spawn_timer   = _SPAWN_DELAY_MS
        self._state.transition_to(GameState.PLAYING)

    def _spawn_target(self) -> None:
        self._target = Target.spawn(
            WIDTH, HEIGHT,
            self._diff.current_radius,
            self._diff.current_ttl,
        )
        self._waiting_spawn = False

    def _handle_events(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self._quit()

            state = self._state.current_state

            if state == GameState.START:
                action = self._start_screen.handle_event(event)
                if   action == "start":        self._start_round()
                elif action == "instructions": self._state.transition_to(GameState.INSTRUCTIONS)
                elif action == "settings":     self._state.transition_to(GameState.SETTINGS)
                elif action == "exit":         self._quit()

            elif state == GameState.INSTRUCTIONS:
                if self._instr_screen.handle_event(event) == "back":
                    self._state.transition_to(GameState.START)

            elif state == GameState.SETTINGS:
                if self._settings_screen.handle_event(event) == "back":
                    self._state.transition_to(GameState.START)

            elif state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._game_frame.blit(self._screen, (0, 0))
                    self._state.transition_to(GameState.PAUSED)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    now    = pygame.time.get_ticks()
                    if self._target and self._target.is_hit(mx, my):
                        rt  = self._target.get_reaction_time(now)
                        pts = self._score.register_hit(rt, self._target.ttl_ms)
                        self._feedback.add_hit_feedback((mx, my), pts)
                        self._play("hit")
                        self._target        = None
                        self._waiting_spawn = True
                        self._spawn_timer   = _SPAWN_DELAY_MS
                    else:
                        self._score.register_miss()
                        self._feedback.add_miss_feedback((mx, my))
                        self._play("miss")

            elif state == GameState.PAUSED:
                action = self._pause_screen.handle_event(event)
                if   action == "resume":  self._state.transition_to(GameState.PLAYING)
                elif action == "restart": self._start_round()
                elif action == "menu":
                    self._target = None
                    self._state.transition_to(GameState.START)

            elif state == GameState.RESULTS:
                action = self._results_screen.handle_event(event)
                if   action == "restart": self._start_round()
                elif action == "menu":    self._state.transition_to(GameState.START)
                elif action == "exit":    self._quit()

    def _update(self, dt: int) -> None:
        if not self._state.is_state(GameState.PLAYING):
            return

        self._game_timer += dt
        if self._game_timer >= GAME_DURATION * 1000:
            self._target = None
            self._state.transition_to(GameState.RESULTS)
            return

        self._diff.update(self._game_timer // 1000)

        now = pygame.time.get_ticks()
        if self._target:
            if self._target.update(now) == "timeout":
                self._score.register_miss()
                self._target        = None
                self._waiting_spawn = True
                self._spawn_timer   = _SPAWN_DELAY_MS

        if self._waiting_spawn:
            self._spawn_timer -= dt
            if self._spawn_timer <= 0:
                self._spawn_target()

        self._feedback.update(dt)

    def _draw_crosshair(self, surface: pygame.Surface) -> None:
        mx, my = pygame.mouse.get_pos()
        c  = _CROSSHAIR_COLOR
        sz = _CROSSHAIR_SIZE
        g  = _CROSSHAIR_GAP
        pygame.draw.line(surface, c, (mx - sz, my), (mx - g, my), 2)
        pygame.draw.line(surface, c, (mx + g,  my), (mx + sz, my), 2)
        pygame.draw.line(surface, c, (mx, my - sz), (mx, my - g), 2)
        pygame.draw.line(surface, c, (mx, my + g),  (mx, my + sz), 2)

    def _draw(self) -> None:
        state = self._state.current_state

        if state == GameState.START:
            self._start_screen.draw(self._screen)

        elif state == GameState.INSTRUCTIONS:
            self._instr_screen.draw(self._screen)

        elif state == GameState.SETTINGS:
            self._settings_screen.draw(self._screen)

        elif state == GameState.PLAYING:
            self._screen.fill(_BG_COLOR)
            if self._target:
                self._target.draw(self._screen)
            time_left = max(0.0, (GAME_DURATION * 1000 - self._game_timer) / 1000)
            self._hud.draw(self._screen, time_left)
            self._feedback.draw(self._screen, self._fonts["medium"])
            self._draw_crosshair(self._screen)

        elif state == GameState.PAUSED:
            self._screen.blit(self._game_frame, (0, 0))
            self._pause_screen.draw(self._screen)
            self._draw_crosshair(self._screen)

        elif state == GameState.RESULTS:
            self._results_screen.draw(self._screen)

        pygame.display.flip()

    @staticmethod
    def _quit() -> None:
        pygame.quit()
        sys.exit()
