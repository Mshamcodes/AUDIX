# FILE: audio_response_parser.py
# Purpose: Parses responses from the ESP32 and extracts relevant information

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