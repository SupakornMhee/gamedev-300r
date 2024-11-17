import pygame
from src.constants import *
from src.HitBox import Hitbox

class EntityBase():
    def __init__(self, conf):
        self.entity_type = conf.entity_type
        self.direction = 'right'
        self.direction_x = 'right'
        self.direction_y = 'down'
        self.idle_x = True
        self.idle_y = True
        self.animation_list = conf.animation
        self.attack = conf.attack
        #print(f"[DEBUG] {self.__class__.__name__} initialized with Attack={self.attack}.")
        # dims
        self.x = conf.x
        self.y = conf.y
        self.width = conf.width
        self.height = conf.height
        
        # sprite offset          check
        self.offset_x = conf.offset_x or 0
        self.offset_y = conf.offset_y or 0

        self.walk_speed = conf.walk_speed

        self.health = conf.health
        self.init_health = conf.health
        
        #invincible
        self.invulnerable = False
        self.invulnerable_duration = 0
        self.invulnerable_timer = 0

        #timer for turning transparency (flash)
        self.flash_timer = 0

        self.is_dead = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        print(f"[DEBUG] EntityBase initialized: {self.rect} with health={self.health}, attack={self.attack}.")
        self.state_machine = None
        self.curr_animation = None
        
        self.cooldown = 0
        self.able_to_attack = True
        
    def GetHitBox(self) :
        if self.direction_x == 'left':
            hitbox_x = self.x - (self.width * 0.7)  # Adjust hitbox for left attack
            hitbox_y = self.y
        elif self.direction_x == 'right':
            hitbox_x = self.x + self.width  # Adjust hitbox for right attack
            hitbox_y = self.y
        else:  # Default case
            hitbox_x = self.x
            hitbox_y = self.y

        return Hitbox(hitbox_x, hitbox_y, self.width * 0.7, self.height)
    def CreateAnimations(self):
        pass

    def ChangeCoord(self, x=None, y=None):
        if x is not None:
            self.x = x
            self.rect.x = self.x

        if y is not None:
            self.y=y
            self.rect.y = self.y

    def MoveX(self, x):
        new_x = self.x + x
        # self.rect.x = self.x
        if 0 <= new_x <= WIDTH - self.width:
            self.x = new_x
            self.rect.x = self.x
    def Attack(self, target):
        if target and not target.invulnerable:
            print(f"{self.__class__.__name__} attacking {target.__class__.__name__} with {self.attack} damage.")
            target.Damage(self.attack)
            target.SetInvulnerable(0.5)
    def MoveY(self, y):
        new_y = self.y + y
    # Ensure the player stays within vertical boundaries
        if 0 <= new_y <= HEIGHT - self.height:
            self.y = new_y
            self.rect.y = self.y

    def Collides(self, target):
        return not(self.rect.x + self.width < target.rect.x or self.rect.x > target.rect.x + target.width or
                   self.rect.y + self.height < target.rect.y or self.rect.y > target.rect.y + target.height)

    def Damage(self, dmg):
        print(f"Leonidas takes {dmg} damage.")
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            print("Leonidas is dead.")

    def Restore(self) :
        if self.health != self.init_health :
            self.health = self.init_health
    
    def SetInvulnerable(self, duration):
        self.invulnerable = True
        self.invulnerable_duration = duration

    def ChangeState(self, name):
        self.state_machine.Change(name)

    def ChangeAnimation(self, name):
        self.curr_animation = self.animation_list[name]

    def update(self, dt, events):
        if self.invulnerable:
            self.flash_timer = self.flash_timer+dt
            self.invulnerable_timer = self.invulnerable_timer+dt

            if self.invulnerable_timer > self.invulnerable_duration:
                self.invulnerable = False
                self.invulnerable_timer = 0
                self.invulnerable_duration=0
                self.flash_timer=0

        self.state_machine.update(dt, events)

        if self.curr_animation:
            self.curr_animation.update(dt)

    def ProcessAI(self, params, dt):
        self.state_machine.ProcessAI(params, dt)

    def render(self, adjacent_offset_x=0, adjacent_offset_y=0):
        if self.invulnerable and self.flash_timer > 0.06:
            self.flash_timer = 0
            if self.curr_animation.idleSprite is not None:
                self.curr_animation.idleSprite.set_alpha(64)
            self.curr_animation.image.set_alpha(64)

        self.x = self.x + adjacent_offset_x
        self.y = self.y + adjacent_offset_y
        self.state_machine.render()
        if self.curr_animation.idleSprite is not None:
            self.curr_animation.idleSprite.set_alpha(255)
        self.curr_animation.image.set_alpha(255)

        self.x = self.x - adjacent_offset_x
        self.y = self.y - adjacent_offset_y

