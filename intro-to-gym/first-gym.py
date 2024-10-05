import gymnasium as gym

# https://gymnasium.farama.org/environments/classic_control/cart_pole/
# A pole is attached by an un-actuated joint to a cart, which moves along a frictionless track. 
# The pendulum is placed upright on the cart and 
# the goal is to balance the pole by applying forces in the left and right direction on the cart
env = gym.make('CartPole-v1')

observation, info = env.reset()
epi_reward_total = 0
for _ in range(1_000):
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    epi_reward_total += reward
    
    if terminated or truncated:
        print(f'Episode return (no discount): {epi_reward_total}')
        observation, info = env.reset()
        epi_reward_total = 0

env.close()