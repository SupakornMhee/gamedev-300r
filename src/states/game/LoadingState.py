from src.states.BaseState import BaseState
import pygame, sys
import random
from src.recourses import *
from src.constants import *

class LoadingState(BaseState):
    def __init__(self):
        # Modified wave titles with empty strings for some waves
        self.wave_titles = [
            "The Awakening of Leonidas",
            "",
            "",
            "",
            "The Messenger’s Omen",
            "",
            "",
            "",
            "",
            "Xerxes Descends"
        ]
        self.current_wave = 0
        self.show_wave_title = True
        self.title_start_time = pygame.time.get_ticks()
        self.display_duration = 6000  # Show each wave message for 6 seconds (6000 ms)
        self.fade_duration = 2000  # Time for fading out the text (in ms)
        self.text_opacity = 255
        self.font = pygame.font.Font('./fonts/CooperMdBT-Regular.ttf', 48)
        
        # Load music for loading state
        pygame.mixer.init()
        self.loading_song = './sounds/loadingsong.mp3'  # Path to the loading song

        # Dust effect configuration
        self.dust_particles = [
            {"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), "size": random.randint(1, 4), "alpha": random.randint(50, 150)}
            for _ in range(100)
        ]

    def Enter(self, params):
        print("Entering LoadingState...")
        self.title_start_time = pygame.time.get_ticks()
        self.current_wave = 0  # Reset to the first wave when entering
        
        # Play loading song for the first wave
        pygame.mixer.music.load(self.loading_song)
        pygame.mixer.music.play()  # Play the song once

    def Exit(self):
        print("Exiting LoadingState...")
        pygame.mixer.music.stop()  # Stop the loading song when exiting

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()

        # Check if the wave title has been shown for the display duration
        if self.show_wave_title:
            if current_time - self.title_start_time > self.display_duration:
                # After 6 seconds, begin the fade-out phase
                self.show_wave_title = False
                self.text_opacity = 255  # Reset opacity for fade-out effect
                self.fade_out_start_time = current_time  # Start fade-out timer

        if not self.show_wave_title:
            fade_elapsed = current_time - self.fade_out_start_time
            self.text_opacity = max(0, 255 - int((fade_elapsed / self.fade_duration) * 255))

            if self.text_opacity == 0:
                # Move to the next wave after the current one fully fades out
                if self.current_wave < len(self.wave_titles) - 1:
                    self.current_wave += 1
                    self.show_wave_title = True
                    self.title_start_time = pygame.time.get_ticks()  # Reset title start time for the next wave

                    # Restart the loading song for each new wave
                    pygame.mixer.music.stop()  # Stop any music currently playing
                    pygame.mixer.music.load(self.loading_song)
                    pygame.mixer.music.play()  # Play the song once for each wave
                else:
                    pass  # Add any final state logic here if needed

    def render(self, screen):
        # Clear the screen with a black background
        screen.fill((0, 0, 0))

        # Render dust effect in the background
        self.render_dust_effect(screen)

        # Get the title for the current wave
        wave_title = f"Wave {self.current_wave + 1}: {self.wave_titles[self.current_wave]}"
        title_surface = self.font.render(wave_title, True, (255, 215, 0))  # Gold color for wave title
        title_surface.set_alpha(self.text_opacity)  # Apply opacity for fade effect
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(title_surface, title_rect)

    def render_dust_effect(self, screen):
        # Render each dust particle with a war-like floating effect
        for particle in self.dust_particles:
            # Update position for a slow drift effect
            particle["y"] += random.randint(-1, 1)  # Simulate slight vertical drift
            particle["x"] += random.randint(-1, 1)  # Simulate slight horizontal drift

            # Wrap around the screen edges to keep particles on screen
            if particle["y"] < 0:
                particle["y"] = HEIGHT
            elif particle["y"] > HEIGHT:
                particle["y"] = 0
            if particle["x"] < 0:
                particle["x"] = WIDTH
            elif particle["x"] > WIDTH:
                particle["x"] = 0

            # Draw the particle
            particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (200, 200, 200, particle["alpha"]), (particle["size"], particle["size"]), particle["size"])
            screen.blit(particle_surface, (particle["x"], particle["y"]))