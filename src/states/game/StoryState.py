from src.states.BaseState import BaseState 
import pygame, sys
import random

from src.constants import *
from src.recourses import *

class StoryState(BaseState):
    def __init__(self):
        pass
    
    def AssignVariable(self) :
        # Basic setup and initializations
        pygame.mixer.init()
        pygame.mixer.music.load('./sounds/backgroundstory1.mp3')
        pygame.mixer.music.set_volume(0.5)
        self.start_time = None  # Set in Enter method
        self.current_text_index = 0
        self.show_instructions = False  # Flag to toggle instruction page
        self.instruction_start_time = None  # Track when instructions are shown

        # Story texts and backgrounds
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
        self.backgrounds = [
            pygame.image.load('./graphics/400n.png'),
            pygame.image.load('./graphics/leonidas_vs_xerxes.jpg'),
            pygame.image.load('./graphics/Fought.jpg'),
            pygame.image.load('./graphics/Loss.jfif')
        ]

        # Instructions content
        self.instructions = [
            "The Tome of Victory",
            "WASD : Move Leonidas",
            "TAB : Inventory",
            "P : Pause",
            "R : Rage Mode"
        ]
        
        # Font and background setup
        font_path = './fonts/CooperMdBT-Regular.ttf'  # Change to a more war-like font if desired
        self.font = pygame.font.Font(font_path, 48)
        self.small_font = pygame.font.Font(font_path, 24)
        self.instruction_font = pygame.font.Font(font_path, 40)  # Slightly smaller font for instructions

        # Sepia overlay for vintage effect
        self.sepia_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.sepia_overlay.fill((112, 66, 20, 50))
        self.text_opacity = 0
        self.fade_duration = 2000

        # Skip gauge variables
        self.skip_start_time = None
        self.skip_duration = 3000  # 3 seconds hold duration to skip

    def Enter(self, params):
        self.AssignVariable()
        # pygame.mixer.music.play()
        # self.start_time = params.get('initial_delay', pygame.time.get_ticks())
        pygame.mixer.music.stop()
        
        # โหลดและเล่นเพลงใหม่
        try:
            pygame.mixer.music.load('./sounds/backgroundstory1.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Could not load story background music: {e}")
            
        self.start_time = params.get('initial_delay', pygame.time.get_ticks())

    def update(self, dt, events):
        if self.show_instructions:
            if self.instruction_start_time is None:
                self.instruction_start_time = pygame.time.get_ticks()  # Start time when instructions are shown

            # Check if 5 seconds have passed
            if pygame.time.get_ticks() - self.instruction_start_time >= 5000:
                # After 5 seconds, change to the next state (e.g., 'main_menu' or game start)
                g_state_manager.Change('load',{"items":[0]*9})  # You can replace this with the state you want
            return

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Handle Enter key hold for skip functionality
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if self.skip_start_time is None:
                self.skip_start_time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.skip_start_time >= self.skip_duration:
                self.show_instructions = True
        else:
            self.skip_start_time = None  # Reset if Enter is released

        # Text display timing
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.start_time
        display_duration = 10000 if self.current_text_index == 0 else 7000

        # Text fade-in effect
        if time_elapsed < self.fade_duration:
            self.text_opacity = min(255, int((time_elapsed / self.fade_duration) * 255))
        else:
            self.text_opacity = 255

        # Move to next text after display duration
        if time_elapsed >= display_duration:
            if self.current_text_index < len(self.texts) - 1:
                self.current_text_index += 1
                self.start_time = current_time  # Reset start time
                self.text_opacity = 0
            else:
                self.show_instructions = True

    def render(self, screen):
        if self.show_instructions:
            self.render_instructions(screen)
        else:
            # Display background and overlays for story
            if self.current_text_index < len(self.backgrounds):
                background_image = self.backgrounds[self.current_text_index]
                background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
                screen.blit(background_image, (0, 0))
            screen.blit(self.sepia_overlay, (0, 0))

            # Render story text and effects
            self.render_text_wrapped(self.texts[self.current_text_index], screen)
            self.render_skip_gauge(screen)
            self.render_dust_and_scratches(screen)

    def render_instructions(self, screen):
        # Create a dramatic background for the instruction page
        screen.fill((0, 0, 0))  # Black background for instruction
        y = HEIGHT / 4
        
        # Add an elegant and majestic font style with a golden color for the instruction title
        title_surface = self.instruction_font.render(self.instructions[0], True, (255, 215, 0))  # Gold color
        title_rect = title_surface.get_rect(center=(WIDTH / 2, y))
        screen.blit(title_surface, title_rect)
        y += 100  # Increase the gap after the title

        # Render the rest of the instructions with spacious and elegant line breaks
        for line in self.instructions[1:]:
            text_surface = self.instruction_font.render(line, True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect(center=(WIDTH / 2, y))
            screen.blit(text_surface, text_rect)
            y += 80  # Increase the spacing for dramatic effect

        # Optional: Add a border or some visual effect (e.g., "spartan" style)
        pygame.draw.rect(screen, (255, 215, 0), (50, 50, WIDTH - 100, HEIGHT - 100), 5)  # Gold border to frame the instructions

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

        y = HEIGHT / 2 - len(lines) * 25
        for line in lines:
            line_surface = self.font.render(line, True, (255, 229, 204))
            line_surface.set_alpha(self.text_opacity)
            rect = line_surface.get_rect(center=(WIDTH / 2, y))
            screen.blit(line_surface, rect)
            y += 50

    def render_skip_gauge(self, screen):
        # Render skip gauge if Enter is held
        if self.skip_start_time:
            current_time = pygame.time.get_ticks()
            hold_time = current_time - self.skip_start_time
            gauge_progress = min(hold_time / self.skip_duration, 1.0)

            gauge_width, gauge_height = 120, 30
            gauge_x, gauge_y = WIDTH - 140, HEIGHT - 50

            pygame.draw.rect(screen, (80, 0, 0), (gauge_x, gauge_y, gauge_width, gauge_height))
            pygame.draw.rect(screen, (200, 0, 0), (gauge_x, gauge_y, gauge_width * gauge_progress, gauge_height))

            skip_text = self.small_font.render("SKIP", True, (255, 255, 255))
            skip_rect = skip_text.get_rect(center=(gauge_x + gauge_width // 2, gauge_y + gauge_height // 2))
            screen.blit(skip_text, skip_rect)

    def render_dust_and_scratches(self, screen):
        # Render random dust and scratches for vintage effect
        for _ in range(50):
            x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            color = (200, 200, 200) if random.randint(0, 1) == 0 else (255, 255, 255)
            pygame.draw.circle(screen, color, (x, y), 1)
        for _ in range(10):
            x_start, y_start = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            x_end, y_end = x_start + random.randint(-20, 20), y_start + random.randint(-20, 20)
            pygame.draw.line(screen, (150, 150, 150), (x_start, y_start), (x_end, y_end), 1)

    def Exit(self):
        pygame.mixer.music.stop()
