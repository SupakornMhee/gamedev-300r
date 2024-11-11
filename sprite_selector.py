import pygame
import sys

# Initialize Pygame
pygame.init()

# Load the spritesheet
spritesheet_path = "sprite_sheet.png"  # Update with the correct path if necessary
spritesheet = pygame.image.load(spritesheet_path)
spritesheet_rect = spritesheet.get_rect()
screen = pygame.display.set_mode((spritesheet_rect.width, spritesheet_rect.height))
pygame.display.set_caption("Spritesheet Selector")

# Define initial coordinates for the selection box
box_start = None
selection_boxes = []

print("Instructions:")
print("1. Click and drag to create a selection box around each item.")
print("2. When finished, press 'Enter' to print the coordinates of each box.")
print("3. Press 'R' to reset the boxes or 'ESC' to exit.")

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(spritesheet, (0, 0))

    for box in selection_boxes:
        pygame.draw.rect(screen, (255, 0, 0), box, 2)  # Draw each selection box in red

    if box_start:
        mouse_pos = pygame.mouse.get_pos()
        temp_box = pygame.Rect(box_start, (mouse_pos[0] - box_start[0], mouse_pos[1] - box_start[1]))
        pygame.draw.rect(screen, (0, 255, 0), temp_box, 2)  # Draw current box in green

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            box_start = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if box_start:
                box_end = pygame.mouse.get_pos()
                rect = pygame.Rect(
                    min(box_start[0], box_end[0]), 
                    min(box_start[1], box_end[1]), 
                    abs(box_start[0] - box_end[0]), 
                    abs(box_start[1] - box_end[1])
                )
                selection_boxes.append(rect)
                box_start = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Selected coordinates:")
                for idx, box in enumerate(selection_boxes):
                    print(f"Item {idx}: {box}")
                running = False
            elif event.key == pygame.K_r:
                selection_boxes = []  # Reset all boxes
            elif event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
sys.exit()
