# AUDIX

AUDIX is a small audio-control prototype made of two parts:

- A Python controller app that decides a target volume from an environment label and sends commands over serial.
- An ESP32 firmware project that receives serial commands and applies the requested volume value.

The current flow is simple:

1. Run the ESP32 firmware on the board.
2. Run the Python app on the host machine.
3. Enter an environment such as `quiet`, `noise`, or `speech`.
4. The Python app sends `SET_VOLUME:<value>` to the ESP32.
5. The firmware replies with `OK:VOLUME=<value>`.

## Repository Layout

```text
AUDIX/
|-- main.py
|-- config/
|   `-- settings.py
|-- controller/
|   |-- audio_decisions_engine.py
|   `-- audio_serial_manager.py
|-- core/
|   |-- audio_state.py
|   `-- audio_state_engine.py
|-- utils/
|   `-- logger.py
`-- audix_firmware/
    |-- CMakeLists.txt
    `-- main/
        |-- CMakeLists.txt
        `-- audix_firmware.c
```

## Current code flow 

```text
User Input
   ↓
Decision Engine (Python)
   ↓
Command Generation
   ↓
Serial Manager (UART)
   ↓
ESP32 Firmware (ESP-IDF)
   ↓
Command Execution
   ↓
Response (UART)
   ↓
Python Logger (Display)
```


## Components

### Python application

- [`main.py`](/c:/Users/Mahadev%20GI/AUDIX/main.py) is the host-side entry point.
- [`controller/audio_decisions_engine.py`](/c:/Users/Mahadev%20GI/AUDIX/controller/audio_decisions_engine.py) maps environment labels to volume levels.
- [`controller/audio_serial_manager.py`](/c:/Users/Mahadev%20GI/AUDIX/controller/audio_serial_manager.py) sends commands to the ESP32 over UART using `pyserial`.
- [`config/settings.py`](/c:/Users/Mahadev%20GI/AUDIX/config/settings.py) defines the serial port and baud rate.

Current environment mapping:

- `quiet` -> `30`
- `speech` -> `50`
- `noise` -> `80`

### ESP32 firmware

- [`audix_firmware/main/audix_firmware.c`](/c:/Users/Mahadev%20GI/AUDIX/audix_firmware/main/audix_firmware.c) initializes UART0 at `115200`, waits for serial input, parses `SET_VOLUME:<value>`, clamps the value to `0..100`, and returns a status string.
- [`audix_firmware/CMakeLists.txt`](/c:/Users/Mahadev%20GI/AUDIX/audix_firmware/CMakeLists.txt) defines the ESP-IDF project.
- [`audix_firmware/main/CMakeLists.txt`](/c:/Users/Mahadev%20GI/AUDIX/audix_firmware/main/CMakeLists.txt) registers the firmware source file with ESP-IDF.

## Requirements

### Host machine

- Python 3.10+ recommended
- `pyserial`
- A Windows serial port connection to the ESP32 board

Install the Python dependency manually for now because [`requirements.txt`](/c:/Users/Mahadev%20GI/AUDIX/requirements.txt) is currently empty:

```powershell
pip install pyserial
```

### Firmware toolchain

- ESP-IDF v5.3.x
- ESP32 target support installed
- ESP-IDF PowerShell environment opened before running `idf.py`

## Configuration

Set the serial port in [`config/settings.py`](/c:/Users/Mahadev%20GI/AUDIX/config/settings.py) before running the Python app:

```python
SERIAL_PORT = "COM9"
BAUD_RATE = 115200
```

Update `COM9` to the port exposed by your ESP32 board on your machine.

## Build the firmware

From the firmware project directory:

```powershell
cd "C:\Users\Mahadev GI\AUDIX\audix_firmware"
idf.py build
```

If you need a clean rebuild:

```powershell
idf.py fullclean
idf.py build
```

If the build fails with a Git safe-directory error for ESP-IDF, add the ESP-IDF folders to Git's safe directory list:

```powershell
git config --global --add safe.directory C:/Espressif/frameworks/esp-idf-v5.3.1
git config --global --add safe.directory C:/Espressif/frameworks/esp-idf-v5.3.1/components/openthread/openthread
```

## Flash the firmware

Replace `COM3` with your actual ESP32 port:

```powershell
idf.py -p COM3 flash
```

Build, flash, and monitor in one command:

```powershell
idf.py -p COM3 flash monitor
```

Open the serial monitor only:

```powershell
idf.py -p COM3 monitor
```

Exit the monitor with `Ctrl+]`.

## Run the Python controller

From the repository root:

```powershell
cd "C:\Users\Mahadev GI\AUDIX"
python main.py
```

Example session:

```text
Enter environment (quiet/noise/speech or 'exit'): quiet
Sent: SET_VOLUME:30
ESP32: OK:VOLUME=30
```

Type `exit` to stop the host application.

## Current Serial Protocol

Command sent by host:

```text
SET_VOLUME:<0-100>
```

Responses returned by firmware:

```text
READY
OK:VOLUME=<value>
ERROR
```

## Notes    

- `idf.py build` builds the whole ESP-IDF project, not an individual `.c` file directly.
- The repository currently contains both a Python prototype flow and supporting audio state classes. The main runnable host path is [`main.py`](/c:/Users/Mahadev%20GI/AUDIX/main.py).
- [`sdkconfig`](/c:/Users/Mahadev%20GI/AUDIX/sdkconfig) is ignored by Git in this repository's current `.gitignore`, so board-specific config may exist locally without being committed.
