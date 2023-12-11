import gymnasium as gym

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

    def reset(self):
        pass

    def step(self):
        pass

    def close(self):
        pass
