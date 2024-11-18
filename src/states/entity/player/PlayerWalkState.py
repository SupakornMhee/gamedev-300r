from src.constants import *
from src.states.entity.EntityWalkState import EntityWalkState
import pygame, time

class PlayerWalkState(EntityWalkState):
    def __init__(self, player):
        super(PlayerWalkState, self).__init__(player)

        self.entity.ChangeAnimation('right')

    def Exit(self):
        pass

    def Enter(self, params):
        self.entity.offset_y = 0
        self.entity.offset_x = 0

    def update(self, dt, events):
        pressedKeys = pygame.key.get_pressed()
        
        if pressedKeys[pygame.K_a]:
            self.entity.idle_x = False
            self.entity.direction = 'left'
            self.entity.direction_x = 'left'
            self.entity.ChangeAnimation('left')
        elif pressedKeys[pygame.K_d]:
            self.entity.idle_x = False
            self.entity.direction = 'right'
            self.entity.direction_x = 'right'
            self.entity.ChangeAnimation('right')
        else:
            self.entity.idle_x = True
        if pressedKeys[pygame.K_s]:
            self.entity.idle_y = False
            self.entity.direction = 'down'
            self.entity.direction_y = 'down'
            #self.entity.ChangeAnimation('down')
        elif pressedKeys[pygame.K_w]:
            self.entity.idle_y = False
            self.entity.direction = 'up'
            self.entity.direction_y = 'up'
            #self.entity.ChangeAnimation('up')
        else:
            self.entity.idle_y = True
        if self.entity.idle_x and self.entity.idle_y:
            self.entity.ChangeState('idle')
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.entity.ChangeState('swing_sword')
                    
        #move and bump to the wall check
        super().update(dt, events)