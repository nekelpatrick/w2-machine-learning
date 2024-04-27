from env import DungeonEnv

env = DungeonEnv()
obs = env.reset()
done = False
while not done:
    action = env.action_space.sample()  # Randomly sample an action
    obs, reward, done, info = env.step(action)
    env.render()
env.close()
