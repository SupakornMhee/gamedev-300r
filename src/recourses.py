import pygame
from src.Util import SpriteManager, Animation
import src.Util as Util
from src.StateMachine import *

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

gFonts = {
    'title': pygame.font.Font('fonts/title.ttf',60),
    'Press_Enter': pygame.font.Font('fonts/title.ttf',100),
    'Story': pygame.font.Font('fonts/CooperMdBT-Regular.ttf',48),
    'Pause': pygame.font.Font('fonts/title.ttf',60),
    'Result': pygame.font.Font('fonts/Oregano-Italic.ttf',80)
}

gPlayer_animation_list = {"down": sprite_collection["character_walk_down"].animation,
                         "right": sprite_collection["character_walk_right"].animation,
                         "up": sprite_collection["character_walk_up"].animation,
                         "left": sprite_collection["character_walk_left"].animation,
                        "attack_down": sprite_collection["character_attack_down"].animation,
                        "attack_right": sprite_collection["character_attack_right"].animation,
                        "attack_up": sprite_collection["character_attack_up"].animation,
                        "attack_left": sprite_collection["character_attack_left"].animation
}

gGeeGee_animation_list = {"right": sprite_collection["geegee_walk_right"].animation,
                         "left": sprite_collection["geegee_walk_left"].animation,
                        "attack_right": sprite_collection["geegee_attack_right"].animation,
                        "attack_left": sprite_collection["geegee_attack_left"].animation
}