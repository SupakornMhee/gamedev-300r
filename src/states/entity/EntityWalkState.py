import random

from src.states.BaseState import BaseState
from src.constants import *

class EntityWalkState(BaseState):
    def __init__(self, entity):
        self.entity = entity
        # Use "walk" if "right" does not exist
        if "right" in self.entity.animation_list:
            self.entity.ChangeAnimation("right")
        else:
            self.entity.ChangeAnimation("walk")

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
        # ตำแหน่งของผู้เล่น
        player_x, player_y = params["player"]
        other_entities = params.get("entities", [])

        # คำนวณทิศทางเข้าหาผู้เล่น
        if self.entity.x < player_x:
            self.entity.direction_x = 'right'
        elif self.entity.x > player_x:
            self.entity.direction_x = 'left'

        if self.entity.y < player_y:
            self.entity.direction_y = 'down'
        elif self.entity.y > player_y:
            self.entity.direction_y = 'up'

        # ตรวจสอบการชนก่อนเคลื่อนที่
        if self.entity.direction_x == 'left' and not self.will_collide(-self.entity.walk_speed * dt, 0, other_entities):
            self.entity.MoveX(-self.entity.walk_speed * dt)
        elif self.entity.direction_x == 'right' and not self.will_collide(self.entity.walk_speed * dt, 0, other_entities):
            self.entity.MoveX(self.entity.walk_speed * dt)

        if self.entity.direction_y == 'up' and not self.will_collide(0, -self.entity.walk_speed * dt, other_entities):
            self.entity.MoveY(-self.entity.walk_speed * dt)
        elif self.entity.direction_y == 'down' and not self.will_collide(0, self.entity.walk_speed * dt, other_entities):
            self.entity.MoveY(self.entity.walk_speed * dt)
    def will_collide(self, dx, dy, other_entities):
        # จำลองตำแหน่งใหม่
        new_rect = self.entity.rect.copy()
        new_rect.x += dx
        new_rect.y += dy

        # ตรวจสอบการชนกับ entity อื่น
        for other in other_entities:
            if other is not self.entity and new_rect.colliderect(other.rect):
                return True
        return False


    def render(self, screen):
        animation = self.entity.curr_animation.image

        screen.blit(animation, (math.floor(self.entity.rect.x - self.entity.offset_x),
                    math.floor(self.entity.rect.y - self.entity.offset_y)))
