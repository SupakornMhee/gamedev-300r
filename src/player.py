from src.EntityBase import EntityBase
from src.Dependencies import *

class Player(EntityBase):
    def __init__(self, conf):
        super(Player, self).__init__(conf)
        self.obtained_items = [0]*9 # แต่ละอัน มีทั้งหมด 9 อัน
        self.armor = 5
        self.dmg_reduct = 0
        self.attack_spd = 5
        self.attack_boss = 5
        self.health_regen = 1

    def get_stats(self) :
        return [
            self.health, 
            self.attack, 
            self.walk_speed, 
            self.attack_spd, 
            self.armor, 
            self.dmg_reduct,
            self.attack_boss,
            self.health_regen 
        ]

    def update(self, dt, events):
        super().update(dt, events)


    def Collides(self, target):
        y, height = self.y + self.height/2, self.height-self.height/2

        return not (self.x + self.width < target.x or self.x > target.x + target.width or
                    y + height < target.y or y > target.y + target.height)


    def render(self):
        super().render()

    def CreateAnimations(self):
        self.animation_list = gPlayer_animation_list