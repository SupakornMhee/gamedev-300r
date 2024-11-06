import pygame
from src.Util import SpriteManager, Animation
import src.Util as Util
from src.StateMachine import *

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

gFonts = {
    'title': pygame.font.Font('fonts/title.ttf',60),
    'Press_Enter': pygame.font.Font('fonts/title.ttf',100),
    'Story': pygame.font.Font('fonts/title.ttf',48)
}
'''
gFonts = {
    'small': pygame.font.Font('fonts/font.ttf', 24),
    'medium': pygame.font.Font('fonts/font.ttf', 48),
    'large': pygame.font.Font('fonts/font.ttf', 96),
    'zelda_small': pygame.font.Font('fonts/zelda.otf', 96),
    'zelda': pygame.font.Font('fonts/zelda.otf', 192),
    'gothic_medium': pygame.font.Font('fonts/GothicPixels.ttf', 48),
    'gothic_large': pygame.font.Font('fonts/GothicPixels.ttf', 96),
}
'''

# gPlayer_animation_list = {"down": sprite_collection["character_walk_down"].animation,
#                          "right": sprite_collection["character_walk_right"].animation,
#                          "up": sprite_collection["character_walk_up"].animation,
#                          "left": sprite_collection["character_walk_left"].animation,
#                         "attack_down": sprite_collection["character_attack_down"].animation,
#                         "attack_right": sprite_collection["character_attack_right"].animation,
#                         "attack_up": sprite_collection["character_attack_up"].animation,
#                         "attack_left": sprite_collection["character_attack_left"].animation,
# }