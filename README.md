# K3AYV's MeshBot

A Meshtastic bot that provides weather reports and network diagnostics over mesh networks. !ping and !test commands were inspired by [smuniz/mesh_grumpy_bot](https://github.com/smuniz/mesh_grumpy_bot).

## Features

- Real-time weather reports from OpenWeather API
- Signal quality testing (SNR/RSSI)
- Network connectivity checks
- Scheduled weather updates
- Severe weather alerts monitoring

## Commands

- `!weather` - Get current weather report
- `!test` - Check signal quality
- `!ping` - Test node connectivity
- `!help` - List available commands

## Requirements

- Python 3.11+name\Downloads\Bl_container\training\fold\"

- Meshtastic device with Bluetooth capability
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

4. Insert BLE address your Mesh device.
```bash
# Initialize Meshtastic connection
logging.info("Initializing connection over BLE")
interface = meshtastic.ble_interface.BLEInterface('xx:xx:xx:xx:xx:xx')
logging.info("Meshtastic connection established successfully")
```

5. Create Executable:
```bash
pyinstaller --onefile meshbot.py
```

6. Run the Script

## Using with WiFi and Serial Nodes:

This script can easily be modified to work with WiFi and Serial nodes.

- Swap out:
  - `import meshtastic.ble_interface`\
for:
  - `import meshtastic.tcp_interface`

- Swap out:
  - `interface = meshtastic.ble_interface.BLEInterface('xx:xx:xx:xx:xx:xx')`\
for:
  - `interface = meshtastic.tcp_interface.TCPInterface('192.168.x.x')`
