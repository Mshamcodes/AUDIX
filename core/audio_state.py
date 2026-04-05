"""
@file audio_state.py
@brief Audio State Model for AUDIX System

This module defines the AudioState class, which represents the current
state of the audio system.

It acts as a single source of truth for:
- Volume level
- Audio mode
- Playback status

"""

class AudioState: 
    def __init__(self):
        # Default audio settings
        self.volume = 50           
        self.mode = "AWARE"
        self.is_playing = False

    def __str__(self):
        return f"AudioState(volume={self.volume}, mode='{self.mode}', is_playing={self.is_playing})" 

# TEST 
if __name__ == "__main__":
    audio_state = AudioState()
    print(audio_state)