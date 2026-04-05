"""
@file audio_decision_engine.py
@brief Core Audio Decision Engine for AUDIX System

This module manages the internal audio state and applies validated updates
based on system commands.

It acts as the control layer between:
- Input commands (manual/AI)
- Audio state management

Features:
- Volume control with safety constraints
- Mode validation
- Playback state management

"""

from core.audio_state import AudioState


class AudioDecisionEngine:
    def __init__(self):
        self.aud_state = AudioState()

    def set_volume(self, volume):
        # Safety constraint
        volume = max(0, min(100, volume))
        self.aud_state.volume = volume

    def set_mode(self, mode):
        if mode in {"QUIET", "AWARE", "TRANSPARENT"}:
            self.aud_state.mode = mode
        else:
            print(f"Invalid mode: {mode}. Mode must be one of 'QUIET', 'AWARE', or 'TRANSPARENT'.")

    def play_command(self, command):
        if command == "play":
            self.aud_state.is_playing = True

    def pause_command(self, command):
        if command == "pause":
            self.aud_state.is_playing = False

    def get_audio_state(self):
        return self.aud_state


# TEST
if __name__ == "__main__":
    engine = AudioDecisionEngine()

    engine.set_volume(100)   # should clamp to 100
    engine.set_mode("QUIET")
    engine.play_command("play")

    print(engine.get_audio_state())
