import aec_rps

mapping = {0: 'ROCK', 1: 'PAPER', 2: 'SCISSORS', 3: 'NONE'}

env = aec_rps.env(render_mode="human")
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()
    print(f'opponent is doing {mapping[int(observation)]}')

    if termination or truncation:
        action = None
    else:
        # this is where you would insert your policy
        action = env.action_space(agent).sample()
        print(f'I\'m going to do {mapping[int(action)]}')

    env.step(action)
env.close()