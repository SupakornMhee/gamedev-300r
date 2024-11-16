import random

from src.states.BaseState import BaseState
from src.constants import *

class EntityWalkState(BaseState):
    def __init__(self, entity):
        self.entity = entity
        self.entity.ChangeAnimation('right')  # Default animation
        self.last_horizontal_direction = "right"  # Default direction

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
                self.entity.ChangeAnimation("left")
                self.last_horizontal_direction = "left"
            elif self.entity.direction_x == "right":
                self.entity.MoveX(self.entity.walk_speed * dt)
                self.entity.ChangeAnimation("right")
                self.last_horizontal_direction = "right"
        if not self.entity.idle_y :
            if self.entity.direction_y == 'up':
                self.entity.MoveY(-self.entity.walk_speed * dt)
                self.entity.ChangeAnimation(f"{self.last_horizontal_direction}")
            elif self.entity.direction_y == 'down':
                self.entity.MoveY(self.entity.walk_speed * dt)
                self.entity.ChangeAnimation(f"{self.last_horizontal_direction}")

        #print(self.entity.rect.x, self.entity.rect.y, self.entity.walk_speed*dt)

    def Enter(self, params):
        pass
    def Exit(self):
        pass

    def ProcessAI(self, params, dt):
        player_x, player_y = params["player"]
        player_entity = params["player_entity"]
        self.entity.target = player_entity  # Set target for attack

    # Check proximity to player for attack
        distance_x = abs(self.entity.x - player_x)
        distance_y = abs(self.entity.y - player_y)

        if distance_x < 50 and distance_y < 50:  # Example attack range
            self.entity.ChangeState("attack")
        else:
        # Move towards player
            if self.entity.x < player_x:
                self.entity.direction_x = "right"
            elif self.entity.x > player_x:
                self.entity.direction_x = "left"

            if self.entity.y < player_y:
                self.entity.direction_y = "down"
            elif self.entity.y > player_y:
                self.entity.direction_y = "up"

            self.entity.MoveX(self.entity.walk_speed * dt if self.entity.direction_x == "right" else -self.entity.walk_speed * dt)
            self.entity.MoveY(self.entity.walk_speed * dt if self.entity.direction_y == "down" else -self.entity.walk_speed * dt)
        if abs(self.entity.x - player_x) < 50 and abs(self.entity.y - player_y) < 50:
            self.entity.Attack(player_entity)
   

    def render(self, screen):
        animation = self.entity.curr_animation.image

        screen.blit(animation, (math.floor(self.entity.rect.x - self.entity.offset_x),
                    math.floor(self.entity.rect.y - self.entity.offset_y)))