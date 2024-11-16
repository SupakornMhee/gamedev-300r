import random

from src.states.BaseState import BaseState
from src.constants import *

class EntityWalkState(BaseState):
    def __init__(self, entity):
        self.entity = entity
        self.entity.ChangeAnimation('right')

        #AI control
        self.move_duration = 0
        self.movement_timer = 0

        #hit wall?
        self.bumped = False

    def update(self, dt, events):
        self.bumped=False
        
        if not self.entity.idle_x :
            if self.entity.direction_x == "left":
                self.entity.MoveX(-self.entity.walk_speed*dt)
            elif self.entity.direction_x == "right":
                self.entity.MoveX(self.entity.walk_speed * dt)
        if not self.entity.idle_y :
            if self.entity.direction_y == 'up':
                self.entity.MoveY(-self.entity.walk_speed * dt)
            elif self.entity.direction_y == 'down':
                self.entity.MoveY(self.entity.walk_speed * dt)

        #print(self.entity.rect.x, self.entity.rect.y, self.entity.walk_speed*dt)

    def Enter(self, params):
        pass
    def Exit(self):
        pass

    def ProcessAI(self, params, dt):
        directions = ['left', 'right', 'up', 'down']
        player_x, player_y = params["player"]
        
        
        if self.move_duration == 0 or self.bumped:
            self.move_duration = random.randint(0, 5)
            self.entity.direction = random.choice(directions)
            self.entity.ChangeAnimation(self.entity.direction)

        elif self.movement_timer > self.move_duration:
            self.movement_timer = 0
            if random.randint(0, 3) == 1:
                self.entity.ChangeState('idle')
            else:
                self.move_duration = random.randint(0, 5)
                self.entity.direction = random.choice(directions)
                self.entity.ChangeAnimation(self.entity.direction)

        self.movement_timer = self.movement_timer+dt


    def render(self, screen):
        animation = self.entity.curr_animation.image

        screen.blit(animation, (math.floor(self.entity.rect.x - self.entity.offset_x),
                    math.floor(self.entity.rect.y - self.entity.offset_y)))