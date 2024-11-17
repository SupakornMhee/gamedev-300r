import math

from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame
from src.recourses import *
from src.entity_defs import *

class EntityAttackState(BaseState):
    def __init__(self, entity):
        self.entity = entity
        self.attack_timer = 0

    def Enter(self, params):
        #direction = self.entity.direction_x
        #self.entity.ChangeAnimation(f"attack_{direction}")
        self.attack_timer = 0  # Reset attack timer
        
        if self.entity.direction_x == 'left':
            hitbox_x = self.entity.x - (self.entity.width * 0.7)  # Adjust hitbox for left attack
            hitbox_y = self.entity.y
        elif self.entity.direction_x == 'right':
            hitbox_x = self.entity.x + self.entity.width  # Adjust hitbox for right attack
            hitbox_y = self.entity.y
        else:  # Default case
            hitbox_x = self.entity.x
            hitbox_y = self.entity.y

        self.sword_hitbox = Hitbox(hitbox_x, hitbox_y, self.entity.width * 0.7, self.entity.height)

        # Reset and change entity animation
        self.entity.curr_animation.Refresh()
        self.entity.ChangeAnimation("attack_" + self.entity.direction_x)

    def Exit(self):
        pass

    def update(self, dt, events):
        pass
    
    def ProcessAI(self, params, dt): 
        self.entity.ChangeState("walk")
        self.attack_timer += dt
        if self.entity.curr_animation.times_played > 0:
            self.entity.curr_animation.times_played = 0
            self.entity.ChangeState("walk")
            return
        # Perform attack logic during animation
        # if self.attack_timer > 0.5:  # Example: Attack every 0.5 seconds
        #     if self.entity.target and self.entity.Collides(self.entity.target) and not self.entity.target.invulnerable:
        #         #self.entity.Attack(self.entity.target)
        #         self.entity.target.SetInvulnerable(0.5)

        
            
    def render(self, screen):
        animation = self.entity.curr_animation.image
        screen.blit(animation, (self.entity.x, self.entity.y))
        
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
            self.sword_hitbox.x, self.sword_hitbox.y, self.sword_hitbox.width, self.sword_hitbox.height
        ))
