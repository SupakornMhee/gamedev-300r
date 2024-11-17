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

        # Spawn a portion of enemies immediately
        self.initial_spawn()

    def get_level_data(self):
        """Define level-specific configurations."""
        level_config = [
            {"monsters": 10, "duration": 20, "boss": "xerxes"},
            {"monsters": 15, "duration": 30, "boss": None},
            {"monsters": 20, "duration": 40, "boss": None},
            {"monsters": 25, "duration": 50, "boss": None},
            {"monsters": 20, "duration": 60, "boss": "loog_nong"},  # Loog_nong in level 5
            {"monsters": 30, "duration": 70, "boss": None},
            {"monsters": 35, "duration": 80, "boss": None},
            {"monsters": 40, "duration": 90, "boss": None},
            {"monsters": 45, "duration": 100, "boss": None},
            {"monsters": 30, "duration": 120, "boss": "xerxes"},  # Xerxes in level 10
        ]
        adjusted_wave_number = self.wave_number - 1  # Adjust index to start from 1
        if adjusted_wave_number < 0 or adjusted_wave_number >= len(level_config):
            print(f"[DEBUG] Invalid wave number: {self.wave_number}")
            return None
        print(f"[DEBUG] Level data for wave {self.wave_number}: {level_config[adjusted_wave_number]}")
        return level_config[adjusted_wave_number]

    def initial_spawn(self):
        """Spawn a few monsters immediately at the start of the level."""
        initial_count = max(1, self.level_data['monsters'] // 5)  # Spawn 20% of total monsters
        for _ in range(initial_count):
            conf = ENTITY_DEFS["geegee"]
            new_entity = self.create_entity_outside_map(conf)
            if not any(new_entity.Collides(entity) for entity in self.entities):
                self.entities.append(new_entity)
                self.monsters_spawned += 1
                print(f"Initial Spawned GeeGee {self.monsters_spawned}/{self.level_data['monsters']} from outside map.")

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
        new_entity.ChangeState("walk")  # Ensure entity starts in walk state
        return new_entity

    def create_entity_outside_map(self, conf):
        """Create an entity starting from outside the map and set its movement direction."""
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            conf.x = random.randrange(0, self.width)
            conf.y = -conf.height + 5  # Slightly above the top edge
        elif side == 'bottom':
            conf.x = random.randrange(0, self.width)
            conf.y = self.height - 5  # Slightly below the bottom edge
        elif side == 'left':
            conf.x = -conf.width + 5  # Slightly left of the left edge
            conf.y = random.randrange(0, self.height)
        elif side == 'right':
            conf.x = self.width - 5  # Slightly right of the right edge
            conf.y = random.randrange(0, self.height)
        
        print(f"[DEBUG] Spawning GeeGee outside map at ({conf.x}, {conf.y}) on side {side}")
        new_entity = self.create_entity(conf)

        # Set target position for movement (center of the map or toward the player)
        new_entity.target_x = self.width // 2  # Center X
        new_entity.target_y = self.height // 2  # Center Y
        return new_entity

    def GenerateEntities(self, dt):
        """Spawn monsters progressively based on the level configuration."""
        self.spawn_timer += dt  # Increment timer

    # Spawn regular monsters
        if (self.spawn_timer >= self.level_data['duration'] / self.level_data['monsters'] and
                self.monsters_spawned < self.level_data['monsters']):
            self.spawn_timer = 0  # Reset spawn timer
            conf = ENTITY_DEFS["geegee"]
            conf.x = random.randrange(0, int(self.width) - int(conf.width))
            conf.y = random.randrange(0, int(self.height) - int(conf.height))
        
            new_entity = self.create_entity(conf)
            if not any(new_entity.Collides(entity) for entity in self.entities):
                self.entities.append(new_entity)
                self.monsters_spawned += 1
                print(f"Spawned GeeGee {self.monsters_spawned}/{self.level_data['monsters']}")

    # Spawn boss in the first 10 seconds if applicable
        if (self.timer <= 10 and self.level_data['boss'] and
            not any(entity.entity_type == self.level_data['boss'] for entity in self.entities)):
            print(f"[DEBUG] Boss spawn condition met. Timer: {self.timer}, Boss: {self.level_data['boss']}")
            boss_conf = ENTITY_DEFS[self.level_data['boss']]
            print(f"[DEBUG] Boss config loaded: {boss_conf}")
            print(boss_conf.x , boss_conf.y)
            boss_conf.x = self.width // 2
            boss_conf.y = self.height // 2
            print(f"[DEBUG] Boss spawn position set to ({boss_conf.x}, {boss_conf.y})")
            boss_entity = self.create_entity(boss_conf)
            self.entities.append(boss_entity)
            print(f"[DEBUG] Spawned Boss: {self.level_data['boss']} at position ({boss_entity.x}, {boss_entity.y})")
        else:
            if self.timer > 10:
                print(f"[DEBUG] Timer exceeded 10 seconds. Current Timer: {self.timer}")
            if not self.level_data['boss']:
                print(f"[DEBUG] No boss defined for this level.")
            if any(entity.entity_type == self.level_data['boss'] for entity in self.entities):
                print(f"[DEBUG] Boss {self.level_data['boss']} already exists in the game.")

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
                # Move entity toward target if it's outside the map
                if hasattr(entity, "target_x") and hasattr(entity, "target_y"):
                    dx = entity.target_x - entity.x
                    dy = entity.target_y - entity.y
                    distance = (dx**2 + dy**2)**0.5

                    if distance > 1:  # Move toward target
                        move_x = (dx / distance) * entity.walk_speed * dt
                        move_y = (dy / distance) * entity.walk_speed * dt

                        # Debugging movement
                        print(f"[DEBUG] Moving GeeGee from ({entity.x}, {entity.y}) toward ({entity.target_x}, {entity.target_y})")
                        entity.MoveX(move_x)
                        entity.MoveY(move_y)
                    else:
                        # Once inside the map, remove the target and let AI take over
                        del entity.target_x
                        del entity.target_y
                        print(f"[DEBUG] GeeGee reached target at ({entity.x}, {entity.y}) and is now under AI control.")

                # Pass control to the AI logic in EntityWalkState
                if not hasattr(entity, "target_x") and not hasattr(entity, "target_y"):
                    entity.ProcessAI({"player": (self.player.x, self.player.y), "player_entity": self.player}, dt)
                    print(f"[DEBUG] Updating GeeGee AI at position ({entity.x}, {entity.y})")

    def render(self, screen: pygame.Surface):
        """Render the world and its entities."""
        screen.blit(self.bg_image, (0, 0))
        self.player.render()

        for entity in self.entities:
            # Debug: Log positions during rendering
            print(f"[DEBUG] Rendering GeeGee at position ({entity.rect.x}, {entity.rect.y})")
            entity.render()