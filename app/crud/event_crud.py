from sqlalchemy.orm import Session
from app.models.event_model import Event
from app.schemas.event_schema import EventCreate
import json
from typing import List, Optional

# Create a new event
def create_event(db: Session, event_in: EventCreate) -> Event:
    event = Event(
        id=event_in.id,
        slug=event_in.slug,
        title=event_in.title,
        description=event_in.description,
        start_at=event_in.start_at,
        end_at=event_in.end_at,
        venue=event_in.venue,
        max_capacity=event_in.max_capacity,
        owner=event_in.owner,
        hosts=",".join(event_in.hosts),  # store as CSV string
        attendees=json.dumps(event_in.attendees),  # store as JSON string
        status=event_in.status,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_event_by_id(db: Session, event_id: str) -> Event:
    return db.query(Event).filter(Event.id == event_id).first()

def list_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    return db.query(Event).offset(skip).limit(limit).all()

def update_event(db: Session, event_id: str, updates: dict) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return None

    # Special handling for hosts and attendees
    if "hosts" in updates:
        updates["hosts"] = ",".join(updates["hosts"])  # List[str] → CSV
    if "attendees" in updates:
        updates["attendees"] = json.dumps(updates["attendees"])  # List[str] → JSON

    for key, value in updates.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event

def filter_events(
    db: Session,
    owner: Optional[str] = None,
    attendee: Optional[str] = None,
    start_from: Optional[str] = None,
    end_to: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_dir: str = "desc"
) -> List[Event]:
    query = db.query(Event)

    if owner:
        query = query.filter(Event.owner == owner)
    if attendee:
        query = query.filter(Event.attendees.like(f"%{attendee}%"))
    if start_from:
        query = query.filter(Event.start_at >= start_from)
    if end_to:
        query = query.filter(Event.end_at <= end_to)
    if status:
        query = query.filter(Event.status == status)

    sort_column = getattr(Event, sort_by, Event.created_at)
    if sort_dir == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    return query.offset(skip).limit(limit).all()