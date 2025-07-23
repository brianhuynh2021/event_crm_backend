from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EventBase(BaseModel):
    slug: str
    title: str
    description: str
    start_at: datetime
    end_at: datetime
    venue: str
    max_capacity: int
    owner: str  # user_id
    hosts: List[str]
    attendees: Optional[List[str]] = []
    status: Optional[str] = "draft"

class EventCreate(EventBase):
    id: str  # explicitly required

class EventOut(EventBase):
    id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True