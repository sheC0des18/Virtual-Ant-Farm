import pygame
from environment import Environment
from ant_agent import AntAgent

# Initialise PyGame
pygame.init()

# Screen dimensions and grid size
grid_size = 20
cell_size = 30
screen_width = grid_size * cell_size
screen_height = grid_size * cell_size + 100  # Extra space for stats
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ant Farm Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_WATER = (0, 0, 255)
GREEN = (0, 255, 0)  # Food
GRAY = (169, 169, 169)  # Obstacle
YELLOW = (255, 255, 0)  # Nest for Colony 1
RED = (255, 0, 0)  # Nest for Colony 0
PALE_BROWN = (210, 180, 140)
PALE_PINK = (255, 182, 193)

# Fonts
font = pygame.font.SysFont(None, 24)

# Pheromone grid
pheromone_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Ant sprite path
ANT_SPRITE_PATH = r"C:\Users\succe\assets\ant.png"

# Nests sprite path
NEST_RED_PATH = r"C:\Users\succe\assets\nest_red.png"
NEST_YELLOW_PATH = r"C:\Users\succe\assets\nest_yellow.png"

def load_ant_sprite():
    #Load and scale the ant sprite
    try:
        ant_sprite = pygame.image.load(ANT_SPRITE_PATH)
        ant_sprite = pygame.transform.scale(ant_sprite, (cell_size, cell_size))
        return ant_sprite
    except Exception as e:
        print(f"Error loading ant sprite: {e}")
        return None


def load_nest_sprites():
    #Load and scale the nest sprites
    try:
        nest_red = pygame.image.load(NEST_RED_PATH)
        nest_yellow = pygame.image.load(NEST_YELLOW_PATH)
        nest_red = pygame.transform.scale(nest_red, (cell_size, cell_size))
        nest_yellow = pygame.transform.scale(nest_yellow, (cell_size, cell_size))
        return nest_red, nest_yellow
    except Exception as e:
        print(f"Error loading nest sprites: {e}")
        return None, None


def update_pheromone_trails():
    #Decay pheromones over time
    decay_factor = 0.95
    for x in range(grid_size):
        for y in range(grid_size):
            pheromone_grid[x][y] *= decay_factor

def draw_pheromone_trails():
    #Visualise pheromone trails for each colony
    for x in range(grid_size):
        for y in range(grid_size):
            intensity = pheromone_grid[x][y]
            if intensity > 0:
                color = PALE_BROWN if (x + y) % 2 == 0 else PALE_PINK
                pygame.draw.rect(screen, color, (y * cell_size, x * cell_size, cell_size, cell_size))

def draw_grid(nest_red_sprite, nest_yellow_sprite):
    #Draw the grid, obstacles, nests, and resources
    for x in range(grid_size):
        for y in range(grid_size):
            cell = environment.grid[x][y]
            if isinstance(cell, str) and cell.startswith('nest_'):
                # Use images for nests
                sprite = nest_red_sprite if cell == 'nest_0' else nest_yellow_sprite
                screen.blit(sprite, (y * cell_size, x * cell_size))
            elif isinstance(cell, dict) and cell.get('type') == 'resource':
                color = GREEN if cell.get('resource_type') == 'food' else BLUE_WATER
                pygame.draw.rect(screen, color, (y * cell_size, x * cell_size, cell_size, cell_size))
            elif cell == 'Obstacle':
                pygame.draw.rect(screen, GRAY, (y * cell_size, x * cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, WHITE, (y * cell_size, x * cell_size, cell_size, cell_size))

            # Draw grid lines
            pygame.draw.rect(screen, BLACK, (y * cell_size, x * cell_size, cell_size, cell_size), 1)

def updated_draw_ants(ant_sprite):
    #Draw ants using sprites or fallback to colored circles
    for i, colony in enumerate(ant_colonies):
        for ant in colony:
            try:
                x, y = ant.position
                if ant_sprite:
                    screen.blit(ant_sprite, (y * cell_size, x * cell_size))
                else:
                    color = (128, 0, 128) if i == 0 else (255, 165, 0)
                    pygame.draw.circle(
                        screen, color,
                        (y * cell_size + cell_size // 2, x * cell_size + cell_size // 2),
                        cell_size // 3
                    )
            except TypeError as e:
                print(f"Error drawing ant: {e}")

def draw_stats():
    #Display colony stats without overlapping
    pygame.draw.rect(screen, WHITE, (0, screen_height - 100, screen_width, 100))  # Clear the stats area
    stats_text = [
        f"Colony {i}: Resources Collected: {colony_resources_collected[i]}, Score: {colony_scores[i]}"
        for i in range(len(colony_resources_collected))
    ]
    for i, text in enumerate(stats_text):
        stat_surface = font.render(text, True, BLACK)
        screen.blit(stat_surface, (10, screen_height - 90 + i * 30))  # Adjusted spacing to avoid overlap

    if paused:  # If the simulation is paused, display the message
        pause_text = font.render("Simulation Paused. Press SPACE to resume.", True, BLACK)
        screen.blit(pause_text, (10, screen_height - 30))  # Display pause message below the stats

# Initialise environment
nests = [[(5, 5)], [(15, 15)]]  # Ensure nests are tuples
colony_count = 2
environment = Environment(grid_size, nests, colony_count)
environment.populate_resources_and_obstacles(num_resources=10, num_obstacles=5)

# Initialise ant colonies
ant_colonies = [
    [AntAgent(environment=environment, colony_memory=environment.colony_memories[0], colony_id=0) for _ in range(10)],
    [AntAgent(environment=environment, colony_memory=environment.colony_memories[1], colony_id=1) for _ in range(10)]
]

# Colony stats
colony_resources_collected = [0] * colony_count
colony_scores = [0] * colony_count


# Load ant sprite
ant_sprite = load_ant_sprite()

# Load nest sprites
nest_red_sprite, nest_yellow_sprite = load_nest_sprites()

# Simulation loop
# Simulation loop
running = True
paused = False  # Initialise the paused variable to track the pause state
step = 0

while running and step < 100:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Toggle pause when spacebar is pressed
                paused = not paused

    if not paused:  # Only execute simulation logic if not paused
        update_pheromone_trails()

        for i, colony in enumerate(ant_colonies):
            for ant in colony:
                print(f"Debug: Ant {ant.colony_id} - Position Type: {type(ant.position)}, Position: {ant.position}")
                try:
                    x, y = ant.position
                    pheromone_grid[x][y] = min(100, pheromone_grid[x][y] + 10)
                    current_state = ant.position
                    available_actions = ant.get_actions()
                    ant.take_action(available_actions)
                    reward = environment.get_reward(ant.position, ant.colony_id)

                    if reward > 0:  # Resource collected
                        colony_resources_collected[i] += 1
                        colony_scores[i] += reward

                    next_state = ant.position
                    ant.learn(current_state, ant.last_action, reward, next_state)
                except Exception as e:
                    print(f"Error processing ant: {ant.position} - {e}")
            for ant in colony:
                cell_content = environment.grid[ant.position[0]][ant.position[1]]
                print(f"Ant {ant.colony_id} at position {ant.position}, Cell: {cell_content}")
                reward = environment.get_reward(ant.position, ant.colony_id)
                print(f"Reward for Ant {ant.colony_id}: {reward}")
                ant.decay_epsilon()  # Decay epsilon for exploration-exploitation balance

        # Rendering
        screen.fill(WHITE)
        draw_grid(nest_red_sprite, nest_yellow_sprite)  # Draw grid, resources, nests, obstacles
        draw_pheromone_trails()  # Draw pheromone trails
        updated_draw_ants(ant_sprite)  # Draw ants on top
        draw_stats()  # Overlay stats
        pygame.display.flip()
        pygame.time.delay(200)
        step += 1

    # Display a "Paused" message
    else:
        draw_stats()  # Display the stats and pause message even if paused
        pygame.display.flip()


pygame.quit()