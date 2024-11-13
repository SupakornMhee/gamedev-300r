from src.states.BaseState import BaseState
import pygame, sys
import random
from src.recourses import *
from src.constants import *

class LoadingState(BaseState):
    def __init__(self):
        # เปลี่ยนจาก array เป็น dictionary เหมือนใน ResultState
        self.wave_titles = {
            1: "The Awakening of Leonidas",
            2: "",
            3: "",
            4: "",
            5: "The Messenger's Omen",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "Xerxes Descends"
        }
        # เพิ่มตัวแปรสำหรับการกระพริบ
        self.blink_speed = 100  # ความเร็วในการกระพริบ (ยิ่งมากยิ่งกระพริบเร็ว)
        self.min_opacity = 100  # ค่าความโปร่งใสต่ำสุด
        self.current_wave = 1  # เริ่มที่ wave 1
        self.show_wave_title = True
        self.title_start_time = None
        self.display_duration = 6000
        self.fade_duration = 2000
        self.text_opacity = 255
        self.font = pygame.font.Font('./fonts/CooperMdBT-Regular.ttf', 48)
        
        pygame.mixer.init()
        self.loading_song = './sounds/loadingsong.mp3'

        self.dust_particles = [
            {"x": random.randint(0, WIDTH), 
             "y": random.randint(0, HEIGHT), 
             "size": random.randint(1, 4), 
             "alpha": random.randint(50, 150)}
            for _ in range(100)
        ]

    def Enter(self, params):
        if params is None:
            params = {}
        # รับค่า wave_number จาก params เหมือน ResultState
        self.current_wave = params.get("wave_number", 1)
        self.title_start_time = pygame.time.get_ticks()
        
        pygame.mixer.music.load(self.loading_song)
        pygame.mixer.music.play()

    def Exit(self):
        pygame.mixer.music.stop()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.title_start_time

        if self.show_wave_title:
            if time_elapsed > self.display_duration:
                self.show_wave_title = False
                self.text_opacity = 255
                self.fade_out_start_time = current_time
            else:
                # คำนวณความโปร่งใสสำหรับการกระพริบ
                blink_value = (math.sin(time_elapsed * self.blink_speed / 1000) + 1) / 2
                self.text_opacity = int(self.min_opacity + (255 - self.min_opacity) * blink_value)

        if not self.show_wave_title:
            fade_elapsed = current_time - self.fade_out_start_time
            self.text_opacity = max(0, 255 - int((fade_elapsed / self.fade_duration) * 255))

            if self.text_opacity == 0:
                # เปลี่ยนเป็นส่งค่า wave_number ไปยัง PlayState
                g_state_manager.Change('play', {'wave_number': self.current_wave})

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.render_dust_effect(screen)

        # แก้การเข้าถึงชื่อ wave จาก dictionary
        wave_title = f"Wave {self.current_wave} {self.wave_titles[self.current_wave]}"
        title_surface = self.font.render(wave_title, True, (255, 215, 0))
        title_surface.set_alpha(self.text_opacity)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(title_surface, title_rect)

    def render_dust_effect(self, screen):
        for particle in self.dust_particles:
            particle["y"] += random.randint(-1, 1)
            particle["x"] += random.randint(-1, 1)

            if particle["y"] < 0:
                particle["y"] = HEIGHT
            elif particle["y"] > HEIGHT:
                particle["y"] = 0
            if particle["x"] < 0:
                particle["x"] = WIDTH
            elif particle["x"] > WIDTH:
                particle["x"] = 0

            particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, 
                             (200, 200, 200, particle["alpha"]), 
                             (particle["size"], particle["size"]), 
                             particle["size"])
            screen.blit(particle_surface, (particle["x"], particle["y"]))