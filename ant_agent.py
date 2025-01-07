import random

class AntAgent:
    def __init__(self, environment, colony_memory, colony_id):
        self.environment = environment
        self.position = random.choice(environment.nests[colony_id])  # Start at the nest (x, y)
        self.colony_memory = colony_memory
        self.colony_id = colony_id
        self.q_table = {}
        self.last_action = None
        self.epsilon = 1.0  # Exploration rate
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor

        # Debugging: Log ant initialisation
        print(f"Ant {self.colony_id} initialised at position: {self.position}")

    def get_actions(self):
        #Get available actions based on the environment
        return ['up', 'down', 'left', 'right']

    def choose_action(self, available_actions):
        #Choose an action using epsilon-greedy strategy or target-seeking
        state = self.position
        if random.uniform(0, 1) < self.epsilon:
            # Explore: Random movement
            return random.choice(available_actions)
        else:
            # Exploit: Move toward the nearest resource if one exists
            nearest_resource = self.environment.closest_entity(self.position, 'resource')
            if nearest_resource == float('inf'):  # No resources found
                return random.choice(available_actions)
            target_x, target_y = nearest_resource
            x, y = self.position

            # Determine the best action to move closer to the target
            if abs(target_x - x) > abs(target_y - y):  # Prioritise vertical movement
                return 'down' if target_x > x else 'up'
            else:
                return 'right' if target_y > y else 'left'

    def take_action(self, available_actions):
        #Execute an action and update the Q-table
        action = self.choose_action(available_actions)
        self.last_action = action
        try:
            new_position, reward = self.environment.move_ant(self.position, self.colony_id, action)
            print(f"Ant {self.colony_id} at position {self.position} moved {action} to {new_position}")
            self.position = new_position
            print(f"Ant {self.colony_id} received reward: {reward}")
            self.learn(self.position, action, reward, new_position)  # Update Q-table
        except Exception as e:
            print(f"Error in move_ant: {e}. Falling back to direct move.")
            self.move(action)  # Fallback move

    def move(self, action):
        #Fallback move if environment interaction fails
        x, y = self.position
        if action == 'up' and x > 0:
            x -= 1
        elif action == 'down' and x < self.environment.grid_size - 1:
            x += 1
        elif action == 'left' and y > 0:
            y -= 1
        elif action == 'right' and y < self.environment.grid_size - 1:
            y += 1
        self.position = (x, y)

    def learn(self, state, action, reward, next_state):
        #Update Q-table using Q-learning
        old_q = self.q_table.get((state, action), 0)
        future_q = max([self.q_table.get((next_state, a), 0) for a in self.get_actions()])
        self.q_table[(state, action)] = old_q + self.alpha * (reward + self.gamma * future_q - old_q)

    def decay_epsilon(self):
        #Decay epsilon for exploration-exploitation balance
        self.epsilon = max(0.01, self.epsilon * 0.995)
