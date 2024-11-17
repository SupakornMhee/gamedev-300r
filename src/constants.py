import math
import json
import pygame

WIDTH = 1152 #1280
HEIGHT = 648 #720

MAP_RENDER_OFFSET_X = 0
MAP_RENDER_OFFSET_Y = 0
TILE_SIZE = 48

PLAYER_WALK_SPEED = 180

NUMBER_OF_MONSTER = [0, 5, 10, 15, 20]

ITEM_IMAGE_LIST = []

# Load the spritesheet
spritesheet = pygame.image.load("graphics/item_sheet.png")

# Define coordinates for each item
item_rects = [
    pygame.Rect(1, 1, 59, 51),    # Item 1: Sword of Leonidas
    pygame.Rect(74, 4, 99, 54),   # Item 2: Hermes's boots
    pygame.Rect(177, 1, 57, 63),  # Item 3: Armor of King Dream
    pygame.Rect(1, 57, 70, 70),   # Item 4: Shield of Sparta
    pygame.Rect(82, 60, 69, 73),  # Item 5: Helm of Hercules
    pygame.Rect(177, 66, 56, 63), # Item 6: Mark's Gauntlet
    pygame.Rect(3, 129, 63, 61),  # Item 7: Ring of Midas
    pygame.Rect(84, 134, 70, 60), # Item 8: Amulet of Athena
    pygame.Rect(168, 129, 73, 66) # Item 9: Cape of the Phantom
]

ITEM_IMAGE_LIST = []

for idx, rect in enumerate(item_rects):
    try:
        image = spritesheet.subsurface(rect)
        ITEM_IMAGE_LIST.append(image)
    except ValueError as e:
        ITEM_IMAGE_LIST.append(None)

ITEM_DESC_FULL = [
    {"name": "Sword of Leonidas", "description": "+4% Attack Damage", "tier": "common"},
    {"name": "Hermes's boots", "description": "+2% Movement Speed", "tier": "common"},
    {"name": "Armor of King Dream", "description": "+5 Health", "tier": "uncommon"},
    {"name": "Shield of Sparta", "description": "+2 Armor", "tier": "common"},
    {"name": "Helm of Hercules", "description": "+5 Armor", "tier": "uncommon"},
    {"name": "Mark's Gauntlet", "description": "+2 Attack Damage", "tier": "common"},
    {"name": "Ring of Midas", "description": "+10% Damage against bosses", "tier": "legendary"},
    {"name": "Amulet of Athena", "description": "+0.5/s Health regenerate", "tier": "legendary"},
    {"name": "Cape of the Phantom", "description": "+5% Damage reduction", "tier": "legendary"}
]
ITEM_NAME_LIST = list(map(lambda x:x["name"],ITEM_DESC_FULL))
ITEM_DESC_LIST = list(map(lambda x:x["description"],ITEM_DESC_FULL))
ITEM_TIER_LIST = list(map(lambda x:x["tier"],ITEM_DESC_FULL))

DESCRIPTION_COLORS = {
    "health": (255, 0, 0),       # Red for health-related items
    "defense": (0, 0, 255),      # Blue for defense-related items
    "attack": (255, 165, 0),     # Orange for attack-related items
    "speed": (0, 255, 0)         # Green for speed-related items
}

# Define colors for borders based on item tier
COLORS = {
    "legendary": (255, 215, 0),  # Gold for legendary items
    "uncommon": (0, 0, 255),     # Blue for uncommon items
    "common": (169, 169, 169)    # Gray for common items
}

def get_description_color(description: str):
    """Determine the color of the description text based on keywords."""
    description_lower = description.lower()
    if "health" in description_lower:
        return DESCRIPTION_COLORS["health"]
    elif "defense" in description_lower or "armor" in description_lower or "damage reduction" in description_lower:
        return DESCRIPTION_COLORS["defense"]
    elif "attack" in description_lower or "damage against bosses" in description_lower:
        return DESCRIPTION_COLORS["attack"]
    elif "speed" in description_lower or "movement" in description_lower:
        return DESCRIPTION_COLORS["speed"]
    else:
        return (200, 200, 200)  # Default color 

STATS_LABEL_LIST = [
    ("health", (255, 0, 0)),
    ("attack_damage", (255, 69, 0)),
    ("movement_speed", (0, 255, 255)),
    ("attack_speed", (0, 255, 0)),
    ("armor", (255, 255, 255)),
    ("damage_reduction", (0, 0, 255)),
    ("damage_against_bosses", (255, 140, 0)),
    ("health_regenerate", (255, 0, 0))
]

def get_border_color(tier):
    return COLORS.get(tier, COLORS["common"])

def draw_bordered_rect(screen, rect, color, border_color, border_width=3):
    pygame.draw.rect(screen, border_color, rect, border_width)
    inner_rect = rect.inflate(-border_width * 2, -border_width * 2)
    pygame.draw.rect(screen, color, inner_rect)

def get_stat_color(stat_name):
    """Get the color associated with a stat name."""
    return STAT_LABELS.get(stat_name, (255, 255, 255))  # Default to white if not found

def draw_stat_labels(screen, font, stats, start_x, start_y, line_height=30):
    """Draws stat labels on the screen with appropriate colors."""
    y_offset = start_y
    for stat_name, value in stats.items():
        color = get_stat_color(stat_name)
        label = stat_name.replace("_", " ").capitalize()
        text = font.render(f"{label}: {value}", True, color)
        screen.blit(text, (start_x, y_offset))
        y_offset += line_height










'''
NUMBER_OF_MONSTER=10

MAP_WIDTH = WIDTH // TILE_SIZE - 2
MAP_HEIGHT = int(math.floor(HEIGHT/TILE_SIZE)) - 2

MAP_RENDER_OFFSET_X = (WIDTH - (MAP_WIDTH * TILE_SIZE)) // 2
MAP_RENDER_OFFSET_Y = (HEIGHT - (MAP_HEIGHT *TILE_SIZE)) // 2

TILE_TOP_LEFT_CORNER = 4
TILE_TOP_RIGHT_CORNER = 5
TILE_BOTTOM_LEFT_CORNER = 23
TILE_BOTTOM_RIGHT_CORNER = 24

TILE_FLOORS = [
    7, 8, 9, 10, 11, 12, 13,
    26, 27, 28, 29, 30, 31, 32,
    45, 46, 47, 48, 49, 50, 51,
    64, 65, 66, 67, 68, 69, 70,
    88, 89, 107, 108
]

TILE_EMPTY = 19

TILE_TOP_WALLS = [58, 59, 60]
TILE_BOTTOM_WALLS = [79, 80, 81]
TILE_LEFT_WALLS = [77, 96, 115]
TILE_RIGHT_WALLS = [78, 97, 116]
'''