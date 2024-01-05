from env.env import CustomEnv
from stable_baselines3 import PPO
import random


import gymnasium as gym
from env.env import CustomEnv  # Import your custom environment class


def test_environment(env, num_episodes=5):
    rewards = []
    for episode in range(num_episodes):
        observation = env.reset()  # Reset the environment
        done = False
        total_reward = 0

        while not done:
            # Here, we choose a random action. In a real scenario, this would come from your agent.
            action = env.action_space.sample()
            observation, reward, done, truncate, info = env.step()  # Perform a step

            total_reward += reward
            print(
                f"Step in Episode {episode + 1}: Action = {action}, Reward = {reward}, Done = {done}"
            )

            print(info)

        print(f"Episode {episode + 1} finished with total reward: {total_reward}")
        rewards.append(total_reward)

    print()
    for i in range(num_episodes):
        print(f"rewards for episode {i}: {rewards[i]}")


# Create and test the environment
env = CustomEnv()
test_environment(env)
