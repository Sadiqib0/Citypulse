"""
Analytics service for processing and analyzing city data.
Provides statistical analysis, anomaly detection, and predictions.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.events import Event, SensorData, Alert, EventType, EventSeverity
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for data analytics and insights."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_overview_analytics(self) -> Dict[str, Any]:
        """
        Get comprehensive analytics overview.
        
        Returns:
            Dictionary containing overview metrics
        """
        # Total events
        total_events_query = select(func.count(Event.id))
        total_events = await self.db.scalar(total_events_query)
        
        # Active events
        active_events_query = select(func.count(Event.id)).where(Event.is_active == True)
        active_events = await self.db.scalar(active_events_query)
        
        # Event distribution by type
        event_dist_query = select(
            Event.event_type,
            func.count(Event.id)
        ).group_by(Event.event_type)
        result = await self.db.execute(event_dist_query)
        event_distribution = {row[0].value: row[1] for row in result}
        
        # Severity distribution
        severity_dist_query = select(
            Event.severity,
            func.count(Event.id)
        ).group_by(Event.severity)
        result = await self.db.execute(severity_dist_query)
        severity_distribution = {row[0].value: row[1] for row in result}
        
        # Alert counts
        total_alerts_query = select(func.count(Alert.id))
        total_alerts = await self.db.scalar(total_alerts_query)
        
        unresolved_alerts_query = select(func.count(Alert.id)).where(
            Alert.is_resolved == False
        )
        unresolved_alerts = await self.db.scalar(unresolved_alerts_query)
        
        # Average sensor value (simplified)
        avg_sensor_query = select(func.avg(SensorData.value))
        avg_sensor_value = await self.db.scalar(avg_sensor_query) or 0.0
        
        return {
            "total_events": total_events or 0,
            "active_events": active_events or 0,
            "total_sensors": settings.SENSOR_COUNT,
            "active_sensors": settings.SENSOR_COUNT,
            "total_alerts": total_alerts or 0,
            "unresolved_alerts": unresolved_alerts or 0,
            "avg_sensor_value": float(avg_sensor_value),
            "event_distribution": event_distribution,
            "severity_distribution": severity_distribution
        }
    
    async def get_traffic_analytics(self) -> Dict[str, Any]:
        """
        Get traffic-specific analytics.
        
        Returns:
            Dictionary containing traffic metrics
        """
        # Get recent traffic events
        query = select(Event).where(
            Event.event_type == EventType.TRAFFIC
        ).order_by(Event.created_at.desc()).limit(100)
        
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        if not events:
            return {
                "current_congestion_level": 0.0,
                "average_speed": 0.0,
                "incident_count": 0,
                "affected_areas": [],
                "peak_hours": [],
                "trends": {}
            }
        
        # Calculate metrics
        congestion_levels = [
            e.metadata.get("congestion_level", 0) 
            for e in events 
            if e.metadata
        ]
        avg_congestion = np.mean(congestion_levels) if congestion_levels else 0.0
        
        # Get affected areas
        affected_areas = list(set([
            e.location for e in events if e.location
        ]))[:5]
        
        # Analyze time patterns
        event_hours = [e.created_at.hour for e in events]
        hour_counts = pd.Series(event_hours).value_counts()
        peak_hours = hour_counts.nlargest(3).index.tolist()
        
        return {
            "current_congestion_level": float(avg_congestion),
            "average_speed": random.uniform(30, 60),  # Simulated
            "incident_count": len(events),
            "affected_areas": affected_areas,
            "peak_hours": peak_hours,
            "trends": {
                "hourly_distribution": hour_counts.to_dict()
            }
        }
    
    async def get_weather_analytics(self) -> Dict[str, Any]:
        """
        Get weather-specific analytics.
        
        Returns:
            Dictionary containing weather metrics
        """
        # Get recent weather events
        query = select(Event).where(
            Event.event_type == EventType.WEATHER
        ).order_by(Event.created_at.desc()).limit(10)
        
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        if not events:
            return {
                "current_temperature": 20.0,
                "feels_like": 20.0,
                "humidity": 50.0,
                "wind_speed": 10.0,
                "conditions": "Clear",
                "forecast": [],
                "alerts": []
            }
        
        latest = events[0]
        metadata = latest.metadata or {}
        
        # Extract weather data
        temperature = metadata.get("temperature", 20.0)
        humidity = metadata.get("humidity", 50.0)
        wind_speed = metadata.get("wind_speed", 10.0)
        
        # Calculate feels like temperature
        feels_like = temperature - (wind_speed * 0.2)
        
        # Get weather alerts
        weather_alerts = [
            e.title for e in events 
            if e.severity in [EventSeverity.HIGH, EventSeverity.CRITICAL]
        ]
        
        return {
            "current_temperature": float(temperature),
            "feels_like": float(feels_like),
            "humidity": float(humidity),
            "wind_speed": float(wind_speed),
            "conditions": latest.title,
            "forecast": [],  # Would integrate with weather API
            "alerts": weather_alerts[:3]
        }
    
    async def detect_anomalies(
        self,
        sensor_id: str,
        lookback_minutes: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Detect anomalies in sensor data using statistical methods.
        
        Args:
            sensor_id: Sensor identifier
            lookback_minutes: Time window for analysis
            
        Returns:
            List of detected anomalies
        """
        cutoff_time = datetime.utcnow() - timedelta(minutes=lookback_minutes)
        
        query = select(SensorData).where(
            SensorData.sensor_id == sensor_id,
            SensorData.timestamp >= cutoff_time
        ).order_by(SensorData.timestamp)
        
        result = await self.db.execute(query)
        readings = result.scalars().all()
        
        if len(readings) < 10:
            return []
        
        # Convert to pandas for analysis
        df = pd.DataFrame([
            {"timestamp": r.timestamp, "value": r.value}
            for r in readings
        ])
        
        # Calculate statistical bounds
        mean = df["value"].mean()
        std = df["value"].std()
        threshold = settings.ANOMALY_THRESHOLD
        
        # Detect anomalies
        anomalies = []
        for _, row in df.iterrows():
            z_score = abs((row["value"] - mean) / std) if std > 0 else 0
            if z_score > threshold:
                anomalies.append({
                    "timestamp": row["timestamp"],
                    "value": row["value"],
                    "expected_range": (mean - threshold * std, mean + threshold * std),
                    "z_score": z_score
                })
        
        return anomalies
    
    async def generate_predictions(
        self,
        event_type: str,
        horizon_hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Generate simple predictions for event occurrences.
        
        Args:
            event_type: Type of event to predict
            horizon_hours: Prediction horizon in hours
            
        Returns:
            List of predictions
        """
        # Get historical data
        cutoff_time = datetime.utcnow() - timedelta(days=7)
        
        query = select(Event).where(
            Event.event_type == event_type,
            Event.created_at >= cutoff_time
        ).order_by(Event.created_at)
        
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        if len(events) < 5:
            return []
        
        # Simple time-series pattern analysis
        event_hours = [e.created_at.hour for e in events]
        hour_freq = pd.Series(event_hours).value_counts()
        
        # Generate predictions for next 24 hours
        predictions = []
        current_time = datetime.utcnow()
        
        for hour_offset in range(horizon_hours):
            pred_time = current_time + timedelta(hours=hour_offset)
            pred_hour = pred_time.hour
            
            # Predict based on historical frequency
            frequency = hour_freq.get(pred_hour, 0)
            total_events = len(events)
            probability = frequency / total_events if total_events > 0 else 0
            
            predictions.append({
                "prediction_type": event_type,
                "timestamp": pred_time,
                "predicted_value": probability,
                "confidence": min(0.9, probability * 1.2),
                "metadata": {
                    "historical_frequency": int(frequency),
                    "hour": pred_hour
                }
            })
        
        return predictions


# Random import for simulation
import random
