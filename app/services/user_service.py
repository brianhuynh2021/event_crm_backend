from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user_model import User
from app.models.event_model import Event
from app.models.event_attendee_model import EventAttendee
from app.schemas.email_schema import EmailRequest


def apply_user_filters(db: Session, f: EmailRequest):
    filters = f.filters
    # Subquery count
    hosted_subq = (
        db.query(Event.owner, func.count().label("hosted_count"))
        .group_by(Event.owner)
        .subquery()
    )
    attended_subq = (
        db.query(EventAttendee.user_id, func.count().label("attended_count"))
        .group_by(EventAttendee.user_id)
        .subquery()
    )

    q = (
        db.query(User)
        .outerjoin(hosted_subq, User.id == hosted_subq.c.owner)
        .outerjoin(attended_subq, User.id == attended_subq.c.user_id)
    )

    if filters.company:
        q = q.filter(User.company == filters.company)
    if filters.job_title:
        q = q.filter(User.job_title == filters.job_title)
    if filters.city:
        q = q.filter(User.city == filters.city)
    if filters.state:
        q = q.filter(User.state == filters.state)
    if filters.hosted_min is not None and filters.hosted_max is not None:
        q = q.filter(
            func.coalesce(hosted_subq.c.hosted_count, 0).between(
                filters.hosted_min, filters.hosted_max
            )
        )
    if filters.attended_min is not None and filters.attended_max is not None:
        q = q.filter(
            func.coalesce(attended_subq.c.attended_count, 0).between(
                filters.attended_min, filters.attended_max
            )
        )

    return q
