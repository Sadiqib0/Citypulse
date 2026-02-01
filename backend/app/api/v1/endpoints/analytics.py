"""
API endpoints for analytics and insights.
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.api.v1.deps import get_analytics_service
from app.services.analytics.analytics_service import AnalyticsService
from app.schemas.events import (
    AnalyticsOverview,
    TrafficAnalytics,
    WeatherAnalytics,
    PredictionResult
)

router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get comprehensive analytics overview.
    
    Returns:
        Overview metrics including event counts, distributions, and key statistics
    """
    data = await analytics.get_overview_analytics()
    return AnalyticsOverview(**data)


@router.get("/traffic", response_model=TrafficAnalytics)
async def get_traffic_analytics(
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get traffic-specific analytics.
    
    Returns:
        Traffic metrics including congestion levels, incidents, and patterns
    """
    data = await analytics.get_traffic_analytics()
    return TrafficAnalytics(**data)


@router.get("/weather", response_model=WeatherAnalytics)
async def get_weather_analytics(
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Get weather-specific analytics.
    
    Returns:
        Weather metrics including current conditions, forecasts, and alerts
    """
    data = await analytics.get_weather_analytics()
    return WeatherAnalytics(**data)


@router.get("/anomalies")
async def detect_anomalies(
    sensor_id: str = Query(..., description="Sensor ID to analyze"),
    lookback_minutes: int = Query(60, ge=10, le=1440, description="Analysis window in minutes"),
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Detect anomalies in sensor data.
    
    Args:
        sensor_id: Sensor identifier
        lookback_minutes: Time window for analysis (10-1440 minutes)
        
    Returns:
        List of detected anomalies with statistical details
    """
    anomalies = await analytics.detect_anomalies(sensor_id, lookback_minutes)
    return {
        "sensor_id": sensor_id,
        "lookback_minutes": lookback_minutes,
        "anomalies_count": len(anomalies),
        "anomalies": anomalies
    }


@router.get("/predictions")
async def get_predictions(
    event_type: str = Query(..., description="Event type to predict"),
    horizon_hours: int = Query(24, ge=1, le=168, description="Prediction horizon in hours"),
    analytics: AnalyticsService = Depends(get_analytics_service)
):
    """
    Generate predictions for event occurrences.
    
    Args:
        event_type: Type of event to predict (traffic, weather, etc.)
        horizon_hours: Prediction horizon (1-168 hours)
        
    Returns:
        List of predictions with timestamps and confidence levels
    """
    predictions = await analytics.generate_predictions(event_type, horizon_hours)
    return {
        "event_type": event_type,
        "horizon_hours": horizon_hours,
        "predictions_count": len(predictions),
        "predictions": predictions
    }
