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

    def __init__(self, num_floors, max_timesteps=200):
        self.num_floors = num_floors

        """
        Observations are the current position, the current number of people in the elevator,
        the floors people are waiting for outside, and the floors people are waiting for inside
        """

        # Set abitrary maximum number of people per layer
        self.observation_space = spaces.Dict(
            {
                "position": spaces.Discrete(self.num_floors),
                "num_people": spaces.Discrete(2000),
                "floors_selected": spaces.MultiBinary(self.num_floors),
                "floors_waiting": spaces.MultiBinary(self.num_floors)
            }
        )

        # We have three actions, "down", "stay", and "up"
        self.action_space = spaces.Discrete(3)

        # Maximum timesteps
        self.max_timesteps = max_timesteps

        self.arrival_pattern = None  # TODO: Implement different arrival patterns if time allows

    def _get_obs(self):
        return {
            "position": self._position,
            "num_people": self._num_people,
            "floors_selected": self._floors_selected,
            "floors_waiting": self._floors_waiting
        }

    def _get_info(self):
        return {
            "people_waiting": self._people_waiting,
            "people_inside": self._people_inside
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._position = 0  # Start on the first floor
        self._num_people = 0  # No people in the elevator
        self._floors_selected = np.zeros(self.num_floors, dtype=np.int8)  # Boolean array of selected floors inside
        self._floors_waiting = np.zeros(self.num_floors, dtype=np.int8)  # Boolean array of selected floors outside

        # Keep track of other variables not in observation
        self._people_waiting = np.zeros(self.num_floors, dtype=np.int32)  # People outside elevator
        self._people_inside = np.zeros(self.num_floors, dtype=np.int32)  # People inside elevator

        # Timestep tracking
        self.num_timesteps = 0

        # Get the observation and info
        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        # Make the changes in action
        if action == 0:
            # Move the elevator down one if possible
            if self._position > 0:
                self._position -= 1
        elif action == 2:
            # Move the elevator up one if possible
            if self._position < self.num_floors - 1:
                self._position += 1
        elif action == 1:
            # Everyone inside gets out, everyone outside goes in
            # Update observation
            self._floors_selected[self._position] = 0
            self._floors_waiting[self._position] = 0
            self._num_people -= self._people_inside[self._position]
            self._num_people += self._people_waiting[self._position]

            # Update invisible information
            people_entered = self._people_waiting[self._position]
            self._people_waiting[self._position] = 0
            self._people_inside[self._position] = 0

            # Generate floor information for new people entering the elevator
            if self._position == 0:
                # Goes to a random floor above
                new_floors = self.np_random.integers(1, self.num_floors, size=people_entered)
                for floor in new_floors:
                    self._people_inside[floor] += 1
            else:
                # Goes to the first floor
                self._people_inside[0] += people_entered
        else:
            # Do nothing, invalid action
            print(f'Warning, invalid action taken: {action}')

        # Calculate the reward
        # -0.5 reward for everyone inside the elevator, -1 reward for everyone waiting for the elevator
        reward = -sum(self._people_inside) * 0.5 - sum(self._people_waiting)

        # Generate new people at every floor
        new_people = self.np_random.integers(1, 5)
        new_people_floors = self.np_random.integers(0, self.num_floors, size=new_people)
        for new_people_floor in new_people_floors:
            self._people_waiting[new_people_floor] += 1

        # Update what is seen by the elevator
        for index, num_people in enumerate(self._people_inside):
            self._floors_selected[index] = int(num_people > 0)

        for index, num_people in enumerate(self._people_waiting):
            self._floors_waiting[index] = int(num_people > 0)

        # Return observation and info
        self.num_timesteps += 1
        observation = self._get_obs()
        info = self._get_info()
        terminated = False  # Never ends
        truncated = (self.num_timesteps > self.max_timesteps)  # Max timesteps

        return observation, reward, terminated, truncated, info

    def close(self):
        # No resources to close
        return
