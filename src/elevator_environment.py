import numpy as np

import gymnasium as gym
from gymnasium import spaces

class ElevatorEnv(gym.Env):
    """
    State space: Current elevator floor, Current people in elevator, floors to go to, floors people are waiting at
    Action space: Up, down, or stay

    Step: If going up or down, move elevator. Otherwise, all people waiting on current floor get in elevator,
          and everyone who needs to get out gets out. More people arrive on each floor after this.
    Reward: -x for every person in elevator, -y for every person waiting outside elevator
    """

    def __init__(self, num_floors):
        self.num_floors = num_floors

        """
        Observations are the current position, the current number of people in the elevator,
        the floors people are waiting for outside, and the floors people are waiting for inside
        """

        self.observation_space = spaces.Dict(
            {
                "position": spaces.Discrete(self.num_floors),
                "num_people": spaces.Box(low=0, shape=(1, 1), dtype=np.int32),
                "floors_selected": spaces.MultiBinary(self.num_floors),
                "floors_waiting": spaces.MultiBinary(self.num_floors)
            }
        )

        # We have three actions, "up", "stay", and "down"
        self.action_space = spaces.Discrete(3)

        # Keep track of other variables not in observation
        self.people_waiting = np.empty((self.num_floors, 1), dtype=np.int32)  # People outside elevator
        self.people_inside = np.empty((self.num_floors, 1), dtype=np.int32)  # People inside elevator

        self.arrival_pattern = None  # TODO: Implement different arrival patterns if time allows

    def reset(self):
        pass

    def step(self):
        pass

    def close(self):
        pass
