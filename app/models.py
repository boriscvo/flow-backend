from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, Integer, String, DateTime
from .db import Base

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(
        String,
        primary_key=True,
        default=lambda: uuid.uuid4().hex[:6],
    )
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    scheduled_at_utc = Column(DateTime, nullable=False)
    timezone = Column(String, nullable=False)
    status = Column(String, default="scheduled")
    snooze_count = Column(Integer, default=0, nullable=False)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)
