import pygame
from settings import *
from mainmenu import Button 

class PauseMenu():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.title_font = pygame.font.Font(COUNTDOWN_FONT, 100)
        self.button_font = pygame.font.Font(COUNTDOWN_FONT, 50)
        
        center_x = WIDTH // 2
        start_y = HEIGHT // 2 - 100 
        btn_w, btn_h = 400, 80
        spacing = 110
        
        
        self.buttons = {
            "resume": Button("Resume Game", center_x - btn_w//2, start_y, btn_w, btn_h, self.button_font, (50, 50, 50), (100, 100, 100), (255, 255, 255)),
            "settings": Button("Settings", center_x - btn_w//2, start_y + spacing, btn_w, btn_h, self.button_font, (50, 50, 50), (100, 100, 100), (255, 255, 255)),
            "quit": Button("Quit to Menu", center_x - btn_w//2, start_y + spacing*2, btn_w, btn_h, self.button_font, (150, 50, 50), (200, 70, 70), (255, 255, 255))
        }

    def update(self):
        # Vẽ lớp phủ mờ (overlay) đen
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        self.display_surface.blit(overlay, (0, 0))

        # Render Title
        title_text = self.title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3.5))
        self.display_surface.blit(title_text, title_rect)

        # Cập nhật và vẽ các nút
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.check_hover(mouse_pos)
            btn.draw(self.display_surface)