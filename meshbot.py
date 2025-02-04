import meshtastic
import meshtastic.tcp_interface
import requests
from datetime import datetime
import schedule
import time
import json
from pubsub import pub
import logging
import random
import tkinter as tk
from tkinter import scrolledtext
import sys
import threading

class GUIHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)

class LogWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Bot Logs")
        self.root.geometry("800x600")

        # Create scrolled text widget for logs
        self.log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
        self.log_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Setup logger
        self.setup_logger()

    def setup_logger(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Create GUI handler
        gui_handler = GUIHandler(self.log_area)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        root_logger.addHandler(gui_handler)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        root_logger.addHandler(console_handler)

    def write(self, text):
        self.log_area.insert(tk.END, text)
        self.log_area.see(tk.END)
        self.root.update()

    def flush(self):
        pass

# OpenWeather API configuration
API_KEY = "your_api_key"
CITY_ID = "your_city_id"
BASE_URL = "http://api.openweathermap.org/data/2.5"
LAT = "xx.xxxx"
LON = "-xx.xxxx"

def initialize_meshtastic():
    logging.info("Initializing connection over WiFi")
    interface = meshtastic.tcp_interface.TCPInterface('192.168.x.x')
    logging.info("Meshtastic connection established successfully")
    return interface

def get_random_fact():
    """Get a random fact from multiple APIs"""
    logging.info("Fetching random fact...")
    
    fact_sources = [
        lambda: requests.get('http://numbersapi.com/random/math').text,
        lambda: requests.get('https://uselessfacts.jsph.pl/api/v2/facts/random?language=en').json()['text'],
        lambda: get_today_historical_fact()
    ]
    
    return random.choice(fact_sources)()

def get_today_historical_fact():
    """Helper function for historical facts"""
    today = datetime.now()
    response = requests.get(f'https://history.muffinlabs.com/date/{today.month}/{today.day}')
    data = response.json()
    event = random.choice(data['data']['Events'])
    return f"{event['year']}: {event['text']}"

def onReceive(packet, interface):
    """Callback for received messages"""
    logging.info(f"Received packet: {packet}")
    if 'text' in packet['decoded']:
        text = packet['decoded']['text']
        logging.info(f"Received message: {text}")
        
        if text.lower() == '!weather':
            logging.info("Weather command received, generating report...")
            weather_report_job()
        elif text.lower() == '!test':
            logging.info("Test command received, generating signal report...")
            signal_test_report(packet)
        elif text.lower() == '!ping':
            logging.info("Ping command received, sending response...")
            send_meshtastic_message("Ping OK")
        elif text.lower() == '!fact':
            logging.info("Fact command received, fetching fact...")
            try:
                fact = get_random_fact()
                send_meshtastic_message(fact)
            except Exception as e:
                logging.error(f"Error fetching fact: {e}")
                send_meshtastic_message("Fact service unavailable")
        elif text.lower() == '!help':
            logging.info("Help command received, sending command list...")
            send_help_message()

def get_weather():
    logging.info("Fetching weather data from OpenWeather API...")
    response = requests.get(
        f"{BASE_URL}/weather?id={CITY_ID}&appid={API_KEY}&units=imperial"
    )
    logging.info("Weather data received successfully")
    return response.json()

def get_weather_alerts():
    logging.info("Checking for weather alerts...")
    response = requests.get(
        f"{BASE_URL}/onecall?lat={LAT}&lon={LON}&exclude=minutely,hourly&appid={API_KEY}"
    )
    logging.info("Alert check completed")
    return response.json()

def format_weather_report(weather_data):
    logging.info("Formatting weather report...")
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind']['speed']
    report = f"Weather Report\nTemp: {temp}°F\nHumidity: {humidity}%\nWind: {wind_speed}mph\nConditions: {description}"
    logging.info(f"Formatted report: {report}")
    return report

def signal_test_report(packet):
    """Generate and send signal quality report"""
    logging.info("Generating signal quality report...")
    snr = packet.get('rxSnr', 'N/A')
    rssi = packet.get('rxRssi', 'N/A')
    via_route = packet.get('via', [])
    if via_route:
        hop_info = f"Hops: {len(via_route)}"
    else:
        hop_info = "Direct"
    report = f"Signal Quality Report\nSNR: {snr} dB\nRSSI: {rssi} dBm\n{hop_info}"
    send_meshtastic_message(report)
    logging.info("Signal quality report sent")

def send_help_message():
    """Send list of available commands"""
    help_text = """Commands:
!weather - Weather report
!test - Signal quality
!ping - Test node
!fact - Random fact
!help - Commands"""
    send_meshtastic_message(help_text)
    logging.info("Help message sent")

def send_meshtastic_message(message):
    logging.info(f"Sending message on channel 0: {message}")
    interface.sendText(message, channelIndex=0)
    logging.info("Message sent successfully")

def weather_report_job():
    logging.info("Starting weather report job...")
    weather_data = get_weather()
    report = format_weather_report(weather_data)
    send_meshtastic_message(report)
    logging.info("Weather report job completed")

def check_severe_weather():
    logging.info("Starting severe weather check...")
    alerts = get_weather_alerts()
    if 'alerts' in alerts:
        logging.warning(f"Found {len(alerts['alerts'])} weather alerts!")
        for alert in alerts['alerts']:
            alert_msg = f"WEATHER ALERT: {alert['event']}\n{alert['description']}"
            send_meshtastic_message(alert_msg)
    else:
        logging.info("No severe weather alerts found")

def advertise_bot():
    """Send periodic reminder about the bot's presence"""
    advertisement = "MeshBot is active! Reply !help for available commands"
    send_meshtastic_message(advertisement)
    logging.info("Sent bot reminder message")

def bot_main():
    global interface
    logging.info("Weather service starting...")
    
    # Initialize Meshtastic
    interface = initialize_meshtastic()
    
    # Subscribe to received messages
    pub.subscribe(onReceive, "meshtastic.receive")
    logging.info("Subscribed to Meshtastic messages")

    # Schedule regular weather reports
    schedule.every().day.at("06:00").do(weather_report_job)
    schedule.every().day.at("22:00").do(weather_report_job)
    logging.info("Scheduled regular weather reports for 06:00 and 22:00")

    # Schedule severe weather checks
    schedule.every().hour.do(check_severe_weather)
    logging.info("Scheduled hourly severe weather checks")

    # Schedule bot advertisements every 8 hours
    schedule.every(8).hours.do(advertise_bot)
    logging.info("Scheduled bot advertisements every 8 hours")

    # Send initial startup message
    send_meshtastic_message("K3AYV's MeshBot started! Reply !help for usage")
    logging.info("Weather service initialization complete")

    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    root = tk.Tk()
    log_window = LogWindow(root)
    
    # Start the weather bot in a separate thread
    bot_thread = threading.Thread(target=bot_main, daemon=True)
    bot_thread.start()
    
    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()
