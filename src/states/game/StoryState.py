from src.states.BaseState import BaseState 
import pygame, sys
#from moviepy.editor import VideoFileClip

from src.constants import *
from src.recourses import *

class StoryState(BaseState):
    def __init__(self):
        # ตั้งค่าตัวแปรพื้นฐาน
        self.start_time = pygame.time.get_ticks()  # เริ่มนับเวลาจากการเปิดหน้านี้
        self.current_text_index = 0  # ตำแหน่งของข้อความที่จะแสดงในปัจจุบัน

        # ข้อความที่จะใช้แสดงผลตามลำดับ
        self.texts = [
            "400 BC",
            "King Leonidas and his 300 Spartans rose to fight against the vast Persian army, led by King Xerxes I.",
            "They fought to defend the land of Greece at the narrow pass of Thermopylae.",
            "Xerxes and the Persian army... prepare yourselves!",
            "We will bring them back, let King Leonidas rise again, and this time, victory will be ours!",
            "Though that battle ended in the defeat of Leonidas, today, history will be",
            "rewritten"
        ]

        # โหลดฟอนต์ CooperMdBT-Regular จากโฟลเดอร์ font
        font_path = './fonts/CooperMdBT-Regular.ttf'
        self.font = pygame.font.Font(font_path, 48)  # ตั้งค่าฟอนต์

    def Enter(self, params):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # ตรวจสอบเวลาที่ผ่านไปนับตั้งแต่เริ่มต้นแสดงข้อความ
        current_time = pygame.time.get_ticks()
        # หากเป็นข้อความแรก ("400 BC") ให้แสดงนานขึ้น (5 วินาที)
        display_duration = 15000 if self.current_text_index == 0 else 3000

        if current_time - self.start_time >= display_duration:
            if self.current_text_index < len(self.texts) - 1:
                self.current_text_index += 1
                self.start_time = current_time  # รีเซ็ตเวลาเมื่อเปลี่ยนข้อความ

    def render_text_wrapped(self, text, screen):
        # แบ่งข้อความตามความกว้างหน้าจอ
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            # ตรวจสอบความกว้างของข้อความในบรรทัด
            test_line = f"{current_line} {word}".strip()
            text_surface = self.font.render(test_line, True, (255, 255, 255))
            if text_surface.get_width() > WIDTH - 40:  # 40 เป็นระยะขอบซ้ายและขวา
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        lines.append(current_line)  # เพิ่มบรรทัดสุดท้าย

        # แสดงแต่ละบรรทัดที่หน้าจอ
        y = HEIGHT / 2 - len(lines) * 25  # ตำแหน่ง Y เริ่มต้น
        for line in lines:
            line_surface = self.font.render(line, True, (255, 255, 255))
            rect = line_surface.get_rect(center=(WIDTH / 2, y))
            screen.blit(line_surface, rect)
            y += 50  # เพิ่มระยะห่างระหว่างบรรทัด

    def render(self, screen):
        # แสดงข้อความตามลำดับในตำแหน่งกลางจอ
        text = self.texts[self.current_text_index]
        self.render_text_wrapped(text, screen)

    def Exit(self):
        pass
