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
        self.attack_boss = self.attack
        self.health_regen = 1
        # {"name": "Sword of Leonidas", "description": "+5% Attack Damage", "tier": "common"},
        # {"name": "Hermes's boots", "description": "+5% Movement Speed", "tier": "common"},
        # {"name": "Armor of King Dream", "description": "+10 Health", "tier": "uncommon"},
        # {"name": "Shield of Sparta", "description": "+5 Armor", "tier": "common"},
        # {"name": "Helm of Hercules", "description": "+10 Armor", "tier": "uncommon"},
        # {"name": "Mark's Gauntlet", "description": "+3 Attack Damage", "tier": "uncommon"},
        # {"name": "Ring of Midas", "description": "+10% Damage against bosses", "tier": "legendary"},
        # {"name": "Amulet of Athena", "description": "+0.5/s Health regenerate", "tier": "legendary"},
        # {"name": "Cape of the Phantom", "description": "+5% Damage reduction", "tier": "legendary"}
        self.armor += 5*self.items[3] + 10*self.items[4]
        self.init_health += 10*self.items[2]
        self.health = self.init_health
        print(self.health,self.items[2])
        self.attack *= 1+0.05*self.items[0]; self.attack += 3*self.items[5]
        self.health_regen += 0.5*self.items[7]
        self.attack_boss += 0.10*self.items[6] ; self.attack_boss += 3*self.items[5]; self.attack_boss *= 1+0.04*self.items[0];
        self.walk_speed *= (1+0.05*self.items[1])
        self.dmg_reduct += 5*self.items[8]
        self.world = None  # World reference for interaction with enemies
        self.rage_effect_time = 0
        self.rage_times_used = 0
        
        try:
            pygame.mixer.init()  # Make sure mixer is initialized
            self.rage_sound = pygame.mixer.Sound("./sounds/fusrodah.mp3")
            print("[DEBUG] Rage sound loaded successfully")
        except Exception as e:
            print(f"[DEBUG] Error loading rage sound: {e}")
            self.rage_sound = None
    
    def get_stats(self) :
        return [
            self.init_health, 
            self.attack, 
            self.walk_speed, 
            self.armor, 
            str(self.dmg_reduct)+'%',
            str(self.attack_boss),
            str(self.health_regen)+'%' 
        ]

    def update(self, dt, events):
        super().update(dt, events)
        # Handle rage activation input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print(f"[DEBUG] R pressed - Rage status: {self.rage_damage_taken}/{self.rage_threshold}")
                    if self.rage_damage_taken >= self.rage_threshold and not self.is_rage_active:
                        self.activate_rage()
        
        # Update rage visual effect
        if self.is_rage_active:
            self.rage_effect_time += dt

        self.health = min(self.init_health, self.health + self.health_regen * dt)
    def activate_rage(self):
        print(f"[DEBUG] Activating Rage! Current attack: {self.attack}")
        self.is_rage_active = True
        self.rage_timer = 0
        self.attack = self.original_attack * 2  # Double attack
        self.invulnerable = True
        
        # Reset rage accumulation and increase threshold
        self.rage_damage_taken = 0
        self.rage_times_used += 1 
        self.rage_threshold = 100 * (2 ** self.rage_times_used)
        print(f"[DEBUG] New rage threshold: {self.rage_threshold}")
        
        # Play rage sound
        if self.rage_sound:
            self.rage_sound_channel = self.rage_sound.play()
    
    def deactivate_rage(self):
        print("[DEBUG] Deactivating Rage")
        self.is_rage_active = False
        self.attack = self.original_attack
        self.invulnerable = False
        self.rage_effect_time = 0
        
        # Stop rage sound
        if self.rage_sound_channel:
            self.rage_sound_channel.stop()

    def Collides(self, target):
        y, height = self.y + self.height/2, self.height-self.height/2

        return not (self.x + self.width < target.x or self.x > target.x + target.width or
                    y + height < target.y or y > target.y + target.height)


    def render(self):
        super().render()
        # Render rage meter
        if not self.is_rage_active:
            screen = pygame.display.get_surface()
            
            # Render rage meter above player
            meter_width = 50
            meter_height = 5
            meter_x = self.x + (self.width - meter_width) / 2
            meter_y = self.y - 10
            
            # Background bar
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                (meter_x, meter_y, meter_width, meter_height)
            )
            
            # Fill bar
            fill_ratio = min(self.rage_damage_taken / self.rage_threshold, 1.0)
            fill_width = fill_ratio * meter_width
            if fill_width > 0:
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (meter_x, meter_y, fill_width, meter_height)
                )


    def CreateAnimations(self):
        self.animation_list = gPlayer_animation_list