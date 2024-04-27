# env.py
import gym
from gym import spaces
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np

from dungeonGenerator import generate_dungeon

# Assuming generate_dungeon is already defined and imported correctly


plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
(line,) = ax.plot([], [], "r-")  # Initialize a line plot
plt.ylabel("Cumulative Reward")
plt.xlabel("Step")


def update_plot(step, cum_reward):
    line.set_xdata(np.append(line.get_xdata(), step))
    line.set_ydata(np.append(line.get_ydata(), cum_reward))
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.01)


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
        self.state = None
        self.player_position = (0, 0)
        self.cumulative_reward = 0  # Initialize cumulative reward
        self.reset()

    def reset(self):
        self.cleared_rooms = set()
        self.state = generate_dungeon(self.rows, self.cols, self.cleared_rooms)
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

        # Check what is at the new position
        if self.state[new_x][new_y] == 1:  # Wall
            reward = -10
        elif self.state[new_x][new_y] == 3:  # Monster
            reward = 10
            self.state[new_x][new_y] = 0  # Remove the monster
        else:
            reward = -1

        self.player_position = (new_x, new_y)
        self.cumulative_reward += reward
        done = len(self.cleared_rooms) == self.rows * self.cols

        # Log the action and result

        print(
            f"Action: {['Up', 'Down', 'Left', 'Right'][action]}, Position: {self.player_position}, Reward: {reward}, Cumulative Reward: {self.cumulative_reward}"
        )

        return np.array(self.state), reward, done, {}

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
            plt.figtext(
                0.5,
                0.01,
                f"Cumulative Reward: {self.cumulative_reward}",
                ha="center",
                fontsize=12,
                bbox={"facecolor": "orange", "alpha": 0.5, "pad": 5},
            )
            plt.show(block=False)
            plt.pause(0.1)
            plt.close(fig)
            print("Rendered the dungeon.")

            dungeon_array[self.player_position[0]][
                self.player_position[1]
            ] = original_value

    def close(self):
        plt.close()
