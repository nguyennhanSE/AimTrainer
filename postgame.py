from settings import *
import pygame

class PostGame():
    def __init__(self, total_clicks, total_hits, time_outs, final_score, reaction_times):
        self.display_surface = pygame.display.get_surface()
        self.total_clicks, self.total_hits = total_clicks, total_hits
        self.time_outs = time_outs
        self.misses = (self.total_clicks - self.total_hits) + self.time_outs
        self.font = pygame.font.Font(COUNTDOWN_FONT, FONT_SIZE)
        self.base_font_size = 60
        self.multiplier = 1
        self.final_score = "{:,}".format(final_score)
        
        
        self.reaction_times = reaction_times
        if len(self.reaction_times) > 0:
            self.avg_reaction = int(sum(self.reaction_times) / len(self.reaction_times))
            self.best_reaction = min(self.reaction_times)
        else:
            self.avg_reaction = 0
            self.best_reaction = 0

        total_actions = self.total_clicks + self.time_outs
        if total_actions > 0:
            self.accuracy = round((self.total_hits / total_actions) * 100, 2)
        else:
            self.accuracy = 0
            
        self.score_font = pygame.font.Font(COUNTDOWN_FONT, self.base_font_size + (7 * self.total_hits))
        self.stats_font = pygame.font.Font(COUNTDOWN_FONT, self.base_font_size)

    def update(self):
        # Load background image and create text objects
        postgame_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        stats_numbers_text = self.score_font.render(f"SCORE: {self.final_score}", True, (255, 255, 255))
        
        hits_text = self.stats_font.render(f"HITS: {self.total_hits}", True, (255, 255, 255))
        misses_text = self.stats_font.render(f"MISSES: {self.misses}", True, (255, 255, 255))
        accuracy_text = self.stats_font.render(f"ACCURACY: {self.accuracy}%", True, (255, 255, 255))
        
        # BỔ SUNG: Render các dòng Text cho Reaction Time
        avg_text = self.stats_font.render(f"AVG REACTION: {self.avg_reaction}ms", True, (255, 255, 255))
        best_text = self.stats_font.render(f"BEST REACTION: {self.best_reaction}ms", True, (255, 255, 255))
        
        stats_percentage_text = self.stats_font.render(f"Press Space to Main Menu", True, (180, 180, 180)) 

        if stats_numbers_text.get_width() > 1920:
            new_height = int((stats_numbers_text.get_height() / stats_numbers_text.get_width()) * 1920)
            stats_numbers_text = pygame.transform.scale(stats_numbers_text, (1920, new_height))

        # Khởi tạo Rect
        game_over = game_over_text.get_bounding_rect()
        stats_numbers = stats_numbers_text.get_bounding_rect()
        hits_rect = hits_text.get_bounding_rect()
        misses_rect = misses_text.get_bounding_rect()
        accuracy_rect = accuracy_text.get_bounding_rect()
        avg_rect = avg_text.get_bounding_rect()
        best_rect = best_text.get_bounding_rect()
        stats_percentage = stats_percentage_text.get_bounding_rect()

        # Tính toán lại tổng chiều cao
        gap = 20
        height = (game_over_text.get_height() + gap + 
                  stats_numbers_text.get_height() + gap + 
                  hits_text.get_height() + gap + 
                  misses_text.get_height() + gap + 
                  accuracy_text.get_height() + gap + 
                  avg_text.get_height() + gap + 
                  best_text.get_height() + gap + 
                  stats_percentage_text.get_height())
                  
        final_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA) 

        # Căn chỉnh Y liên tiếp nhau
        game_over.centerx, game_over.y = 960, (1080 - height) / 2
        stats_numbers.centerx, stats_numbers.y = 960, game_over.bottom + gap
        hits_rect.centerx, hits_rect.y = 960, stats_numbers.bottom + gap
        misses_rect.centerx, misses_rect.y = 960, hits_rect.bottom + gap
        accuracy_rect.centerx, accuracy_rect.y = 960, misses_rect.bottom + gap
        avg_rect.centerx, avg_rect.y = 960, accuracy_rect.bottom + gap
        best_rect.centerx, best_rect.y = 960, avg_rect.bottom + gap
        stats_percentage.centerx, stats_percentage.y = 960, best_rect.bottom + gap + 40 

        # Vẽ lên Surface
        final_surface.blit(game_over_text, game_over)
        final_surface.blit(stats_numbers_text, stats_numbers)
        final_surface.blit(hits_text, hits_rect)
        final_surface.blit(misses_text, misses_rect)
        final_surface.blit(accuracy_text, accuracy_rect)
        final_surface.blit(avg_text, avg_rect)
        final_surface.blit(best_text, best_rect)
        final_surface.blit(stats_percentage_text, stats_percentage)

        self.display_surface.blit(postgame_image, (0, 0))
        
        overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        self.display_surface.blit(overlay, (0, 0))
        
        self.display_surface.blit(final_surface, (0, 0))