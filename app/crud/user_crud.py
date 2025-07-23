from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from sqlalchemy import and_

# Create
def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(**user_in.dict())
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
    gender: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_dir: str = "desc"
) -> List[User]:
    query = db.query(User)

    if company:
        query = query.filter(User.company == company)
    if job_title:
        query = query.filter(User.job_title == job_title)
    if city:
        query = query.filter(User.city == city)
    if state:
        query = query.filter(User.state == state)
    if gender:
        query = query.filter(User.gender==gender)
    # Sorting
    sort_column = getattr(User, sort_by, None)
    if sort_column is not None:
        if sort_dir == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

    return query.offset(skip).limit(limit).all()