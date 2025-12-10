# weather_utils.py

import os
import requests
from urllib.parse import quote

def get_location():
    """Get the user's current city based on IP address."""
    ip_info_url = "https://ipinfo.io/json"
    try:
        response = requests.get(ip_info_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        city = data.get('city', 'Unknown')
        return city if city != 'Unknown' else None
    except requests.RequestException as e:
        print(f"Error fetching location: {e}")
        return None

def get_weather(city):
    """Get weather information for a city and return as a string."""
    api_key = os.getenv('WEATHER_API_KEY', '')
    if not api_key:
        return "Weather API key not configured. Please set WEATHER_API_KEY environment variable."
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={quote(city)}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()

        if data.get('cod') == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"{description} with a temperature of {temp} degrees Celsius"
        else:
            return f"Failed to retrieve weather information. Error code: {data.get('cod')}"
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")  # Print the error for debugging
        return "An error occurred while fetching the weather information"
