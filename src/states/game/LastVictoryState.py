from src.states.BaseState import BaseState 
import pygame, sys
import random

from src.constants import *
from src.recourses import *

class LastVictoryState(BaseState):
    def __init__(self):
        pass
    
    def AssignVariable(self) :
        # Initialize mixer and load background music
        self.background_music = pygame.mixer.Sound('./sounds/LastVioctoryOK.mp3')
        self.background_music.set_volume(0.5)

        # Phase control for victory announcement and credits
        self.phase = "victory"  # Initial phase is the victory announcement
        self.text_opacity = 0

        # Victory message and credits text
        self.victory_text = "And so, history was shattered and rewritten in glory! Against all odds, Leonidas rose victorious, crushing the mighty Persian empire under the reign of King Xerxes I!"
        self.credits_text = [
            "300: REWRITTEN",
            "",
            "Director",
            "6422781276",
            "Danuvasin Pangsa-art",
            "",
            "Producer",
            "6422781235",
            "Thanapoom Noywijith",
            "",
            "Senior Developer",
            "6422780146",
            "Supakorn Nilsuwan",
            "",
            "Art Director",
            "6422782738",
            "Put Thitisawat",
        ]

        # Load font
        font_path = './fonts/CooperMdBT-Regular.ttf'
        self.font = pygame.font.Font(font_path, 48)
        self.small_font = pygame.font.Font(font_path, 36)

        # Positioning for scrolling credits
        self.credit_y = HEIGHT + 50  # Start off-screen

        # Sepia overlay for atmosphere
        self.sepia_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.sepia_overlay.fill((112, 66, 20, 50))  # Sepia tone

        # Fade and transition timing
        self.fade_duration = 2000
        self.victory_display_duration = 5000
        
    def Enter(self, params=None):
        self.AssignVariable()
        # Start playing background music
        self.background_music.play(loops=-1)
        # Use initial_delay from params if provided
        self.start_time = params.get('initial_delay', pygame.time.get_ticks()) if params else pygame.time.get_ticks()

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
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change("start")

        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.start_time

        if self.phase == "victory":
            # Fade-in effect for the victory message
            if time_elapsed < self.fade_duration:
                self.text_opacity = min(255, int((time_elapsed / self.fade_duration) * 255))
            else:
                self.text_opacity = 255

            # Transition to credits after displaying the victory message
            if time_elapsed >= self.victory_display_duration:
                self.phase = "credits"
                self.start_time = current_time  # Reset time for credits
                self.text_opacity = 0  # Reset opacity for credits

        elif self.phase == "credits":
            # Scroll credits upwards
            self.credit_y -= 1  # Adjust speed here
            if self.credit_y < -len(self.credits_text) * 50:  # End credits when fully scrolled off
                self.background_music.stop()  # Stop music when credits end
                self.phase = "end"

    def render(self, screen):
        screen.fill((0, 0, 0))  # Black background for end credits feel

        # Sepia overlay
        screen.blit(self.sepia_overlay, (0, 0))

        if self.phase == "victory":
            # Display victory message with fade-in
            self.render_text_wrapped(self.victory_text, screen)

        elif self.phase == "credits":
            # Display scrolling credits
            y = self.credit_y
            for line in self.credits_text:
                credit_surface = self.small_font.render(line, True, (255, 255, 255))
                rect = credit_surface.get_rect(center=(WIDTH // 2, y))
                screen.blit(credit_surface, rect)
                y += 50  # Spacing between lines

    def render_text_wrapped(self, text, screen):
        # Wrap and render text with fade-in
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_surface = self.font.render(test_line, True, (255, 229, 204))
            if text_surface.get_width() > WIDTH - 40:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        lines.append(current_line)

        # Display wrapped lines centered with fade-in effect
        y = HEIGHT / 2 - len(lines) * 25
        for line in lines:
            line_surface = self.font.render(line, True, (255, 229, 204))
            line_surface.set_alpha(self.text_opacity)
            rect = line_surface.get_rect(center=(WIDTH / 2, y))
            screen.blit(line_surface, rect)
            y += 50

    def Exit(self):
        # Stop music when exiting LastVictoryState
        self.background_music.stop()
