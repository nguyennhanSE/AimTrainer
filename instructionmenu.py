import pygame
from settings import *
from mainmenu import Button 

class InstructionMenu():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.title_font = pygame.font.Font(COUNTDOWN_FONT, 100)
        self.text_font = pygame.font.Font(COUNTDOWN_FONT, 45)
        self.button_font = pygame.font.Font(COUNTDOWN_FONT, 50)
        
        self.text_color = (255, 255, 255)
        
        center_x = WIDTH // 2
        self.start_y = HEIGHT // 2 - 100
        btn_w, btn_h = 500, 80
        
        # Tạo nút Back to Menu
        self.buttons = {
            "back": Button("Back to Menu", center_x - btn_w//2, HEIGHT - 180, btn_w, btn_h, self.button_font, (150, 50, 50), (200, 70, 70), self.text_color)
        }

        # Nội dung hướng dẫn luật chơi
        self.instructions = [
            "HOW TO PLAY",
            "",
            "- Targets appear at random positions on the screen.",
            "- Click them as quickly and accurately as possible.",
            "- If a target disappears before you click, it's a MISS.",
            "- Get the highest score before the time runs out!"
        ]

    def update(self):
        # Vẽ background gốc
        bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.display_surface.blit(bg_image, (0, 0))
        
        # Vẽ lớp phủ mờ (overlay) tối hơn chút để chữ dễ đọc
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210)) 
        self.display_surface.blit(overlay, (0, 0))

        # Render Title
        title_text = self.title_font.render("INSTRUCTIONS", True, self.text_color)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//5))
        self.display_surface.blit(title_text, title_rect)

        # Render từng dòng text hướng dẫn
        for i, line in enumerate(self.instructions):
            text_surf = self.text_font.render(line, True, self.text_color)
            text_rect = text_surf.get_rect(center=(WIDTH//2, self.start_y + i * 55))
            self.display_surface.blit(text_surf, text_rect)

        # Cập nhật và vẽ nút Back
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.check_hover(mouse_pos)
            btn.draw(self.display_surface)