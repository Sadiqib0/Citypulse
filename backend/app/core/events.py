"""
Application lifecycle event handlers.
Manages startup and shutdown events.
"""
import asyncio
from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.services.collectors.data_collector import DataCollectorService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


async def startup_event(app: FastAPI):
    """
    Handle application startup.
    - Initialize database tables
    - Start background data collection tasks
    """
    logger.info("Starting CityPulse application...")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created successfully")
    
    # Initialize and start data collector
    if settings.SIMULATE_DATA:
        collector = DataCollectorService()
        app.state.data_collector = collector
        app.state.collector_task = asyncio.create_task(collector.start_collection())
        logger.info("Data collection service started")
    
    logger.info("CityPulse startup complete")


async def shutdown_event(app: FastAPI):
    """
    Handle application shutdown.
    - Stop background tasks
    - Close database connections
    """
    logger.info("Shutting down CityPulse application...")
    
    # Stop data collector
    if hasattr(app.state, 'collector_task'):
        app.state.collector_task.cancel()
        try:
            await app.state.collector_task
        except asyncio.CancelledError:
            pass
    
    # Dispose database engine
    await engine.dispose()
    
    logger.info("CityPulse shutdown complete")
