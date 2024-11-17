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
import pygame
from src.entity_defs import *
from src.constants import *
from src.EntityBase import EntityBase
from src.states.entity.EntityAttackState import *
from src.states.entity.EntityWalkState import *
from src.states.entity.EntityIdleState import *
from src.player import Player
from src.StateMachine import StateMachine

class World:
    def __init__(self, wave_number, player: Player):
        self.width = WIDTH
        self.height = HEIGHT
        self.wave_number = wave_number
        self.bg_image = pygame.image.load("graphics/battlefield.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.entities = []
        self.spawn_timer = 0  # Timer to manage spawn intervals
        self.player = player
        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0
        self.level_data = self.get_level_data()  # Get level-specific data
        self.timer = 0
        self.remaining_time = self.level_data['duration']  # Duration for the level
        self.monsters_spawned = 0  # Track number of monsters spawned
        self.monsters_remained = 0
        # Spawn a portion of enemies immediately
        self.initial_spawn()

    def get_level_data(self):
        """Define level-specific configurations."""
        level_config = [
            {"monsters": 10, "duration": 20, "boss": None},
            {"monsters": 15, "duration": 30, "boss": None},
            {"monsters": 20, "duration": 40, "boss": None},
            {"monsters": 25, "duration": 50, "boss": None},
            {"monsters": 20, "duration": 60, "boss": "messenger"},
            {"monsters": 30, "duration": 70, "boss": None},
            {"monsters": 35, "duration": 80, "boss": None},
            {"monsters": 40, "duration": 90, "boss": None},
            {"monsters": 45, "duration": 100, "boss": None},
            {"monsters": 30, "duration": 120, "boss": "xerxes"},
        ]
        return level_config[self.wave_number]

    def initial_spawn(self):
        """Spawn a few monsters immediately at the start of the level."""
        initial_count = max(1, self.level_data['monsters'] // 5)  # Spawn 20% of total monsters
        for _ in range(initial_count):
            conf = ENTITY_DEFS["geegee"]
            conf.x = random.randrange(0, int(self.width) - int(conf.width))
            conf.y = random.randrange(0, int(self.height) - int(conf.height))
            print(conf.x,conf.y)
            new_entity = self.create_entity(conf)
            if not any(new_entity.Collides(entity) for entity in self.entities):
                self.entities.append(new_entity)
                self.monsters_spawned += 1
                print(f"Initial Spawned GeeGee {self.monsters_spawned}/{self.level_data['monsters']}")

    def create_entity(self, conf):
        """Create and initialize an entity with a state machine."""
        new_entity = EntityBase(conf)
        new_entity.state_machine = StateMachine()
        new_entity.state_machine.SetScreen(pygame.display.get_surface())  # Set screen for rendering
        new_entity.state_machine.SetStates({
            "walk": EntityWalkState(new_entity),
            "idle": EntityIdleState(new_entity),
            "attack": EntityAttackState(new_entity),
        })
        new_entity.ChangeState("idle")  # Set the initial state
        return new_entity

    def GenerateEntities(self, dt):
        """Spawn monsters progressively based on the level configuration."""
        self.spawn_timer += dt  # Increment timer
        #print(self.spawn_timer)
        # Spawn regular monsters at random intervals
        if (self.spawn_timer >= self.level_data['duration'] / self.level_data['monsters'] and
                self.monsters_spawned < self.level_data['monsters']):
            self.spawn_timer = 0  # Reset spawn timer
            conf = ENTITY_DEFS["geegee"]
            conf.x = random.randrange(0, int(self.width) - int(conf.width))
            conf.y = random.randrange(0, int(self.height) - int(conf.height))
            choice = random.choice([1,2,3,4])
            if choice == 1: conf.x = 0 # ขอบบน
            if choice == 2: conf.x = int(self.width) - int(conf.width) #ขอบล่าง
            if choice == 3: conf.y = 0 #ขอบซ้าย
            if choice == 4: conf.y = int(self.height) - int(conf.height) #ขอบขวา
            new_entity = self.create_entity(conf)
            if not any(new_entity.Collides(entity) for entity in self.entities):
                self.entities.append(new_entity)
                self.monsters_spawned += 1
                print(f"Spawned GeeGee {self.monsters_spawned}/{self.level_data['monsters']}")

        # Spawn boss in the last 10 seconds if applicable
        if (self.remaining_time <= 10 and self.level_data['boss'] and
                not any(entity.entity_type == self.level_data['boss'] for entity in self.entities)):
            boss_conf = ENTITY_DEFS[self.level_data['boss']]
            boss_conf.x = self.width // 2
            boss_conf.y = self.height // 2
            boss_entity = self.create_entity(boss_conf)
            self.entities.append(boss_entity)
            print(f"Spawned Boss: {self.level_data['boss']}")

    def countEnemies(self):
        return len(self.entities)

    def update(self, dt, events):
        """Update world and spawn logic."""
        self.timer += dt
        self.remaining_time -= dt  # Decrease remaining time

        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return

        self.player.update(dt, events)
        self.GenerateEntities(dt)  # Generate entities dynamically
        for entity in self.entities[:]:  # Use a copy to avoid errors while removing
            if entity.is_dead:
                self.entities.remove(entity)
            else:
                entity.ProcessAI({"player": (self.player.x, self.player.y), "player_entity": self.player}, dt)

    def render(self, screen: pygame.Surface):
        """Render the world and its entities."""
        screen.blit(self.bg_image, (0, 0))
        self.player.render()
        for entity in self.entities:
            entity.render()
