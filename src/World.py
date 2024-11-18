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
        self.monsters_remained = self.level_data['monsters']
        self.boss_spawned = False  # Track if the boss has been spawned
        self.boss_defeated = False  # Track if the boss has been defeated
        # Spawn a portion of enemies immediately
        self.initial_spawn()
        self.flash_timer = 0  # Timer for screen flash effect
        self.is_screen_flashing = False  # Flag to indicate screen flashing

    def get_level_data(self):
        """Define level-specific configurations."""
        level_config = [
            {"monsters": 5, "duration": 15, "boss": None},
            {"monsters": 10, "duration": 20, "boss": None},
            {"monsters": 15, "duration": 25, "boss": None},
            {"monsters": 20, "duration": 30, "boss": None},
            {"monsters": 25, "duration": 40, "boss": "loog_nong"},
            {"monsters": 30, "duration": 50, "boss": None},
            {"monsters": 35, "duration": 50, "boss": None},
            {"monsters": 40, "duration": 55, "boss": None},
            {"monsters": 45, "duration": 60, "boss": None},
            {"monsters": 45, "duration": 80, "boss": "xerxes"},
        ]
        adjusted_wave_number = self.wave_number - 1
        if adjusted_wave_number < 0 or adjusted_wave_number >= len(level_config):
            print(f"[DEBUG] Invalid wave number: {self.wave_number}")
            return None
        print(f"[DEBUG] Level data for wave {self.wave_number}: {level_config[adjusted_wave_number]}")
        return level_config[adjusted_wave_number]

    def initial_spawn(self):
        """Spawn a few monsters immediately at the start of the level."""
        initial_count = max(1, self.level_data['monsters'] // 5)
        for _ in range(initial_count):
            conf = ENTITY_DEFS["geegee"]
            conf.x = random.randrange(0, int(self.width) - int(conf.width))
            conf.y = random.randrange(0, int(self.height) - int(conf.height))
            new_entity = self.create_entity(conf)
            if not any(new_entity.Collides(entity) for entity in self.entities):
                self.entities.append(new_entity)
                self.monsters_spawned += 1
                print(f"Initial Spawned GeeGee {self.monsters_spawned}/{self.level_data['monsters']}")

    def create_entity(self, conf):
        """Create and initialize an entity with a state machine."""
        new_entity = EntityBase(conf)
        if conf.entity_type == "GeeGee":
            wave_multiplier = 1 + (0.015 * (self.wave_number - 1))  
            new_entity.health = conf.health * wave_multiplier
            new_entity.attack = conf.attack * wave_multiplier
            print(f"[DEBUG] Wave {self.wave_number} GeeGee stats:")
            print(f"[DEBUG] - Base health: {conf.health} -> Scaled: {new_entity.health}")
            print(f"[DEBUG] - Base attack: {conf.attack} -> Scaled: {new_entity.attack}")
        new_entity.state_machine = StateMachine()
        new_entity.state_machine.SetScreen(pygame.display.get_surface())
        new_entity.state_machine.SetStates({
            "walk": EntityWalkState(new_entity),
            "idle": EntityIdleState(new_entity),
            "attack": EntityAttackState(new_entity),
        })
        new_entity.ChangeState("walk")
        return new_entity

    def GenerateEntities(self, dt):
        """Spawn monsters progressively based on the level configuration."""
        self.spawn_timer += dt

    # Spawn regular monsters at random intervals
        if (self.spawn_timer >= self.level_data['duration'] / self.level_data['monsters'] and
            self.monsters_spawned < self.level_data['monsters']):
            self.spawn_timer = 0  # Reset spawn timer
            conf = ENTITY_DEFS["geegee"]
            conf.x = random.randrange(0, int(self.width) - int(conf.width))
            conf.y = random.randrange(0, int(self.height) - int(conf.height))
            choice = random.choice([1, 2, 3, 4])
            if choice == 1: conf.x = 0  # Top edge
            if choice == 2: conf.x = int(self.width) - int(conf.width)  # Bottom edge
            if choice == 3: conf.y = 0  # Left edge
            if choice == 4: conf.y = int(self.height) - int(conf.height)  # Right edge
            new_entity = self.create_entity(conf)
            if not any(new_entity.Collides(entity) for entity in self.entities):
                self.entities.append(new_entity)
                self.monsters_spawned += 1
                print(f"Spawned GeeGee {self.monsters_spawned}/{self.level_data['monsters']}")

    # Spawn boss in the last 10 seconds if applicable
        if (self.remaining_time <= 10 and self.level_data['boss'] and 
        not self.boss_spawned and not self.boss_defeated):
            boss_conf = ENTITY_DEFS[self.level_data['boss']]
            boss_conf.x = random.randrange(0, int(self.width) - int(boss_conf.width))
            boss_conf.y = random.randrange(0, int(self.height) - int(boss_conf.height))
            choice = random.choice([1, 2, 3, 4])
            if choice == 1: boss_conf.x = 0  # Top edge
            if choice == 2: boss_conf.x = int(self.width) - int(boss_conf.width)  # Bottom edge
            if choice == 3: boss_conf.y = 0  # Left edge
            if choice == 4: boss_conf.y = int(self.height) - int(boss_conf.height)  # Right edge
            boss_entity = self.create_entity(boss_conf)
            self.entities.append(boss_entity)
            self.boss_spawned = True  # Mark boss as spawned
            self.is_screen_flashing = True
            self.flash_timer = 2  # Flash the screen for 2 seconds
            print(f"[DEBUG] Spawned Boss: {self.level_data['boss']} at position ({boss_entity.x}, {boss_entity.y})")

    def countEnemies(self):
        return len(self.entities)

    def update(self, dt, events):
        """Update world and spawn logic."""
        self.timer += dt
        self.remaining_time -= dt
        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return

        self.player.update(dt, events)
        self.GenerateEntities(dt)

        for entity in self.entities[:]:
            print(f"[DEBUG] {entity.entity_type} is dead.")
            
            
            if entity.is_dead:
                if self.level_data['boss'] and entity.entity_type == self.level_data['boss']:
                    print("-----------------------------------------------------")
                    print(f"[DEBUG] {entity.entity_type} has been defeated!")
                    self.boss_defeated = True  # Mark the boss as defeated
                else:
                    print(f"[DEBUG] {entity.entity_type} is not the boss.")
                    
                self.entities.remove(entity)
            else:
                entity.ProcessAI({"player": (self.player.x, self.player.y), "player_entity": self.player}, dt)
        if self.is_screen_flashing:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self.is_screen_flashing = False
                

    def render(self, screen: pygame.Surface):
        """Render the world and its entities."""
        screen.blit(self.bg_image, (0, 0))
        self.player.render()
        for entity in self.entities:
            entity.render()
        # Apply flashing effect
        if self.is_screen_flashing:
            alpha = int(abs(self.flash_timer % 0.5 - 0.25) * 1020)  # Fade effect
            flash_surface = pygame.Surface(screen.get_size())
            flash_surface.fill((0, 0, 0))  # White flash
            flash_surface.set_alpha(alpha)
            screen.blit(flash_surface, (0, 0))