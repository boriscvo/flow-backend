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
    id: str
    title: str
    message: str
    phoneNumber: str
    scheduledAt: datetime
    timezone: str
    status: str
    snoozeCount: int | None = None

class ReminderDetailsOut(ReminderOut):
    createdAt: datetime
    failureReason: str | None = None

