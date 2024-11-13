from src.states.BaseState import BaseState
import pygame, sys
from src.recourses import *
from src.constants import *
from src.entity_defs import *

from src.entity_defs import EntityConf
from src.player import Player

from src.states.entity.player.PlayerWalkState import PlayerWalkState
from src.states.entity.player.PlayerIdleState import PlayerIdleState
from src.states.entity.player.PlayerAttackState import PlayerAttackState
from src.StateMachine import StateMachine

# from src.world.Dungeon import Dungeon
from src.World import World


class PlayState(BaseState):
    def __init__(self):
        pass

    def Enter(self, params):
        self.paused = True
        self.paused_option = 0
        self.show_instructions = False
        self.world = World(None, None)
        # self.level = params['level']
        # ทำหน้าเข้าเกม
        
        
        '''
        entity_conf = ENTITY_DEFS["player"]
        self.player = Player(entity_conf)
        self.world = World(self.player)

        self.player.state_machine = StateMachine()
        self.player.state_machine.SetScreen(pygame.display.get_surface())
        self.player.state_machine.SetStates(
            {
                "walk": PlayerWalkState(self.player, self.dungeon),
                "idle": PlayerIdleState(self.player),
                "swing_sword": PlayerAttackState(self.player, self.dungeon),
            }
        )

        self.player.ChangeState("walk")
        '''
    def getWinCondition(self) :
        return None
    
    def getLoseCondition(self) :
        return None

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # กด p เพื่อ pause/resume
                if event.key == pygame.K_p:
                    self.paused = True
                    self.paused_option = 0  # default option

        if self.getWinCondition() :
            pass
        if self.getLoseCondition() :
            pass
        
        # ถ้า paused -- โดน return ตัดจบ
        if self.paused:

            # ทำสามอัน: resume / retry (เริ่มด่าน 1 ใหม่) / quit
            # 0 = resume / 1 = retry / 2 = quit
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:  # go up
                        # self.paused_option = [2, 0, 1][self.paused_option]
                        self.paused_option = (self.paused_option - 1) % 4
                    if event.key == pygame.K_s:  # go down
                        # self.paused_option = [1, 2, 0][self.paused_option]
                        self.paused_option = (self.paused_option + 1) % 4
                    if event.key == pygame.K_RETURN:  # กด enter
                        if self.paused_option == 0:
                            self.paused = False
                            # เล่นต่อ
                        elif self.paused_option == 1:
                            self.paused = False
                            # เริ่มใหม่ตั้งแต่ด่านแรก
                        elif self.paused_option == 2:  # Help
                            self.show_instructions = True
                            
                        elif self.paused_option == 3:
                            g_state_manager.Change("start")
                            # pygame.quit()
                            # sys.exit()
                    elif self.show_instructions and event.key == pygame.K_BACKSPACE:
                        self.show_instructions = False  # Close instructions page
            return None

        #self.World.update(dt, events)

        # if self.player.health == 0:
        #     g_state_manager.Change("game_over")

        # temp
        # self.room.update(dt, events)
    def renderPausePage(self, screen: pygame.Surface):
        if self.show_instructions:
            self.render_instructions(screen)
        else:
            # Render pause menu options
            screen.fill((0, 0, 0))
            t_paused_option = ["Resume", "Retry", "Help", "Quit"]
            t_paused_color = [(255, 255, 255)] * 4
            t_paused_color[self.paused_option] = (255, 165, 0)  # Highlight selected option
            
            t_paused_option_font = [None] * 4
            for i in range(4):
                t_paused_option_font[i] = gFonts["Pause"].render(t_paused_option[i], False, t_paused_color[i])
            t_rect = [None] * 4
            for i in range(4):
                t_rect[i] = t_paused_option_font[i].get_rect(center=(WIDTH // 2, HEIGHT // 2 + 72 * (i - 1)))
                screen.blit(t_paused_option_font[i], t_rect[i])
                
    def render_instructions(self, screen):
        # Display instructions on black background
        screen.fill((0, 0, 0))
        instructions = [
            "The Tome of Victory",
            "WASD : Move Leonidas",
            "TAB : Inventory",
            "ESC : Pause"
        ]
        
        # Render instructions with dramatic spacing and style
        font = pygame.font.Font('./fonts/CooperMdBT-Regular.ttf', 40)
        y = HEIGHT / 4
        title_surface = font.render(instructions[0], True, (255, 215, 0))  # Gold color for title
        title_rect = title_surface.get_rect(center=(WIDTH / 2, y))
        screen.blit(title_surface, title_rect)
        y += 100  # Space below title

        # Render rest of instructions in white
        for line in instructions[1:]:
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WIDTH / 2, y))
            screen.blit(text_surface, text_rect)
            y += 80  # Spacing between lines

        # Optional: Draw a golden frame around instructions
        pygame.draw.rect(screen, (255, 215, 0), (50, 50, WIDTH - 100, HEIGHT - 100), 5)

        # Display "Press BackTab to exit" at the bottom left
        hint_font = pygame.font.Font('./fonts/CooperMdBT-Regular.ttf', 24)
        hint_text = hint_font.render("Press Backspace to exit", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(bottomleft=(20, HEIGHT - 20))
        screen.blit(hint_text, hint_rect)
    
    def render(self, screen: pygame.Surface):
        # World Render
        self.world.render(screen)

        # ใส่ stats ต่างๆ ภายในเกม ตรงด้านบนจอ
        # Ex. Health, Enemy Remaining, etc.

        '''
        health_left = self.player.health

        for i in range(3):
            if health_left > 1:
                heart_frame = 2
            elif health_left ==1:
                heart_frame = 1
            else:
                heart_frame = 0

            screen.blit(gHeart_image_list[heart_frame], (i * (TILE_SIZE+3), 6))
            health_left -=2

        '''

        # temp
        # self.room.render(screen)
        if self.paused: self.renderPausePage(screen)
            

    def Exit(self):
        pass
