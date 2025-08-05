from fastapi import APIRouter, Depends, HTTPException, Query
from .models import EventSchema, EventBucSchema, EventCreateSchema, UpdateSchema, get_utc_now
from api.db.config import DATABASE_URL
from api.db.session import get_session 
from sqlmodel import Session, select
from typing import List
from timescaledb.hyperfunctions import time_bucket
from pprint import pprint
from datetime import datetime, timezone, timedelta
from sqlalchemy import func, case

router = APIRouter()

DEFAULT_LOOKUP_PAGES = ['/api/events/about', '/api/events/contact', '/api/events/dashboard', '/api/events/pages', '/api/events/pricing', '/api/events/privacy', '/api/events/terms', "/api/events/404", "/api/events/500"]

@router.get("/", response_model=List[EventBucSchema])
async def root(
    session: Session = Depends(get_session), 
    duration: str = Query(default='1 day'),
    pages: List = Query(default=None)
    ):
    bucket = time_bucket(duration, EventSchema.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(bucket.label('bucket'), EventSchema.page.label('page'), func.count().label("count"))
        .where(EventSchema.page.in_(lookup_pages))
        .group_by(bucket, EventSchema.page)
        .order_by(bucket, EventSchema.page)
        )
    results = session.exec(query).fetchall()
    return results

@router.post("/", response_model=EventSchema)
async def send_data(payload: EventCreateSchema, session:Session = Depends(get_session)):
    print(payload)
    data = payload.model_dump()
    obj = EventSchema.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.put('/{event_id}', response_model=EventSchema)
async def update_id(event_id: int, payload:UpdateSchema, session:Session = Depends(get_session)):
    if event_id < 1:
        raise HTTPException(status_code=404, detail="Event not found")
    response = session.get(EventSchema, event_id)
    if not response:
        raise HTTPException(status_code=404, detail="Event not found")
    data = payload.model_dump()
    print(data)
    for key, value in data.items():
        setattr(response, key, value)
    response.updatedAt = get_utc_now()
    session.add(response)
    session.commit()
    session.refresh(response)

    return response
    

@router.get("/{event_id}", response_model=EventSchema)
async def get_id(event_id: int, session: Session = Depends(get_session)):
    if event_id < 1:
        raise HTTPException(status_code=404, detail="Event not found")
    data = session.get(EventSchema, event_id)
    return data