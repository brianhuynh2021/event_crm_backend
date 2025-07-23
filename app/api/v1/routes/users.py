from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user_schema import UserOut
from app.crud.user_crud import filter_users
from app.api.v1.deps import get_db

router = APIRouter()

@router.get("/")
def get_user():
    return {"user": []}


@router.get("/filter", response_model=List[UserOut])
def filter_user_endpoint(
    company: Optional[str] = None,
    job_titile: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    gender: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_dir: str = "desc",
    db: Session = Depends(get_db)
):
    return filter_users(
        db=db,
        company=company,
        job_title=job_titile,
        city=city,
        state=state,
        gender=gender,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_dir=sort_dir
    )