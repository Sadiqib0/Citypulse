"""
API endpoints for events management.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from uuid import UUID
from app.db.session import get_db
from app.models.events import Event, EventType, EventSeverity
from app.schemas.events import EventResponse, EventCreate, EventUpdate
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/", response_model=List[EventResponse])
async def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List all events with optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        event_type: Filter by event type
        severity: Filter by severity level
        is_active: Filter by active status
        db: Database session
        
    Returns:
        List of events
    """
    query = select(Event)
    
    # Apply filters
    if event_type:
        try:
            query = query.where(Event.event_type == EventType(event_type))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid event type")
    
    if severity:
        try:
            query = query.where(Event.severity == EventSeverity(severity))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid severity level")
    
    if is_active is not None:
        query = query.where(Event.is_active == is_active)
    
    # Order by created_at descending
    query = query.order_by(Event.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    events = result.scalars().all()
    
    return events


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific event by ID.
    
    Args:
        event_id: Event UUID
        db: Database session
        
    Returns:
        Event details
    """
    query = select(Event).where(Event.id == event_id)
    result = await db.execute(query)
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event


@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new event.
    
    Args:
        event_in: Event creation data
        db: Database session
        
    Returns:
        Created event
    """
    event = Event(**event_in.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    
    return event


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: UUID,
    event_in: EventUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing event.
    
    Args:
        event_id: Event UUID
        event_in: Event update data
        db: Database session
        
    Returns:
        Updated event
    """
    query = select(Event).where(Event.id == event_id)
    result = await db.execute(query)
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update fields
    update_data = event_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    await db.commit()
    await db.refresh(event)
    
    return event


@router.delete("/{event_id}", status_code=204)
async def delete_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an event (soft delete by marking inactive).
    
    Args:
        event_id: Event UUID
        db: Database session
    """
    query = select(Event).where(Event.id == event_id)
    result = await db.execute(query)
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.is_active = False
    await db.commit()


@router.get("/stats/summary")
async def get_event_summary(
    db: AsyncSession = Depends(get_db)
):
    """
    Get summary statistics for events.
    
    Args:
        db: Database session
        
    Returns:
        Summary statistics
    """
    # Total count
    total_query = select(func.count(Event.id))
    total = await db.scalar(total_query)
    
    # Count by type
    type_query = select(
        Event.event_type,
        func.count(Event.id)
    ).group_by(Event.event_type)
    result = await db.execute(type_query)
    by_type = {row[0].value: row[1] for row in result}
    
    # Count by severity
    severity_query = select(
        Event.severity,
        func.count(Event.id)
    ).group_by(Event.severity)
    result = await db.execute(severity_query)
    by_severity = {row[0].value: row[1] for row in result}
    
    # Recent events (last 24h)
    cutoff = datetime.utcnow() - timedelta(hours=24)
    recent_query = select(func.count(Event.id)).where(
        Event.created_at >= cutoff
    )
    recent = await db.scalar(recent_query)
    
    return {
        "total_events": total or 0,
        "recent_events_24h": recent or 0,
        "by_type": by_type,
        "by_severity": by_severity
    }
