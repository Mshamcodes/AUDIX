# AUDIX — AI-driven Embedded Audio Control System

## 🚀 Overview

AUDIX is an intelligent embedded audio control system that dynamically adjusts volume based on environmental conditions.

It integrates:

* Python-based AI decision engine
* UART communication (Python ↔ ESP32)
* ESP32 firmware using ESP-IDF
* State-aware control with verification and stability logic

---

## 🧠 Key Features

* ✅ Manual & AI modes
* ✅ AI-based adaptive volume control
* ✅ State-aware decision system (self-correcting)
* ✅ Hysteresis (anti-flicker control)
* ✅ Reliable UART communication
* ✅ Retry & timeout handling
* ✅ Response verification (closed-loop system)

---

## 🏗️ Architecture

```text
Environment → AI → Command → UART → ESP32 → Response → State Update
```

Detailed flow:

```text
Environment (Simulated Noise)
        ↓
AI Decision Engine
        ↓
Command Builder
        ↓
Serial Manager (UART)
        ↓
ESP32 Firmware (ESP-IDF)
        ↓
Response Parsing
        ↓
State Synchronization
```

---

## 📂 Project Structure

```text
AUDIX/
│
├── main.py
├── README.md
├── requirements.txt
│
├── controller/
│   ├── audio_serial_manager.py
│   ├── audio_response_parser.py
│   └── audio_mode_manager.py
│
├── core/
│   └── audio_state.py
│
├── ai/
│   └── ai_module.py
│
├── environment/
│   └── environment_simulator.py
│
├── utils/
│   └── logger.py
│
├── config/
│   └── settings.py
│
└── firmware/
    └── audix_firmware.c
```

---

## 🎮 Modes of Operation

### 🔵 Manual Mode

User directly controls audio:

```text
quiet / aware / transparent / play / pause
```

---

### 🟢 AI Mode

System automatically adjusts volume based on environment:

* Reads simulated noise level
* Applies hysteresis-based decision
* Avoids unnecessary commands
* Maintains system stability

---

## 🔧 Serial Protocol

### Commands (Python → ESP32)

```text
CMD:SET_VOLUME:<value>
CMD:PLAY
CMD:PAUSE
```

### Responses (ESP32 → Python)

```text
RESP:VOLUME:<value>
RESP:PLAYING:<0/1>
ERR:<message>
```

---

## ⚙️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Configure Serial Port

Edit:

```python
config/settings.py
```

```python
SERIAL_PORT = "COM9"
BAUD_RATE = 115200
```

---

### 3. Flash ESP32 Firmware

```bash
idf.py -p COM3 flash monitor
```

---

### 4. Run Python Application

```bash
python main.py
```

---

## 🧪 Example Usage

```text
Select mode [MANUAL | AI | EXIT]: AI

ENVIRONMENT: {'noise_level': 54}
AI DECISION -> set_volume 60
VOLUME VERIFIED ✅
STATE UPDATED -> AudioState(volume=60, ...)

OUTPUT: 
PS C:\Users\Mahadev GI\AUDIX> python .\main.py
[2026-04-06 00:42:10] Application System Started
Select mode [MANUAL | AI | EXIT] AI
[2026-04-06 00:42:13] AI MODE → One-shot decision
[2026-04-06 00:42:13] ENVIRONMENT: {'noise_level': 50}
[2026-04-06 00:42:13] AI DECISION -> Action: set_volume, Value: 50
[2026-04-06 00:42:13] Sent: CMD:SET_VOLUME:50
[2026-04-06 00:42:13] ESP32: RESP:VOLUME:50
[2026-04-06 00:42:13] VERIFY VOLUME: RESP:VOLUME:50
[2026-04-06 00:42:13] VOLUME VERIFIED ✅
[2026-04-06 00:42:13] STATE UPDATED -> AudioState(volume=50, mode='AWARE', is_playing=False)
AudioState(volume=50, mode='AWARE', is_playing=False)
Select mode [MANUAL | AI | EXIT] MANUAL
[2026-04-06 00:42:18] Entered MANUAL mode
Manual → quiet | aware | transparent | play | pause | menu: aware
[2026-04-06 00:42:20] Sent: CMD:SET_VOLUME:80
[2026-04-06 00:42:20] ESP32: RESP:VOLUME:80
[2026-04-06 00:42:20] VERIFY VOLUME: RESP:VOLUME:80
[2026-04-06 00:42:20] VOLUME VERIFIED ✅
[2026-04-06 00:42:20] STATE UPDATED -> AudioState(volume=80, mode='AWARE', is_playing=False)
AudioState(volume=80, mode='AWARE', is_playing=False)
Manual → quiet | aware | transparent | play | pause | menu: menu
[2026-04-06 00:42:24] Exiting MANUAL mode and selected MENU option
Select mode [MANUAL | AI | EXIT] AI
[2026-04-06 00:42:27] AI MODE → One-shot decision
[2026-04-06 00:42:27] ENVIRONMENT: {'noise_level': 51}
[2026-04-06 00:42:27] AI DECISION -> Action: set_volume, Value: 50
[2026-04-06 00:42:27] Sent: CMD:SET_VOLUME:50
[2026-04-06 00:42:27] ESP32: RESP:VOLUME:50
[2026-04-06 00:42:27] VERIFY VOLUME: RESP:VOLUME:50
[2026-04-06 00:42:27] VOLUME VERIFIED ✅
[2026-04-06 00:42:27] STATE UPDATED -> AudioState(volume=50, mode='AWARE', is_playing=False)
AudioState(volume=50, mode='AWARE', is_playing=False)
Select mode [MANUAL | AI | EXIT] AI
[2026-04-06 00:42:30] AI MODE → One-shot decision
[2026-04-06 00:42:30] ENVIRONMENT: {'noise_level': 51}
[2026-04-06 00:42:30] AI DECISION -> Action: none, Value: None
[2026-04-06 00:42:30] AI: No change required ✅
Select mode [MANUAL | AI | EXIT] MANUAL
[2026-04-06 00:42:54] Entered MANUAL mode
Manual → quiet | aware | transparent | play | pause | menu: play
[2026-04-06 00:42:55] Sent: CMD:PLAY
[2026-04-06 00:42:55] ESP32: RESP:PLAYING:1
[2026-04-06 00:42:55] PLAY STATE UPDATED ✅
[2026-04-06 00:42:55] STATE UPDATED -> AudioState(volume=50, mode='AWARE', is_playing=True)
AudioState(volume=50, mode='AWARE', is_playing=True)
Manual → quiet | aware | transparent | play | pause | menu: MENU
[2026-04-06 00:43:02] Exiting MANUAL mode and selected MENU option
Select mode [MANUAL | AI | EXIT] back
[2026-04-06 00:43:06] ERROR: Invalid mode. Use 'manual' or 'ai'
Select mode [MANUAL | AI | EXIT] AI
[2026-04-06 00:43:07] AI MODE → One-shot decision
[2026-04-06 00:43:07] ENVIRONMENT: {'noise_level': 53}
[2026-04-06 00:43:07] AI DECISION -> Action: none, Value: None
[2026-04-06 00:43:07] AI: No change required ✅
Select mode [MANUAL | AI | EXIT] [2026-04-06 01:06:38] Keyboard recieved Ctrl+C
[2026-04-06 01:06:38] Shutting down system
PS C:\Users\Mahadev GI\AUDIX> 
```

---

## 🧠 AI Logic

* Uses environment input (noise level)
* Applies hysteresis to prevent flickering
* Uses system state to avoid redundant commands
* Acts only when change is required

---

## 🔮 Future Improvements

* Command ID protocol (async communication)
* FreeRTOS-based firmware architecture
* Real microphone input
* Machine learning-based decision engine

---

## 💡 Key Learning Outcomes

* Embedded system communication (UART)
* State machine design
* AI-driven control systems
* Reliability (retry, timeout, verification)
* Control system concepts (hysteresis)

---

## 👨‍💻 Author

Mahadev G I
