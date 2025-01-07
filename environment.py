import random
import numpy as np

class Environment:
    def __init__(self, grid_size, nests, colony_count):
        self.grid_size = grid_size
        self.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]  # Initialize grid

        # Ensure nests is a list of lists containing tuples
        if all(isinstance(nest, list) and len(nest) == 2 for nest in nests):
            self.nests = [[tuple(nest)] for nest in nests]  # Convert to expected format
        else:
            self.nests = nests  # Assume correctly formatted input

        self.colony_count = colony_count
        self.colony_memories = {i: {'visited_cells': set()} for i in range(colony_count)}
        self.resource_types = ['food', 'water']
        self.resources = []
        self.obstacles = []
        self._initialise_grid()
        self._initialise_pheromones()

    def _initialise_grid(self):
        #Initialise the grid by placing static elements like nests
        for colony_id, nest_group in enumerate(self.nests):
            for nest in nest_group:
                self.grid[nest[0]][nest[1]] = f'nest_{colony_id}'
                print(f"Nest for Colony {colony_id} initialized at {nest}")

    def populate_resources_and_obstacles(self, num_resources, num_obstacles):
        #Populate the environment with initial resources and obstacles
        self._spawn_entities(self.resources, 'resource', num_resources)
        self._spawn_entities(self.obstacles, 'obstacle', num_obstacles)

        # Debugging: Verify grid content
        print("Initial Grid State:")
        for row in self.grid:
            print(row)

        # Debugging: Print resource and obstacle locations
        print(f"Resources: {self.resources}")
        print(f"Obstacles: {self.obstacles}")

    def _initialise_pheromones(self):
        #Initialise pheromone maps for the environment
        self.pheromone_map = np.zeros((self.grid_size, self.grid_size))

    def _spawn_entities(self, entity_list, entity_type, count):
        #Spawn entities dynamically
        while len(entity_list) < count:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if self.grid[x][y] is None:  # Place only in empty cells
                if entity_type == 'resource':
                    resource_type = random.choice(self.resource_types)
                    self.grid[x][y] = {'type': entity_type, 'resource_type': resource_type}
                elif entity_type == 'obstacle':
                    self.grid[x][y] = 'Obstacle'
                entity_list.append((x, y))
            else:
                print(f"Skipping placement at occupied cell: ({x}, {y})")

    def update_grid(self):
        #Update the grid to reflect current resource and obstacle positions
        # Clear the grid except for static elements like nests
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self._initialize_grid()  # Reinitialise nests

        # Add dynamic elements back to the grid
        for x, y in self.resources:
            self.grid[x][y] = {'type': 'resource', 'resource_type': random.choice(self.resource_types)}
        for x, y in self.obstacles:
            self.grid[x][y] = 'Obstacle'

    def move_ant(self, position, colony_id, action):
        #Move the ant and calculate the reward for its action
        x, y = position
        if action == 'up' and x > 0 and self.grid[x-1][y] != 'Obstacle':
            x -= 1
        elif action == 'down' and x < self.grid_size - 1 and self.grid[x+1][y] != 'Obstacle':
            x += 1
        elif action == 'left' and y > 0 and self.grid[x][y-1] != 'Obstacle':
            y -= 1
        elif action == 'right' and y < self.grid_size - 1 and self.grid[x][y+1] != 'Obstacle':
            y += 1

        # Leave a pheromone trail at the current position
        pheromone_intensity = 10  # Example value
        self.pheromone_map[x][y] += pheromone_intensity

        new_position = (x, y)  # Ensure position is always a tuple
        self.colony_memories[colony_id]['visited_cells'].add(new_position)
        reward = self.get_reward(new_position, colony_id)
        return new_position, reward


    def get_reward(self, position, colony_id):
        #Calculate the reward for the given position
        x, y = position
        cell = self.grid[x][y]
        print(f"Ant at position: {position}, Cell content: {cell}")  # Debugging
        reward = 0

        if isinstance(cell, dict) and cell.get('type') == 'resource':
            # Resources give rewards based on type
            if cell.get('resource_type') == 'food':
                reward = 10  # Higher reward for food
            elif cell.get('resource_type') == 'water':
                reward = 5  # Lower reward for water
            # Only remove resource if the reward is granted
            self.grid[x][y] = None
            self.resources.remove(position)
        elif cell == 'Obstacle':
            # Obstacles give negative reward
            reward = -5
        elif cell == f'nest_{colony_id}':
            # Returning to own nest gives a reward
            reward = 5
        return reward

    def update_environment(self):
        #Periodically update the environment
        if random.random() < 0.1:  # Small chance for resource or obstacle updates
            self._spawn_entities(self.resources, 'resource', len(self.resources) + 1)
            self._spawn_entities(self.obstacles, 'obstacle', len(self.obstacles) + 1)

    def closest_entity(self, position, entity_type):
        #Find the closest entity of the specified type
        entities = self.resources if entity_type == 'resource' else self.obstacles
        if not entities:
            return float('inf')  # Return a large value if no entities exist
        closest = min(entities, key=lambda entity: np.linalg.norm(np.array(position) - np.array(entity)))
        return closest

    def count_entities(self, position, entity_type, radius):
        #Count the number of entities within a given radius
        entities = self.resources if entity_type == 'resource' else self.obstacles
        return sum(1 for entity in entities if np.linalg.norm(np.array(position) - np.array(entity)) <= radius)

    def get_grid(self):
        #Return a numerical representation of the grid
        numerical_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for colony_id, nest_group in enumerate(self.nests):
            for nest in nest_group:
                numerical_grid[nest[0]][nest[1]] = 3  # Mark nests
        for x, y in self.resources:
            numerical_grid[x][y] = 1  # Mark resources
        for x, y in self.obstacles:
            numerical_grid[x][y] = -1  # Mark obstacles
        return numerical_grid
