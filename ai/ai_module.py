# FILE: ai_module.py 
# PURPOSE: It is the heart of AI feature 


class AIModule:
    def tap_action(self, environment, current_state):
        noise = environment["noise_level"]
        current_volume = current_state.volume

        # Smart + adaptive logic
        if noise > 70 and current_volume != 90:
            return ("set_volume", 90)

        elif noise > 40 and current_volume != 60:
            return ("set_volume", 60)

        elif noise <= 40 and current_volume != 30:
            return ("set_volume", 30)

        # KEY: No unnecessary command
        return ("none", None)