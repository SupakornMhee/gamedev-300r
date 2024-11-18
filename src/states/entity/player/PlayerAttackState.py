import math

from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame
from src.recourses import *
from src.entity_defs import *
from src.EntityBase import EntityBase
from src.player import Player
class PlayerAttackState(BaseState):
    def __init__(self, player):
        self.player: Player = player
        self.hit_sound = pygame.mixer.Sound("./sounds/sword.mp3")
        
    def Enter(self, params=None):
        self.player.offset_x = 0
        self.player.offset_y = 0
        self.take_damage = True
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
            entity:EntityBase
            if entity.entity_type == "GeeGee":  # Check if the entity is GeeGee
                if entity.Collides(self.sword_hitbox) and self.take_damage:
                    print(f"[DEBUG] Leonidas hit GeeGee at ({entity.x}, {entity.y}).")
                    entity.Damage(self.player.attack)
                    self.take_damage = False
                    print(f"[DEBUG] GeeGee health: {entity.health}")
                    self.hit_sound.play()

                    if entity.health <= 0:
                        print(f"[DEBUG] GeeGee at ({entity.x}, {entity.y}) is dead.")
                        self.player.world.entities.remove(entity)
            elif entity.entity_type == "loog_nong":
                if entity.Collides(self.sword_hitbox) and self.take_damage:
                    print(f"[DEBUG] Leonidas hit Loog_Nong at ({entity.x}, {entity.y}).")
                    entity.Damage(self.player.attack)
                    self.take_damage = False
                    print(f"[DEBUG] Loog_Nong health: {entity.health}")
                    self.hit_sound.play()
                    if entity.health <= 0:
                        print(f"[DEBUG] Loog_Nong at ({entity.x}, {entity.y}) is dead.")
                        self.player.world.entities.remove(entity)

        # Collision logic for GeeGee
            elif entity.entity_type == "xerxes":
                if entity.Collides(self.sword_hitbox) and self.take_damage:
                    print(f"[DEBUG] Leonidas hit Xerxes at ({entity.x}, {entity.y}).")
                    entity.Damage(self.player.attack)
                    self.take_damage = False
                    self.hit_sound.play()
                    print(f"[DEBUG] Xerxes health: {entity.health}")
                    if entity.health <= 0:
                        print(f"[DEBUG] Xerxes at ({entity.x}, {entity.y}) is dead.")
                        self.player.world.entities.remove(entity)

        # Handle attack input
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.ChangeState('swing_sword')

    def render(self, screen):
        # Render the player animation
        animation = self.player.curr_animation.image
        screen.blit(animation, (math.floor(self.player.x - self.player.offset_x), math.floor(self.player.y - self.player.offset_y)))

        # Draw sword hitbox for debugging
        pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(
            self.sword_hitbox.x, self.sword_hitbox.y, self.sword_hitbox.width, self.sword_hitbox.height
        ))
        