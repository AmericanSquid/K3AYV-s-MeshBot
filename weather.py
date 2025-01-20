import meshtastic
import meshtastic.ble_interface
import requests
from datetime import datetime
import schedule
import time
import json
from pubsub import pub
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# OpenWeather API configuration
API_KEY = "your_api_key_here"
CITY_ID = "your_city_id_here"
BASE_URL = "http://api.openweathermap.org/data/2.5"

# Initialize Meshtastic connection
logging.info("Initializing connection to Meshtastic device")
interface = meshtastic.ble_interface.BLEInterface('your_ble_device')
logging.info("Meshtastic connection established successfully")

def onReceive(packet, interface):
    """Callback for received messages"""
    logging.info(f"Received packet: {packet}")
    if 'text' in packet['decoded']:
        text = packet['decoded']['text']
        logging.info(f"Received message: {text}")
        if text.lower() == '!weather':
            logging.info("Weather command received, generating report...")
            weather_report_job()

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

def main():
    logging.info("Weather service starting...")

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

    # Send initial startup message
    send_meshtastic_message("Weather service started! Use !weather for current conditions")

    logging.info("Weather service initialization complete")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
