"""
Database models for city events and sensor data.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from app.db.base import Base, TimestampMixin


class EventType(str, enum.Enum):
    """Enumeration of event types."""
    TRAFFIC = "traffic"
    WEATHER = "weather"
    SOCIAL = "social"
    SENSOR = "sensor"
    ALERT = "alert"


class EventSeverity(str, enum.Enum):
    """Enumeration of event severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Event(Base, TimestampMixin):
    """Model for city events."""
    
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(Enum(EventType), nullable=False, index=True)
    severity = Column(Enum(EventSeverity), nullable=False, default=EventSeverity.LOW)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    meta_data = Column(JSON, default={})
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Event {self.id}: {self.title}>"


class Sensor(Base, TimestampMixin):
    """Model for IoT sensors."""
    
    __tablename__ = "sensors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    sensor_type = Column(String(100), nullable=False)
    location = Column(String(255))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    status = Column(String(50), default="active")
    meta_data = Column(JSON, default={})
    
    def __repr__(self):
        return f"<Sensor {self.sensor_id}: {self.name}>"


class SensorData(Base, TimestampMixin):
    """Model for sensor readings."""
    
    __tablename__ = "sensor_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(String(100), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50))
    quality = Column(Float, default=1.0)
    meta_data = Column(JSON, default={})
    
    def __repr__(self):
        return f"<SensorData {self.sensor_id}: {self.value}>"


class Alert(Base, TimestampMixin):
    """Model for system alerts."""
    
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_type = Column(String(100), nullable=False)
    severity = Column(Enum(EventSeverity), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(String(1000), nullable=False)
    source = Column(String(255))
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)
    meta_data = Column(JSON, default={})
    
    def __repr__(self):
        return f"<Alert {self.id}: {self.title}>"