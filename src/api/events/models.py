# from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Field, SQLModel
import sqlmodel
from datetime import datetime, timezone
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now 

 
# def get_utc_now():
#     return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

class EventSchema(TimescaleModel, table=True):
    page: str = Field(index=True)
    description: Optional[str] = ''
    # sensor_id: int
    # value: float   
    __chunk_time_interval__='INTERVAL 1 day' 
    __drop_after__='INTERVAL 3 months'
    # createdAt: datetime = Field(default_factory=get_utc_now, sa_type=sqlmodel.DateTime(timezone=True), nullable=False)
    updatedAt: datetime = Field(default_factory= get_utc_now, sa_type=sqlmodel.DateTime(timezone=True), nullable=False)


class EventListSchema(SQLModel):
    results: List[EventSchema]
    count: int



class EventCreateSchema(SQLModel):
    page: str
    description: str


class UpdateSchema(SQLModel): 
    description: str