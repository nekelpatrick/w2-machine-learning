# env.py
import gym
from gym import spaces
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np

from dungeonGenerator import generate_dungeon

# Assuming generate_dungeon is already defined and imported correctly


class DungeonEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, rows=5, cols=7, room_size=10):
        super(DungeonEnv, self).__init__()
        self.rows = rows
        self.cols = cols
        self.room_size = room_size
        self.action_space = spaces.Discrete(4)  # 0=up, 1=down, 2=left, 3=right
        self.observation_space = spaces.Box(
            low=0, high=3, shape=(rows * room_size, cols * room_size), dtype=int
        )

        # Initialize the state and player position
        self.state = None
        self.player_position = (0, 0)  # Starting at top-left corner
        self.reset()

    def reset(self):
        self.state = generate_dungeon(self.rows, self.cols)
        # Find a free spot for the player to start
        free_positions = np.argwhere(self.state == 0)  # Assuming 0 is a free space
        if free_positions.size > 0:
            start_pos = free_positions[0]  # Take the first free spot or choose randomly
            self.player_position = (start_pos[0], start_pos[1])
        return np.array(self.state)

    def state_to_index(self, state):
        """Convert the state to an index for the Q-table, assuming state is player's position."""
        x, y = state
        return x * (self.cols * self.room_size) + y

    def step(self, action):
        x, y = self.player_position
        if action == 0 and x > 0:  # Move up
            x -= 1
        elif action == 1 and x < self.rows * self.room_size - 1:  # Move down
            x += 1
        elif action == 2 and y > 0:  # Move left
            y -= 1
        elif action == 3 and y < self.cols * self.room_size - 1:  # Move right
            y += 1

        # Check what is at the new position
        if self.state[x][y] == 1:  # Wall
            reward = -10  # Penalty for hitting a wall
        elif self.state[x][y] == 3:  # Monster
            reward = 10  # Reward for hitting a monster
            self.state[x][y] = 0  # Remove the monster
        else:
            reward = -1  # Small penalty for each move

        self.player_position = (x, y)
        done = np.all(self.state != 3)  # End if no monsters left
        info = {}
        return np.array(self.state), reward, done, info

    def render(self, mode="human", episode=None, render_every=100):
        if mode == "human" and (episode is None or episode % render_every == 0):
            dungeon_array = np.array(self.state)
            player_val = 4
            original_value = dungeon_array[self.player_position[0]][
                self.player_position[1]
            ]
            dungeon_array[self.player_position[0]][self.player_position[1]] = player_val

            cmap = colors.ListedColormap(["white", "black", "grey", "red", "blue"])
            norm = colors.BoundaryNorm([0, 1, 2, 3, 4, 5], cmap.N)

            fig, ax = plt.subplots(figsize=(10, 8))
            im = ax.imshow(dungeon_array, cmap=cmap, norm=norm)
            plt.colorbar(im, ax=ax, ticks=[0, 1, 2, 3, 4], orientation="vertical")
            ax.axis("off")
            ax.set_title("Dungeon Map with Player Position")
            plt.show(block=False)
            plt.pause(0.1)  # Pause to update the plot
            plt.close(fig)  # Close the plot automatically

            dungeon_array[self.player_position[0]][
                self.player_position[1]
            ] = original_value

    def close(self):
        plt.close()
