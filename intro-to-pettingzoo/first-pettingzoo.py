from pettingzoo.classic import rps_v2

id_hands = {0: 'Rock', 1: 'Paper', 2: 'Scissors', 3: 'None'}
def hand_str(hand_id):
    return id_hands[int(hand_id)]

# https://pettingzoo.farama.org/content/basic_usage/

# https://pettingzoo.farama.org/environments/classic/rps/
env = rps_v2.env(max_cycles=2, render_mode="human")
env.reset(seed=42)

# agent_iter(max_iter=2**63) returns an iterator that yields the current agent of the environment. 
# It terminates when all agents in the environment are done or when max_iter (steps have been executed).
for agent in env.agent_iter():
    print(f'who\'s turn? = {agent}')

    # The observation is the last opponent action and its space is a scalar value with 4 possible values.
    observation, reward, termination, truncation, info = env.last()
    print(f'I received {reward}. Opponent\'s hand: {hand_str(observation)}')

    if termination or truncation:
        action = None
    else:
        # this is where you would insert your policy
        action = env.action_space(agent).sample()
        print(f'I chose {hand_str(action)}')

    env.step(action)
env.close()