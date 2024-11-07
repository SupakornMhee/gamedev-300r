# import pygame, sys
# import math
# import random

# from src.states.BaseState import BaseState
# from src.constants import *
# from src.recourses import *

# class StartState(BaseState):
#     def __init__(self):
#         # ส่วนที่เกี่ยวกับหน้าจอและการสั่น
#         self.bg_image = pygame.image.load("./graphics/background.png")
#         self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 5, HEIGHT + 5))
#         self.time = 0  
#         self.shake_duration = 20  
#         self.shake_intensity = 5  
#         self.shake_time = 0  
        
#         # ตำแหน่งเริ่มต้นของข้อความให้อยู่นอกจอ
#         self.title_pos_x = -300  
#         self.subtitle_pos_x = WIDTH + 300  
#         self.final_title_pos_x = WIDTH / 2
#         self.final_subtitle_pos_x = WIDTH / 2
        
#         # ตัวแปรควบคุมการสั่นและการจางของหน้าจอ
#         self.shake_triggered = False
#         self.fade_alpha = 0
#         self.fade_wait_time = 60
        
#         # โหลดเสียงเพลงและเสียงเอฟเฟกต์
#         pygame.mixer.init()
#         self.sword_sound = pygame.mixer.Sound("./sounds/Sword_Sound_Effect.mp3")  # เสียงดาบ
#         self.background_music = pygame.mixer.Sound("./sounds/Immortals.mp3")  # เพลงพื้นหลัง
#         self.background_music.set_volume(0.5)  # กำหนดความดังเริ่มต้น

#         # ตัวแปรควบคุมการลดเสียง
#         self.fade_out_music = False
#         self.music_started = False  # ตัวแปรตรวจสอบว่าดนตรีเริ่มเล่นแล้วหรือยัง

#     def Enter(self, params):
#         self.background_music.play(loops=-1)
#         print(self.bg_image)

#     def update(self, dt, events):
#         for event in events:
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame.quit()
#                     sys.exit()
#                 if event.key == pygame.K_RETURN:
#                     # เริ่มการจางสีดำและลดเสียงเพลงลงเมื่อกด Enter
#                     self.fade_alpha = 5
#                     self.fade_out_music = True

#         # ทำให้สีดำเข้มขึ้นเรื่อยๆ จนเต็มหน้าจอ
#         if self.fade_alpha > 0 and self.fade_alpha < 255:
#             self.fade_alpha += 5
#             if self.fade_alpha >= 255:
#                 self.fade_alpha = 255
#                 self.fade_wait_time = 60

#         # ลดเสียงเพลงเมื่อจางเป็นสีดำ
#         if self.fade_out_music and self.background_music.get_volume() > 0:
#             current_volume = self.background_music.get_volume()
#             self.background_music.set_volume(max(0, current_volume - 0.01))  # ลดทีละเล็กน้อย
#             if current_volume <= 0:
#                 self.fade_out_music = False

#         # รอให้หน้าจอดำสนิทสักพักก่อนเปลี่ยนไปหน้าต่อไป
#         elif self.fade_alpha == 255 and self.fade_wait_time > 0:
#             self.fade_wait_time -= 1
#             if self.fade_wait_time == 0:
#                 g_state_manager.Change('story_1')

#     def render(self, screen):
#         shake_offset_x, shake_offset_y = 0, 0
#         if self.shake_time > 0:
#             shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
#             shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
#             self.shake_time -= 1

#         # แสดงพื้นหลัง
#         screen.blit(self.bg_image, (shake_offset_x, shake_offset_y))

#         # เคลื่อนตำแหน่งข้อความเข้ามาในจอ
#         if self.title_pos_x < self.final_title_pos_x:
#             self.title_pos_x += 5  
#             self.subtitle_pos_x -= 5

#         # แสดงข้อความ "300" พร้อมขอบดำ
#         title_text = "300"
#         t_title_outline = gFonts['title'].render(title_text, False, (0, 0, 0))  # ข้อความสีดำ
#         t_title = gFonts['title'].render(title_text, False, (255, 165, 0))  # ข้อความสีส้ม
#         title_rect = t_title.get_rect(center=(self.title_pos_x + shake_offset_x, HEIGHT / 2 - 150 + shake_offset_y))

#         # วาดข้อความสีดำเพื่อทำเป็นขอบ
#         for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
#             screen.blit(t_title_outline, title_rect.move(offset))

#         # วาดข้อความสีส้มทับบนขอบ
#         screen.blit(t_title, title_rect)

#         # แสดงข้อความ "Rewritten" พร้อมขอบดำ
#         subtitle_text = "Rewritten"
#         t_subtitle_outline = gFonts['title'].render(subtitle_text, False, (0, 0, 0))  # ข้อความสีดำ
#         t_subtitle = gFonts['title'].render(subtitle_text, False, (255, 165, 0))  # ข้อความสีส้ม
#         subtitle_rect = t_subtitle.get_rect(center=(self.subtitle_pos_x + shake_offset_x, HEIGHT / 2 - 90 + shake_offset_y))

#         # วาดข้อความสีดำเพื่อทำเป็นขอบ
#         for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
#             screen.blit(t_subtitle_outline, subtitle_rect.move(offset))

#         # วาดข้อความสีส้มทับบนขอบ
#         screen.blit(t_subtitle, subtitle_rect)

#         # เริ่มการสั่นและเล่นเสียงดาบเมื่อข้อความทั้งสองมาถึงตำแหน่งสุดท้าย
#         if not self.shake_triggered and self.title_pos_x >= self.final_title_pos_x and self.subtitle_pos_x <= self.final_subtitle_pos_x:
#             self.shake_time = self.shake_duration
#             self.sword_sound.play()  # เล่นเสียงดาบ
#             self.shake_triggered = True
#             if not self.music_started:
#                 self.background_music.play(loops=-1)  # เล่นเพลงพื้นหลังวนลูปเมื่อข้อความครบ
#                 self.music_started = True

#         # แสดงข้อความ "Press Enter to Start"
#         if self.shake_triggered:
#             t_press_enter_outline = gFonts['Press_Enter'].render("Press Enter to Start", False, (0, 0, 0))
#             t_press_enter = gFonts['Press_Enter'].render("Press Enter to Start", False, (255, 255, 255))
#             rect = t_press_enter.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 192))

#             # วาดข้อความสีดำเพื่อทำเป็นขอบ
#             for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
#                 screen.blit(t_press_enter_outline, rect.move(offset))

#             # วาดข้อความสีขาวทับบนขอบ
#             screen.blit(t_press_enter, rect)

#         # แสดงเลเยอร์จางสีดำ
#         if self.fade_alpha > 0:
#             fade_surface = pygame.Surface((WIDTH, HEIGHT))
#             fade_surface.set_alpha(self.fade_alpha)
#             fade_surface.fill((0, 0, 0))
#             screen.blit(fade_surface, (0, 0))

#         # อัพเดทตัวจับเวลาสำหรับการแสดงผล
#         self.time += 1

#     def Exit(self):
#         # หยุดเพลงเมื่อออกจากสถานะนี้
#         self.background_music.stop()



import pygame, sys
import math
import random

from src.states.BaseState import BaseState
from src.constants import *
from src.recourses import *

class StartState(BaseState):
    def __init__(self):
        # Background and shake effect setup
        self.bg_image = pygame.image.load("./graphics/background.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 5, HEIGHT + 5))
        self.time = 0  
        self.shake_duration = 20  
        self.shake_intensity = 5  
        self.shake_time = 0  
        
        # Initial text positions (off-screen)
        self.title_pos_x = -300  
        self.subtitle_pos_x = WIDTH + 300  
        self.final_title_pos_x = WIDTH / 2
        self.final_subtitle_pos_x = WIDTH / 2
        
        # Fade and shake control variables
        self.shake_triggered = False
        self.fade_alpha = 0
        self.fade_wait_time = 60
        
        # Load sound effects and music
        pygame.mixer.init()
        self.sword_sound = pygame.mixer.Sound("./sounds/Sword_Sound_Effect.mp3")
        self.background_music = pygame.mixer.Sound("./sounds/Immortals.mp3")
        self.background_music.set_volume(0.5)

        # Music fade control
        self.fade_out_music = False
        self.music_started = False

    def Enter(self, params):
        print(self.bg_image)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    # Start fade-out effect and music fade
                    self.fade_alpha = 5
                    self.fade_out_music = True

        # Incremental fade-out effect
        if self.fade_alpha > 0 and self.fade_alpha < 255:
            self.fade_alpha += 5
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_wait_time = 60

        # Fade out music gradually
        if self.fade_out_music and self.background_music.get_volume() > 0:
            current_volume = self.background_music.get_volume()
            self.background_music.set_volume(max(0, current_volume - 0.01))
            if current_volume <= 0:
                self.fade_out_music = False

        # Complete fade and transition to StoryState
        elif self.fade_alpha == 255 and self.fade_wait_time > 0:
            self.fade_wait_time -= 1
            if self.fade_wait_time == 0:
                # Pass precise transition time to StoryState
                g_state_manager.Change('story_1', {'initial_delay': pygame.time.get_ticks()})

    def render(self, screen):
        shake_offset_x, shake_offset_y = 0, 0
        if self.shake_time > 0:
            shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_time -= 1

        # Display background
        screen.blit(self.bg_image, (shake_offset_x, shake_offset_y))

        # Move text positions onto the screen
        if self.title_pos_x < self.final_title_pos_x:
            self.title_pos_x += 5  
            self.subtitle_pos_x -= 5

        # Display "300" title with outline
        title_text = "300"
        t_title_outline = gFonts['title'].render(title_text, False, (0, 0, 0))
        t_title = gFonts['title'].render(title_text, False, (255, 165, 0))
        title_rect = t_title.get_rect(center=(self.title_pos_x + shake_offset_x, HEIGHT // 2 - 150 + shake_offset_y))

        # Draw title outline
        for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            screen.blit(t_title_outline, title_rect.move(offset))
        screen.blit(t_title, title_rect)

        # Display "Rewritten" subtitle with outline
        subtitle_text = "Rewritten"
        t_subtitle_outline = gFonts['title'].render(subtitle_text, False, (0, 0, 0))
        t_subtitle = gFonts['title'].render(subtitle_text, False, (255, 165, 0))
        subtitle_rect = t_subtitle.get_rect(center=(self.subtitle_pos_x + shake_offset_x, HEIGHT // 2 - 90 + shake_offset_y))

        # Draw subtitle outline
        for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            screen.blit(t_subtitle_outline, subtitle_rect.move(offset))
        screen.blit(t_subtitle, subtitle_rect)

        # Trigger shake effect and play sword sound once
        if not self.shake_triggered and self.title_pos_x >= self.final_title_pos_x and self.subtitle_pos_x <= self.final_subtitle_pos_x:
            self.shake_time = self.shake_duration
            self.sword_sound.play()
            self.shake_triggered = True
            if not self.music_started:
                self.background_music.play(loops=-1)
                self.music_started = True

        # Display "Press Enter to Start" prompt
        if self.shake_triggered:
            t_press_enter_outline = gFonts['Press_Enter'].render("Press Enter to Start", False, (0, 0, 0))
            t_press_enter = gFonts['Press_Enter'].render("Press Enter to Start", False, (255, 255, 255))
            rect = t_press_enter.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 192))
            for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                screen.blit(t_press_enter_outline, rect.move(offset))
            screen.blit(t_press_enter, rect)

        # Apply black fade overlay
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.set_alpha(self.fade_alpha)
            fade_surface.fill((0, 0, 0))
            screen.blit(fade_surface, (0, 0))

    def Exit(self):
        # Stop background music when exiting
        self.background_music.stop()
