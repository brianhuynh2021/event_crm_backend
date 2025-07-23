from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    avatar = Column(String, nullable=True)
    gender = Column(String)
    job_title = Column(String)
    company = Column(String)
    city = Column(String)
    state = Column(String)
    hosted_count = Column(Integer, default=0)
    attended_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Schema
# - id: str (PK)
# - firstName: str
# - lastName: str
# - phoneNumber: str
# - email: str
# - avatar: str
# - gender: str
# - jobTitle: str
# - company: str
# - city: str
# - state: str
# - createdAt: str (ISO timestamp)
# - updatedAt: str (ISO timestamp)