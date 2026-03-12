from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes.weather import router as weather_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather Dashboard API",
    description="Real-time weather data API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(weather_router, prefix="/api/weather", tags=["weather"])

@app.get("/")
def read_root():
    return {"message": "Weather Dashboard API is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
