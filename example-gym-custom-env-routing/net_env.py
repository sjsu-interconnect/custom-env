import numpy as np

import gymnasium as gym
from gymnasium import spaces

class NetworkEnv(gym.Env):

    def __init__(self, render_mode=None, link_cap: int=5):
        # The capacity of each link
        self.link_cap = link_cap
        
        # The number of time steps (incremented per request arrival)
        self.round = 0
        
        # Observations are dictionaries with the link states and requested capacity.
        # The remaining capacity (link state) of each link is concatenated.
        # A Box represents the Cartesian product of n closed intervals: [a,b].
        self.observation_space = spaces.Dict(
            {
                "links": spaces.Box(0, self.link_cap, shape=(3,), dtype=int),
                "req": spaces.Box(0, self.link_cap, shape=(1,), dtype=int),
            }
        )

        # We have 3 actions, corresponding to each path
        self.action_space = spaces.Discrete(3)

    def _get_obs(self):
        # Since we will need to compute observations both in ``reset`` and
        # ``step``, it is often convenient to have a (private) method ``_get_obs``
        # that translates the environment’s state into an observation. However,
        # this is not mandatory and you may as well compute observations in
        # ``reset`` and ``step`` separately:
        return {"links": self._linkstates, "req": self._req}

    def _get_info(self):
        return {
            "utilization": self._linkstates / self.link_cap,
        }
    
    def _generate_req(self):
        return np.array([self.np_random.integers(1, 3 + 1),])

    def reset(self, seed=None, options=None):
                # Reset
        # ~~~~~
        #
        # The ``reset`` method will be called to initiate a new episode. You may
        # assume that the ``step`` method will not be called before ``reset`` has
        # been called. Moreover, ``reset`` should be called whenever a done signal
        # has been issued. Users may pass the ``seed`` keyword to ``reset`` to
        # initialize any random number generator that is used by the environment
        # to a deterministic state. It is recommended to use the random number
        # generator ``self.np_random`` that is provided by the environment’s base
        # class, ``gymnasium.Env``. If you only use this RNG, you do not need to
        # worry much about seeding, *but you need to remember to call
        # ``super().reset(seed=seed)``* to make sure that ``gymnasium.Env``
        # correctly seeds the RNG. Once this is done, we can randomly set the
        # state of our environment. In our case, we randomly choose the agent’s
        # location and the random sample target positions, until it does not
        # coincide with the agent’s position.
        #
        # The ``reset`` method should return a tuple of the initial observation
        # and some auxiliary information. We can use the methods ``_get_obs`` and
        # ``_get_info`` that we implemented earlier for that:

        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.round = 0

        # remove all requests (recover full capacity)
        self._linkstates = np.array([self.link_cap] * 3)
        # generate the first request for the next episode
        self._req = self._generate_req()
        
        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        # Step
        # ~~~~
        #
        # The ``step`` method usually contains most of the logic of your
        # environment. It accepts an ``action``, computes the state of the
        # environment after applying that action and returns the 5-tuple
        # ``(observation, reward, terminated, truncated, info)``. See
        # :meth:`gymnasium.Env.step`. Once the new state of the environment has
        # been computed, we can check whether it is a terminal state and we set
        # ``done`` accordingly. 

        # An episode is done iff 8 requests have arrived
        self.round += 1
        terminated = (self.round == 8)

        # If the request was mapped, what would be the remaining capacity
        pseudo_cap = self._linkstates[action] - self._req[0]
        if pseudo_cap >= 0:
            self._linkstates[action] = pseudo_cap
            reward = +1 * self._req[0] # positive feedback 
        else:
            # no update on state (blocking)
            reward = -1 * self._req[0] # penalty

        self._req = self._generate_req()

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, False, info
