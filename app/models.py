from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    scheduled_at_utc = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
