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

gPlayer_animation_list = {"right": sprite_collection["leonidas_walk_right"].animation,
                         "left": sprite_collection["leonidas_walk_left"].animation,
                        "attack_right": sprite_collection["leonidas_attack_right"].animation,
                        "attack_left": sprite_collection["leonidas_attack_left"].animation
}

gGeeGee_animation_list = {"right": sprite_collection["geegee_walk_right"].animation,
                         "left": sprite_collection["geegee_walk_left"].animation,
                        "attack_right": sprite_collection["geegee_attack_right"].animation,
                        "attack_left": sprite_collection["geegee_attack_left"].animation
}

gXerxes_animation_list = {"walk": sprite_collection["xerxes_walk"].animation,
                        "attack_right": sprite_collection["loog_nong_attack_right"].animation,
                        "attack_left": sprite_collection["loog_nong_attack_left"].animation
}
gLoog_nong_animation_list = {"right": sprite_collection["loog_nong_walk"].animation,
                         "left": sprite_collection["loog_nong_walk"].animation,
                        "attack_right": sprite_collection["loog_nong_attack_right"].animation,
                        "attack_left": sprite_collection["loog_nong_attack_left"].animation
}
