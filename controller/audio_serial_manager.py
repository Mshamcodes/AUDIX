# FILE: audio_serial_manager.py
# Purpose: Manages serial communication for audio settings

import serial
import time

class AudioSerialManager:
    def __init__(self, port, baudrate=115200):
        self.ser_manager = serial.Serial(port, baudrate, timeout=1)

        self.ser_manager.reset_input_buffer()
        self.ser_manager.reset_output_buffer()

        time.sleep(2)

    def send_command(self, command, timeout=1, retries=3):
        for attempt in range(retries):
            # Clear old data
            self.ser_manager.reset_input_buffer()

            full_command = command + "\n"
            self.ser_manager.write(full_command.encode())     # Send the command from USB to UART TX from here to ESP

            start_time = time.time()

            while time.time() - start_time < timeout:
                if self.ser_manager.in_waiting:
                    try:
                        response = self.ser_manager.readline().decode('utf-8', errors='ignore').strip()    # Read the responce from ESP32 via UART TX
                        if response:
                            return response
                    except Exception:
                        pass

            print(f"[WARN] Timeout... retry {attempt+1}")

        return "ERR:TIMEOUT"

    def close(self):
        self.ser_manager.close()