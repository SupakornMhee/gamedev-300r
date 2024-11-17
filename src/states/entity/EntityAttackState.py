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
        if self.entity.height>140 : #xerxes 150
            if self.entity.direction_x == 'left':
                self.entity.offset_x = 0
                self.entity.offset_y = 0
            if self.entity.direction_x == 'right':
                self.entity.offset_x = 0
                self.entity.offset_y = 0
        elif self.entity.height>110 : #loognong
            if self.entity.direction_x == 'left':
                self.entity.offset_x = 9.15
                self.entity.offset_y = 0
            if self.entity.direction_x == 'right':
                self.entity.offset_x = 9.15
                self.entity.offset_y = 0
        else :
            self.entity.offset_x = 0
            self.entity.offset_y = 0
        
        
        
        
        #direction = self.entity.direction_x
        #self.entity.ChangeAnimation(f"attack_{direction}")
        self.attack_timer = 0  # Reset attack timer
        
        if self.entity.entity_type == "xerxes":
            if self.entity.direction_x == 'left':
                hitbox_x = self.entity.x - (self.entity.width * 0.4)  # Wider hitbox for left-facing attack
                hitbox_y = self.entity.y
            elif self.entity.direction_x == 'right':
                hitbox_x = self.entity.x + self.entity.width*2  # Wider hitbox for right-facing attack
                hitbox_y = self.entity.y
            else:  # Default case
                hitbox_x = self.entity.x
                hitbox_y = self.entity.y
            hitbox_width = self.entity.width * 0.6  # Adjust hitbox width
            hitbox_height = self.entity.height * 1  # Adjust hitbox height

    # LoogNong-specific hitbox
        elif self.entity.entity_type == "loog_nong":
            if self.entity.direction_x == 'left':
                hitbox_x = self.entity.x - (self.entity.width * 0.4)  # Narrower hitbox for left-facing attack
                hitbox_y = self.entity.y
            elif self.entity.direction_x == 'right':
                hitbox_x = self.entity.x + (self.entity.width * 0.7)   # Narrower hitbox for right-facing attack
                hitbox_y = self.entity.y
            else:  # Default case
                hitbox_x = self.entity.x
                hitbox_y = self.entity.y
            hitbox_width = self.entity.width * 0.5  # Narrower width for LoogNong
            hitbox_height = self.entity.height * 0.55  # Reduced height for LoogNong

    # Default case for other entities (e.g., geegee)
        else:
            if self.entity.direction_x == 'left':
                hitbox_x = self.entity.x - (self.entity.width * 0.4)  # Adjust for left-facing attack
                hitbox_y = self.entity.y
            elif self.entity.direction_x == 'right':
                hitbox_x = self.entity.x + self.entity.width   # Adjust for right-facing attack
                hitbox_y = self.entity.y
            else:  # Default case
                hitbox_x = self.entity.x
                hitbox_y = self.entity.y
            hitbox_width = self.entity.width * 0.7  # Standard width
            hitbox_height = self.entity.height  # Full height

    # Create the sword hitbox
        self.sword_hitbox = Hitbox(hitbox_x, hitbox_y, hitbox_width, hitbox_height)


        # Reset and change entity animation
        self.entity.curr_animation.Refresh()
        self.entity.ChangeAnimation("attack_" + self.entity.direction_x)

    def Exit(self):
        pass

    def update(self, dt, events):
        if self.entity.entity_type == "xerxes":
            print(f"[DEBUG] Xerxes health: {self.entity.health}")

    # Check for collisions if Leonidas is attacking
        for target in self.entity.world.entities:
            if target.entity_type == "xerxes" and self.sword_hitbox.Collides(target.GetHitBox()):
                damage = self.entity.attack_power
                target.Damage(damage)
                print(f"[DEBUG] Leonidas attacked Xerxes for {damage} damage. Xerxes health: {target.health}")

    # Check for collisions if Xerxes is attacking Leonidas
        for target in self.entity.world.entities:
            if target.entity_type == "leonidas" and self.sword_hitbox.Collides(target.GetHitBox()):
                damage = self.entity.attack_power
                target.Damage(damage)
                print(f"[DEBUG] Xerxes attacked Leonidas for {damage} damage. Leonidas health: {target.health}")
    
    def ProcessAI(self, params, dt): 
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
        screen.blit(animation, (math.floor(self.entity.x - self.entity.offset_x),
                    math.floor(self.entity.y - self.entity.offset_y)))
        
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
            self.sword_hitbox.x, self.sword_hitbox.y, self.sword_hitbox.width, self.sword_hitbox.height
        ))
