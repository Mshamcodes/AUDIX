"""
@file main.py
@brief Main Application Entry Point for AUDIX System

This module integrates all system components:
- Manual control
- AI-based decision making
- UART communication
- State synchronization

It acts as the central orchestrator of the AUDIX system.
"""

import signal 
import sys
import time
from controller.audio_mode_manager import AudioModeSelection
from controller.audio_serial_manager import AudioSerialManager
from controller.audio_responce_parser import AudioResponseParser
from core.audio_state import AudioState
from environment.environment_simulator import EnvironmentSimulator
from ai.ai_module import AIModule
from utils.logger import log, error
from config.settings import SERIAL_PORT, BAUD_RATE


# COMMAND BUILDER
def build_aud_command(action, value):
    if action == "set_volume":
        return f"CMD:SET_VOLUME:{value}"
    elif action == "set_mode":
        return f"CMD:SET_MODE:{value}"
    elif action == "play":
        return "CMD:PLAY"
    elif action == "pause":
        return "CMD:PAUSE"
    else:
        return None


# responce handler 
def handle_response(parsed, serial_manager, parser, audio_state):
    if not parsed:
        error("Invalid response format")
        return

    #  1. VOLUME
    if parsed["type"] == "volume":
        audio_state.volume = parsed["value"]

        # verify command 
        verify_resp = serial_manager.send_command("CMD:GET_VOLUME")    
        log(f"VERIFY VOLUME: {verify_resp}")

        verify_parsed = parser.aud_parse_response(verify_resp)

        if verify_parsed and verify_parsed["type"] == "volume":
            if verify_parsed["value"] == audio_state.volume:
                log("VOLUME VERIFIED ✅")
            else:
                error("VOLUME MISMATCH ❌")
        else:
            error("VOLUME VERIFY FAILED ❌")

    # 2. MODE
    elif parsed["type"] == "mode":
        audio_state.mode = parsed["value"]

        # verify command 
        verify_resp = serial_manager.send_command("CMD:GET_MODE")
        log(f"VERIFY MODE: {verify_resp}")

        verify_parsed = parser.aud_parse_response(verify_resp)

        if verify_parsed and verify_parsed["type"] == "mode":
            if verify_parsed["value"] == audio_state.mode:
                log("MODE VERIFIED ✅")
            else:
                error("MODE MISMATCH ❌")
        else:
            error("MODE VERIFY FAILED ❌")

    # 3. PLAY / PAUSE
    elif parsed["type"] == "playing":
        audio_state.is_playing = bool(parsed["value"])
        log("PLAY STATE UPDATED ✅")

    # 4. ERROR
    elif parsed["type"] == "error":
        error(f"ESP32 ERROR: {parsed['message']}")
        return

    log(f"STATE UPDATED -> {audio_state}")

def cleanup(serial_manager):
    log("Shutting down system")
    try:
        serial_manager.close()
    except:
        pass
    sys.exit(0)


def main():
    aud_mode_selection = AudioModeSelection()
    aud_serial_manager = AudioSerialManager(SERIAL_PORT, BAUD_RATE)
    aud_command_parser = AudioResponseParser()
    aud_state = AudioState()
    env = EnvironmentSimulator()
    ai = AIModule()

    log("Application System Started")

    valid_inputs = {"quiet", "aware", "transparent", "play", "pause"}

    try:
        while True:
            user_selected_mode = input("Select mode [MANUAL | AI | EXIT] ").strip().lower()

            if not user_selected_mode:
                continue

            if user_selected_mode == "exit":
                cleanup(aud_serial_manager)

            if user_selected_mode not in {"manual", "ai"}:
                error("Invalid mode. Use 'manual' or 'ai'")
                continue

            # MANUAL MODE LOOP
            if user_selected_mode == "manual":
                log("Entered MANUAL mode")

                while True:
                    user_input = input("Manual → quiet | aware | transparent | play | pause | menu: ").strip().lower()

                    if not user_input:
                        continue

                    if user_input == "menu":
                        log("Exiting MANUAL mode and selected MENU option")
                        break

                    if user_input not in valid_inputs:
                        error("Invalid input")
                        continue

                    action, value = aud_mode_selection.decide_aud_mode(user_input)

                    command = build_aud_command(action, value)

                    if not command:
                        error("Failed to build command")
                        continue

                    response = aud_serial_manager.send_command(command)

                    log(f"Sent: {command}")
                    log(f"ESP32: {response}")

                    parsed = aud_command_parser.aud_parse_response(response)
                    handle_response(parsed, aud_serial_manager, aud_command_parser, aud_state)

                    print(aud_state)

            # AI MODE LOOP
            elif user_selected_mode == "ai":
                    log("AI MODE → One-shot decision")

                    # 1. Read environment
                    env_data = env.get_environment()
                    log(f"ENVIRONMENT: {env_data}")

                    # 2. AI decision WITH state awareness
                    action, value = ai.tap_action(env_data, aud_state)
                    log(f"AI DECISION -> Action: {action}, Value: {value}")

                    # 3. IMPORTANT: Skip if no change needed
                    if action == "none":
                        log("AI: No change required ✅")
                        continue

                    # 4. Build command
                    command = build_aud_command(action, value)

                    if not command:
                        error("Failed to build command")
                        continue

                    # 5. Send command
                    response = aud_serial_manager.send_command(command)

                    log(f"Sent: {command}")
                    log(f"ESP32: {response}")

                    # 6. Handle response
                    parsed = aud_command_parser.aud_parse_response(response)
                    handle_response(parsed, aud_serial_manager, aud_command_parser, aud_state)

                    print(aud_state)

                    time.sleep(2)

    except KeyboardInterrupt:
        log("Keyboard recieved Ctrl+C")
        cleanup(aud_serial_manager)

if __name__ == "__main__":
    main()