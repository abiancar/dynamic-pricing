from env.env import CustomEnv
import numpy as np

env = CustomEnv()

obs, info = env.reset()


for episode in range(300):
    # print(np.array([episode] * 10).astype(np.float32))
    action = model.predict(obs)

    obs, reward, done, trunc, info = env.step(action)

    print(reward, "points with a price of: $", episode, "per ticket")
