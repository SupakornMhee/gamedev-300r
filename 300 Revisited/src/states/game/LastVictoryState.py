from src.states.BaseState import BaseState 
import pygame, sys
from moviepy.editor import VideoFileClip
import random

from src.constants import *
from src.recourses import *

class LastVictoryState(BaseState):
    def __init__(self):
        # Basic setup
        pygame.mixer.init()
        pygame.mixer.music.load('./sounds/backgroundstory1.mp3')
        pygame.mixer.music.set_volume(0.5)
        self.start_time = pygame.time.get_ticks()
        self.current_text_index = 0
        self.texts = [
            "400 BC",
            "King Leonidas and his 300 Spartans rose to fight against the 100,000 Persian soldiers, led by King Xerxes I.",
            "They fought to defend the land of Greece at the narrow pass of Thermopylae.",
            "But King Leonidas and his 300 Spartans were defeated by the Persian Empire.",
            "Xerxes and the Persian army... prepare yourselves!",
            "We will bring them back!!!!! Let King Leonidas rise again, and this time, victory will be ours!",
            "Though that battle ended in the defeat of Leonidas, today, history will be",
            "rewritten"
        ]

        # Load font with a vintage style
        font_path = './fonts/CooperMdBT-Regular.ttf'
        self.font = pygame.font.Font(font_path, 48)

        # Load background images
        self.backgrounds = [
            pygame.image.load('./graphics/400n.png'),
            pygame.image.load('./graphics/leonidas_vs_xerxes.jpg'),
            pygame.image.load('./graphics/Fought.jpg'),
            pygame.image.load('./graphics/Loss.jfif')
        ]

        # Sepia overlay surface
        self.sepia_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.sepia_overlay.fill((112, 66, 20, 50))  # Warm sepia color with transparency

        # Fade-in effect attributes
        self.text_opacity = 0
        self.fade_duration = 2000  # Duration of fade-in in milliseconds

    def Enter(self, params):
        pygame.mixer.music.play(-1)
        pass

    def update(self, dt, events):
        # Handle events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Get the current time and display duration
        current_time = pygame.time.get_ticks()
        display_duration = 5000 if self.current_text_index == 0 else 7000

        # Update fade-in effect
        time_elapsed = current_time - self.start_time
        if time_elapsed < self.fade_duration:
            self.text_opacity = min(255, int((time_elapsed / self.fade_duration) * 255))
        else:
            self.text_opacity = 255  # Ensure maximum opacity after fade-in completes

        # Move to the next text after the display duration
        if time_elapsed >= display_duration:
            if self.current_text_index < len(self.texts) - 1:
                self.current_text_index += 1
                self.start_time = current_time  # Reset start time
                self.text_opacity = 0  # Reset opacity for new text

    def render_text_wrapped(self, text, screen):
        # Wrap text and apply fade-in effect
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_surface = self.font.render(test_line, True, (255, 229, 204))  # Warm text color
            if text_surface.get_width() > WIDTH - 40:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        lines.append(current_line)  # Add the last line

        # Display each line centered on the screen with fade-in effect
        y = HEIGHT / 2 - len(lines) * 25  # Starting y-position
        for line in lines:
            line_surface = self.font.render(line, True, (255, 229, 204))
            line_surface.set_alpha(self.text_opacity)
            rect = line_surface.get_rect(center=(WIDTH / 2, y))
            screen.blit(line_surface, rect)
            y += 50  # Line spacing

    def render_dust_and_scratches(self, screen):
        # Simulate dust and scratches
        for _ in range(50):  # Adjust number for more/less dust
            x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            color = (200, 200, 200) if random.randint(0, 1) == 0 else (255, 255, 255)
            pygame.draw.circle(screen, color, (x, y), 1)  # Small dust particles
        for _ in range(10):  # Adjust for more/less scratches
            x_start, y_start = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            x_end, y_end = x_start + random.randint(-20, 20), y_start + random.randint(-20, 20)
            pygame.draw.line(screen, (150, 150, 150), (x_start, y_start), (x_end, y_end), 1)

    def render(self, screen):
        # Select and resize the background image
        if self.current_text_index < len(self.backgrounds):
            background_image = self.backgrounds[self.current_text_index]
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            screen.blit(background_image, (0, 0))

        # Apply sepia overlay for retro feel
        screen.blit(self.sepia_overlay, (0, 0))

        # Render text with vintage fade-in
        text = self.texts[self.current_text_index]
        self.render_text_wrapped(text, screen)

        # Simulate dust and scratches
        self.render_dust_and_scratches(screen)

        # Apply flicker effect
        if random.randint(0, 20) < 2:  # Random flicker chance
            flicker_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flicker_overlay.fill((0, 0, 0, 50))  # Slight dark overlay for flicker
            screen.blit(flicker_overlay, (0, 0))

    def Exit(self):
        pass
