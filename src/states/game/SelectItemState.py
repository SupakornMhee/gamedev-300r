from src.states.BaseState import BaseState
import pygame, sys
from src.recourses import *
from src.constants import *
import random 

from src.entity_defs import EntityConf
from src.player import Player

from src.states.entity.player.PlayerWalkState import PlayerWalkState
from src.states.entity.player.PlayerIdleState import PlayerIdleState
from src.states.entity.player.PlayerAttackState import PlayerAttackState
from src.StateMachine import StateMachine

class SelectItemState(BaseState) :
    def __init__(self):
        pass

    def Enter(self, params):
        self.player = None #Player()
        self.wave_number = params.get("wave_number", 5)
        self.option = 0
        self.item_option = self.getRandomItem()
        self.obtained_items = [0]*9
        pass
    
    def getRandomItem(self) :
        selection = []
        
        while len(selection) < 3:
            k = random.randint(0,8)
            c = random.random()
            if k in selection : continue
            if ITEM_TIER_LIST[k] == "legendary" and c > 0.2: continue
            if ITEM_TIER_LIST[k] == "uncommon" and c > 0.5: continue
            selection.append(k)
            
        return selection
    
    def Exit(self):
        pass

    
    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_a:  # go up
                    # self.paused_option = [2, 0, 1][self.paused_option]
                    self.option = (self.option - 1) % 3
                if event.key == pygame.K_d:  # go down
                    # self.paused_option = [1, 2, 0][self.paused_option]
                    self.option = (self.option + 1) % 3
                if event.key == pygame.K_RETURN:  # กด enter
                    # mock up
                    print("You choose", ITEM_NAME_LIST[self.item_option[self.option]])
                    #self.player.upgrade(self.item_option[self.option])
                    #self.obtained_items[self.item_option[self.option]] += 1
                    # go to load next state
                    g_state_manager.Change('load', {'wave_number': self.wave_number + 1})
                    

    
    def render(self, screen: pygame.Surface):
        screen.fill((20, 20, 20))

        main_frame_rect = pygame.Rect(50, 50, screen.get_width() - 100, screen.get_height() - 100)
        pygame.draw.rect(screen, (50, 50, 80), main_frame_rect)
        pygame.draw.rect(screen, (150, 150, 180), main_frame_rect, 5)

        title_font = pygame.font.SysFont(None, 48)
        title_lines = self.render_text_multiline("Power-Up Selection", title_font, (255, 255, 255), main_frame_rect.width - 20)
        title_y = 70
        for line_surface in title_lines:
            line_rect = line_surface.get_rect(center=(main_frame_rect.centerx, title_y))
            screen.blit(line_surface, line_rect.topleft)
            title_y += line_surface.get_height() + 5

        wave_font = pygame.font.SysFont(None, 36)
        wave_text = wave_font.render("Wave " + str(self.wave_number), True, (255, 255, 255))
        screen.blit(wave_text, (main_frame_rect.centerx - wave_text.get_width() // 2, title_y + 20))

        item_box_width = 220
        item_box_height = 320
        item_gap_x = 100
        item_gap_y = 40

        columns = 3
        start_x = main_frame_rect.left + (main_frame_rect.width - (columns * item_box_width + (columns - 1) * item_gap_x)) // 2
        start_y = title_y + 60

        item_rects = []
        #for idx, power_up in enumerate(self.item_option):
        # power_up --> 
        for idx, k in enumerate(self.item_option) : # k = index of item
            row = idx // columns
            col = idx % columns
            x_pos = start_x + col * (item_box_width + item_gap_x)
            y_pos = start_y + row * (item_box_height + item_gap_y)

            item_frame_rect = pygame.Rect(x_pos, y_pos, item_box_width, item_box_height)
            pygame.draw.rect(screen, (70, 70, 100), item_frame_rect)
            if idx == self.option : pygame.draw.rect(screen, (220, 40, 40), item_frame_rect, 3)
            else : pygame.draw.rect(screen, (150, 150, 180), item_frame_rect, 3)

            tier = ITEM_TIER_LIST[k]
            border_color = COLORS.get(tier)
            pygame.draw.rect(screen, border_color, item_frame_rect.inflate(-10, -10), 2)

            image_frame_rect = pygame.Rect(x_pos + (item_box_width - 100) // 2, y_pos + 20, 100, 100)
            pygame.draw.rect(screen, (50, 50, 80), image_frame_rect)
            pygame.draw.rect(screen, border_color, image_frame_rect, 3)

            if ITEM_IMAGE_LIST[k]:
                item_image_rect = ITEM_IMAGE_LIST[k].get_rect(center=image_frame_rect.center)
                screen.blit(ITEM_IMAGE_LIST[k], item_image_rect.topleft)

            name_font = pygame.font.SysFont(None, 30)
            item_name = ITEM_NAME_LIST[k]
            name_text = name_font.render(item_name, True, (255, 255, 255))
            name_text_rect = name_text.get_rect(center=(item_frame_rect.centerx, y_pos + 130))
            screen.blit(name_text, name_text_rect.topleft)

            tier_text = name_font.render(f"Tier: {tier.title()}", True, border_color)
            tier_text_rect = tier_text.get_rect(center=(item_frame_rect.centerx, y_pos + 160))
            screen.blit(tier_text, tier_text_rect.topleft)

            desc_font = pygame.font.SysFont(None, 24)
            description_color = get_description_color(ITEM_DESC_LIST[k])
            wrapped_desc = self.render_text_multiline(ITEM_DESC_LIST[k], desc_font, description_color, item_box_width - 20)

            for i, line_surface in enumerate(wrapped_desc):
                line_x = item_frame_rect.centerx - line_surface.get_width() // 2
                line_y = y_pos + 200 + i * 20
                screen.blit(line_surface, (line_x, line_y))

            current_level = self.obtained_items[k]
            next_level = min(current_level + 1, 3)
            level_text = desc_font.render(f"Level: {current_level} -> {next_level}" if current_level else f"Level: {current_level+1}", True, (255, 255, 255))
            level_text_rect = level_text.get_rect(center=(item_frame_rect.centerx, y_pos + item_box_height - 40))
            screen.blit(level_text, level_text_rect.topleft)

            # item_rects.append((item_frame_rect, power_up))

        pygame.display.flip()
         
    def render_text_multiline(self, text, font, color, max_width):
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        
        return [font.render(line, True, color) for line in lines]