import random

from src.states.BaseState import BaseState
from src.constants import *
from src.HitBox import Hitbox
from src.EntityBase import EntityBase
from src.player import Player

class EntityWalkState(BaseState):
    def __init__(self, entity):
        self.entity: EntityBase = entity
        self.entity.ChangeAnimation("right")
        
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
                elif self.entity.direction_x == "right":
                    self.entity.MoveX(self.entity.walk_speed * dt)
                    self.entity.ChangeAnimation("right")
            if not self.entity.idle_y :
                if self.entity.direction_y == 'up':
                    self.entity.MoveY(-self.entity.walk_speed * dt)
                elif self.entity.direction_y == 'down':
                    self.entity.MoveY(self.entity.walk_speed * dt)
            #print(self.entity.direction_x)
            #print(self.entity.rect.x, self.entity.rect.y, self.entity.walk_speed*dt)

    def Enter(self, params):
        self.entity.offset_x = 0
        self.entity.offset_y = 0
    def Exit(self):
        pass

    def ProcessAI(self, params, dt):    
        if self.entity.cooldown < 0:
            self.entity.able_to_attack = True
        else :
            self.entity.cooldown -= dt
        #print(self.entity.cooldown)
        player_x, player_y = params["player"]
        player_entity:Player = params["player_entity"]
        self.entity.target = player_entity  # Set target for attack
        
    # Check proximity to player for attack
        #distance_x = abs(self.entity.x - player_x)
        #distance_y = abs(self.entity.y - player_y)

        if player_entity.Collides(self.entity.GetHitBox()) :
            if self.entity.able_to_attack: #cooldown able to attack
                self.entity.ChangeState("attack")
                self.entity.cooldown = 0.5 # 0.5 s
                self.entity.able_to_attack = False
                all_damage = self.entity.attack*(1-0.01*player_entity.dmg_reduct)
                if player_entity.armor == 0:
                    player_entity.Damage(all_damage)
                elif all_damage/2 < player_entity.armor :
                    player_entity.armor -= all_damage/2
                    player_entity.Damage(all_damage/2)
                else :
                    player_entity.armor = 0
                    player_entity.Damage(all_damage - player_entity.armor)
                    print(player_entity.Damage(all_damage - player_entity.armor))
                
        else:
        # Move towards player
            if self.entity.x < player_x:
                self.entity.direction_x = "right"
                self.entity.ChangeAnimation("right")
                self.entity.MoveX(self.entity.walk_speed*dt)
            elif self.entity.x > player_x:
                self.entity.direction_x = "left"
                self.entity.ChangeAnimation("left")
                self.entity.MoveX(-self.entity.walk_speed*dt)

            if self.entity.y < player_y:
                self.entity.direction_y = "down"
                self.entity.MoveY(self.entity.walk_speed * dt)
            elif self.entity.y > player_y:
                self.entity.direction_y = "up"
                self.entity.MoveY(-self.entity.walk_speed * dt)

            
        # if abs(self.entity.x - player_x) < 50 and abs(self.entity.y - player_y) < 50:
        #     self.entity.Attack(player_entity)
            
    def render(self, screen):
        animation = self.entity.curr_animation.image

        screen.blit(animation, (math.floor(self.entity.rect.x - self.entity.offset_x),
                    math.floor(self.entity.rect.y - self.entity.offset_y)))
