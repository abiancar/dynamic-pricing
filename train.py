from env.env import CustomEnv
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback


class InfoCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(InfoCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        # Access and print the 'info' dictionary
        info = self.locals.get("infos")
        if info is not None:
            print(info[0])  # Assuming a single environment
        return True


env = CustomEnv()  # Assuming CustomEnv is your environment class

# Initialize a PPO agent
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=0.03,
    n_steps=10,
    batch_size=10,
    n_epochs=10,
    gamma=0.01,
    gae_lambda=0.95,
    clip_range=0.9,
    verbose=1,
)

# Create an instance of the custom callback
info_callback = InfoCallback()

# Train the agent with the callback
model.learn(total_timesteps=36500, progress_bar=True)

# Save the agent
model.save("ppo_railpricing")
