from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.event_schema import EventOut
from app.crud.event_crud import filter_events
from app.api.v1.deps import get_db
router = APIRouter()

@router.get("/")
def get_event():
    return {"events": []}

@router.get("/filter", response_model=List[EventOut])
def filter_event_endpoint(
    owner: Optional[str] = None,
    attendee: Optional[str] = None,
    start_from: Optional[str] = None,
    end_to: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_dir: str = "desc",
    db: Session = Depends(get_db)
):
    return filter_events(
        db=db,
        owner=owner,
        attendee=attendee,
        start_from=start_from,
        end_to=end_to,
        status=status,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_dir=sort_dir
    )