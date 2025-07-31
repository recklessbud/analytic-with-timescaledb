from fastapi import APIRouter
from .models import EventSchema, EventListSchema, EventCreateSchema, UpdateSchema
from api.db.config import DATABASE_URL

router = APIRouter()

@router.get("/")
async def root() -> EventListSchema:
    print(DATABASE_URL)
    return {"results": [{"id": 1}, {"id": 3}, {"id": 4},{ "id": 5}],}

@router.post("/")
async def send_data(payload: EventCreateSchema) -> EventSchema:
    print(payload)
    return {"id": 12}


@router.put('/{event_id}')
async def update_id(event_id: int, payload:UpdateSchema) -> EventSchema:
    return {"id": event_id}

@router.get("/{event_id}")
async def get_id(event_id: int) -> EventSchema:
    return {"id": event_id}