# env.py
import gym
from gym import spaces
from matplotlib import colors, pyplot as plt
import numpy as np
from app import X, Y
from dungeonGenerator import generate_dungeon

# Assuming generate_dungeon is already defined and imported correctly


plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
(line,) = ax.plot([], [], "r-")  # Initialize a line plot
plt.ylabel("Cumulative Reward")
plt.xlabel("Step")


class DungeonEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, rows=2, cols=3, room_size=6, update_callback=None):
        super(DungeonEnv, self).__init__()
        self.rows = rows
        self.cols = cols
        self.room_size = room_size
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=3, shape=(
            rows * room_size, cols * room_size), dtype=int)
        self.state = None
        self.player_position = (0, 0)
        self.cumulative_reward = 0
        # Ensure update_callback is defined here
        self.update_callback = update_callback
        self.reset()
        self.step_count = 0
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.total_monsters = 0  # Track total number of monsters

    def reset(self):
        self.cleared_rooms = set()
        # Adjust generate_dungeon to return total monsters
        self.state, self.total_monsters = generate_dungeon(
            self.rows, self.cols, self.cleared_rooms)
        free_positions = np.argwhere(self.state == 0)
        if free_positions.size > 0:
            start_pos = free_positions[0]
            self.player_position = (start_pos[0], start_pos[1])
        self.cumulative_reward = 0  # Reset cumulative reward
        print("Environment reset.")
        return np.array(self.state)

    def state_to_index(self, state):
        """Convert the state to an index for the Q-table, assuming state is player's position."""
        x, y = state
        return x * (self.cols * self.room_size) + y

    def step(self, action):
        old_x, old_y = self.player_position
        new_x, new_y = (
            old_x,
            old_y,
        )  # Initialize new_x and new_y outside the conditional statements
        if action == 0 and old_x > 0:  # Move up
            new_x = old_x - 1
        elif action == 1 and old_x < self.rows * self.room_size - 1:  # Move down
            new_x = old_x + 1
        elif action == 2 and old_y > 0:  # Move left
            new_y = old_y - 1
        elif action == 3 and old_y < self.cols * self.room_size - 1:  # Move right
            new_y = old_y + 1
        else:
            new_x, new_y = old_x, old_y  # No movement if action is not possible

        self.step_count += 1  # Increment step_count every time step is called
        if self.update_callback:
            self.update_callback(self.step_count, self.cumulative_reward)
        # Check what is at the new position
        # Monster interaction logic
        if self.state[new_x][new_y] == 3:  # Monster
            reward = 100
            self.state[new_x][new_y] = 0  # Remove the monster
            self.total_monsters -= 1
            if self.total_monsters == 0:  # All monsters defeated
                reward += 500  # Large bonus for defeating all monsters
        else:
            # Normal or wall penalty
            reward = -1 if self.state[new_x][new_y] == 0 else -100

        self.player_position = (new_x, new_y)
        self.cumulative_reward += reward
        done = len(self.cleared_rooms) == self.rows * self.cols

        if self.update_callback:
            self.update_callback(self.player_position, self.cumulative_reward)

        print(
            f"Action: {['Up', 'Down', 'Left', 'Right'][action]}, Position: {self.player_position}, Reward: {reward}, Cumulative Reward: {self.cumulative_reward}"
        )

        return np.array(self.state), reward, done, {}

    def render(self, mode='human', render_every=10):
        if self.step_count % render_every != 0:
            return

        self.ax.clear()  # Clear the previous plot
        dungeon_array = np.array(self.state)
        player_val = 4
        original_value = dungeon_array[self.player_position[0]
                                       ][self.player_position[1]]
        dungeon_array[self.player_position[0]
                      ][self.player_position[1]] = player_val

        cmap = colors.ListedColormap(['white', 'black', 'grey', 'red', 'blue'])
        norm = colors.BoundaryNorm([0, 1, 2, 3, 4, 5], cmap.N)

        im = self.ax.imshow(dungeon_array, cmap=cmap, norm=norm)
        if hasattr(self, 'colorbar'):
            self.colorbar.update_normal(im)
        else:
            self.colorbar = self.fig.colorbar(
                im, ax=self.ax, ticks=[0, 1, 2, 3, 4], orientation='vertical')

        self.ax.axis('off')
        self.ax.set_title('Dungeon Map with Player Position')
        plt.figtext(0.5, 0.01, f'Cumulative Reward: {self.cumulative_reward}', ha='center', fontsize=12,
                    bbox={'facecolor': 'orange', 'alpha': 0.5, 'pad': 5})
        self.fig.canvas.draw()
        plt.pause(0.1)

        dungeon_array[self.player_position[0]
                      ][self.player_position[1]] = original_value

    def update_realtime_graph(self, step, reward):
        """ Method to send data to Dash/Plotly """
        X.append(step)
        Y.append(reward)

    def close(self):
        plt.close()
