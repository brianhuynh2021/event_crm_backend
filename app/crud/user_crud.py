from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user_model import User
from app.models.event_attendee_model import EventAttendee
from app.schemas.user_schema import UserCreate
from app.models.event_model import Event
from sqlalchemy import func, and_

# Create
def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Get by ID
def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

# Get by email
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

# List users
def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

# Update user
def update_user(db: Session, user_id: str, updates: dict) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    for key, value in updates.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def filter_users(
    db: Session,
    company: Optional[str] = None,
    job_title: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    hosted_min: Optional[int] = None,
    hosted_max: Optional[int] = None,
    attended_min: Optional[int] = None,
    attended_max: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_dir: str = "desc"
) -> List[User]:
    # Subqueries for hosted and attended counts
    hosted_subq = db.query(
        Event.owner,
        func.count(Event.id).label("hosted_count")
    ).group_by(Event.owner).subquery()

    attended_subq = db.query(
        EventAttendee.user_id,
        func.count(EventAttendee.event_id).label("attended_count")
    ).group_by(EventAttendee.user_id).subquery()

    query = db.query(User).outerjoin(
        hosted_subq, User.id == hosted_subq.c.owner
    ).outerjoin(
        attended_subq, User.id == attended_subq.c.user_id
    ).add_columns(
        hosted_subq.c.hosted_count,
        attended_subq.c.attended_count
    )

    # Filter base fields
    filters = {
        "company": company,
        "job_title": job_title,
        "city": city,
        "state": state
    }

    for field, value in filters.items():
        if value:
            query = query.filter(getattr(User, field) == value)

    # Hosted range filter
    if hosted_min is not None:
        query = query.filter(
            func.coalesce(hosted_subq.c.hosted_count, 0) >= hosted_min
        )
    if hosted_max is not None:
        query = query.filter(
            func.coalesce(hosted_subq.c.hosted_count, 0) <= hosted_max
        )

    # Attended range filter
    if attended_min is not None:
        query = query.filter(
            func.coalesce(attended_subq.c.attended_count, 0) >= attended_min
        )
    if attended_max is not None:
        query = query.filter(
            func.coalesce(attended_subq.c.attended_count, 0) <= attended_max
        )

    # Sorting
    sort_column = getattr(User, sort_by, None)
    if sort_column is not None:
        if sort_dir == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

    results = query.offset(skip).limit(limit).all()
    return [row[0] for row in results]  # extract User only from tuple