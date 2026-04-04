# FILE: environment_simulator.py
# Purpose: Manages the environment simulation for the whole system

import random

class EnvironmentSimulator:
    def __init__(self):
        self.noise_level = 50

    def get_environment(self):
        """
        Simulate environmental conditions
        """

        # Small variation instead of random jump
        change_val = random.randint(-5, 5)

        self.noise_level += change_val

        # Clamp range
        self.noise_level = max(20, min(90, self.noise_level))

        return {
            "noise_level": self.noise_level
        }
