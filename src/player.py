from src.EntityBase import EntityBase
from src.Dependencies import *
from src.recourses import gPlayer_animation_list
class Player(EntityBase):
    def __init__(self, conf, items=[0]*9):
        super(Player, self).__init__(conf)
        #self.health = conf["health"]
        
        self.items = items # แต่ละอัน มีทั้งหมด 9 อัน
        self.armor = 0
        self.dmg_reduct = 0
        self.attack_spd = 5
        self.attack_boss = 5
        self.health_regen = 1
        # {"name": "Sword of Leonidas", "description": "+5% Attack Damage", "tier": "common"},
        # {"name": "Hermes's boots", "description": "+2% Movement Speed", "tier": "common"},
        # {"name": "Armor of King Dream", "description": "+10 Health", "tier": "uncommon"},
        # {"name": "Shield of Sparta", "description": "+1 Armor", "tier": "common"},
        # {"name": "Helm of Hercules", "description": "+3 Armor", "tier": "uncommon"},
        # {"name": "Mark's Gauntlet", "description": "+2 Attack Damage", "tier": "common"},
        # {"name": "Ring of Midas", "description": "+10% Damage against bosses", "tier": "legendary"},
        # {"name": "Amulet of Athena", "description": "+0.5/s Health regenerate", "tier": "legendary"},
        # {"name": "Cape of the Phantom", "description": "+5% Damage reduction", "tier": "legendary"}
        self.armor += 1*self.items[3] + 3*self.items[4]
        self.init_health += 10*self.items[2]
        self.health = self.init_health
        print(self.health,self.items[2])
        self.attack *= 1+0.04*self.items[0]; self.attack += 2*self.items[5]
        self.health_regen += 0.5*self.items[7]
        self.attack_boss += 0.10*self.items[6]
        self.walk_speed *= (1+0.02*self.items[1])
        self.dmg_reduct += 5*self.items[8]
        self.world = None  # World reference for interaction with enemies
    
    def get_stats(self) :
        return [
            self.init_health, 
            self.attack, 
            self.walk_speed, 
            self.armor, 
            str(self.dmg_reduct)+'%',
            str(self.attack_boss)+'%',
            str(self.health_regen)+'%' 
        ]

    def update(self, dt, events):
        super().update(dt, events)
        self.health = min(self.init_health, self.health + self.health_regen * dt)

    def Collides(self, target):
        y, height = self.y + self.height/2, self.height-self.height/2

        return not (self.x + self.width < target.x or self.x > target.x + target.width or
                    y + height < target.y or y > target.y + target.height)


    def render(self):
        super().render()

    def CreateAnimations(self):
        self.animation_list = gPlayer_animation_list