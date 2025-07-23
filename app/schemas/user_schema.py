from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    avatar: Optional[str] = None
    gender: str
    job_title: str
    company: str
    city: str
    state: str
    
# For creating a new user
class UserCreate(UserBase):
    id: str  # Required explicitly

# For returning a user to client
class UserOut(UserBase):
    id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    hosted_count: Optional[int]
    attended_count: Optional[int]
    class Config:
        orm_mode = True