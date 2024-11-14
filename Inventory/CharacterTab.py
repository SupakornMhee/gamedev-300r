import pygame
import json
from Util import COLORS, get_border_color, draw_bordered_rect, draw_stat_labels

class CharacterTab:
    def __init__(self, screen, item_spritesheet, profile_spritesheet, obtained_items):
        self.screen = screen
        self.item_spritesheet = item_spritesheet
        self.profile_spritesheet = profile_spritesheet
        self.obtained_items = obtained_items
        self.item_images = []

        # Load character data
        with open("character.json") as f:
            self.character_data = json.load(f)

        # Load item data and sprite images
        with open("items.json") as f:
            self.items_data = json.load(f)
        self.load_item_sprites()

    def load_item_sprites(self):
        item_rects = [
            pygame.Rect(1, 1, 59, 51),
            pygame.Rect(74, 4, 99, 54),
            pygame.Rect(177, 1, 57, 63),
            pygame.Rect(1, 57, 70, 70),
            pygame.Rect(82, 60, 69, 73),
            pygame.Rect(177, 66, 56, 63),
            pygame.Rect(3, 129, 63, 61),
            pygame.Rect(84, 134, 70, 60),
            pygame.Rect(168, 129, 73, 66)
        ]

        for rect in item_rects:
            try:
                image = self.item_spritesheet.subsurface(rect)
                self.item_images.append(image)
            except ValueError as e:
                print(f"Error loading item image from rect {rect}: {e}")
                self.item_images.append(None)

        for item in self.items_data:
            image_index = item.get("image_index")
            if image_index is not None and 0 <= image_index < len(self.item_images):
                item["image"] = self.item_images[image_index]
            else:
                item["image"] = None

    def display_character_tab(self):
        self.screen.fill((80, 80, 80))

        profile_image_rect = pygame.Rect(1, 0, 93, 104)
        profile_image = self.profile_spritesheet.subsurface(profile_image_rect)
        profile_position = (50, 50)
        profile_border_rect = pygame.Rect(profile_position[0] - 5, profile_position[1] - 5, 93 + 10, 104 + 10)
        draw_bordered_rect(self.screen, profile_border_rect, (0, 0, 0), (0, 0, 0))  # Black border around profile
        self.screen.blit(profile_image, profile_position)

        font = pygame.font.SysFont(None, 40)
        name_text = font.render(self.character_data["name"], True, (255, 0, 0))
        self.screen.blit(name_text, (160, 50))

        stats_font = pygame.font.SysFont(None, 30)
        stats = self.character_data["base_stats"]
        draw_stat_labels(self.screen, stats_font, stats, 160, 100)

        self.draw_obtained_items()

    def draw_obtained_items(self):
        item_box_size = 70
        item_padding = 15
        start_x = 500
        start_y = 50
        columns = 3

        for index, item_data in enumerate(self.items_data):
            col = index % columns
            row = index // columns
            x = start_x + col * (item_box_size + item_padding)
            y = start_y + row * (item_box_size + item_padding)

            item_name = item_data["name"]
            is_obtained = item_name in self.obtained_items

            if is_obtained:
                item_info = self.obtained_items[item_name]
                item_level = item_info if isinstance(item_info, int) else item_info.get("level", 1)
            else:
                item_level = 0

            item_rect = pygame.Rect(x, y, item_box_size, item_box_size)
            pygame.draw.rect(self.screen, (100, 100, 100), item_rect)

            tier = item_data.get("tier", "common")
            border_color = get_border_color(tier)
            pygame.draw.rect(self.screen, border_color, item_rect, 3)

            if item_data["image"]:
                item_image = pygame.transform.scale(item_data["image"], (item_box_size - 10, item_box_size - 10))
                if not is_obtained:
                    item_image.set_alpha(100)
                self.screen.blit(item_image, (x + 5, y + 5))

            if is_obtained:
                level_font = pygame.font.SysFont(None, 20)
                level_text = level_font.render(f"{item_level}", True, (0, 0, 0))
                self.screen.blit(level_text, (x + item_box_size - 20, y + item_box_size - 20))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.display_character_tab()
            pygame.display.flip()

        pygame.quit()
