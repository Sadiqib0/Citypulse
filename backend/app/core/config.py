"""
Core configuration settings for CityPulse application.
Manages environment variables and application settings.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    PROJECT_NAME: str = "CityPulse"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # Database
    DATABASE_URL: str
    POSTGRES_USER: str = "citypulse"
    POSTGRES_PASSWORD: str = "citypulse123"
    POSTGRES_DB: str = "citypulse"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 300  # 5 minutes
    
    # External APIs
    OPENWEATHER_API_KEY: Optional[str] = None
    TRAFFIC_API_KEY: Optional[str] = None
    
    # Data Collection
    DATA_COLLECTION_INTERVAL: int = 10  # seconds
    SENSOR_COUNT: int = 20
    SIMULATE_DATA: bool = True
    
    # Analytics
    ANALYTICS_WINDOW_SIZE: int = 100
    ANOMALY_THRESHOLD: float = 2.5
    
    # Alerts
    ALERT_EMAIL_ENABLED: bool = False
    ALERT_SMTP_SERVER: str = "smtp.gmail.com"
    ALERT_SMTP_PORT: int = 587
    ALERT_EMAIL_FROM: str = "alerts@citypulse.com"
    ALERT_EMAIL_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
