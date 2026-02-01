"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from enum import Enum


class EventType(str, Enum):
    """Event type enumeration."""
    TRAFFIC = "traffic"
    WEATHER = "weather"
    SOCIAL = "social"
    SENSOR = "sensor"
    ALERT = "alert"


class EventSeverity(str, Enum):
    """Event severity enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventBase(BaseModel):
    """Base schema for events."""
    event_type: EventType
    severity: EventSeverity = EventSeverity.LOW
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    location: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    meta_data: Dict[str, Any] = Field(default_factory=dict)


class EventCreate(EventBase):
    """Schema for creating an event."""
    pass


class EventUpdate(BaseModel):
    """Schema for updating an event."""
    severity: Optional[EventSeverity] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None
    meta_data: Optional[Dict[str, Any]] = None


class EventResponse(EventBase):
    """Schema for event responses."""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SensorBase(BaseModel):
    """Base schema for sensors."""
    sensor_id: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    sensor_type: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    status: str = "active"
    meta_data: Dict[str, Any] = Field(default_factory=dict)


class SensorCreate(SensorBase):
    """Schema for creating a sensor."""
    pass


class SensorResponse(SensorBase):
    """Schema for sensor responses."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SensorDataBase(BaseModel):
    """Base schema for sensor data."""
    sensor_id: str
    timestamp: datetime
    value: float
    unit: Optional[str] = None
    quality: float = Field(default=1.0, ge=0, le=1)
    meta_data: Dict[str, Any] = Field(default_factory=dict)


class SensorDataCreate(SensorDataBase):
    """Schema for creating sensor data."""
    pass


class SensorDataResponse(SensorDataBase):
    """Schema for sensor data responses."""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlertBase(BaseModel):
    """Base schema for alerts."""
    alert_type: str = Field(..., min_length=1, max_length=100)
    severity: EventSeverity
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=1000)
    source: Optional[str] = Field(None, max_length=255)
    meta_data: Dict[str, Any] = Field(default_factory=dict)


class AlertCreate(AlertBase):
    """Schema for creating an alert."""
    pass


class AlertResponse(AlertBase):
    """Schema for alert responses."""
    id: UUID
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AnalyticsOverview(BaseModel):
    """Schema for analytics overview."""
    total_events: int
    active_events: int
    total_sensors: int
    active_sensors: int
    total_alerts: int
    unresolved_alerts: int
    avg_sensor_value: float
    event_distribution: Dict[str, int]
    severity_distribution: Dict[str, int]


class TrafficAnalytics(BaseModel):
    """Schema for traffic analytics."""
    current_congestion_level: float
    average_speed: float
    incident_count: int
    affected_areas: List[str]
    peak_hours: List[int]
    trends: Dict[str, Any]


class WeatherAnalytics(BaseModel):
    """Schema for weather analytics."""
    current_temperature: float
    feels_like: float
    humidity: float
    wind_speed: float
    conditions: str
    forecast: List[Dict[str, Any]]
    alerts: List[str]


class PredictionResult(BaseModel):
    """Schema for prediction results."""
    prediction_type: str
    timestamp: datetime
    predicted_value: float
    confidence: float
    meta_data: Dict[str, Any]