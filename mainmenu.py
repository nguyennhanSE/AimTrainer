from settings import *
import pygame

class Button:
    def __init__(self, text, x, y, width, height, font, bg_color, hover_color, text_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, surface):
        # Đổi màu nếu chuột đang hover
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # Vẽ nút với viền bo góc (border_radius) cho giao diện hiện đại
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        
        # Render text ở giữa nút
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

class MainMenuScreen():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # Giảm size chữ Title xuống một chút để nhường chỗ cho các nút
        self.font = pygame.font.Font(COUNTDOWN_FONT, 120) 
        self.button_font = pygame.font.Font(COUNTDOWN_FONT, 50)
        
        # Màu sắc cho UI
        self.btn_color = (50, 50, 50) # Xám đậm
        self.btn_hover_color = (100, 100, 100) # Xám nhạt khi hover
        self.text_color = (255, 255, 255)
        
        # Khởi tạo kích thước và vị trí các nút
        center_x = WIDTH // 2
        start_y = HEIGHT // 2 - 50
        btn_w, btn_h = 400, 80
        spacing = 110
        
        self.buttons = {
            "start": Button("Start Game", center_x - btn_w//2, start_y, btn_w, btn_h, self.button_font, self.btn_color, self.btn_hover_color, self.text_color),
            "instruction": Button("Instruction", center_x - btn_w//2, start_y + spacing, btn_w, btn_h, self.button_font, self.btn_color, self.btn_hover_color, self.text_color),
            "settings": Button("Settings", center_x - btn_w//2, start_y + spacing*2, btn_w, btn_h, self.button_font, self.btn_color, self.btn_hover_color, self.text_color),
            "exit": Button("Exit Game", center_x - btn_w//2, start_y + spacing*3, btn_w, btn_h, self.button_font, self.btn_color, self.btn_hover_color, self.text_color)
        }

    def update(self):
        # Load và vẽ background
        title_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.display_surface.blit(title_image, (0, 0))
        
        # Vẽ Title
        aim_trainer_text = self.font.render("AIM TRAINER", True, (255, 255, 255))
        aim_trainer_rect = aim_trainer_text.get_rect(center=(WIDTH//2, HEIGHT//3.5))
        self.display_surface.blit(aim_trainer_text, aim_trainer_rect)

        # Cập nhật trạng thái hover và vẽ các nút
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.check_hover(mouse_pos)
            btn.draw(self.display_surface)