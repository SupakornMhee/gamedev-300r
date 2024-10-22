from src.states.BaseState import BaseState
import pygame, sys

from src.constants import *
from src.recourses import *

class StartState(BaseState):
    def __init__(self):
        self.bg_image = pygame.image.load("./graphics/background.png")
        self.bg_image = pygame.transform.scale(
            self.bg_image, (WIDTH + 5, HEIGHT + 5))
        

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
                    g_state_manager.Change('story_1')

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        # t_title = gFonts['zelda'].render("Legend of 50", False, (34, 34, 34))
        # rect = t_title.get_rect(center=(WIDTH / 2 + 6, HEIGHT / 2 - 90))
        # screen.blit(t_title, rect)
        text1 = "THIS IS PAGE 1 I SUS"
        t_title = gFonts['title'].render(text1, False, (255, 165, 0))
        rect = t_title.get_rect(center=(WIDTH / 2 + 6, HEIGHT / 2 - 90))
        screen.blit(t_title, rect)
        # t_title = gFonts['zelda'].render("Legend of 50", False, (175, 53, 42))
        # rect = t_title.get_rect(center=(WIDTH / 2 , HEIGHT / 2 - 96))
        # screen.blit(t_title, rect)

        t_press_enter = pygame.font.Font(None, 96).render("Press Enter to Start", False, (255, 255, 255))
        rect = t_press_enter.get_rect(center=(WIDTH / 2, HEIGHT / 2 +192))
        screen.blit(t_press_enter, rect)
        # print("This is Page 1 I SUS")
        
        
        game_title = "300: Revisited"

    def Exit(self):
        pass

