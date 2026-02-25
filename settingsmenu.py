import pygame
from settings import *
from mainmenu import Button 

class SettingsMenu():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.title_font = pygame.font.Font(COUNTDOWN_FONT, 100)
        self.button_font = pygame.font.Font(COUNTDOWN_FONT, 45)
        
        self.btn_color = (50, 50, 50)
        self.btn_hover_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        
        center_x = WIDTH // 2
        start_y = HEIGHT // 2 - 150
        btn_w, btn_h = 500, 80
        spacing = 110
        
        # Lưu trữ các lựa chọn cài đặt
        self.duration_options = [5, 60, 90]
        self.current_duration_idx = 0 # Mặc định 60 giây theo yêu cầu MVP
        
        self.size_options = ["Large", "Normal", "Small"]
        self.current_size_idx = 1 # Mặc định Normal

        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.current_difficulty_idx = 1
        
        self.cursor_options = ["System", "Crosshair"]
        self.current_cursor_idx = 0
        # Tạo các nút
        self.buttons = {
            "duration": Button(f"Duration: {self.duration_options[self.current_duration_idx]}s", center_x - btn_w//2, start_y, btn_w, btn_h, self.button_font, self.btn_color, self.btn_hover_color, self.text_color),
            "size": Button(f"Target Size: {self.size_options[self.current_size_idx]}", center_x - btn_w//2, start_y + spacing, btn_w, btn_h, self.button_font, self.btn_color, self.btn_hover_color, self.text_color),
            "difficulty": Button(f"Difficulty: {self.difficulty_options[self.current_difficulty_idx]}", center_x - btn_w//2, start_y + spacing*2, btn_w, btn_h, self.button_font, self.btn_color, self.btn_hover_color, self.text_color),
            "cursor": Button(f"Cursor: {self.cursor_options[self.current_cursor_idx]}", center_x - btn_w//2, start_y + spacing*3, btn_w, btn_h, self.button_font, self.btn_color, self.btn_hover_color, self.text_color),
            "back": Button("Back", center_x - btn_w//2, start_y + spacing*4.2, btn_w, btn_h, self.button_font, (150, 50, 50), (200, 70, 70), self.text_color) 
        }

    # Hàm xử lý khi click vào nút Duration
    def toggle_duration(self):
        self.current_duration_idx = (self.current_duration_idx + 1) % len(self.duration_options)
        self.buttons["duration"].text = f"Duration: {self.duration_options[self.current_duration_idx]}s"

    # Hàm xử lý khi click vào nút Size
    def toggle_size(self):
        self.current_size_idx = (self.current_size_idx + 1) % len(self.size_options)
        self.buttons["size"].text = f"Target Size: {self.size_options[self.current_size_idx]}"

    def toggle_difficulty(self):
        self.current_difficulty_idx = (self.current_difficulty_idx + 1) % len(self.difficulty_options)
        self.buttons["difficulty"].text = f"Difficulty: {self.difficulty_options[self.current_difficulty_idx]}" 
    
    def toggle_cursor(self):
        self.current_cursor_idx = (self.current_cursor_idx + 1) % len(self.cursor_options)
        self.buttons["cursor"].text = f"Cursor: {self.cursor_options[self.current_cursor_idx]}"
        
    def update(self):
        # Vẽ background gốc
        bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.display_surface.blit(bg_image, (0, 0))
        
        # Vẽ lớp phủ mờ (overlay) cho menu Settings
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        self.display_surface.blit(overlay, (0, 0))

        # Render Title
        title_text = self.title_font.render("SETTINGS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        self.display_surface.blit(title_text, title_rect)

        # Cập nhật và vẽ các nút
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            btn.check_hover(mouse_pos)
            btn.draw(self.display_surface)