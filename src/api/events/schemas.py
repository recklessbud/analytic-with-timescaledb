from pydantic import BaseModel
from typing import List, Optional

class EventSchema(BaseModel):
    id: int


class EventListSchema(BaseModel):
    results: List[EventSchema]


class EventCreateSchema(BaseModel):
    path: str


class UpdateSchema(BaseModel):
    description: str