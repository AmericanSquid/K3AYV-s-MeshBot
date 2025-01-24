# K3AYV's MeshBot

A Meshtastic bot that provides weather reports and network diagnostics over mesh networks. 

!ping and !test commands were inspired by [smuniz/mesh_grumpy_bot](https://github.com/smuniz/mesh_grumpy_bot).

## Features

- **Real-time weather reports:** Provides up-to-date weather information using the OpenWeather API.
- **Signal quality testing:** Measures SNR (Signal-to-Noise Ratio) and RSSI (Received Signal Strength Indicator).
- **Network connectivity checks:** Ensures stable and reliable network connections.
- **Random fact generator:** Pulls interesting trivia from the Numbers API, Useless Facts API, and Muffin Labs History API.
- **Self-advertising bot:** Periodically promotes its features to reach new users.
- **Scheduled weather updates:** Automates regular weather report delivery.
- **Severe weather alerts:** Monitors and notifies users about critical weather conditions.

## Commands

- `!weather` - Get current weather report
- `!test` - Check signal quality
- `!ping` - Test node connectivity
- `!fact` - Generate a random fact
- `!help` - List available commands

## Requirements

- Python 3.1
- Meshtastic device
- OpenWeather API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AmericanSquid/k3ayv-s-meshbot.git
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Edit variables in the script for OpenWeather API:
```bash
# OpenWeather API configuration
API_KEY = "your_api_key"
CITY_ID = "your_city_id"
BASE_URL = "http://api.openweathermap.org/data/2.5"
LAT = "xx.xxxx"
LON = "-xx.xxxx"
```

4. Insert internal IP address for your Mesh device.
```bash
# Initialize Meshtastic connection
logging.info("Initializing connection over WiFi")
interface = meshtastic.tcp_interface.TCPInterface('192.168.x.x')
logging.info("Meshtastic connection established successfully")
```

5. Create Executable:
```bash
pyinstaller --onefile meshbot.py
```

6. Run the Script

## Using with BLE and Serial Nodes:

This script can easily be modified to work with BLE and Serial nodes.

- Swap out:
  - `import meshtastic.tcp_interface`\
  for:
  - `import meshtastic.ble_interface`

- Swap out:
  - `interface = meshtastic.tcp_interface.TCPInterface('192.168.x.x')`\
  for:
  - `interface = meshtastic.ble_interface.BLEInterface('xx:xx:xx:xx:xx:xx')`
