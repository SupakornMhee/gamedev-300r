import pygame
from CharacterTab import CharacterTab

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Load the spritesheets
    item_spritesheet = pygame.image.load("sprite_sheet.png")
    profile_spritesheet = pygame.image.load("sprite_sheet_character.png")

    # Example obtained items with cumulative levels for testing
    obtained_items = {
        "Boots of Speed": 1,               # Level 1 item
        "Sword of Leonidas": 1,            # Level 1 item
        "Armor of King Dream": 2,          # Level 2 item
        "Ring of Midas": 1,                # Level 1 item
        "Cape of the Phantom": 1           # Level 1 item
    }

    # Initialize and run the CharacterTab
    character_tab = CharacterTab(screen, item_spritesheet, profile_spritesheet, obtained_items)
    character_tab.run()
