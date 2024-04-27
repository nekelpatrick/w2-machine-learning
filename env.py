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
        self.player_position = (0, 0)  # Reset player position to top-left corner
        return np.array(self.state)

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

    def render(self, mode="human"):
        if mode == "human":
            dungeon_array = np.array(self.state)
            # Set the player's position temporarily to a unique identifier not used elsewhere
            player_val = 4
            original_value = dungeon_array[self.player_position[0]][
                self.player_position[1]
            ]  # Save the original value at the player's position
            dungeon_array[self.player_position[0]][self.player_position[1]] = player_val

            # Create a colormap and normalization that includes all values
            # Colormap: 0 -> white (free space), 1 -> black (wall), 2 -> grey (unused), 3 -> red (monster), 4 -> blue (player)
            cmap = colors.ListedColormap(["white", "black", "grey", "red", "blue"])
            # Normalization: Adjust bounds to include all values
            norm = colors.BoundaryNorm([0, 1, 2, 3, 4, 5], cmap.N)

            fig, ax = plt.subplots(figsize=(10, 8))
            im = ax.imshow(dungeon_array, cmap=cmap, norm=norm)
            plt.colorbar(im, ax=ax, ticks=[0, 1, 2, 3, 4], orientation="vertical")
            ax.axis("off")
            ax.set_title("Dungeon Map with Player Position")
            plt.show()

            # Restore the original value at the player's position after rendering
            dungeon_array[self.player_position[0]][
                self.player_position[1]
            ] = original_value

    def close(self):
        plt.close()
