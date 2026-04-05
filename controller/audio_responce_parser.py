"""
@file audio_response_parser.py
@brief UART Response Parser for AUDIX System

This module parses responses received from the ESP32 firmware over UART
and converts them into structured Python dictionaries.

Supported response formats:
- RESP:VOLUME:<int>
- RESP:MODE:<string>
- RESP:PLAYING:<0/1>
- ERR:<message>
"""

class AudioResponseParser:
    def aud_parse_response(self, response: str):
        if not response:
            return None

        response = response.strip()
        parts = response.split(":")

        if parts[0] == "RESP" and len(parts) >= 3:
            if parts[1] == "VOLUME":
                try:
                    return {
                        "type": "volume",
                        "value": int(parts[2])
                    }
                except ValueError:
                    return None
        
        if parts[0] == "RESP" and len(parts) >= 3:
            if parts[1] == "MODE":
                try:
                    return {
                        "type": "mode",
                        "value": int(parts[2])
                    }
                except ValueError:
                    return None
        
        if parts[0] == "RESP" and len(parts) >= 3:
            if parts[1] == "PLAYING":
                try:
                    return {
                        "type": "playing",
                        "value": int(parts[2])
                    }
                except ValueError:
                    return None

        if parts[0] == "ERR":
            return {
                "type": "error",
                "message": ":".join(parts[1:])
            }

        return None