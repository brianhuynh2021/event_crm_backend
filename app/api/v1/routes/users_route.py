from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user_schema import UserOut
from app.crud.user_crud import filter_users
from app.api.v1.deps import get_db
from app.schemas.email_schema import EmailRequest
from app.utils.email_util import send_email_to_user_smtp
from app.services.user_service import apply_user_filters

router = APIRouter()

@router.get("/")
def get_user():
    return {"user": []}


@router.get("/filter", response_model=List[UserOut])
def filter_user_endpoint(
    company: Optional[str] = None,
    job_title: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    hosted_min: Optional[int] = Query(None),
    hosted_max: Optional[int] = Query(None),
    attended_min: Optional[int] = Query(None),
    attended_max: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_dir: str = "desc",
    db: Session = Depends(get_db)
):
    return filter_users(
        db=db,
        company=company,
        job_title=job_title,
        city=city,
        state=state,
        hosted_min=hosted_min,
        hosted_max=hosted_max,
        attended_min=attended_min,
        attended_max=attended_max,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_dir=sort_dir
    )

@router.post("/send-email-smtp")
async def send_email_to_filtered_users_smtp(
    payload: EmailRequest, 
    db: Session = Depends(get_db)
):
    query = apply_user_filters(db, payload)
    users = query.all()

    if not users:
        raise HTTPException(status_code=404, detail="No users match the filter criteria")

    for user in users:
        await send_email_to_user_smtp(
            to=str(user.email),
            subject=payload.subject,
            content=payload.content,
            db=db,                      # ✅ pass db
            user_id=str(user.id)            # ✅ pass user ID to log
        )

    return {
        "message": f"Sent email to {len(users)} user(s).",
        "recipients": [
            {
                "full_name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "company": user.company,
                "job_title": user.job_title,
                "city": user.city
            }
            for user in users
        ]
    }