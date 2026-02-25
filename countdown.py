from settings import *
from target import Target
import pygame, random

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color, font):
        super().__init__()
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = pygame.time.get_ticks()
        self.ttl = 600 
        
    def update(self):
        self.rect.y -= 2 
        if pygame.time.get_ticks() - self.spawn_time > self.ttl:
            self.kill()
class Countdown():
    def __init__(self, seconds, target_size="Normal", difficulty="Medium"):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(COUNTDOWN_FONT, 80)
        self.float_font = pygame.font.Font(COUNTDOWN_FONT, 40)
        self.floating_texts = pygame.sprite.Group()
        self.decrement_time = pygame.time.get_ticks()
        self.should_decrement = False
        self.time_left = int(seconds)
        self.initial_countdown_length = self.time_left
        self.target_group = pygame.sprite.Group()
        self.targets_spawned = 0
        self.hits = 0
        self.time_outs = 0
        self.target_size = target_size
        self.difficulty = difficulty
        self.score = 0
        self.score_font = pygame.font.Font(COUNTDOWN_FONT, 60)
        self.reaction_times = []
    def add_floating_text(self, x, y, text, color):
        text_sprite = FloatingText(x, y, text, color, self.float_font)
        self.floating_texts.add(text_sprite)
        
    def cooldowns(self):
        curr_time = pygame.time.get_ticks()

        if not self.should_decrement and self.time_left > 0:
            if curr_time - self.decrement_time > 999:
                self.should_decrement = True

    def draw_timer(self):
        if self.should_decrement:
            self.time_left -= 1
            self.decrement_time = pygame.time.get_ticks()
            self.should_decrement = False
        if self.time_left > 0:
            count_string = str(self.time_left)
        else:
            count_string = ""

        color = TEXT_COLOR
        offset_x, offset_y = 0, 0
        if 0 < self.time_left <= 5:
            color = (255, 50, 50) 
            offset_x = random.randint(-4, 4) 
            offset_y = random.randint(-4, 4)
        
        count_surf = self.font.render(count_string, True, color, None)
        x, y = WIDTH - 20 + offset_x, HEIGHT - 10 + offset_y
        count_rect = count_surf.get_rect(bottomright = (x, y))
        self.display_surface.blit(count_surf, count_rect)

    def draw_score(self):
        score_text = f"SCORE: {self.score:,}" 
        score_surf = self.score_font.render(score_text, True, TEXT_COLOR)
        score_rect = score_surf.get_rect(midtop=(WIDTH // 2, 20)) 
        self.display_surface.blit(score_surf, score_rect)
        
    def spawn_target(self):
        # 1. Ánh xạ chữ "Large/Normal/Small" thành kích thước pixel cụ thể
        size_mapping = {"Large": 90, "Normal": 60, "Small": 30}
        target_width = size_mapping.get(self.target_size, 60)
        
        # 2. Bán kính r bây giờ sẽ thay đổi linh hoạt theo size
        r = target_width // 2 
        diff_mapping = {"Easy": 2500, "Medium": 1500, "Hard": 800}
        ttl = diff_mapping.get(self.difficulty, 1500)
        if self.time_left > 0 and len(self.target_group) < 1:
            x = random.randint(r, WIDTH - r)
            y = random.randint(r, HEIGHT - r)
            
            # 3. Truyền thêm size cho Target
            spawned_target = Target(x, y, time_to_live=ttl, target_size=self.target_size) 
            self.target_group.add(spawned_target)
            self.targets_spawned += 1
            
        self.target_group.draw(self.display_surface)

    def pause_offset(self, offset):
        self.decrement_time += offset
        for target in self.target_group:
            target.spawn_time += offset
        for text in self.floating_texts:
            text.spawn_time += offset
            
    def update(self):
        self.cooldowns()
        self.draw_timer()
        self.draw_score()
        # Quét qua các target để check TTL timeout mỗi frame
        for target in self.target_group:
            target.update()
            if target.is_timeout:
                self.time_outs += 1 
                # Hiện chữ MISS màu đỏ khi target hết giờ tự hủy
                self.add_floating_text(target.rect.centerx, target.rect.centery, "MISS!", (255, 50, 50))
                
        self.spawn_target()
        self.floating_texts.update()
        self.floating_texts.draw(self.display_surface)