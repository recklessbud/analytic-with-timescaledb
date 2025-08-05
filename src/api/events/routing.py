from fastapi import APIRouter, Depends, HTTPException
from .models import EventSchema, EventListSchema, EventCreateSchema, UpdateSchema, get_utc_now
from api.db.config import DATABASE_URL
from api.db.session import get_session 
from sqlmodel import Session, select
from typing import List

router = APIRouter()


@router.get("/", response_model=EventListSchema)
async def root(session: Session = Depends(get_session)):
    query = select(EventSchema).order_by(EventSchema.id.desc())
    results = session.exec(query).all() 
    print(DATABASE_URL) 
    return { 
        "results": results,
        "count": len(results) 
        } 

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