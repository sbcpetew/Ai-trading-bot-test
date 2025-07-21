import gym
import numpy as np
import pandas as pd
from gym import spaces


class TradingEnv(gym.Env):
    """Simple trading environment."""

    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self.data = data.reset_index(drop=True)
        self.current_step = 0
        self.position = 0  # -1 short, 0 flat, 1 long
        self.balance = 0.0
        self.action_space = spaces.Discrete(3)  # short, flat, long
        self.observation_space = spaces.Box(
            -np.inf,
            np.inf,
            shape=(len(data.columns),),
            dtype=np.float32,
        )

    def reset(self):
        self.current_step = 0
        self.position = 0
        self.balance = 0.0
        return self._get_obs()

    def _get_obs(self):
        return self.data.iloc[self.current_step].values.astype(np.float32)

    def step(self, action: int):
        if self.current_step >= len(self.data) - 1:
            done = True
            reward = 0
            return self._get_obs(), reward, done, {}

        price = self.data.iloc[self.current_step]["close"]
        next_price = self.data.iloc[self.current_step + 1]["close"]
        prev_balance = self.balance
        if action == 2:  # long
            self.balance += next_price - price
            self.position = 1
        elif action == 0:  # short
            self.balance += price - next_price
            self.position = -1
        else:
            self.position = 0
        self.current_step += 1
        reward = self.balance - prev_balance
        done = self.current_step >= len(self.data) - 1
        return self._get_obs(), reward, done, {}
