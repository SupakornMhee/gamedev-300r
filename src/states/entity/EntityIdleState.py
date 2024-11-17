import math
from src.states.BaseState import BaseState
import random

class EntityIdleState(BaseState):
    def __init__(self, entity):
        self.entity = entity
        self.entity.ChangeAnimation(self.entity.direction_x)

        # Monster AI waiting
        self.wait_duration = 0
        self.wait_timer = 0

    def Enter(self, params):
        # Check if direction_x animation exists, fallback to "walk"
        if self.entity.direction_x in self.entity.animation_list:
            self.entity.ChangeAnimation(self.entity.direction_x)
        else:
            self.entity.ChangeAnimation("walk")  # Default to "walk" for Xerxes

    def Exit(self):
        pass

    def update(self, dt, events):
        pass

    def ProcessAI(self, params, dt):
        if self.wait_duration == 0:
            self.wait_duration = random.randint(1, 3)
        self.wait_timer += dt
        if self.wait_timer >= self.wait_duration:
            self.entity.ChangeState('walk')

    def render(self, screen):
        idle_image = self.entity.curr_animation.idleSprite
        # Render the idle sprite
        screen.blit(idle_image, (math.floor(self.entity.rect.x - self.entity.offset_x),
                    math.floor(self.entity.rect.y - self.entity.offset_y)))
