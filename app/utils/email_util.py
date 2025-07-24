import aiosmtplib
from email.message import EmailMessage
from app.models.email_log_model import EmailLog
from sqlalchemy.orm import Session
import os
import uuid


async def send_email_to_user_smtp(
    to: str,
    subject: str,
    content: str,
    db: Session,
    user_id: str = ''
):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_SENDER")
    message["To"] = to
    message["Subject"] = subject
    message.set_content(content)

    status = "sent"

    try:
        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=os.getenv("EMAIL_SENDER"),
            password=os.getenv("EMAIL_PASSWORD"),
        )
    except Exception as e:
        print(f"❌ Failed to send to {to}: {e}")
        status = "failed"

    # ✅ Save to DB
    email_log = EmailLog(
        id=str(uuid.uuid4()),
        user_id=user_id,
        subject=subject,
        content=content,
        status=status,
    )
    db.add(email_log)
    db.commit()