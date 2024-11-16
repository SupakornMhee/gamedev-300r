import math

from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame
from src.recourses import *

class PlayerAttackState(BaseState):
    def __init__(self, player):
        self.player = player

        self.player.curr_animation.Refresh()
        self.player.ChangeAnimation("attack_"+self.player.direction)


    def Enter(self, params):
        #sounds


        if self.player.direction_x == 'left':
            hitbox_x = self.player.x - (self.player.width - 40)#- hitbox_width
            hitbox_y = self.player.y #+ 6
        elif self.player.direction_x == 'right':
            hitbox_x = self.player.x + (self.player.width - 40)#+ self.player.width
            hitbox_y = self.player.y #+ 6

        self.sword_hitbox = Hitbox(hitbox_x, hitbox_y, self.player.width*0.7, self.player.height)

        self.player.curr_animation.Refresh()
        #print(self.player.curr_animation.index)
        self.player.ChangeAnimation("attack_"+self.player.direction_x)

    def Exit(self):
        pass

    def update(self, dt, events):
        '''
        for entity in self.dungeon.current_room.entities:
            if entity.Collides(self.sword_hitbox) and not entity.invulnerable:
                entity.Damage(1)
                entity.SetInvulnerable(0.2)
                #gSounds['hit_enemy'].play()
        '''
        if self.player.curr_animation.times_played > 0:
            self.player.curr_animation.times_played = 0
            self.player.ChangeState("idle")  #check

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.ChangeState('swing_sword')


    def render(self, screen):
        animation = self.player.curr_animation.image
        
        screen.blit(animation, (math.floor(self.player.x), math.floor(self.player.y)))

        #hit box debug
        pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(self.sword_hitbox.x, self.sword_hitbox.y, self.sword_hitbox.width, self.sword_hitbox.height))