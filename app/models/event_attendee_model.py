from sqlalchemy import Column, String, ForeignKey
from app.db.base import Base

class EventAttendee(Base):
    __tablename__ = "event_attendees"
    event_id = Column(String, ForeignKey("events.id"), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
