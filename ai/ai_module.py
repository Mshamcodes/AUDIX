"""
@file ai_module.py
@brief AI Decision Module for AUDIX System

This module contains the core AI logic used to determine audio control actions
based on environmental inputs and current system state.

The AI implements:
- Rule-based decision making
- Hysteresis (anti-flicker logic)
- State-aware correction (self-healing system)
"""

class AIModule:
    def __init__(self):
        self.last_volume_level = None   # "LOW" , "MED" , "HIGH"

    def tap_action(self, environment, current_state):
        noise = environment["noise_level"]
        current_volume = current_state.volume

        if noise > 60:
            level = "HIGH"
            target_volume = 80
        elif noise  < 30:
            level = "LOW"
            target_volume = 20
        else:
            level = "MED"
            target_volume = 50

        #  CASE 1: Level changed → act
        if level != self.last_volume_level:
            self.last_volume_level = level
            return ("set_volume", target_volume)

        #  CASE 2: Level same but state wrong → fix
        if current_volume != target_volume:
            return ("set_volume", target_volume)

        #  CASE 3: Everything correct → do nothing
        return ("none", None)