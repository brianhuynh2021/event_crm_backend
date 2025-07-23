from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(String)
    start_at = Column(DateTime(timezone=True))
    end_at = Column(DateTime(timezone=True))
    venue = Column(String)
    max_capacity = Column(Integer)
    owner = Column(String, index=True)  # user_id of the owner
    hosts = Column(String)  # simple string list for now (e.g. "id1,id2")
    attendees = Column(String)
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
# Event Schema
# - id: str (PK)
# - slug: str (unique, used for URLs)
# - title: str
# - description: str
# - startAt: str (ISO timestamp)
# - endAt: str (ISO timestamp)
# - venue: str
# - maxCapacity: int
# - owner: str (user_id)
# - hosts: str (comma-separated user_ids or future relation table)
# - createdAt: str (timestamp)
# - updatedAt: str (timestamp)
# - status: str (e.g. 'draft', 'published')
