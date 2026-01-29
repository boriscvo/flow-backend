from pydantic import BaseModel
from datetime import datetime

class ReminderCreate(BaseModel):
    title: str
    message: str
    phoneNumber: str
    scheduledAtDate: str
    scheduledAtTime: str
    timezone: str

class ReminderOut(BaseModel):
    id: int
    title: str
    message: str
    phoneNumber: str
    scheduledAt: datetime
    timezone: str
    status: str
    error: str | None = None
    createdAt: datetime
