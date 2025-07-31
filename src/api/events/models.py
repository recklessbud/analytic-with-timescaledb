# from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Field, SQLModel

class EventSchema(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ''
    description: Optional[str] = ''


class EventListSchema(SQLModel):
    results: List[EventSchema]


class EventCreateSchema(SQLModel):
    path: str


class UpdateSchema(SQLModel):
    description: str