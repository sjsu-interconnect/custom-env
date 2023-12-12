from elevator_environment import ElevatorEnv
from ray.tune.registry import register_env
from ray.rllib.algorithms.dqn.dqn import DQNConfig, DQN


def env_creator(env_config):
    return ElevatorEnv(8)


# Register the name of the env
register_env("MyGrid", env_creator)

# Getting the config and setting the environment
config = DQNConfig()
config = config.environment(env="MyGrid")

algo = DQN(config=config)

for _ in range(10):
    algo.train()
