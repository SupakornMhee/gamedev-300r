import pygame
import random
import json
from Util import COLORS, get_description_color  # Import from utils

class ItemSelectionScreen:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont(None, 24)
        self.obtained_items = player.obtained_items

        # Load item data from JSON and spritesheet
        self.load_items()

    def load_items(self):
        # Load the spritesheet
        spritesheet = pygame.image.load("sprite_sheet.png")

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

        self.item_images = []
        for idx, rect in enumerate(item_rects):
            try:
                image = spritesheet.subsurface(rect)
                self.item_images.append(image)
            except ValueError as e:
                self.item_images.append(None)

        with open("items.json") as f:
            self.items = json.load(f)

        for item in self.items:
            item["image"] = self.item_images[item["image_index"]]

    def select_power_ups(self):
        available_items = [item for item in self.items if self.obtained_items.get(item["name"], 1) < 3]
        selection = []

        while len(selection) < 3:
            new_item = random.choice(available_items)
            if new_item not in selection:
                if new_item["tier"] == "legendary" and random.random() > 0.2:
                    continue
                elif new_item["tier"] == "uncommon" and random.random() > 0.5:
                    continue
                selection.append(new_item)

        return selection

    def render_text_multiline(self, text, font, color, max_width):
        """Render text with line wrapping within max_width."""
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        return [font.render(line, True, color) for line in lines]

    def run(self, current_wave=1, max_wave=10):
        while current_wave <= max_wave:
            power_up_choices = self.select_power_ups()
            wave_complete = False

            while not wave_complete:
                self.screen.fill((20, 20, 20))

                main_frame_rect = pygame.Rect(50, 50, self.screen.get_width() - 100, self.screen.get_height() - 100)
                pygame.draw.rect(self.screen, (50, 50, 80), main_frame_rect)
                pygame.draw.rect(self.screen, (150, 150, 180), main_frame_rect, 5)

                title_font = pygame.font.SysFont(None, 48)
                title_lines = self.render_text_multiline("Power-Up Selection", title_font, (255, 255, 255), main_frame_rect.width - 20)
                title_y = 70
                for line_surface in title_lines:
                    line_rect = line_surface.get_rect(center=(main_frame_rect.centerx, title_y))
                    self.screen.blit(line_surface, line_rect.topleft)
                    title_y += line_surface.get_height() + 5

                wave_font = pygame.font.SysFont(None, 36)
                wave_text = wave_font.render(f"Wave {current_wave}", True, (255, 255, 255))
                self.screen.blit(wave_text, (main_frame_rect.centerx - wave_text.get_width() // 2, title_y + 20))

                item_box_width = 220
                item_box_height = 320
                item_gap_x = 50
                item_gap_y = 40

                columns = 3
                start_x = main_frame_rect.left + (main_frame_rect.width - (columns * item_box_width + (columns - 1) * item_gap_x)) // 2
                start_y = title_y + 60

                item_rects = []
                for idx, power_up in enumerate(power_up_choices):
                    row = idx // columns
                    col = idx % columns
                    x_pos = start_x + col * (item_box_width + item_gap_x)
                    y_pos = start_y + row * (item_box_height + item_gap_y)

                    item_frame_rect = pygame.Rect(x_pos, y_pos, item_box_width, item_box_height)
                    pygame.draw.rect(self.screen, (70, 70, 100), item_frame_rect)
                    pygame.draw.rect(self.screen, (150, 150, 180), item_frame_rect, 3)

                    tier = power_up.get("tier", "common")
                    border_color = COLORS.get(tier, COLORS["common"])
                    pygame.draw.rect(self.screen, border_color, item_frame_rect.inflate(-10, -10), 2)

                    image_frame_rect = pygame.Rect(x_pos + (item_box_width - 100) // 2, y_pos + 20, 100, 100)
                    pygame.draw.rect(self.screen, (50, 50, 80), image_frame_rect)
                    pygame.draw.rect(self.screen, border_color, image_frame_rect, 3)

                    if power_up["image"]:
                        item_image_rect = power_up["image"].get_rect(center=image_frame_rect.center)
                        self.screen.blit(power_up["image"], item_image_rect.topleft)

                    name_font = pygame.font.SysFont(None, 30)
                    item_name = power_up["name"]
                    name_text = name_font.render(item_name, True, (255, 255, 255))
                    name_text_rect = name_text.get_rect(center=(item_frame_rect.centerx, y_pos + 130))
                    self.screen.blit(name_text, name_text_rect.topleft)

                    tier_text = name_font.render(f"Tier: {tier.title()}", True, border_color)
                    tier_text_rect = tier_text.get_rect(center=(item_frame_rect.centerx, y_pos + 160))
                    self.screen.blit(tier_text, tier_text_rect.topleft)

                    desc_font = pygame.font.SysFont(None, 24)
                    description_color = get_description_color(power_up["description"])
                    wrapped_desc = self.render_text_multiline(power_up["description"], desc_font, description_color, item_box_width - 20)

                    for i, line_surface in enumerate(wrapped_desc):
                        line_x = item_frame_rect.centerx - line_surface.get_width() // 2
                        line_y = y_pos + 200 + i * 20
                        self.screen.blit(line_surface, (line_x, line_y))

                    current_level = self.obtained_items.get(item_name, 1)
                    next_level = min(current_level + 1, 3)
                    level_text = desc_font.render(f"Level: {current_level} -> {next_level}" if item_name in self.obtained_items else f"Level: {current_level}", True, (255, 255, 255))
                    level_text_rect = level_text.get_rect(center=(item_frame_rect.centerx, y_pos + item_box_height - 40))
                    self.screen.blit(level_text, level_text_rect.topleft)

                    item_rects.append((item_frame_rect, power_up))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for rect, power_up in item_rects:
                            if rect.collidepoint(mouse_pos):
                                item_name = power_up["name"]
                                if item_name in self.obtained_items:
                                    self.obtained_items[item_name] = min(self.obtained_items[item_name] + 1, 3)
                                else:
                                    self.obtained_items[item_name] = 1
                                wave_complete = True
                                break

                if wave_complete:
                    current_wave += 1

        return self.obtained_items

# Test
#def main():
    #pygame.init()
    #screen = pygame.display.set_mode((1000, 700))
    
    # Mock Player class
    #class Player:
        #def __init__(self):
            #self.obtained_items = {}
    
    #player = Player()

    #item_selection_screen = ItemSelectionScreen(screen, player)
    #obtained_items = item_selection_screen.run(current_wave=1, max_wave=10)
    #print("Updated player stats:", obtained_items)

#if __name__ == "__main__":
    #main()
