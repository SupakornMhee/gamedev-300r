import math

from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame
from src.recourses import *
from src.entity_defs import *
class PlayerAttackState(BaseState):
    def __init__(self, player):
        self.player = player
        
    def Enter(self, params=None):
        # Setup sword hitbox based on player direction
        if self.player.direction_x == 'left':
            hitbox_x = self.player.x - (self.player.width * 0.7)  # Adjust hitbox for left attack
            hitbox_y = self.player.y
        elif self.player.direction_x == 'right':
            hitbox_x = self.player.x + self.player.width  # Adjust hitbox for right attack
            hitbox_y = self.player.y
        else:  # Default case
            hitbox_x = self.player.x
            hitbox_y = self.player.y

        self.sword_hitbox = Hitbox(hitbox_x, hitbox_y, self.player.width * 0.7, self.player.height)

        # Reset and change player animation
        self.player.curr_animation.Refresh()
        self.player.ChangeAnimation("attack_" + self.player.direction_x)

    def Exit(self):
        pass

    def update(self, dt, events):
        # Return to idle state after attack animation finishes
        if self.player.curr_animation.times_played > 0:
            self.player.curr_animation.times_played = 0
            self.player.ChangeState("idle")
            return

        # Check collisions with GeeGee entities
        for entity in self.player.world.entities:
            if entity.entity_type == "GeeGee":  # Check if the entity is GeeGee
                if entity.Collides(self.sword_hitbox):
                    print(f"[DEBUG] Leonidas hit GeeGee at ({entity.x}, {entity.y}).")
                    entity.health -= self.player.attack
                    print(f"[DEBUG] GeeGee health: {entity.health}")

                    if entity.health <= 0:
                        print(f"[DEBUG] GeeGee at ({entity.x}, {entity.y}) is dead.")
                        self.player.world.entities.remove(entity)

        # Handle attack input
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.ChangeState('swing_sword')

    def render(self, screen):
        # Render the player animation
        animation = self.player.curr_animation.image
        screen.blit(animation, (math.floor(self.player.x), math.floor(self.player.y)))

        # Draw sword hitbox for debugging
        pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(
            self.sword_hitbox.x, self.sword_hitbox.y, self.sword_hitbox.width, self.sword_hitbox.height
        ))