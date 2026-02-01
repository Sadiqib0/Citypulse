"""
Data collection service for simulating real-time city data.
Generates traffic, weather, social events, and IoT sensor readings.
"""
import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import redis.asyncio as redis
import json
import logging
from app.core.config import settings
from app.models.events import EventType, EventSeverity

logger = logging.getLogger(__name__)


class DataCollectorService:
    """Service for collecting and simulating city data."""
    
    def __init__(self):
        self.redis_client = None
        self.is_running = False
        self.sensor_locations = self._generate_sensor_locations()
        
    async def _get_redis(self):
        """Get Redis client connection."""
        if not self.redis_client:
            self.redis_client = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client
    
    def _generate_sensor_locations(self) -> List[Dict[str, Any]]:
        """Generate random sensor locations across the city."""
        locations = []
        base_lat, base_lon = 40.7128, -74.0060  # New York City center
        
        for i in range(settings.SENSOR_COUNT):
            locations.append({
                "sensor_id": f"SENSOR_{i:03d}",
                "name": f"Sensor {i + 1}",
                "latitude": base_lat + random.uniform(-0.1, 0.1),
                "longitude": base_lon + random.uniform(-0.1, 0.1),
                "type": random.choice(["temperature", "humidity", "air_quality", "noise"])
            })
        
        return locations
    
    async def _generate_traffic_event(self) -> Dict[str, Any]:
        """Generate a simulated traffic event."""
        traffic_types = [
            "Heavy Traffic",
            "Accident",
            "Road Construction",
            "Traffic Jam",
            "Slow Moving Traffic"
        ]
        
        severities = {
            "Heavy Traffic": EventSeverity.MEDIUM,
            "Accident": EventSeverity.HIGH,
            "Road Construction": EventSeverity.LOW,
            "Traffic Jam": EventSeverity.HIGH,
            "Slow Moving Traffic": EventSeverity.MEDIUM
        }
        
        event_title = random.choice(traffic_types)
        base_lat, base_lon = 40.7128, -74.0060
        
        return {
            "event_type": EventType.TRAFFIC.value,
            "severity": severities[event_title].value,
            "title": event_title,
            "description": f"Traffic incident detected in the area",
            "location": f"{random.choice(['Broadway', 'Fifth Ave', 'Park Ave', 'Madison Ave'])}",
            "latitude": base_lat + random.uniform(-0.05, 0.05),
            "longitude": base_lon + random.uniform(-0.05, 0.05),
            "meta_data": {
                "congestion_level": random.uniform(0.5, 1.0),
                "estimated_delay": random.randint(5, 30),
                "affected_lanes": random.randint(1, 3)
            }
        }
    
    async def _generate_weather_event(self) -> Dict[str, Any]:
        """Generate a simulated weather event."""
        weather_conditions = [
            ("Clear Sky", EventSeverity.LOW),
            ("Light Rain", EventSeverity.LOW),
            ("Heavy Rain", EventSeverity.MEDIUM),
            ("Thunderstorm", EventSeverity.HIGH),
            ("Snow", EventSeverity.MEDIUM),
            ("Fog", EventSeverity.MEDIUM)
        ]
        
        condition, severity = random.choice(weather_conditions)
        
        return {
            "event_type": EventType.WEATHER.value,
            "severity": severity.value,
            "title": condition,
            "description": f"Current weather condition: {condition}",
            "location": "City Wide",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "meta_data": {
                "temperature": random.uniform(0, 35),
                "humidity": random.uniform(30, 90),
                "wind_speed": random.uniform(0, 50),
                "visibility": random.uniform(1, 10)
            }
        }
    
    async def _generate_sensor_reading(self, sensor: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a sensor reading."""
        value_ranges = {
            "temperature": (0, 40),
            "humidity": (20, 90),
            "air_quality": (0, 500),
            "noise": (30, 100)
        }
        
        min_val, max_val = value_ranges[sensor["type"]]
        
        return {
            "sensor_id": sensor["sensor_id"],
            "timestamp": datetime.utcnow().isoformat(),
            "value": random.uniform(min_val, max_val),
            "unit": self._get_unit(sensor["type"]),
            "quality": random.uniform(0.8, 1.0),
            "meta_data": {
                "sensor_type": sensor["type"],
                "location": f"{sensor['latitude']:.4f}, {sensor['longitude']:.4f}"
            }
        }
    
    def _get_unit(self, sensor_type: str) -> str:
        """Get measurement unit for sensor type."""
        units = {
            "temperature": "°C",
            "humidity": "%",
            "air_quality": "AQI",
            "noise": "dB"
        }
        return units.get(sensor_type, "")
    
    async def _publish_event(self, channel: str, data: Dict[str, Any]):
        """Publish event to Redis pub/sub channel."""
        try:
            redis_client = await self._get_redis()
            await redis_client.publish(channel, json.dumps(data))
            logger.debug(f"Published to {channel}: {data.get('title', 'sensor_data')}")
        except Exception as e:
            logger.error(f"Error publishing to Redis: {e}")
    
    async def collect_traffic_data(self):
        """Continuously collect traffic data."""
        while self.is_running:
            try:
                event = await self._generate_traffic_event()
                await self._publish_event("events:traffic", event)
                await asyncio.sleep(random.uniform(15, 30))
            except Exception as e:
                logger.error(f"Error collecting traffic data: {e}")
                await asyncio.sleep(5)
    
    async def collect_weather_data(self):
        """Continuously collect weather data."""
        while self.is_running:
            try:
                event = await self._generate_weather_event()
                await self._publish_event("events:weather", event)
                await asyncio.sleep(random.uniform(30, 60))
            except Exception as e:
                logger.error(f"Error collecting weather data: {e}")
                await asyncio.sleep(5)
    
    async def collect_sensor_data(self):
        """Continuously collect sensor data from all sensors."""
        while self.is_running:
            try:
                for sensor in self.sensor_locations:
                    reading = await self._generate_sensor_reading(sensor)
                    await self._publish_event(f"sensors:{sensor['sensor_id']}", reading)
                    await self._publish_event("sensors:all", reading)
                
                await asyncio.sleep(settings.DATA_COLLECTION_INTERVAL)
            except Exception as e:
                logger.error(f"Error collecting sensor data: {e}")
                await asyncio.sleep(5)
    
    async def start_collection(self):
        """Start all data collection tasks."""
        self.is_running = True
        logger.info("Starting data collection service...")
        
        tasks = [
            asyncio.create_task(self.collect_traffic_data()),
            asyncio.create_task(self.collect_weather_data()),
            asyncio.create_task(self.collect_sensor_data())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.info("Data collection service cancelled")
        finally:
            self.is_running = False
            if self.redis_client:
                await self.redis_client.close()
    
    async def stop_collection(self):
        """Stop data collection."""
        self.is_running = False
        if self.redis_client:
            await self.redis_client.close()
