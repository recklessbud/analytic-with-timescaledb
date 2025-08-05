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
    user_agent: Optional[str] = Field(default="", index=True)
    ipAddress: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    duration: Optional[int] = Field(default=0)
    sessionId: Optional[str] = Field(index=True) 


    __chunk_time_interval__='INTERVAL 1 day' 
    __drop_after__='INTERVAL 3 months'
 

class EventListSchema(SQLModel):
    results: List[EventSchema]
    count: int


class EventBucSchema(SQLModel):
    bucket:datetime
    page:str
    count:int


class EventCreateSchema(SQLModel):
    page: str = Field(index=True)
    user_agent: Optional[str] = Field(default="", index=True)
    ipAddress: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    duration: Optional[int] = Field(default=0)
    sessionId: Optional[str] = Field(index=True) 


class UpdateSchema(SQLModel): 
    description: str