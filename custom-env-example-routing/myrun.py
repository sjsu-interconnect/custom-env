from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

from net_env import NetworkEnv

import numpy as np

def env_creator(env_config):
    return NetworkEnv()

register_env("netenv-v0", env_creator)

config = PPOConfig()
config = config.rollouts(num_rollout_workers=1)
config = config.training(gamma=0.999, lr=0.001)
algo = config.build(env='netenv-v0')

config = config.training(gamma=0.999, lr=0)
baselinealgo = config.build(env='netenv-v0')

num_train_iter = 10

for _ in range(num_train_iter):
    pporets = algo.train()['hist_stats']['episode_reward']
    baserets = baselinealgo.train()['hist_stats']['episode_reward']

print('------')
print(f'Average return (100 eps) - PPO: {np.mean(pporets[:-100])}')
print(f'Average return (100 eps) - baseline: {np.mean(baserets[:-100])}')