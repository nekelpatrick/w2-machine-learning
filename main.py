from env import DungeonEnv
from q_learning import QLearningAgent
import matplotlib.pyplot as plt

env = DungeonEnv()
n_states = env.rows * env.room_size * env.cols * env.room_size
agent = QLearningAgent(n_states=n_states, n_actions=env.action_space.n)

episodes = 1000  # Number of episodes to train
reward_list = []  # To store total reward per episode

for episode in range(episodes):
    total_reward = 0
    state = env.reset()
    state_index = env.state_to_index(env.player_position)  # Use method from environment
    done = False

    while not done:
        action = agent.choose_action(state_index)
        next_state, reward, done, info = env.step(action)
        next_state_index = env.state_to_index(
            env.player_position
        )  # Use method from environment
        agent.update_q_table(state_index, action, reward, next_state_index)
        state_index = next_state_index
        total_reward += reward
        env.render()

    reward_list.append(total_reward)
    print(
        f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}, Epsilon: {agent.epsilon}"
    )

    # Reduce epsilon to decrease exploration over time
    agent.epsilon *= 0.995
    agent.epsilon = max(
        agent.epsilon, 0.01
    )  # Ensure epsilon does not go below a certain threshold

    if (episode + 1) % 100 == 0:
        plt.plot(reward_list)
        plt.xlabel("Episode")
        plt.ylabel("Total Reward")
        plt.title("Reward Progress Over Time")
        plt.show()

env.close()
