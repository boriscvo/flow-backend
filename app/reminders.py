from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone as dt_timezone
import pytz
import phonenumbers

from .db import SessionLocal
from .models import Reminder
from .schemas import ReminderCreate, ReminderOut, ReminderDetailsOut

router = APIRouter(prefix="/reminders")

def as_utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=dt_timezone.utc)

@router.post("", response_model=ReminderOut)
def create_reminder(data: ReminderCreate):
    try:
        tz = pytz.timezone(data.timezone)
        local_dt = datetime.strptime(
            f"{data.scheduledAtDate} {data.scheduledAtTime}",
            "%Y-%m-%d %H:%M",
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
        scheduledAt=as_utc(reminder.scheduled_at_utc),
        timezone=reminder.timezone,
        status=reminder.status,
        snoozeCount=reminder.snooze_count,
    )


@router.get("", response_model=list[ReminderOut])
def list_reminders():
    db = SessionLocal()
    reminders = db.query(Reminder).order_by(Reminder.scheduled_at_utc.asc()).all()
    db.close()

    return [
        ReminderOut(
            id=r.id,
            title=r.title,
            message=r.message,
            phoneNumber=f"****{r.phone[-4:]}",
            scheduledAt=as_utc(r.scheduled_at_utc),
            timezone=r.timezone,
            status=r.status,
            snoozeCount=r.snooze_count,
        )
        for r in reminders
    ]


@router.get("/{reminder_id}", response_model=ReminderDetailsOut)
def get_reminder(reminder_id: str):
    db = SessionLocal()
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    db.close()

    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    return ReminderDetailsOut(
        id=reminder.id,
        title=reminder.title,
        message=reminder.message,
        phoneNumber=f"****{reminder.phone[-4:]}",
        scheduledAt=as_utc(reminder.scheduled_at_utc),
        timezone=reminder.timezone,
        status=reminder.status,
        snoozeCount=reminder.snooze_count,
        createdAt=as_utc(reminder.created_at),
        failureReason=reminder.error,
    )


@router.delete("/{reminder_id}", status_code=204)
def delete_reminder(reminder_id: str):
    db = SessionLocal()
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()

    if not reminder:
        db.close()
        raise HTTPException(status_code=404, detail="Reminder not found")

    db.delete(reminder)
    db.commit()
    db.close()
