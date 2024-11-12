from src.states.BaseState import BaseState
import pygame, sys
from src.recourses import *
from src.constants import *
import random
from moviepy.editor import VideoFileClip

class ResultState(BaseState):
    def __init__(self):
        self.victory = False
        self.title_duration = 2000
        self.message_duration = 2000  # Duration for each message
        self.start_time = None
        self.wave_number = 1
        self.title_animation_progress = -800
        self.sparta_music_playing = False
        
        # Music settings
        self.music_loaded = False
        self.victory_music = "./sounds/300Victory.mp3"
        self.defeat_music = "./sounds/Conan_sad_music.mp4"
        
        
        # Video and audio handling
        self.video_clip = None
        self.video_surface = None
        self.show_video = False
        self.video_start_time = None
        self.sparta_video = "./sounds/Thisissparta.mp4"
        self.sparta_audio = "./sounds/Thisissparta.mp3"  # แยกไฟล์เสียงออกมา
        self.audio_started = False
        
        # Special sequence for Wave 1
        self.special_victory_sequence_wave1 = [
            "Don't be too happy, these were just worthless soldiers to me.",
            "From now on, my soldiers will be even stronger.",
            "Can you handle it, Leonidas?"
        ]
        
        # Add state flags for Wave 1
        self.show_wave1_sequence = False
        self.wave1_sequence_index = 0
        self.wave1_sequence_start_time = None
        
        # Special sequence for Wave 4
        self.special_victory_sequence_wave4 = [
            "The Persian messenger arrives,",
            "ordering the Spartans to submit to the Persian Empire.",
            "If you submit, Leonidas and the Spartans shall offer earth and water to spare their lives.", 
            "But if you refuse, you will descend to hell, you scoundrel!"
        ]
        self.sequence_index = 0
        self.sequence_start_time = None
        self.show_sequence = False
        
        # State flags
        self.show_title = True
        self.show_but_message = False
        self.but_duration = 1000
        self.but_start_time = None
        self.show_choice = False
        self.choice_messages = [
            "What will Leonidas choose?",
            "Press Y to submit to Xerxes",
            "Press N to fight for Sparta's honor"
        ]
        
        # Victory and Defeat messages
        self.victory_messages = {
            1: "You have begun your journey as a true warrior!",
            2: "Your strength grows with each battle!",
            3: "You're proving yourself worthy of the Spartan legacy!",
            4: "The Persian messenger arrives, ordering the Spartans to submit to the Persian Empire. "
               "If you submit, Leonidas and the Spartans shall offer earth and water to spare their lives. "
               "But if you refuse, you will descend to hell, you scoundrel!",
            5: "You've overcome the messenger's threats and continued the fight!",
            6: "Sparta's spirit burns brighter with each victory!",
            7: "Even mighty Persian forces fall before you!",
            8: "Victory is within reach! The gods favor you!",
            9: "Nothing stands between you and ultimate glory!",
            10: "You have changed history and defeated Xerxes!"
        }
        self.defeat_messages = {
            1: "Couldn't even defeat the lowly soldiers? What hope do you have against King Xerxes?",
            2: "A little tougher soldiers, and you're already struggling?",
            3: "A little tougher soldiers, and you're already struggling?",
            4: "A little tougher soldiers, and you're already struggling?",
            5: "This is the result of rejecting my offer. You could have avoided this pain, fool.",
            6: "A little tougher soldiers, and you're already struggling?",
            7: "A little tougher soldiers, and you're already struggling?",
            8: "A little tougher soldiers, and you're already struggling?",
            9: "A little tougher soldiers, and you're already struggling?",
            10: "History is history, fool. I am king, and you're just a loser!"
        }

    def Enter(self, params):
        if params is None:
            params = {}
        self.victory = params.get("victory", True)
        self.wave_number = params.get("wave_number", 5)
        self.start_time = pygame.time.get_ticks()
        self.show_title = True
        self.show_but_message = False
        self.show_sequence = False
        self.sequence_index = 0
        self.sequence_start_time = None
        self.show_wave1_sequence = False
        self.wave1_sequence_index = 0
        self.wave1_sequence_start_time = None
        self.show_choice = False
        self.title_animation_progress = -800

        # Load video for Wave 5 victory
        if self.victory and self.wave_number == 5:
            try:
                self.video_clip = VideoFileClip(self.sparta_video)
                self.audio_started = False
                pygame.mixer.music.load(self.sparta_audio)  # โหลดไฟล์เสียง
            except Exception as e:
                print(f"Could not load video/audio: {e}")
                self.video_clip = None

        # Load and play music based on victory/defeat
        if not self.music_loaded:
            try:
                if self.victory:
                    pygame.mixer.music.load(self.victory_music)
                else:
                    pygame.mixer.music.load(self.defeat_music)
                
                pygame.mixer.music.set_volume(0.0)  # Start with volume 0
                pygame.mixer.music.play(-1)  # Loop indefinitely
                
                # Fade in over 1 second
                for vol in range(0, 10):
                    pygame.mixer.music.set_volume(vol/10.0)
                    pygame.time.wait(100)
                
                self.music_loaded = True
            except Exception as e:
                print(f"Could not load music: {e}")

        # Set atmosphere based on victory or defeat
        if self.victory:
            self.background_color = (255, 223, 88)
            self.title_color = (255, 0, 0)
            self.shadow_color = (150, 150, 0)
            self.message_color = (0, 0, 0)
            self.effect_particles = self.generate_particles((255, 255, 0), 150)
        else:
            self.background_color = (30, 30, 30)
            self.title_color = (200, 0, 0)
            self.shadow_color = (50, 0, 0)
            self.message_color = (150, 150, 150)
            self.effect_particles = self.generate_particles((100, 100, 100), 80)

    def Exit(self):
        # Clean up video resources
        if self.video_clip is not None:
            self.video_clip.close()
            self.video_clip = None
        
        # # Stop music
        # if self.music_loaded:
        #     pygame.mixer.music.fadeout(1000)  # Fade out over 1 second
        #     self.music_loaded = False
        # Stop all music before exiting
        pygame.mixer.music.stop()  # หยุดเพลงทันทีก่อน
        
        # Reset all music flags
        self.music_loaded = False
        self.sparta_music_playing = False
        self.audio_started = False
        

            
        print("Exiting ResultState...")

    def generate_particles(self, color, alpha):
        particles = []
        for _ in range(50):
            particle = {
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "size": random.randint(1, 3),
                "alpha": alpha,
                "color": color
            }
            particles.append(particle)
        return particles

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                if self.video_clip:
                    self.video_clip.close()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.video_clip:
                        self.video_clip.close()
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                # Wave 4 victory choice handler
                if self.show_choice and self.victory and self.wave_number == 4:
                    if event.key in [pygame.K_y, pygame.K_n]:
                        pygame.mixer.music.fadeout(500)
                        self.music_loaded = False
                        if event.key == pygame.K_y:  # Submit to Xerxes
                            g_state_manager.Change('start')
                        else:  # Continue fighting
                            g_state_manager.Change('play', {'wave_number': self.wave_number + 1})
                # Regular return key handler - only for defeat cases
                elif event.key == pygame.K_RETURN and not self.victory:
                    pygame.mixer.music.fadeout(500)
                    self.music_loaded = False
                    g_state_manager.Change('start')

        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.start_time

        # Special handling for Wave 1 victory sequence
        if self.victory and self.wave_number == 1:
            if self.show_title:
                if self.title_animation_progress < 0:
                    self.title_animation_progress += 40
                if time_elapsed > self.title_duration:
                    self.show_title = False
            elif not self.show_wave1_sequence:
                if time_elapsed > self.title_duration + self.message_duration:
                    self.show_wave1_sequence = True
                    self.wave1_sequence_start_time = current_time
            elif self.show_wave1_sequence:
                if self.wave1_sequence_start_time is None:
                    self.wave1_sequence_start_time = current_time
                
                time_in_sequence = current_time - self.wave1_sequence_start_time
                message_total_time = self.message_duration * (self.wave1_sequence_index + 1)
                
                if time_in_sequence > message_total_time:
                    self.wave1_sequence_index += 1
                    if self.wave1_sequence_index >= len(self.special_victory_sequence_wave1):
                        pygame.mixer.music.fadeout(500)
                        self.music_loaded = False
                        g_state_manager.Change('play', {'wave_number': self.wave_number + 1})

        # Special handling for Wave 5 victory sequence
        elif self.victory and self.wave_number == 5:
            if self.show_title:
                if self.title_animation_progress < 0:
                    self.title_animation_progress += 40
                if time_elapsed > self.title_duration:
                    self.show_title = False
            elif not self.show_video:
                if time_elapsed > self.title_duration + self.message_duration:
                    self.show_video = True
                    self.video_start_time = current_time
                    if not self.sparta_music_playing:
                        try:
                            pygame.mixer.music.stop()  # หยุดเพลงที่กำลังเล่นอยู่ก่อน
                            pygame.mixer.music.load(self.sparta_audio)
                            pygame.mixer.music.play()
                            self.sparta_music_playing = True
                        except Exception as e:
                            print(f"Could not load sparta audio: {e}")
            elif self.show_video and self.video_clip:
                video_time = (current_time - self.video_start_time) / 1000.0
                if video_time >= self.video_clip.duration:
                    pygame.mixer.music.stop()  # หยุดเพลงก่อนเปลี่ยน state
                    self.sparta_music_playing = False
                    g_state_manager.Change('play', {'wave_number': self.wave_number + 1})

        # Special handling for Wave 4 victory sequence
        elif self.victory and self.wave_number == 4:
            if self.show_title:
                if self.title_animation_progress < 0:
                    self.title_animation_progress += 40
                if time_elapsed > self.title_duration:
                    self.show_title = False
                    self.show_but_message = True
                    self.but_start_time = current_time
            elif self.show_but_message:
                if current_time - self.but_start_time > self.but_duration:
                    self.show_but_message = False
                    self.show_sequence = True
                    self.sequence_start_time = current_time
            elif self.show_sequence:
                if self.sequence_start_time is None:
                    self.sequence_start_time = current_time
                
                time_in_sequence = current_time - self.sequence_start_time
                message_total_time = self.message_duration * (self.sequence_index + 1)
                
                if time_in_sequence > message_total_time:
                    self.sequence_index += 1
                    if self.sequence_index >= len(self.special_victory_sequence_wave4):
                        self.show_sequence = False
                        self.show_choice = True
        
        # Regular victory message timing
        elif self.victory:
            if self.show_title:
                if self.title_animation_progress < 0:
                    self.title_animation_progress += 40
                if time_elapsed > self.title_duration:
                    self.show_title = False
            elif time_elapsed > self.title_duration + self.message_duration:
                pygame.mixer.music.fadeout(500)
                self.music_loaded = False
                g_state_manager.Change('play', {'wave_number': self.wave_number + 1})
                
        # Regular defeat message timing
        else:
            if self.show_title:
                if self.title_animation_progress < 0:
                    self.title_animation_progress += 40
                if time_elapsed > self.title_duration:
                    self.show_title = False

    def render(self, screen):
        # Special rendering for Wave 5 victory with video
        if self.victory and self.wave_number == 5:
            if self.show_video and self.video_clip:
                try:
                    # Get current video time
                    video_time = (pygame.time.get_ticks() - self.video_start_time) / 1000.0
                    
                    # Get video frame at current time
                    frame = self.video_clip.get_frame(video_time % self.video_clip.duration)
                    
                    # Convert frame to pygame surface
                    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                    
                    # Scale video to screen size
                    scaled_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
                    
                    # Draw video frame
                    screen.blit(scaled_surface, (0, 0))
                except Exception as e:
                    print(f"Error rendering video frame: {e}")
                    self.show_video = False
                    g_state_manager.Change('play', {'wave_number': self.wave_number + 1})
            else:
                # Regular rendering for pre-video sequence
                screen.fill(self.background_color)
                if self.show_title:
                    self._render_title(screen, "VICTORY!")
                elif not self.show_video:
                    message = self.victory_messages[self.wave_number]
                    self.render_wrapped_text_with_shadow(
                        screen, message, (WIDTH / 2, HEIGHT / 2 - 50),
                        gFonts['Story'], self.message_color, self.shadow_color
                    )
                self.render_particles(screen)
        
        # Special rendering for Wave 1 victory
        elif self.victory and self.wave_number == 1:
            screen.fill(self.background_color)
            if self.show_title:
                self._render_title(screen, "VICTORY!")
            elif not self.show_wave1_sequence:
                message = self.victory_messages[self.wave_number]
                self.render_wrapped_text_with_shadow(
                    screen, message, (WIDTH / 2, HEIGHT / 2 - 50),
                    gFonts['Story'], self.message_color, self.shadow_color
                )
            elif self.show_wave1_sequence:
                if self.wave1_sequence_index < len(self.special_victory_sequence_wave1):
                    message = self.special_victory_sequence_wave1[self.wave1_sequence_index]
                    self.render_wrapped_text_with_shadow(
                        screen, message, (WIDTH / 2, HEIGHT / 2),
                        gFonts['Story'], self.message_color, self.shadow_color
                    )
            self.render_particles(screen)
        
        # Special rendering for Wave 4 victory
        elif self.victory and self.wave_number == 4:
            screen.fill(self.background_color)
            if self.show_title:
                self._render_title(screen, "VICTORY!")
            elif self.show_but_message:
                but_surface = gFonts['Result'].render("BUT", False, self.title_color)
                but_rect = but_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                screen.blit(but_surface, but_rect)
            elif self.show_sequence:
                # Render current sequence message
                if self.sequence_index < len(self.special_victory_sequence_wave4):
                    message = self.special_victory_sequence_wave4[self.sequence_index]
                    self.render_wrapped_text_with_shadow(
                        screen, message, (WIDTH / 2, HEIGHT / 2), 
                        gFonts['Story'], self.message_color, self.shadow_color
                    )
            elif self.show_choice:
                # Render choice messages
                y_offset = -50  # Start above center
                for message in self.choice_messages:
                    self.render_wrapped_text_with_shadow(
                        screen, message, (WIDTH / 2, HEIGHT / 2 + y_offset),
                        gFonts['Story'], self.message_color, self.shadow_color
                    )
                    y_offset += 50  # Move down for next message
            self.render_particles(screen)
        
        # Regular victory/defeat rendering
        else:
            screen.fill(self.background_color)
            if self.show_title:
                title_text = "VICTORY!" if self.victory else "DEFEAT!"
                self._render_title(screen, title_text)
            else:
                message = self.victory_messages[self.wave_number] if self.victory else self.defeat_messages[self.wave_number]
                self.render_wrapped_text_with_shadow(
                    screen, message, (WIDTH / 2, HEIGHT / 2 - 50),
                    gFonts['Story'], self.message_color, self.shadow_color
                )
                
                # Only show "Press Enter to Restart" for defeat cases
                if not self.victory:
                    prompt_surface = gFonts['Story'].render("Press Enter to Restart", False, self.title_color)
                    prompt_rect = prompt_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 300))
                    screen.blit(prompt_surface, prompt_rect)

            self.render_particles(screen)
  

    def _render_title(self, screen, title_text):
        # Render title shadow
        title_surface = gFonts['Result'].render(title_text, False, self.shadow_color)
        title_rect = title_surface.get_rect(center=(WIDTH / 2 + 5, HEIGHT / 2 + 5 + self.title_animation_progress))
        screen.blit(title_surface, title_rect)
        
        # Render title
        title_surface = gFonts['Result'].render(title_text, False, self.title_color)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 + self.title_animation_progress))
        screen.blit(title_surface, title_rect)

    def render_particles(self, screen):
        for particle in self.effect_particles:
            particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle["color"] + (particle["alpha"],), 
                             (particle["size"], particle["size"]), particle["size"])
            screen.blit(particle_surface, (particle["x"], particle["y"]))
            particle["y"] += random.randint(-1, 1)
            particle["x"] += random.randint(-1, 1)

    def render_wrapped_text_with_shadow(self, screen, text, position, font, color, shadow_color, max_width=600):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_surface = font.render(test_line, True, color)
            if test_surface.get_width() > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        lines.append(current_line)
        y_offset = 0
        
        for line in lines:
            # Render shadow
            shadow_surface = font.render(line, True, shadow_color)
            shadow_rect = shadow_surface.get_rect(center=(position[0] + 3, position[1] + y_offset + 3))
            screen.blit(shadow_surface, shadow_rect)

            # Render text
            line_surface = font.render(line, True, color)
            line_rect = line_surface.get_rect(center=(position[0], position[1] + y_offset))
            screen.blit(line_surface, line_rect)

            y_offset += line_surface.get_height() + 5