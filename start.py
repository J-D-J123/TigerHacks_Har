
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Load background image
background_img = pygame.image.load("assets/pictures/menuBg.png") 
topbackground_img   = pygame.image.load("assets/pictures/topbg.jpg")

# Set initial window size and enable resizing
MIN_WIDTH, MIN_HEIGHT = 700, 600  
WIDTH, HEIGHT = MIN_WIDTH, MIN_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Truman's Farm Harvester")

# Colors
WHITE           = (255, 255, 255)
SAND            = (194, 178, 128)
GREEN           = (0, 255, 0)
GREY            = (200, 200, 200)
BLACK           = (0, 0, 0)


SELL_CELL_COLOR = (255, 215, 0)
HOUSE_COLOR     = (150, 111, 51)

# Load custom font
font_path       = "assets/fonts/docktrin.ttf"
font = pygame.font.Font(font_path, 36)
large_font      = pygame.font.Font(font_path, 48)

# Button setup
start_button    = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
quit_button     = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

# Max crops
MAX_CORN_CROPS  = 10

# Game variables
game_running    = False
cell_size       = 100
grid_size       = cell_size   * 5
char_speed      = cell_size   / 8

# Load character images and scale to fit cell size
character_img   = pygame.image.load("assets/pictures/tiger_scythe_up.png")
character_img   = pygame.transform.scale(character_img, (cell_size + 32, cell_size + 32))

character_collect_img = pygame.image.load("assets/pictures/tiger_scythe_down.png")
character_collect_img = pygame.transform.scale(character_collect_img, (cell_size + 32, cell_size + 32))

# Character position starts in the top-left grid location
char_x, char_y = 0, 0

# counter variables
corn_count            = 0
money_amount          = 0

# Track current grid
current_grid = "main"

growth_timer          = 0
growth_interval       = 5000

# Load crop growth stages
crop_stages = [
    pygame.image.load("assets/pictures/firstcorn.png"),
    pygame.image.load("assets/pictures/secondcorn.png"),
    pygame.image.load("assets/pictures/thirdcorn.png"),
]
crop_stages = [pygame.transform.scale(stage, (cell_size, cell_size)) for stage in crop_stages]

# Middle cell coordinates in the house grid (for selling crops)
sell_cell_position = (0, 0)

def initialize_crops():
    positions = set()

    while len(positions) < MAX_CORN_CROPS:  
        pos = (random.randint(0, 4), random.randint(0, 4))
        positions.add(pos)  

    # Ensure each crop has a growth stage assigned starts at first stage
    return [{"position": pos, "stage": 0} for pos in positions]  

crops = []

def resize_elements(new_width, new_height):
    global start_button, quit_button, background_img

    # Resize background
    background_img = pygame.transform.scale(background_img, (new_width, new_height))

    # Resize buttons
    start_button.x = new_width  // 2 - 100
    start_button.y = new_height // 2 - 50
    quit_button.x = new_width   // 2 - 100
    quit_button.y = new_height  // 2 + 20

def draw_menu():
    # Draw background
    screen.blit(background_img, (0, 0))

    # Draw title
    title_text = large_font.render("Truman's Farm Harvester", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    # Draw buttons
    pygame.draw.rect(screen, GREY, start_button)
    pygame.draw.rect(screen, GREY, quit_button)

    start_text = font.render("Start", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    # Start button
    screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width())     // 2,
                             start_button.y + (start_button.height - start_text.get_height())   // 2))
    
    # Exit button
    screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width())         // 2,
                            quit_button.y + (quit_button.height - quit_text.get_height())       // 2))

def draw_game():
    scaled_topbackground_img = pygame.transform.scale(topbackground_img, (grid_size, grid_size))

    grid_x = (WIDTH - grid_size) // 2
    grid_y = (HEIGHT - grid_size) // 2

    # Draw background
    screen.blit(background_img, (0, 0))

    # Calculate grid position to keep it centered
    grid_x = (WIDTH - grid_size) // 2
    grid_y = (HEIGHT - grid_size) // 2

    # Draw the grid
    if current_grid == "main":
        # Draw main grid background
        pygame.draw.rect(screen, SAND, (grid_x, grid_y, grid_size, grid_size))

        # Draw "To Town" text in the top row, centered
        to_town_text = font.render("To Town", True, WHITE)
        screen.blit(to_town_text, (grid_x + (grid_size - to_town_text.get_width()) // 2, grid_y + 5))

        # TODO: 

        for crop in crops:
            pos_x, pos_y = crop["position"]
            x, y = grid_x + pos_x * cell_size, grid_y + pos_y * cell_size
            screen.blit(crop_stages[crop["stage"]], (x, y))

    elif current_grid == "house":
        # Draw the house grid
        pygame.draw.rect(screen, HOUSE_COLOR, (grid_x, grid_y, grid_size, grid_size))

        # Draw "To Farm" text in the bottom row, centered
        to_farm_text = font.render("To Farm", True, BLACK)
        screen.blit(to_farm_text, (grid_x + (grid_size - to_farm_text.get_width()) // 2, grid_y + grid_size - cell_size + 70))
        screen.blit(scaled_topbackground_img, (grid_x, grid_y))

        # Draw the special sell cell in the middle
        sell_x, sell_y = sell_cell_position
        pygame.draw.rect(screen, SELL_CELL_COLOR, (grid_x + sell_x * cell_size, grid_y + sell_y * cell_size, cell_size, cell_size))

    # Draw character image at the current position
    screen.blit(character_img, (grid_x + char_x, grid_y + char_y))

    # Display "Corn = [amount]" on the top-left
    corn_text = font.render(f"Corn: {corn_count}", True, WHITE)
    screen.blit(corn_text, (10, 10))

    # Display "$[amount]" on the top-right
    default_font = pygame.font.Font(None, 46)
    money_text = default_font.render(f"$ {money_amount}", True, GREEN)
    screen.blit(money_text, (WIDTH - money_text.get_width() - 10, 10))


def main():
    global game_running, char_x, char_y, corn_count, money_amount, current_grid
    global growth_timer, crops, screen  # Declare growth_timer and crops as global

    # Variables for the animation
    animation_start_time = None
    animation_duration = 500
    is_animating = False

    # Initial drawing
    resize_elements(WIDTH, HEIGHT)

    # Create a dictionary to track pressed keys
    pressed_keys = {
        "w": False,
        "a": False,
        "s": False,
        "d": False
    }

    # Main game loop
    while True:
        grid_x = (WIDTH - grid_size) // 2  # Define grid_x for use in the event loop
        grid_y = (HEIGHT - grid_size) // 2  # Define grid_y for use in the event loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_running:
                    if start_button.collidepoint(event.pos):
                        game_running = True
                        # Initialize crops when starting the game
                        crops.clear()  # Clear existing crops to avoid duplicates
                        crops.extend(initialize_crops())  # Initialize crops
                        global growth_timer
                        growth_timer = pygame.time.get_ticks()  # Reset growth timer
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.KEYDOWN and game_running:
                # Set pressed state for movement keys
                if event.key == pygame.K_w:
                    pressed_keys["w"] = True
                elif event.key == pygame.K_a:
                    pressed_keys["a"] = True
                elif event.key == pygame.K_s:
                    pressed_keys["s"] = True
                elif event.key == pygame.K_d:
                    pressed_keys["d"] = True
            elif event.type == pygame.KEYUP and game_running:
                # Reset pressed state for movement keys
                if event.key == pygame.K_w:
                    pressed_keys["w"] = False
                elif event.key == pygame.K_a:
                    pressed_keys["a"] = False
                elif event.key == pygame.K_s:
                    pressed_keys["s"] = False
                elif event.key == pygame.K_d:
                    pressed_keys["d"] = False

        # Move character based on pressed keys
        # Move character based on pressed keys
        if game_running:
            if pressed_keys["w"] and char_y == 0 and current_grid == "main":  # Move to house grid
                char_y = cell_size * 4  # Set character position to bottom of the house grid
                current_grid = "house"  # Change to house grid
            elif pressed_keys["s"] and char_y == cell_size * 4 and current_grid == "house":  # Move to main grid
                char_y = 0  # Set character position to top of the main grid
                current_grid = "main"  # Change to main grid

            # Move character left and right, allowing edge movement
            if pressed_keys["a"] and char_x > 0:  # Move left
                char_x -= char_speed
            elif pressed_keys["d"] and char_x < grid_size - cell_size:  # Move right
                char_x += char_speed

            # Allow vertical movement in main and house grids
            if current_grid == "main":
                if pressed_keys["w"] and char_y > 0:  # Move up within the main grid
                    char_y -= char_speed
                elif pressed_keys["s"] and char_y < grid_size - cell_size:  # Move down within the main grid
                    char_y += char_speed
            elif current_grid == "house":
                if pressed_keys["w"] and char_y > 0:  # Move up within the house grid
                    char_y -= char_speed
                elif pressed_keys["s"] and char_y < grid_size - cell_size:  # Move down within the house grid
                    char_y += char_speed

            # Check if character is in the sell cell in the house grid
            if current_grid == "house" and (char_x // cell_size, char_y // cell_size) == sell_cell_position:
                # Sell corn when in sell cell
                if corn_count > 0:
                    money_amount += corn_count
                    corn_count = 0  # Reset corn count after selling

            # Harvesting logic in the main grid
            if current_grid == "main":
                for crop in crops:
                    pos_x, pos_y = crop["position"]
                    crop_rect = pygame.Rect(grid_x + pos_x * cell_size, grid_y + pos_y * cell_size, cell_size,
                                            cell_size)
                    # Check if the character is colliding with a crop
                    if crop_rect.collidepoint(grid_x + char_x + cell_size // 2, grid_y + char_y + cell_size // 2):
                        # Check if crop is at final stage before harvesting
                        if crop["stage"] == len(crop_stages) - 1:
                            corn_count += 1  # Increment corn count
                            crop["stage"] = 0  # Reset crop stage
                            animation_start_time = pygame.time.get_ticks()  # Start the animation
                            is_animating = True  # Set the animation flag
                        else:
                            print("Crop is not ready for harvesting.")  # Print message if not ready

        # Check crop growth based on timer
        if game_running:
            current_time = pygame.time.get_ticks()
            if current_time - growth_timer >= growth_interval:
                for crop in crops:
                    # Increment crop growth stage, reset if at final stage
                    if crop["stage"] < len(crop_stages) - 1:
                        crop["stage"] += 1
                growth_timer = current_time  # Reset growth timer

        # Drawing operations
        if game_running:
            draw_game()
        else:
            draw_menu()

        # Animation logic
        if is_animating:
            # Display the collection animation
            screen.blit(character_collect_img, (grid_x + char_x, grid_y + char_y))
            # Check if the animation duration has passed
            if animation_start_time is not None and pygame.time.get_ticks() - animation_start_time >= animation_duration:
                is_animating = False  # Reset animation flag after duration

        pygame.display.flip()  # Update the full display Surface to the screen
        pygame.time.Clock().tick(60)  # Maintain 60 frames per second


if __name__ == "__main__":
    main()
