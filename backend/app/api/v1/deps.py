"""
Common dependencies for API endpoints.
"""
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.analytics.analytics_service import AnalyticsService


async def get_analytics_service(
    db: AsyncSession = Depends(get_db)
) -> AnalyticsService:
    """
    Dependency for getting analytics service.
    
    Args:
        db: Database session
        
    Returns:
        AnalyticsService instance
    """
    return AnalyticsService(db)
