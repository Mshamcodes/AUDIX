# FILE: main.py
# Purpose: Main application entry point

from controller.audio_decisions_engine import AudioDecisionsEngine
from controller.audio_serial_manager import SerialManager
from utils.logger import log, error
from config.settings import SERIAL_PORT, BAUD_RATE


def main():
    decision_engine = AudioDecisionsEngine()
    serial_manager = SerialManager(SERIAL_PORT, BAUD_RATE)

    log("System Started")

    try:
        while True:
            env = input("Enter environment (quiet/noise/speech or 'exit'): ").strip()

            if env == "exit":
                log("System Stopped")
                break

            action, value = decision_engine.decide(env)

            if action == "set_volume":
                command = f"SET_VOLUME:{value}"
                response = serial_manager.send_command(command)

                log(f"Sent: {command}")
                log(f"ESP32: {response}")

            else:
                error("Unknown environment input")

    finally:
        serial_manager.close()


if __name__ == "__main__":
    main()