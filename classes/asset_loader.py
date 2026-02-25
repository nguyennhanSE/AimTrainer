import os
import pygame

_BASE       = os.path.join(os.path.dirname(__file__), "..")
_FONTS_DIR  = os.path.join(_BASE, "assets", "fonts")
_SOUNDS_DIR = os.path.join(_BASE, "sounds")

_FALLBACK_FONT = "segoeui"


class AssetLoader:

    def load_fonts(self) -> dict[str, pygame.font.Font]:
        from constants import FONT_SMALL, FONT_MEDIUM, FONT_LARGE, FONT_TITLE

        sizes = {
            "small":  FONT_SMALL,
            "medium": FONT_MEDIUM,
            "large":  FONT_LARGE,
            "title":  FONT_TITLE,
        }

        fonts: dict[str, pygame.font.Font] = {}
        for name, size in sizes.items():
            font_path = os.path.join(_FONTS_DIR, "main.ttf")
            if os.path.isfile(font_path):
                fonts[name] = pygame.font.Font(font_path, size)
            else:
                fonts[name] = pygame.font.SysFont(_FALLBACK_FONT, size)

        fonts["small_bold"]  = self._make_bold(FONT_SMALL)
        fonts["medium_bold"] = self._make_bold(FONT_MEDIUM)
        fonts["large_bold"]  = self._make_bold(FONT_LARGE)

        return fonts

    def load_sounds(self) -> dict[str, pygame.mixer.Sound | None]:
        files = {
            "hit":  "hit.mp3",
            "shot": "shot.mp3",
        }

        sounds: dict[str, pygame.mixer.Sound | None] = {}
        for key, filename in files.items():
            path = os.path.join(_SOUNDS_DIR, filename)
            sounds[key] = self._load_sound(path)

        return sounds

    @staticmethod
    def play_music(filename: str, loops: int = -1, volume: float = 0.5) -> None:
        path = os.path.join(_SOUNDS_DIR, filename)
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
        except Exception:
            pass

    @staticmethod
    def stop_music() -> None:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def _make_bold(self, size: int) -> pygame.font.Font:
        font_path = os.path.join(_FONTS_DIR, "main-bold.ttf")
        if os.path.isfile(font_path):
            return pygame.font.Font(font_path, size)
        return pygame.font.SysFont(_FALLBACK_FONT, size, bold=True)

    @staticmethod
    def _load_sound(path: str) -> "pygame.mixer.Sound | None":
        try:
            return pygame.mixer.Sound(path)
        except Exception:
            return None
