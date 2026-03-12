from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class SavedLocation(Base):
    __tablename__ = "saved_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, unique=True, nullable=False, index=True)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class WeatherHistory(Base):
    __tablename__ = "weather_history"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
