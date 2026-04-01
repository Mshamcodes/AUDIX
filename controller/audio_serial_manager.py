# FILE: audio_serial_manager.py
# Purpose: Manages serial communication for audio settings

import serial
import time

class SerialManager:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)

    def send_command(self, command):
        # Flush any stale data in the buffer
        self.ser.reset_input_buffer()
        
        full_command = command + "\n"
        self.ser.write(full_command.encode())
        time.sleep(0.5)  # Give ESP32 time to respond

        # Read response with error handling for corrupt data
        try:
            response = self.ser.readline().decode('utf-8', errors='ignore').strip()
        except Exception as e:
            response = f"Error reading response: {str(e)}"
        
        return response

    def close(self):
        self.ser.close()