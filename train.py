from tqdm import trange

from env.trading_env import TradingEnv
from models.dqn_agent import DQNAgent
from scripts.dataset import generate_dummy_data
from scripts.kill_switch import KillSwitch


def train(num_steps: int = 1000):
    data = generate_dummy_data(num_steps)
    env = TradingEnv(data)
    agent = DQNAgent(state_dim=len(data.columns), action_dim=3)
    kill = KillSwitch()
    state = env.reset()
    eps = 1.0
    for step in trange(num_steps):
        if kill.armed():
            print("Kill switch engaged. Exiting training.")
            break
        action = agent.act(state, eps)
        next_state, reward, done, _ = env.step(action)
        agent.remember(state, action, reward, next_state, done)
        agent.train_step()
        if step % 10 == 0:
            agent.update_target()
        state = next_state
        eps = max(0.1, eps * 0.995)
        if done:
            state = env.reset()
    print("Training finished. Balance:", env.balance)


if __name__ == "__main__":
    train()
