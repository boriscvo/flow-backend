from fastapi import APIRouter, HTTPException
from datetime import datetime
import pytz
import phonenumbers

from .db import SessionLocal
from .models import Reminder
from .schemas import ReminderCreate, ReminderOut

router = APIRouter(prefix="/reminders")

@router.post("", response_model=ReminderOut)
def create_reminder(data: ReminderCreate):
    try:
        tz = pytz.timezone(data.timezone)
        local_dt = datetime.strptime(
            f"{data.scheduledAtDate} {data.scheduledAtTime}",
            "%Y-%m-%d %H:%M"
        )
        local_dt = tz.localize(local_dt)
        scheduled_utc = local_dt.astimezone(pytz.utc)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date or time or timezone")

    if scheduled_utc <= datetime.utcnow().replace(tzinfo=pytz.utc):
        raise HTTPException(status_code=400, detail="Reminder must be in future")

    try:
        phone = phonenumbers.parse(data.phoneNumber)
        if not phonenumbers.is_valid_number(phone):
            raise Exception()
        phone_e164 = phonenumbers.format_number(
            phone, phonenumbers.PhoneNumberFormat.E164
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid phone number")

    db = SessionLocal()
    reminder = Reminder(
        title=data.title,
        message=data.message,
        phone=phone_e164,
        scheduled_at_utc=scheduled_utc,
        status="scheduled",
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    db.close()

    return reminder
