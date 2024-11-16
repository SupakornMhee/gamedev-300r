'''
World.py อันนี้เอาไว้สำหรับสร้างด่าน/โชว์ด่าน

World.py ต้องมี Attribute อะไรบ้าง
1. Background สำหรับ Display
2. Player -- ซึ่งมาจาก EntityBase อีกที
3. Enemies -- ซึ่งมาจาก EntityBase อีกที
4. List of Enemies -- ซึ่งเป็น List ของ Enemies อีกทีนึง

ใน EntityBase มีอะไร
1. direction -- Up Down Left Right
2. animation_list -- 

World.py ต้องมี Function อะไรบ้าง

'''

import random
from src.entity_defs import *
from src.constants import *
from src.Dependencies import *
from src.EntityBase import EntityBase
from src.entity_defs import EntityConf
from src.player import *
import pygame
from src.states.entity.EntityAttackState import *
from src.states.entity.EntityWalkState import *
from src.states.entity.EntityIdleState import *
class World:
    def __init__(self, wave_number, player: Player):
        self.width = WIDTH
        self.height = HEIGHT
        self.wave_number = wave_number 
        self.bg_image = pygame.image.load("graphics/battlefield.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH,HEIGHT))
        
        
        self.entities = []
        self.GenerateEntities()
        
        self.player = player
        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0
        self.timer = 0
        
    def GenerateEntities(self):
        types = ['geegee']
        num_monsters = NUMBER_OF_MONSTER[self.wave_number] if self.wave_number < len(NUMBER_OF_MONSTER) else 0

        while len(self.entities) < num_monsters:
            type = random.choice(types)
            conf = EntityConf(
            animation=ENTITY_DEFS[type].animation,
            walk_speed=ENTITY_DEFS[type].walk_speed,
            x=random.randrange(0, int(self.width) - int(ENTITY_DEFS[type].width)),
            y=random.randrange(0, int(self.height) - int(ENTITY_DEFS[type].height)),
            width=ENTITY_DEFS[type].width,
            height=ENTITY_DEFS[type].height,
            health=ENTITY_DEFS[type].health
        )

            new_entity = EntityBase(conf)
            print(f"Trying to place GeeGee at ({new_entity.x}, {new_entity.y})")
            for entity in self.entities:
                if new_entity.Collides(entity):
                    print(f"Collision detected with Entity at ({entity.x}, {entity.y})")
            if any(new_entity.Collides(entity) for entity in self.entities):
                continue

            self.entities.append(new_entity)
            print(f"Placed GeeGee at ({new_entity.x}, {new_entity.y})")
            new_entity.state_machine = StateMachine()
            new_entity.state_machine.SetScreen(pygame.display.get_surface())
            new_entity.state_machine.SetStates({
            "walk": EntityWalkState(new_entity),
            "idle": EntityIdleState(new_entity),
        })
            new_entity.ChangeState("walk")
    def countEnemies(self):
        return len(self.entities)
    def update(self, dt, events):
        self.timer += dt
        #print(self.timer)
        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return

        self.player.update(dt, events)
         # อัปเดตศัตรู
        for entity in self.entities[:]:  # ใช้สำเนาเพื่อหลีกเลี่ยงข้อผิดพลาดขณะลบ
            if entity.is_dead:
                self.entities.remove(entity)
            else:
                entity.ProcessAI({"player": (self.player.x, self.player.y), "entities": self.entities}, dt)

    def render(self, screen: pygame.Surface):
        
        
        screen.blit(self.bg_image, (0,0))
        self.player.render()
        for entity in self.entities:
            entity.render()
        pass
