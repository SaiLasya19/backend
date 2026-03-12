from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from schemas import WeatherData, ForecastData, SavedLocationSchema
from services.weather_service import WeatherService
from models import SavedLocation, WeatherHistory
from database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/weather/{city}", response_model=WeatherData)
def get_weather(city: str):
    """Get current weather for a city"""
    weather = WeatherService.get_current_weather(city)
    if not weather:
        raise HTTPException(status_code=404, detail="City not found")
    return weather

@router.get("/forecast/{city}", response_model=list[ForecastData])
def get_forecast(city: str, days: int = Query(5, ge=1, le=5)):
    """Get weather forecast for a city"""
    forecast = WeatherService.get_forecast(city, days)
    if not forecast:
        raise HTTPException(status_code=404, detail="City not found")
    return forecast

@router.get("/weather-by-coords/", response_model=WeatherData)
def get_weather_by_coords(lat: float = Query(...), lon: float = Query(...)):
    """Get weather by coordinates (latitude, longitude)"""
    weather = WeatherService.get_weather_by_coordinates(lat, lon)
    if not weather:
        raise HTTPException(status_code=404, detail="Location not found")
    return weather

@router.post("/saved-locations/")
def save_location(city: str, db: Session = Depends(get_db)):
    """Save a location to favorites"""
    weather = WeatherService.get_current_weather(city)
    if not weather:
        raise HTTPException(status_code=404, detail="City not found")
    
    existing = db.query(SavedLocation).filter(SavedLocation.city == city).first()
    if existing:
        return {"message": "Location already saved"}
    
    location = SavedLocation(
        city=weather["city"],
        country=weather["country"]
    )
    db.add(location)
    db.commit()
    
    return {"message": "Location saved successfully"}

@router.get("/saved-locations/", response_model=list[SavedLocationSchema])
def get_saved_locations(db: Session = Depends(get_db)):
    """Get all saved locations"""
    locations = db.query(SavedLocation).all()
    return locations

@router.delete("/saved-locations/{location_id}")
def delete_saved_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a saved location"""
    location = db.query(SavedLocation).filter(SavedLocation.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    db.delete(location)
    db.commit()
    
    return {"message": "Location deleted successfully"}
