from elevator_environment import ElevatorEnv
from ray.tune.registry import register_env
from ray.rllib.algorithms.dqn.dqn import DQNConfig, DQN


def env_creator(env_config):
    return ElevatorEnv(8)


# Register the name of the env
register_env("Elevator", env_creator)

# Getting the config and setting the environment
config = DQNConfig()
config = config.environment(env="Elevator")

algo = DQN(config=config)

for _ in range(20):
    algo.train()

algo.evaluate()
