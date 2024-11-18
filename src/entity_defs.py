from src.constants import *
from src.recourses import *
class EntityConf:
    def __init__(self, animation, walk_speed=60, x=None, y=None, width=48, height=48, health=100, attack=10, offset_x=0, offset_y=0,entity_type="GeeGee"):
        
        self.animation = animation
        self.walk_speed = walk_speed

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.health = health
        self.attack = attack
        
        self.entity_type = entity_type
        
        self.offset_x = offset_x
        self.offset_y = offset_y


ENTITY_DEFS = {
    'player': EntityConf(animation=gPlayer_animation_list, walk_speed=90,
                         x=WIDTH/2-24, y=HEIGHT/2 -33, width=350*0.3, height=373*0.3,
                          health=100, attack=15, offset_x=0, offset_y=0),
    
    'geegee':EntityConf(animation=gGeeGee_animation_list, walk_speed=40, 
                        health=20, attack=5,
                        width=184*0.4, height=228*0.4),

    'xerxes':EntityConf(animation=gXerxes_animation_list, width=226*0.4, height=300*0.4, 
                        health=170, attack=30, offset_x=0, offset_y=0,entity_type="xerxes"),
    
    'loog_nong':EntityConf(animation=gLoog_nong_animation_list, width=229*0.5, height=400*0.5,
                        health = 130, attack = 20, offset_x=0, offset_y=0,entity_type="loog_nong")
}
