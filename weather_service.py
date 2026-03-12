import requests
from config import OPENWEATHER_API_KEY
from datetime import datetime
from typing import Dict, List, Optional

class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    @staticmethod
    def get_current_weather(city: str) -> Optional[Dict]:
        """Fetch current weather for a city"""
        try:
            url = f"{WeatherService.BASE_URL}/weather"
            params = {
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("cod") != 200:
                return None
            
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None
    
    @staticmethod
    def get_forecast(city: str, days: int = 5) -> Optional[List[Dict]]:
        """Fetch weather forecast for a city"""
        try:
            url = f"{WeatherService.BASE_URL}/forecast"
            params = {
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data.get("list", [])[:days]:
                forecasts.append({
                    "date": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "humidity": item["main"]["humidity"],
                    "wind_speed": item["wind"]["speed"],
                    "icon": item["weather"][0]["icon"]
                })
            
            return forecasts
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return None
    
    @staticmethod
    def get_weather_by_coordinates(lat: float, lon: float) -> Optional[Dict]:
        """Fetch weather by latitude and longitude"""
        try:
            url = f"{WeatherService.BASE_URL}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            print(f"Error fetching weather by coordinates: {e}")
            return None
