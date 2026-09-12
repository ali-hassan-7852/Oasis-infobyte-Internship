"""
weather.py
Fetches live weather updates using the OpenWeatherMap free-tier API.

Get a free key at https://openweathermap.org/api (Current Weather Data,
free plan - 1000 calls/day, no credit card required). Set it as the
OPENWEATHER_API_KEY environment variable.
"""

import os
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherService:
    def __init__(self, api_key=None, default_city="Delhi", units="metric"):
        self.api_key = api_key or os.environ.get("OPENWEATHER_API_KEY")
        self.default_city = default_city
        self.units = units  # metric = Celsius

    def get_weather(self, city: str = "") -> str:
        if not self.api_key:
            return (
                "I can't fetch weather right now because no OpenWeatherMap "
                "API key is configured."
            )

        city = city.strip() or self.default_city
        params = {
            "q": city,
            "appid": self.api_key,
            "units": self.units,
        }

        try:
            resp = requests.get(BASE_URL, params=params, timeout=6)
            data = resp.json()

            if resp.status_code != 200:
                message = data.get("message", "unknown error")
                return f"I couldn't get the weather for {city}: {message}."

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]

            return (
                f"It's currently {temp:.1f} degrees in {city}, "
                f"feels like {feels_like:.1f}, with {description}. "
                f"Humidity is {humidity} percent."
            )

        except requests.RequestException as e:
            return f"I couldn't reach the weather service: {e}"
