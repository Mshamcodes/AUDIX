"""
@file audio_mode_manager.py
@brief Manual Audio Mode Selection Module for AUDIX System

This module maps user-selected modes (manual input) to corresponding
audio control actions.

It acts as a bridge between user input and system commands.

Supported modes:
- quiet → low volume
- aware → high volume
- transparent → medium volume
- play → start playback
- pause → stop playback
"""

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
    