import pygame

STAT_LABELS = {
    "health": (255, 0, 0),
    "attack_damage": (255, 69, 0),
    "movement_speed": (0, 255, 255),
    "attack_speed": (0, 255, 0),
    "armor": (255, 255, 255),
    "damage_reduction": (0, 0, 255),
    "damage_against_bosses": (255, 140, 0),
    "health_regenerate": (255, 0, 0),
}

DESCRIPTION_COLORS = {
    "health": (255, 0, 0),
    "defense": (0, 0, 255),
    "attack": (255, 165, 0),
    "speed": (0, 255, 0)
}

COLORS = {
    "legendary": (255, 215, 0),
    "uncommon": (0, 0, 255),
    "common": (169, 169, 169)
}

def get_description_color(description):
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
        return (200, 200, 200)

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
