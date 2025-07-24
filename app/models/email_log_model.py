from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    subject = Column(String, nullable=True)
    content = Column(String, nullable=True)
    status = Column(String, nullable=True)  # e.g., "sent", "failed"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="email_logs")