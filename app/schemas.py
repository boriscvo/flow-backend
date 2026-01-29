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
    phone: str
    scheduled_at_utc: datetime
    status: str

    class Config:
        orm_mode = True
