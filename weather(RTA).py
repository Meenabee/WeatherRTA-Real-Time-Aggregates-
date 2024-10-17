import requests
import time
from collections import defaultdict

# Configuration
API_KEY = '4bd5665c41fc2266e2a0a601c491e7b1'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
INTERVAL = 300  # 5 minutes in seconds
ALERT_THRESHOLD = 35  # Celsius

# Data Storage
daily_data = defaultdict(list)

# Function to fetch weather data from OpenWeatherMap API
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

# Temperature conversion functions
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

# Process daily weather data
def process_daily_data(city, temperature, weather_condition):
    daily_data[city].append({
        'temperature': temperature,
        'weather_condition': weather_condition
    })

# Calculate daily summary for a city
def calculate_daily_summary(city):
    temperatures = [entry['temperature'] for entry in daily_data[city]]
    dominant_condition = max(set(entry['weather_condition'] for entry in daily_data[city]), key=temperatures.count)
    return {
        'average_temp': sum(temperatures) / len(temperatures),
        'max_temp': max(temperatures),
        'min_temp': min(temperatures),
        'dominant_condition': dominant_condition
    }

# Check for alert conditions
def check_alerts(current_temp):
    if current_temp > ALERT_THRESHOLD:
        print(f"Alert: Temperature exceeds {ALERT_THRESHOLD}°C")

# Main loop to fetch and process weather data
while True:
    for city in CITIES:
        data = fetch_weather_data(city)
        if data and 'main' in data:
            # Extract necessary weather information
            temperature_kelvin = data['main']['temp']
            weather_condition = data['weather'][0]['main']

            # Convert temperature to Celsius
            temperature_celsius = kelvin_to_celsius(temperature_kelvin)

            # Process data for daily summary
            process_daily_data(city, temperature_celsius, weather_condition)

            # Check for alerts
            check_alerts(temperature_celsius)

        time.sleep(INTERVAL)

    # At the end of the day (or after a set number of iterations), calculate summaries
    for city in CITIES:
        if daily_data[city]:
            summary = calculate_daily_summary(city)
            print(f"Daily Summary for {city}: {summary}")
            # Optionally, reset daily data for the next day
            daily_data[city].clear()
