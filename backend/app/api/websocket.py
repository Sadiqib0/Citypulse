"""
WebSocket handlers for real-time data streaming.
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set
import redis.asyncio as redis
import json
import asyncio
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and broadcasts."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.redis_client = None
    
    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.discard(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def get_redis(self):
        """Get Redis client connection."""
        if not self.redis_client:
            self.redis_client = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client
    
    async def subscribe_and_broadcast(self, channel: str):
        """
        Subscribe to Redis channel and broadcast messages to WebSocket clients.
        
        Args:
            channel: Redis pub/sub channel name
        """
        redis_client = await self.get_redis()
        pubsub = redis_client.pubsub()
        
        try:
            await pubsub.subscribe(channel)
            logger.info(f"Subscribed to Redis channel: {channel}")
            
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                
                if message and message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        await self.broadcast({
                            "channel": channel,
                            "data": data,
                            "timestamp": data.get("timestamp")
                        })
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding message: {e}")
                
                await asyncio.sleep(0.01)  # Small delay to prevent busy loop
                
        except asyncio.CancelledError:
            logger.info(f"Unsubscribing from channel: {channel}")
            await pubsub.unsubscribe(channel)
            await pubsub.close()
        except Exception as e:
            logger.error(f"Error in subscription: {e}")


# Global connection manager
manager = ConnectionManager()


async def events_websocket_handler(websocket: WebSocket):
    """
    WebSocket handler for real-time event streaming.
    
    Args:
        websocket: WebSocket connection
    """
    await manager.connect(websocket)
    
    # Start Redis subscription in background
    subscription_task = asyncio.create_task(
        manager.subscribe_and_broadcast("events:*")
    )
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            
            # Echo back or handle client messages
            await websocket.send_json({
                "type": "ack",
                "message": "Message received"
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        subscription_task.cancel()
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
        subscription_task.cancel()


async def sensor_websocket_handler(websocket: WebSocket, sensor_id: str):
    """
    WebSocket handler for specific sensor data streaming.
    
    Args:
        websocket: WebSocket connection
        sensor_id: Sensor identifier
    """
    await manager.connect(websocket)
    
    # Subscribe to specific sensor channel
    channel = f"sensors:{sensor_id}"
    subscription_task = asyncio.create_task(
        manager.subscribe_and_broadcast(channel)
    )
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({
                "type": "ack",
                "sensor_id": sensor_id
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        subscription_task.cancel()
    except Exception as e:
        logger.error(f"WebSocket error for sensor {sensor_id}: {e}")
        manager.disconnect(websocket)
        subscription_task.cancel()
