from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from classes.score_manager import ScoreManager

WHITE          = (255, 255, 255)
BLACK          = (0,   0,   0)
GRAY           = (180, 180, 180)
DARK_GRAY      = (40,  40,  40)
YELLOW         = (255, 215, 0)
RED            = (200, 50,  50)
GREEN          = (60,  180, 60)
BLUE           = (50,  120, 200)
DARK_OVERLAY   = (0,   0,   0, 160)
BTN_NORMAL     = (55,  55,  70)
BTN_HOVER      = (90,  90,  120)
BTN_BORDER     = (120, 120, 160)
BTN_TEXT       = (230, 230, 255)
TITLE_COLOR    = (255, 220, 60)
SUBTITLE_COLOR = (200, 200, 200)


def _make_font(size: int) -> pygame.font.Font:
    return pygame.font.SysFont("segoeui", size, bold=False)


def _make_bold_font(size: int) -> pygame.font.Font:
    return pygame.font.SysFont("segoeui", size, bold=True)


def _draw_button(
    surface: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    font: pygame.font.Font,
    hovered: bool = False,
) -> None:
    bg_color = BTN_HOVER if hovered else BTN_NORMAL
    pygame.draw.rect(surface, bg_color,   rect, border_radius=8)
    pygame.draw.rect(surface, BTN_BORDER, rect, width=2, border_radius=8)
    text_surf = font.render(label, True, BTN_TEXT)
    surface.blit(text_surf, text_surf.get_rect(center=rect.center))


def _render_shadow(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    center: tuple[int, int],
    color: tuple[int, int, int] = WHITE,
    shadow_color: tuple[int, int, int] = (20, 20, 20),
    shadow_offset: int = 3,
) -> None:
    shadow_surf = font.render(text, True, shadow_color)
    text_surf   = font.render(text, True, color)
    sx, sy = center[0] + shadow_offset, center[1] + shadow_offset
    surface.blit(shadow_surf, shadow_surf.get_rect(center=(sx, sy)))
    surface.blit(text_surf,   text_surf.get_rect(center=center))


class StartScreen:

    _BUTTON_W   = 260
    _BUTTON_H   = 48
    _BUTTON_GAP = 14

    def __init__(self, width: int, height: int) -> None:
        self._w = width
        self._h = height

        self._title_font    = _make_bold_font(72)
        self._subtitle_font = _make_font(22)
        self._btn_font      = _make_font(24)

        cx = width // 2
        labels_actions = [
            ("Start Game",   "start"),
            ("Instructions", "instructions"),
            ("Statistics",   "statistics"),
            ("Settings",     "settings"),
            ("Exit Game",    "exit"),
        ]

        start_y = height // 2 + 10
        self._buttons: list[tuple[pygame.Rect, str]] = []
        for i, (label, action) in enumerate(labels_actions):
            y = start_y + i * (self._BUTTON_H + self._BUTTON_GAP)
            rect = pygame.Rect(0, 0, self._BUTTON_W, self._BUTTON_H)
            rect.centerx = cx
            rect.y = y
            self._buttons.append((rect, action))

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for rect, action in self._buttons:
                if rect.collidepoint(pos):
                    return action
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(DARK_GRAY)
        pygame.draw.rect(surface, (30, 30, 50), pygame.Rect(0, 0, self._w, 8))
        
        _render_shadow(
            surface, "AIM TRAINER",
            self._title_font,
            (self._w // 2, self._h // 2 - 80),
            color=TITLE_COLOR,
        )
        
        sub_surf = self._subtitle_font.render("Test your reflexes", True, SUBTITLE_COLOR)
        surface.blit(sub_surf, sub_surf.get_rect(center=(self._w // 2, self._h // 2 - 20)))

        mouse_pos = pygame.mouse.get_pos()
        labels = ["Start Game", "Instructions", "Statistics", "Settings", "Exit Game"]
        for (rect, _), label in zip(self._buttons, labels):
            _draw_button(surface, rect, label, self._btn_font, hovered=rect.collidepoint(mouse_pos))


class PauseScreen:

    _BUTTON_W   = 240
    _BUTTON_H   = 50
    _BUTTON_GAP = 16

    def __init__(self, width: int, height: int) -> None:
        self._w = width
        self._h = height

        self._title_font = _make_bold_font(64)
        self._btn_font   = _make_font(24)

        cx = width // 2
        labels_actions = [
            ("Resume",       "resume"),
            ("Restart",      "restart"),
            ("Settings",     "settings"),
            ("Quit to Menu", "menu"),
        ]

        start_y = height // 2 
        self._buttons: list[tuple[pygame.Rect, str]] = []
        for i, (label, action) in enumerate(labels_actions):
            y = start_y + i * (self._BUTTON_H + self._BUTTON_GAP)
            rect = pygame.Rect(0, 0, self._BUTTON_W, self._BUTTON_H)
            rect.centerx = cx
            rect.y = y
            self._buttons.append((rect, action))

        self._overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self._overlay.fill(DARK_OVERLAY)

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for rect, action in self._buttons:
                if rect.collidepoint(pos):
                    return action
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._overlay, (0, 0))
        _render_shadow(
            surface, "PAUSED",
            self._title_font,
            (self._w // 2, self._h // 2 - 60),
            color=WHITE,
        )
        mouse_pos = pygame.mouse.get_pos()
        labels = ["Resume", "Restart", "Settings", "Quit to Menu"]
        for (rect, _), label in zip(self._buttons, labels):
            _draw_button(surface, rect, label, self._btn_font, hovered=rect.collidepoint(mouse_pos))


class ResultsScreen:

    _BUTTON_W   = 200
    _BUTTON_H   = 48
    _BUTTON_GAP = 14

    def __init__(self, width: int, height: int, score_manager: ScoreManager) -> None:
        self._w  = width
        self._h  = height
        self._sm = score_manager

        self._title_font = _make_bold_font(52)
        self._stat_font  = _make_font(26)
        self._label_font = _make_bold_font(26)
        self._btn_font   = _make_font(22)

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

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for rect, action in self._buttons:
                if rect.collidepoint(pos):
                    return action
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(DARK_GRAY)

        cx = self._w // 2

        _render_shadow(surface, "RESULTS", self._title_font, (cx, 60), color=TITLE_COLOR)
        pygame.draw.line(surface, BTN_BORDER, (cx - 200, 100), (cx + 200, 100), 2)

        stats = [
            ("Score",              f"{self._sm.score}",                     YELLOW),
            ("Max Combo",          f"{self._sm.max_combo}x",                (255, 150, 0)),
            ("Hits",               f"{self._sm.hits}",                      GREEN),
            ("Misses",             f"{self._sm.misses}",                    RED),
            ("Accuracy",           f"{self._sm.accuracy:.1f}%",             WHITE),
            ("Avg Reaction",       f"{self._sm.avg_reaction_time:.0f} ms",  WHITE),
            ("Best Reaction",      f"{self._sm.best_reaction_time:.0f} ms", YELLOW),
        ]

        row_h   = 38
        start_y = 120

        for i, (label, value, color) in enumerate(stats):
            y = start_y + i * row_h
            label_surf = self._label_font.render(label + ":", True, GRAY)
            surface.blit(label_surf, label_surf.get_rect(midright=(cx - 10, y + row_h // 2)))
            value_surf = self._stat_font.render(value, True, color)
            surface.blit(value_surf, value_surf.get_rect(midleft=(cx + 10, y + row_h // 2)))

        mouse_pos = pygame.mouse.get_pos()
        labels = ["Play Again", "Main Menu", "Exit"]
        for (rect, _), label in zip(self._buttons, labels):
            _draw_button(surface, rect, label, self._btn_font, hovered=rect.collidepoint(mouse_pos))


class InstructionsScreen:

    _BUTTON_W = 200
    _BUTTON_H = 48

    def __init__(self, width: int, height: int) -> None:
        self._w = width
        self._h = height

        self._title_font     = _make_bold_font(52)
        self._body_font      = _make_font(24)
        self._highlight_font = _make_bold_font(24)
        self._btn_font       = _make_font(22)

        self._back_btn = pygame.Rect(0, 0, self._BUTTON_W, self._BUTTON_H)
        self._back_btn.center = (width // 2, height - 60)

        
        self._instructions = [
            ("target", "Shoot Targets:", " Left click on them before they disappear."),
            ("time",   "Be Quick:",      " Targets shrink and expire faster over time."),
            ("score",  "Combo Bonus:",   " Earn extra points for fast reactions."),
            ("key",    "Pause Game:",    " Press ESC at any time to take a break."),
            ("crown",  "Time Limit:",    " You have 60 seconds. Get the high score!")
        ]

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._back_btn.collidepoint(pygame.mouse.get_pos()):
                return "back"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(DARK_GRAY)
        pygame.draw.rect(surface, (30, 30, 50), pygame.Rect(0, 0, self._w, 8))

       
        _render_shadow(surface, "HOW TO PLAY", self._title_font,
                       (self._w // 2, 70), color=TITLE_COLOR)

        
        panel_w, panel_h = 750, 350
        panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
        panel_rect.center = (self._w // 2, self._h // 2)

        
        overlay = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (20, 20, 30, 150), overlay.get_rect(), border_radius=16)
        pygame.draw.rect(overlay, BTN_BORDER, overlay.get_rect(), width=2, border_radius=16)
        surface.blit(overlay, panel_rect.topleft)

        
        start_y = panel_rect.y + 50
        start_x = panel_rect.x + 40

        for i, (icon, hl_text, norm_text) in enumerate(self._instructions):
            y = start_y + i * 65
            icon_x = start_x + 30
            text_x = start_x + 80

            
            if icon == "target":
                pygame.draw.circle(surface, RED, (icon_x, y), 14)
                pygame.draw.circle(surface, WHITE, (icon_x, y), 10)
                pygame.draw.circle(surface, RED, (icon_x, y), 5)
            
            elif icon == "time":
                pygame.draw.circle(surface, BLUE, (icon_x, y), 15, 3)
                pygame.draw.line(surface, WHITE, (icon_x, y), (icon_x, y - 8), 2)
                pygame.draw.line(surface, WHITE, (icon_x, y), (icon_x + 6, y + 5), 2)
            
            elif icon == "score":
                pts_surf = _make_bold_font(18).render("+100", True, GREEN)
                surface.blit(pts_surf, pts_surf.get_rect(center=(icon_x, y)))
            
            elif icon == "key":
                key_rect = pygame.Rect(0, 0, 38, 26)
                key_rect.center = (icon_x, y)
                pygame.draw.rect(surface, GRAY, key_rect, border_radius=4)
                pygame.draw.rect(surface, WHITE, key_rect, width=2, border_radius=4)
                k_surf = _make_bold_font(12).render("ESC", True, BLACK)
                surface.blit(k_surf, k_surf.get_rect(center=(icon_x, y)))
            
            elif icon == "crown":
                
                pygame.draw.polygon(surface, YELLOW, [
                    (icon_x - 14, y - 10), (icon_x - 7, y + 2),  (icon_x, y - 12),
                    (icon_x + 7, y + 2),   (icon_x + 14, y - 10),
                    (icon_x + 10, y + 12), (icon_x - 10, y + 12)
                ])

            
            hl_surf = self._highlight_font.render(hl_text, True, TITLE_COLOR)
            surface.blit(hl_surf, (text_x, y - hl_surf.get_height() // 2))

            norm_surf = self._body_font.render(norm_text, True, WHITE)
            surface.blit(norm_surf, (text_x + hl_surf.get_width(), y - norm_surf.get_height() // 2))

        
        mouse_pos = pygame.mouse.get_pos()
        _draw_button(surface, self._back_btn, "Back", self._btn_font,
                     hovered=self._back_btn.collidepoint(mouse_pos))

class SettingsScreen:
    _BUTTON_W = 200
    _BUTTON_H = 48

    def __init__(self, width: int, height: int) -> None:
        self._w = width
        self._h = height

        self._title_font = _make_bold_font(48)
        self._label_font = _make_bold_font(24)
        self._val_font   = _make_font(24)
        self._btn_font   = _make_font(22)

        # Nút Back
        self._back_btn = pygame.Rect(0, 0, self._BUTTON_W, self._BUTTON_H)
        self._back_btn.center = (width // 2, height - 50)

        cx = width // 2
        start_y = 120
        gap_y = 52 # Thu gọn khoảng cách các dòng lại một chút để vừa 6 tính năng
        
        # --- Đã giãn khoảng cách 2 nút ra xa nhau ---
        btn_left_x  = cx - 30   
        btn_right_x = cx + 120
        
        # 1. Volume
        self._vol_down   = pygame.Rect(btn_left_x, start_y, 40, 40)
        self._vol_up     = pygame.Rect(btn_right_x, start_y, 40, 40)
        # 2. Duration
        self._dur_down   = pygame.Rect(btn_left_x, start_y + gap_y, 40, 40)
        self._dur_up     = pygame.Rect(btn_right_x, start_y + gap_y, 40, 40)
        # 3. Difficulty
        self._diff_down  = pygame.Rect(btn_left_x, start_y + gap_y*2, 40, 40)
        self._diff_up    = pygame.Rect(btn_right_x, start_y + gap_y*2, 40, 40)
        # 4. Target Size
        self._size_down  = pygame.Rect(btn_left_x, start_y + gap_y*3, 40, 40)
        self._size_up    = pygame.Rect(btn_right_x, start_y + gap_y*3, 40, 40)
        # 5. Crosshair Size
        self._cross_down = pygame.Rect(btn_left_x, start_y + gap_y*4, 40, 40)
        self._cross_up   = pygame.Rect(btn_right_x, start_y + gap_y*4, 40, 40)
        # 6. Mouse Speed 
        self._sens_down  = pygame.Rect(btn_left_x, start_y + gap_y*5, 40, 40)
        self._sens_up    = pygame.Rect(btn_right_x, start_y + gap_y*5, 40, 40)

        # Trạng thái của các settings
        self.diff_opts  = ["Easy", "Normal", "Hard"]
        self.diff_idx   = 0 

        self.size_opts  = ["Small", "Medium", "Large"]
        self.size_idx   = 2

        self.cross_opts = ["Small", "Medium", "Large"]
        self.cross_idx  = 2
        
        self.sens_opts  = ["0.5x", "0.8x", "1.0x", "1.2x", "1.5x", "2.0x"]
        self.sens_idx   = 2 

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        import constants 
        import sys

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            m_pos = event.pos
            if self._back_btn.collidepoint(m_pos):
                return "back"
            
            curr_vol = round(pygame.mixer.music.get_volume(), 1)
            
            if self._vol_down.collidepoint(m_pos):     pygame.mixer.music.set_volume(max(0.0, curr_vol - 0.1))
            elif self._vol_up.collidepoint(m_pos):     pygame.mixer.music.set_volume(min(1.0, curr_vol + 0.1))
            
            elif self._dur_down.collidepoint(m_pos):   constants.GAME_DURATION = max(10, constants.GAME_DURATION - 10)
            elif self._dur_up.collidepoint(m_pos):     constants.GAME_DURATION = min(300, constants.GAME_DURATION + 10)
            
            elif self._diff_down.collidepoint(m_pos):  self.diff_idx = max(0, self.diff_idx - 1)
            elif self._diff_up.collidepoint(m_pos):    self.diff_idx = min(len(self.diff_opts) - 1, self.diff_idx + 1)
            
            elif self._size_down.collidepoint(m_pos):  self.size_idx = max(0, self.size_idx - 1)
            elif self._size_up.collidepoint(m_pos):    self.size_idx = min(len(self.size_opts) - 1, self.size_idx + 1)

            elif self._cross_down.collidepoint(m_pos): self.cross_idx = max(0, self.cross_idx - 1)
            elif self._cross_up.collidepoint(m_pos):   self.cross_idx = min(len(self.cross_opts) - 1, self.cross_idx + 1)
            
            elif self._sens_down.collidepoint(m_pos):  self.sens_idx = max(0, self.sens_idx - 1)
            elif self._sens_up.collidepoint(m_pos):    self.sens_idx = min(len(self.sens_opts) - 1, self.sens_idx + 1)

            # --- LƯU CHÍNH THỨC VÀO CONSTANTS ĐỂ GAME CẬP NHẬT NGAY ---
            ttl_vals = [3000, 2000, 1500]
            constants.INITIAL_TTL = ttl_vals[self.diff_idx]
            
            rad_vals = [20, 30, 40]
            constants.INITIAL_RADIUS = rad_vals[self.size_idx]

            cross_vals = [10, 16, 24]
            constants.CROSSHAIR_SIZE = cross_vals[self.cross_idx]
                
            sens_float_vals = [0.5, 0.8, 1.0, 1.2, 1.5, 2.0]
            constants.MOUSE_SENSITIVITY = sens_float_vals[self.sens_idx]

        return None
    
    def draw(self, surface: pygame.Surface) -> None:
        import constants
        surface.fill(DARK_GRAY)
        
        _render_shadow(surface, "SETTINGS", self._title_font, (self._w // 2, 50), color=TITLE_COLOR)
        cx = self._w // 2

        curr_vol_str = f"{int(round(pygame.mixer.music.get_volume(), 1) * 100)}%"

        items = [
            ("Music Volume:", curr_vol_str, self._vol_down, self._vol_up),
            ("Game Duration:", f"{constants.GAME_DURATION}s", self._dur_down, self._dur_up),
            ("Difficulty:", self.diff_opts[self.diff_idx], self._diff_down, self._diff_up),
            ("Target Size:", self.size_opts[self.size_idx], self._size_down, self._size_up),
            ("Crosshair Size:", self.cross_opts[self.cross_idx], self._cross_down, self._cross_up),
            ("Mouse Speed:", self.sens_opts[self.sens_idx], self._sens_down, self._sens_up)
        ]

        y = 120
        gap_y = 52
        for label_text, val_text, btn_down, btn_up in items:
            label_surf = self._label_font.render(label_text, True, GRAY)
            # Chữ bên trái cách mép giữa màn hình một khoảng
            surface.blit(label_surf, label_surf.get_rect(midright=(cx - 40, y + 20)))
            
            _draw_button(surface, btn_down, "<", self._btn_font)
            
            val_surf = self._val_font.render(val_text, True, WHITE)
            # Chữ ở giữa 2 nút < >
            surface.blit(val_surf, val_surf.get_rect(center=(cx + 65, y + 20)))
            
            _draw_button(surface, btn_up, ">", self._btn_font)
            
            y += gap_y

        mouse_pos = pygame.mouse.get_pos()
        _draw_button(surface, self._back_btn, "Back", self._btn_font,
                     hovered=self._back_btn.collidepoint(mouse_pos))
        
class ModeSelectScreen:

    def __init__(self, width: int, height: int) -> None:
        self._w = width
        self._h = height

        self._title_font = _make_bold_font(52)
        self._desc_font  = _make_font(18)
        self._btn_font   = _make_bold_font(28)
        self._back_font  = _make_font(24)

        cx = width // 2
        cy = height // 2

        # --- Kích thước thẻ (Card) cho các chế độ ---
        card_w = 320
        card_h = 140
        
        # Tọa độ thẻ Basic Mode (Đẩy sang Trái)
        self.rect_basic = pygame.Rect(0, 0, card_w, card_h)
        self.rect_basic.center = (cx - 170, cy)
        
        # Tọa độ thẻ Dynamic Mode (Đẩy sang Phải)
        self.rect_dynamic = pygame.Rect(0, 0, card_w, card_h)
        self.rect_dynamic.center = (cx + 170, cy)

        # Nút Back to Menu (Ở dưới cùng)
        self.rect_back = pygame.Rect(0, 0, 200, 50)
        self.rect_back.center = (cx, height - 70)

        # Danh sách chứa (Rect hitbox, Tên action, Tên hiển thị, Mô tả)
        self._buttons = [
            (self.rect_basic, "mode_basic", "BASIC MODE", "Static targets to train pure reflex."),
            (self.rect_dynamic, "mode_dynamic", "DYNAMIC MODE", "Moving targets! Test your tracking."),
            (self.rect_back, "back", "Back", "")
        ]

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        # Bấm ESC để quay lại Menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for rect, action, _, _ in self._buttons:
                if rect.collidepoint(pos):
                    return action
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(DARK_GRAY)
        pygame.draw.rect(surface, (30, 30, 50), pygame.Rect(0, 0, self._w, 8))
        
        _render_shadow(surface, "SELECT GAME MODE", self._title_font, (self._w // 2, 90), color=TITLE_COLOR)

        mouse_pos = pygame.mouse.get_pos()
        
        for rect, action, label, desc in self._buttons:
            is_back = (action == "back")
            is_hovered = rect.collidepoint(mouse_pos)
            
            # --- TÙY CHỈNH MÀU SẮC THEO TỪNG NÚT ---
            if is_back:
                bg_color = BTN_HOVER if is_hovered else BTN_NORMAL
                border_color = BTN_BORDER
                text_color = BTN_TEXT
                font = self._back_font
            else:
                # Mode Basic (Tone Xanh) và Dynamic (Tone Đỏ)
                if is_hovered:
                    bg_color = (60, 80, 110) if action == "mode_basic" else (110, 60, 60)
                    border_color = TITLE_COLOR
                else:
                    bg_color = (40, 50, 70) if action == "mode_basic" else (70, 40, 40)
                    border_color = GRAY
                text_color = WHITE
                font = self._btn_font

            # Vẽ phần hộp (Background + Viền)
            pygame.draw.rect(surface, bg_color, rect, border_radius=12)
            pygame.draw.rect(surface, border_color, rect, width=2, border_radius=12)

            # Vẽ chữ bên trong
            if is_back:
                text_surf = font.render(label, True, text_color)
                surface.blit(text_surf, text_surf.get_rect(center=rect.center))
            else:
                # Tiêu đề chế độ (Nửa trên của Card)
                highlight = TITLE_COLOR if is_hovered else text_color
                text_surf = font.render(label, True, highlight)
                surface.blit(text_surf, text_surf.get_rect(center=(rect.centerx, rect.centery - 15)))
                
                # Mô tả chế độ (Nửa dưới của Card)
                desc_surf = self._desc_font.render(desc, True, (200, 200, 200))
                surface.blit(desc_surf, desc_surf.get_rect(center=(rect.centerx, rect.centery + 25)))
                
import json
import os

class StatsScreen:
    def __init__(self, width: int, height: int) -> None:
        self._w = width
        self._h = height
        self._title_font = _make_bold_font(48)
        self._label_font = _make_bold_font(22)
        self._val_font   = _make_font(22)
        self._btn_font   = _make_font(22)

        self._back_btn = pygame.Rect(0, 0, 200, 48)
        self._back_btn.center = (width // 2, height - 50)
        self.data = []

    def load_data(self) -> None:
        """Đọc file JSON mỗi khi mở màn hình này lên"""
        self.data = []
        if os.path.exists("stats.json"):
            try:
                with open("stats.json", "r") as f:
                    self.data = json.load(f)
            except Exception:
                pass

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return "back"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._back_btn.collidepoint(event.pos): return "back"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(DARK_GRAY)
        pygame.draw.rect(surface, (30, 30, 50), pygame.Rect(0, 0, self._w, 8))
        _render_shadow(surface, "PLAYER STATISTICS", self._title_font, (self._w // 2, 50), color=TITLE_COLOR)

        if not self.data:
            msg = self._val_font.render("No game data found. Play a round first!", True, GRAY)
            surface.blit(msg, msg.get_rect(center=(self._w // 2, self._h // 2)))
        else:
            # --- TÍNH TOÁN KỶ LỤC ---
            total_games = len(self.data)
            high_score = max((d.get("score", 0) for d in self.data), default=0)
            best_acc = max((d.get("accuracy", 0) for d in self.data), default=0)
            valid_rt = [d.get("best_reaction", 0) for d in self.data if d.get("best_reaction", 0) > 0]
            best_react = min(valid_rt) if valid_rt else 0

            # --- VẼ BẢNG KỶ LỤC (BÊN TRÁI) ---
            start_x, start_y = 60, 150
            pygame.draw.rect(surface, (35, 35, 45), (start_x - 20, start_y - 20, 300, 240), border_radius=12)
            pygame.draw.rect(surface, GRAY, (start_x - 20, start_y - 20, 300, 240), width=2, border_radius=12)
            
            stats = [
                ("Total Matches:", f"{total_games}", WHITE),
                ("High Score:", f"{high_score}", YELLOW),
                ("Best Accuracy:", f"{best_acc}%", GREEN),
                ("Best Reaction:", f"{best_react} ms", TITLE_COLOR),
            ]
            for i, (lbl, val, col) in enumerate(stats):
                y = start_y + i * 50
                surface.blit(self._label_font.render(lbl, True, GRAY), (start_x, y))
                val_surf = self._val_font.render(val, True, col)
                surface.blit(val_surf, val_surf.get_rect(topright=(start_x + 260, y)))

            # --- VẼ BIỂU ĐỒ 10 TRẬN GẦN NHẤT (BÊN PHẢI) ---
            graph_x, graph_y, graph_w, graph_h = 420, 130, 320, 240
            pygame.draw.rect(surface, (30, 30, 30), (graph_x, graph_y, graph_w, graph_h), border_radius=8)
            pygame.draw.rect(surface, GRAY, (graph_x, graph_y, graph_w, graph_h), width=2, border_radius=8)
            
            title = self._val_font.render("Recent Scores (Last 10)", True, WHITE)
            surface.blit(title, title.get_rect(center=(graph_x + graph_w // 2, graph_y + 20)))

            recent = [d.get("score", 0) for d in self.data[-10:]]
            if recent:
                max_s = max(recent) if max(recent) > 0 else 1
                bar_w = 20
                gap = (graph_w - 40 - len(recent) * bar_w) // (len(recent) + 1)
                
                for i, s in enumerate(recent):
                    b_height = int((s / max_s) * 150) # Chiều cao tối đa 150px
                    bx = graph_x + 20 + gap + i * (bar_w + gap)
                    by = graph_y + graph_h - 20 - b_height
                    color = YELLOW if s == high_score else BLUE
                    pygame.draw.rect(surface, color, (bx, by, bar_w, b_height), border_radius=3)

        mouse_pos = pygame.mouse.get_pos()
        _draw_button(surface, self._back_btn, "Back", self._btn_font, hovered=self._back_btn.collidepoint(mouse_pos))