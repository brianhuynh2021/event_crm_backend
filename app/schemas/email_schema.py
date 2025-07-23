# app/schemas/email_schema.py
from typing import Optional
from pydantic import BaseModel, EmailStr

class EmailFilters(BaseModel):
    company: Optional[str] = None
    job_title: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    hosted_min: Optional[int] = None
    hosted_max: Optional[int] = None
    attended_min: Optional[int] = None
    attended_max: Optional[int] = None

class EmailRequest(BaseModel):
    subject: str
    content: str
    filters: EmailFilters