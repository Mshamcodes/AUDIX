# FILE: audio_mode_manager.py
# Purpose: Decide the audio mode based on user selection 
# Audio modes - "quiet", "aware", "transparent"

class AudioModeSelection:
    def decide_aud_mode(self, aud_mode):
        """ 
        Decide the audio mode based on the environment context.
        returns: (action, value)
        """

        if aud_mode == "quiet":
            return ("set_volume", 30)
        elif aud_mode == "aware":
            return ("set_volume", 80)
        elif aud_mode == "transparent":
            return ("set_volume", 50)
        elif aud_mode == "play":
            return ("play", None)
        elif aud_mode == "pause":
            return ("pause", None)
        else:
            return ("none", None)
        
# TEST
if __name__ == "__main__":
    mode_selection = AudioModeSelection()

    test_modes = ["quiet", "aware", "transparent"]

    for mode in test_modes:
        action, value = mode_selection.decide_aud_mode(mode)
        print(f"Mode: {mode} → Action: {action}, Value: {value}")
    