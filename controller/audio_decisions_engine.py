# FILE: audio_decisions_engine.py
# Purpose: Decision engine for audio settings based on user context

class AudioDecisionsEngine:
    def decide(self, env):
        """ 
        Decide the audio mode based on the environment context.
        returns: (action, value)
        """

        if env == "quiet":
            return ("set_volume", 30)
        elif env == "noise":
            return ("set_volume", 80)
        elif env == "speech":
            return ("set_volume", 50)
        else:
            return ("none", None)
        
# TEST
if __name__ == "__main__":
    decision_engine = AudioDecisionsEngine()

    test_envs = ["quiet", "noise", "speech", "unknown"]

    for env in test_envs:
        action, value = decision_engine.decide(env)
        print(f"Env: {env} → Action: {action}, Value: {value}")
    