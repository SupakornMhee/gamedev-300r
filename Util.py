
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

def get_description_color(description):
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
