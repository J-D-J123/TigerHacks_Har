import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Load background image
background_img = pygame.image.load("assets/pictures/menuBg.png") 

# images for "house"
topbackground_img   = pygame.image.load("assets/pictures/topbg.jpg")
sellbuilding_img    = pygame.image.load("assets/pictures/sellstation.png")
storebuilding_img   = pygame.image.load("assets/pictures/jessieAuditorium.png")

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
font            = pygame.font.Font(font_path, 36)
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
char_x, char_y        = 0, 0

# counter variables
corn_count            = 0
money_amount          = 0

# Track current grid
current_grid = "main"

growth_timer          = 0
growth_interval       = 5000 

# Store items
# cornPrice = 50 

# store_items = [
#     {"name": "Corn Prices", "price": cornPrice},
# ]


# Store Button setup
# store_buttons = []
# button_gap = 10 
# button_width = 200  
# button_height = 50  

# # Store variables
# show_store      = False
# close_button    = pygame.Rect(WIDTH - 80, 20, 50, 50)  

# Load crop growth stages
crop_stages = [
    pygame.image.load("assets/pictures/firstcorn.png"),
    pygame.image.load("assets/pictures/secondcorn.png"),
    pygame.image.load("assets/pictures/thirdcorn.png"),
]
crop_stages = [pygame.transform.scale(stage, (cell_size, cell_size)) for stage in crop_stages]

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
    global storeX, storeY

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

        for crop in crops:
            pos_x, pos_y = crop["position"]
            x, y = grid_x + pos_x * cell_size, grid_y + pos_y * cell_size
            screen.blit(crop_stages[crop["stage"]], (x, y))

    elif current_grid == "house":
        # Draw the house grid
        pygame.draw.rect(screen, HOUSE_COLOR, (grid_x, grid_y, grid_size, grid_size))

        # Draw the scaled top background image
        screen.blit(scaled_topbackground_img, (grid_x, grid_y))

        # Scale the building
        scaled_sellbuilding_img = pygame.transform.scale(sellbuilding_img, (int(cell_size * 1.5), int(cell_size * 1)))  

        # Draw sell station in the specified cell
        image_cell_x = 1
        image_cell_y = 1

        # Calculate the position on the screen based on the cell size
        image_x = grid_x + image_cell_x * cell_size + (cell_size - scaled_sellbuilding_img.get_width()) // 2 
        image_y = grid_y + image_cell_y * cell_size + (cell_size - scaled_sellbuilding_img.get_height()) // 2  

        screen.blit(scaled_sellbuilding_img, (image_x, image_y))

        # Sell text under sell station 
        sell_text   = font.render("Sell", True, WHITE)
        screen.blit(sell_text, (image_x + 45, image_y + 20))

        # Buy station 
        storecell_x = 3
        storecell_y = 0.9

        scaled_storestation_img = pygame.transform.scale(storebuilding_img, (int(cell_size * 1.5), int(cell_size * 1)))

        storeX = grid_x + storecell_x * cell_size + (cell_size - scaled_storestation_img.get_width()) // 2
        storeY = grid_y + storecell_y * cell_size + (cell_size - scaled_sellbuilding_img.get_height()) // 2  

        screen.blit(scaled_storestation_img, (storeX, storeY))

        # buy_text = font.render("Buy", True, WHITE)
        # screen.blit(buy_text, (storeX + 50, storeY + 20))

        # Draw "To Farm" text in the bottom row, centered
        to_farm_text = font.render("To Farm", True, WHITE)
        screen.blit(to_farm_text, (grid_x + (grid_size - to_farm_text.get_width()) // 2, grid_y + grid_size - to_farm_text.get_height()))

    # Draw character image at the current position
    screen.blit(character_img, (grid_x + char_x, grid_y + char_y))

    # Display "Corn = [amount]" on the top-left
    corn_text = font.render(f"Crop: {corn_count}", True, BLACK)
    screen.blit(corn_text, (10, 10))

    # Display "$[amount]" on the top-right
    default_font = pygame.font.Font(None, 46)
    money_text = default_font.render(f"$ {money_amount}", True, BLACK)
    screen.blit(money_text, (WIDTH - money_text.get_width() - 10, 10))

def main():
    global game_running, char_x, char_y, corn_count, money_amount, current_grid
    global growth_timer, crops, screen  # Declare growth_timer and crops as global

    # Variables for the animation
    animation_start_time = None
    animation_duration = 100
    is_animating = False

    # Initial drawing
    resize_elements(WIDTH, HEIGHT)

    # Create a dictionary to track pressed keys
    pressed_keys = {
        "w": False,
        "a": False,
        "s": False,
        "d": False,
    }

    # Main game loop
    while True:
        # global show_store

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
                        crops.clear()  
                        crops.extend(initialize_crops())  
                        global growth_timer
                        growth_timer = pygame.time.get_ticks()  
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.KEYDOWN and game_running:
                
                if event.key == pygame.K_w:
                    pressed_keys["w"] = True
                elif event.key == pygame.K_a:
                    pressed_keys["a"] = True
                elif event.key == pygame.K_s:
                    pressed_keys["s"] = True
                elif event.key == pygame.K_d:
                    pressed_keys["d"] = True
            elif event.type == pygame.KEYUP and game_running:
                
                if event.key == pygame.K_w:
                    pressed_keys["w"] = False
                elif event.key == pygame.K_a:
                    pressed_keys["a"] = False
                elif event.key == pygame.K_s:
                    pressed_keys["s"] = False
                elif event.key == pygame.K_d:
                    pressed_keys["d"] = False

        # Move character based on pressed keys
        if game_running:
            if pressed_keys["w"] and char_y == 0 and current_grid == "main":  
                char_y = cell_size * 4  
                current_grid = "house"  
            elif pressed_keys["s"] and char_y == cell_size * 4 and current_grid == "house":  
                char_y = 0  
                current_grid = "main"  

            # Move character left and right
            if pressed_keys["a"] and char_x > 0:  
                char_x -= char_speed
            elif pressed_keys["d"] and char_x < grid_size - cell_size:  
                char_x += char_speed

            # Allow vertical movement in main and house grids
            if current_grid == "main":
                if pressed_keys["w"] and char_y > 0:  
                    char_y -= char_speed
                elif pressed_keys["s"] and char_y < grid_size - cell_size:  
                    char_y += char_speed
            elif current_grid == "house":
                if pressed_keys["w"] and char_y > 0: 
                    char_y -= char_speed
                elif pressed_keys["s"] and char_y < grid_size - cell_size: 
                    char_y += char_speed

            # Check if character is in the sell cell in the house grid
            if (
                current_grid == "house" 
                and char_x < 1.25 * cell_size 
                and char_y < 0.8 * cell_size and char_x != 0.10

            ):
                # print("selling")
                # Sell corn when in sell cell
                if corn_count > 0:
                    money_amount += corn_count
                    corn_count = 0
            
            # print(f"x={char_x}, y={char_y}")
            # if (
            #     current_grid == "house"
            #     and char_x >= 275 
            #     and char_y >= 80  
            # ):
                # show_store = True
                # print("selling")
            # else:
            #     show_store = False

            # Harvesting logic in the main grid
            if current_grid == "main":
                for crop in crops:
                    pos_x, pos_y = crop["position"]
                    crop_rect = pygame.Rect(grid_x + pos_x * cell_size, grid_y + pos_y * cell_size, cell_size,
                                            cell_size)
                    
                    # Check if the character is colliding with a crop
                    if crop_rect.collidepoint(grid_x + char_x + cell_size // 2, grid_y + char_y + cell_size // 2):
                        
                        if crop["stage"] == len(crop_stages) - 1:
                            corn_count += 1 
                            crop["stage"] = 0  
                            animation_start_time = pygame.time.get_ticks()  
                            is_animating = True  
                        # else:
                        #     # testing only 
                        #     print("Crop is not ready for harvesting.")  

        # Check crop growth based on timer
        if game_running:
            # char_xtest = char_x / cell_size
            # char_ytest = char_y / cell_size

            # print(f"x={char_xtest} y={char_ytest}")

            current_time = pygame.time.get_ticks()
            if current_time - growth_timer >= growth_interval:
                for crop in crops:
                    
                    if crop["stage"] < len(crop_stages) - 1:
                        crop["stage"] += 1
                growth_timer = current_time  

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

        pygame.display.flip()  

        # 60 FPS
        pygame.time.Clock().tick(60)  


if __name__ == "__main__":
    main()
