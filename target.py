from settings import *
import pygame

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, time_to_live = 2000, target_size="Normal", *groups):
        super().__init__(*groups)
        pygame.mixer.init()
        
        # 1. Load ảnh gốc
        original_image = pygame.image.load(TARGET_IMAGE).convert_alpha()
        
        # 2. Tính toán pixel dựa trên tùy chọn
        size_mapping = {"Large": 90, "Normal": 60, "Small": 30}
        new_size = size_mapping.get(target_size, 60)
        
        self.radius = new_size // 2
        # 3. Resize ảnh theo kích thước mới
        self.image = pygame.transform.scale(original_image, (new_size, new_size))
        
        # 4. Đổi topleft thành center
        self.rect = self.image.get_rect(center = (x, y))
        
        self.hit_sound = pygame.mixer.Sound('audio/hit.mp3')
        self.hit_channel = pygame.mixer.Channel(5)
        self.spawn_time = pygame.time.get_ticks()
        self.time_to_live = time_to_live
        self.is_timeout = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.time_to_live:
            self.is_timeout = True
            self.kill()

