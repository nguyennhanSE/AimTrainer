from countdown import Countdown
from postgame import PostGame
from settings import *
from mainmenu import MainMenuScreen, Button
from settingsmenu import SettingsMenu
from instructionmenu import InstructionMenu 
from pausemenu import PauseMenu
import ctypes, pygame, sys
import math 
# Maintain resolution regardless of Windows scaling settings
ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()
        self.click_count = 0
        self.game_state = "waiting"
        self.previous_state = "waiting"
        self.bg_image = pygame.image.load(BG_IMAGE_PATH)
        self.shot_sound = pygame.mixer.Sound('audio/shot.mp3')
        pygame.mixer.music.load('audio/menu_music.mp3')
        pygame.mixer.music.set_volume(0.5) 
        pygame.mixer.music.play(-1)
        self.mainmenu = MainMenuScreen()
        self.settings_menu = SettingsMenu()
        self.instruction_menu = InstructionMenu() 
        self.pause_menu = PauseMenu()
        pause_btn_font = pygame.font.Font(COUNTDOWN_FONT, 40)
        self.pause_btn = Button("II PAUSE", WIDTH - 180, 20, 150, 60, pause_btn_font, (50, 50, 50), (100, 100, 100), (255, 255, 255))
        self.pause_start_time = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    # Chức năng bật/tắt Pause bằng phím ESC
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == "playing":
                            self.game_state = "paused"
                            self.pause_start_time = pygame.time.get_ticks() # Lưu lại thời điểm bắt đầu pause
                        elif self.game_state == "paused":
                            self.game_state = "playing"
                            pause_duration = pygame.time.get_ticks() - self.pause_start_time
                            self.countdown.pause_offset(pause_duration)     # Bù đắp thời gian

                    # Nhấn Space ở màn hình Game Over để chơi lại
                    elif event.key == pygame.K_SPACE and self.game_state == "gameover":
                        self.click_count = 0
                        self.countdown.targets_spawned = 0
                        self.game_state = "waiting"
                        del self.countdown
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    if self.game_state == "waiting":
                        
                        if self.mainmenu.buttons["start"].rect.collidepoint(mouse_pos):
                            pygame.mixer.music.stop()
                            selected_duration = self.settings_menu.duration_options[self.settings_menu.current_duration_idx]
                            
                           
                            selected_size = self.settings_menu.size_options[self.settings_menu.current_size_idx] 
                            selected_difficulty = self.settings_menu.difficulty_options[self.settings_menu.current_difficulty_idx]
                            
                            
                            self.countdown = Countdown(selected_duration, selected_size, selected_difficulty)
                            self.game_state = "playing"
                        elif self.mainmenu.buttons["instruction"].rect.collidepoint(mouse_pos): 
                            self.game_state = "instruction"
                        elif self.mainmenu.buttons["settings"].rect.collidepoint(mouse_pos):
                            self.previous_state = "waiting"
                            self.game_state = "settings"
                        elif self.mainmenu.buttons["exit"].rect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
                            
                    elif self.game_state == "settings":
                        
                        if self.settings_menu.buttons["duration"].rect.collidepoint(mouse_pos):
                            self.settings_menu.toggle_duration()
                        elif self.settings_menu.buttons["size"].rect.collidepoint(mouse_pos):
                            self.settings_menu.toggle_size()
                        elif self.settings_menu.buttons["difficulty"].rect.collidepoint(mouse_pos):
                            self.settings_menu.toggle_difficulty()
                        elif self.settings_menu.buttons["cursor"].rect.collidepoint(mouse_pos):
                            self.settings_menu.toggle_cursor()
                        elif self.settings_menu.buttons["back"].rect.collidepoint(mouse_pos):
                            self.game_state = self.previous_state
                            if self.game_state == "paused":
                                # Đổi == thành = để gán giá trị
                                self.countdown.target_size = self.settings_menu.size_options[self.settings_menu.current_size_idx]
                            
                    elif self.game_state == "instruction": 
            
                        if self.instruction_menu.buttons["back"].rect.collidepoint(mouse_pos):
                            self.game_state = "waiting"
                    
                    elif self.game_state == "paused":
                        if self.pause_menu.buttons["resume"].rect.collidepoint(mouse_pos):
                            self.game_state = "playing"
                            pause_duration = pygame.time.get_ticks() - self.pause_start_time
                            self.countdown.pause_offset(pause_duration)
                            
                        elif self.pause_menu.buttons["settings"].rect.collidepoint(mouse_pos):
                            self.previous_state = "paused"
                            self.game_state = "settings"
                            
                        elif self.pause_menu.buttons["quit"].rect.collidepoint(mouse_pos):
                            self.click_count = 0
                            self.game_state = "waiting"
                            pygame.mixer.music.play(-1)
                            del self.countdown
                    
                    elif self.game_state == "playing":
                        
                        if self.pause_btn.rect.collidepoint(mouse_pos):
                            self.game_state = "paused"
                            self.pause_start_time = pygame.time.get_ticks()
                        else:
                            self.click_count += 1
                            self.shot_sound.play()
                            
                            hit_something = False
                        
                        # Logic kiểm tra trúng mục tiêu bằng hình tròn
                        for target in self.countdown.target_group:
                            dx = mouse_pos[0] - target.rect.centerx
                            dy = mouse_pos[1] - target.rect.centery
                            distance_squared = dx**2 + dy**2
                            
                            if distance_squared <= (target.radius ** 2):
                                target.hit_channel.play(target.hit_sound)
                                target.kill()
                                self.countdown.hits += 1
                                
                                reaction_time = pygame.time.get_ticks() - target.spawn_time
                                
                                # BỔ SUNG: Lưu reaction_time vào mảng
                                self.countdown.reaction_times.append(reaction_time)
                                
                                # Bonus tối đa 50 điểm nếu bắn cực nhanh. Chậm thì giảm dần.
                                bonus = max(0, int(((target.time_to_live - reaction_time) / target.time_to_live) * 50))
                                points_earned = 100 + bonus
                                self.countdown.score += points_earned
                                # Đổi chữ "HIT!" thành số điểm nhận được (Ví dụ: "+145")
                                self.countdown.add_floating_text(target.rect.centerx, target.rect.centery, f"+{points_earned}", (50, 255, 50))
                                
                                hit_something = True
                                break
                        
                        # BỔ SUNG: Nếu vòng lặp trên không hit trúng cái nào -> Miss
                        if not hit_something:
                            # Hiện chữ MISS màu đỏ ngay tại vị trí vừa click chuột
                            self.countdown.add_floating_text(mouse_pos[0], mouse_pos[1], "MISS!", (255, 50, 50))
                # Nhấn Space ở màn hình Game Over để chơi lại
                elif event.type == pygame.KEYDOWN and self.game_state == "gameover":
                    if event.key == pygame.K_SPACE:
                        self.click_count = 0
                        self.countdown.targets_spawned = 0
                        self.game_state = "waiting"
                        del self.countdown

            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.clock.tick(FPS)

            # CẬP NHẬT GIAO DIỆN THEO STATE
            if self.game_state == "waiting":
                self.mainmenu.update()
            elif self.game_state == "settings":
                self.settings_menu.update()
            elif self.game_state == "instruction": 
                self.instruction_menu.update()
            elif self.game_state == "playing" and self.countdown.time_left > 0:
                self.countdown.update()
                
            elif self.game_state == "paused":
                # Đóng băng khung hình: Vẽ nền, vẽ target nhưng không gọi hàm update()
                self.countdown.target_group.draw(self.screen)
                self.countdown.draw_score()
                self.pause_menu.update()
            elif self.game_state == "playing" and self.countdown.time_left <= 0:
                self.game_state = "gameover"
                self.postgame = PostGame(self.click_count, self.countdown.hits, self.countdown.time_outs, self.countdown.score, self.countdown.reaction_times)
                pygame.mixer.music.play(-1)
            elif self.game_state == "gameover":
                
                self.postgame.update()
                
            cursor_style = self.settings_menu.cursor_options[self.settings_menu.current_cursor_idx]
            
            # Chỉ đổi thành crosshair khi người chơi đang trong game (playing) và tùy chọn đang bật
            if self.game_state == "playing" and cursor_style == "Crosshair":
                pygame.mouse.set_visible(False) # Ẩn chuột gốc
                mx, my = pygame.mouse.get_pos()
                
                # Vẽ tâm ngắm: 1 chấm đỏ ở giữa và chữ thập xanh lá
                pygame.draw.circle(self.screen, (255, 0, 0), (mx, my), 3)
                pygame.draw.line(self.screen, (0, 255, 0), (mx - 15, my), (mx + 15, my), 2)
                pygame.draw.line(self.screen, (0, 255, 0), (mx, my - 15), (mx, my + 15), 2)
            else:
                pygame.mouse.set_visible(True) # Hiện lại chuột bình thường ở Menu/Pause
            

            pygame.display.update() 
            
            self.clock.tick(FPS)
if __name__ == '__main__':
    game = Game()
    game.run()