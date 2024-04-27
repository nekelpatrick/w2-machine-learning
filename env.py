import gym
from gym import spaces
from matplotlib import pyplot as plt
import numpy as np

from dungeonGenerator import generate_dungeon


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
            plt.imshow(dungeon_array, cmap="gray")
            plt.show()

    def close(self):
        pass
