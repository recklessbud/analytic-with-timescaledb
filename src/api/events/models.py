# from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Field, SQLModel
import sqlmodel
from datetime import datetime, timezone

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

class EventSchema(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ''
    description: Optional[str] = ''
    createdAt: datetime = Field(default_factory=get_utc_now, sa_type=sqlmodel.DateTime(timezone=True), nullable=False)
    updatedAt: datetime = Field(default_factory= get_utc_now, sa_type=sqlmodel.DateTime(timezone=True), nullable=False)


class EventListSchema(SQLModel):
    results: List[EventSchema]
    count: int


class EventCreateSchema(SQLModel):
    page: str
    description: str


class UpdateSchema(SQLModel): 
    description: str