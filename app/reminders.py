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
        timezone=data.timezone,
        status="scheduled",
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    db.close()

    return ReminderOut(
        id=reminder.id,
        title=reminder.title,
        message=reminder.message,
        phoneNumber=f"****{reminder.phone[-4:]}",
        scheduledAt=reminder.scheduled_at_utc,
        timezone=reminder.timezone,
        status=reminder.status,
        error=reminder.error,
        createdAt=reminder.created_at,
    )


@router.get("", response_model=list[ReminderOut])
def list_reminders():
    db = SessionLocal()
    reminders = (
        db.query(Reminder)
        .order_by(Reminder.scheduled_at_utc.asc())
        .all()
    )
    db.close()

    return [
        ReminderOut(
            id=r.id,
            title=r.title,
            message=r.message,
            phoneNumber=f"****{r.phone[-4:]}",
            scheduledAt=r.scheduled_at_utc,
            timezone=r.timezone,
            status=r.status,
            error=r.error,
            createdAt=r.created_at,
        )
        for r in reminders
    ]
