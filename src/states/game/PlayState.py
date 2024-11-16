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
        self.paused = False
        self.paused_option = 0
        self.show_inventory = False
        self.show_instructions = False
        self.wave_number = params.get("wave_number", 1)
        self.world = World(self.wave_number, None)
        print("Entering Playstate...")
        # self.level = params['level']
        # ทำหน้าเข้าเกม
        entity_conf = ENTITY_DEFS["player"]
        self.player = Player(entity_conf)
        self.world = World(self.wave_number,self.player)

        self.player.state_machine = StateMachine()
        self.player.state_machine.SetScreen(pygame.display.get_surface())
        self.player.state_machine.SetStates(
            {
                "walk": PlayerWalkState(self.player),
                "idle": PlayerIdleState(self.player),
                "swing_sword": PlayerAttackState(self.player),
            }
        )
        self.player.ChangeState("walk")
        
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
                        
        if self.show_inventory:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.show_inventory = False
            return None
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = True
                    self.paused_option = 0  # default option
                if event.key == pygame.K_TAB:
                    self.show_inventory = True
                    
        # ถ้า paused -- โดน return ตัดจบ
        if self.paused:
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

        if self.getWinCondition() :
            if self.wave_number == 10:
                g_state_manager.Change("lastvictory")
            else :
                params = {"wave_number": self.wave_number, "victory":True}
                g_state_manager.Change("result",params)
        if self.getLoseCondition() :
            params = {"wave_number": self.wave_number, "victory":False}
            g_state_manager.Change("result",params)
        
        self.world.update(dt, events)
        #print(self.player.x,self.player.y,self.player.direction)
        # if self.player.health == 0:
        #     g_state_manager.Change("game_over")

        # temp
        # self.room.update(dt, events)
        
    def renderInventoryPage(self, screen: pygame.Surface) :
        screen.fill((80, 80, 80))

        profile_spritesheet = pygame.image.load("graphics/leonidas.png")
        profile_image_rect = pygame.Rect(1, 0, 93, 104)
        profile_image = profile_spritesheet.subsurface(profile_image_rect)
        profile_position = (50, 50)
        profile_border_rect = pygame.Rect(profile_position[0] - 5, profile_position[1] - 5, 93 + 10, 104 + 10)
        draw_bordered_rect(screen, profile_border_rect, (0, 0, 0), (0, 0, 0))  # Black border around profile
        screen.blit(profile_image, profile_position)

        font = pygame.font.SysFont(None, 40)
        name_text = font.render("Leonidas", True, (255, 0, 0))
        screen.blit(name_text, (160, 50))

        stats_font = pygame.font.SysFont(None, 30)
        #draw_stat_labels(screen, stats_font, stats, 160, 100)
        
        y_offset = 100
        for i,(stat_name, color) in enumerate(STATS_LABEL_LIST):
            label = stat_name.replace("_", " ").capitalize()
            text = stats_font.render(f"{label}: {self.player.get_stats()[i]}", True, color)
            screen.blit(text, (160, y_offset))
            y_offset += 30

        
        self.renderInventoryItem(screen)
    
    def renderInventoryItem(self, screen: pygame.Surface) :
        item_box_size = 70
        item_padding = 15
        start_x = 500
        start_y = 50
        columns = 3

        obtained_items = [0,3,0,0,1,0,0,0,2] # แต่ละอัน มีทั้งหมด 9 อัน
        
        for index in range(9):
            col = index % columns
            row = index // columns
            x = start_x + col * (item_box_size + item_padding)
            y = start_y + row * (item_box_size + item_padding)
            
            item_level = obtained_items[index]
            is_obtained = obtained_items[index]

            item_rect = pygame.Rect(x, y, item_box_size, item_box_size)
            pygame.draw.rect(screen, (100, 100, 100), item_rect)

            tier = ITEM_TIER_LIST[index]
            border_color = COLORS.get(tier, COLORS["common"])
            pygame.draw.rect(screen, border_color, item_rect, 3)

            item_image = pygame.transform.scale(ITEM_IMAGE_LIST[index], (item_box_size - 10, item_box_size - 10))
            if not is_obtained:
                item_image.set_alpha(100)
            screen.blit(item_image, (x + 5, y + 5))

            if is_obtained:
                level_font = pygame.font.SysFont(None, 20)
                level_text = level_font.render(f"{item_level}", True, (0, 0, 0))
                screen.blit(level_text, (x + item_box_size - 20, y + item_box_size - 20))
        
        
        
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
        
        if self.show_inventory:
            self.renderInventoryPage(screen)
            #self.renderInventoryItem(screen)
            return None
        if self.paused: 
            self.renderPausePage(screen)
            return None
        
        
        # World Render
        self.world.render(screen)

        # ใส่ stats ต่างๆ ภายในเกม ตรงด้านบนจอ
        # Ex. Health, Enemy Remaining, etc.
        # Display the wave number at the top center of the screen
        wave_font = pygame.font.Font('./fonts/CooperMdBT-Regular.ttf', 40)  # Adjust the font and size as needed
        wave_text = wave_font.render(f"Wave: {self.wave_number}", True, (255, 255, 255))  # White color for text
        wave_rect = wave_text.get_rect(center=(WIDTH // 2, 20))  # Position at the top center
        pygame.draw.rect(screen, (0, 0, 0), wave_rect.inflate(20, 10))  # Background rectangle for visibility
        screen.blit(wave_text, wave_rect)
        # Mock data for enemy count and health
        enemy_count = 0  # Placeholder value for enemies
        health = 100     # Placeholder value for health

        # Display enemy count on the top left
        enemy_font = pygame.font.Font('./fonts/CooperMdBT-Regular.ttf', 30)
        enemy_text = enemy_font.render(f"Enemies: {enemy_count}", True, (0, 0, 0))  # Black color for text
        enemy_rect = enemy_text.get_rect(topleft=(20, 20))
        pygame.draw.rect(screen, (255, 255, 255), enemy_rect.inflate(10, 5))  # White background for visibility
        screen.blit(enemy_text, enemy_rect)

        # Display health on the top right
        health_text = enemy_font.render(f"Health: {health}", True, (255, 0, 0))  # Red color for text
        health_rect = health_text.get_rect(topright=(WIDTH - 20, 20))
        pygame.draw.rect(screen, (255, 255, 255), health_rect.inflate(10, 5))  # White background for visibility
        screen.blit(health_text, health_rect)
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
        
            

    def Exit(self):
        print("Exiting PlayState...")
