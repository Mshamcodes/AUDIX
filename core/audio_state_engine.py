# FILE: audio_state_engine.py
# Purpose: Core audio engine for the application

from core.audio_state import AudioState

class AudioStateEngine:
    def __init__(self):
        self.state = AudioState()
    
    def set_volume(self, volume):
        # Safety constraint
        volume = max(0, min(100, volume))
        self.state.volume = volume

    def set_mode(self, mode):
        if mode in {"QUIET", "AWARE", "TRANSPARENT"}:
            self.state.mode = mode
        else:
            print(f"Invalid mode: {mode}. Mode must be one of 'QUIET', 'AWARE', or 'TRANSPARENT'.")
    
    def play_command(self, command):
        if command == "play":
            self.state.is_playing = True
        
    def pause_command(self, command):   
        if command == "pause":
            self.state.is_playing = False

    def get_audio_state(self):
        return self.state
    

# TEST     
if __name__ == "__main__":
    engine = AudioStateEngine()

    engine.set_volume(100)   # should clamp to 100
    engine.set_mode("QUIET")
    engine.play_command("play")

    print(engine.get_audio_state())