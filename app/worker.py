import asyncio
from datetime import datetime, timezone
from .db import SessionLocal
from .models import Reminder
from .vapi_service import trigger_call

async def process_due_reminders():
    db = SessionLocal()
    now = datetime.now(timezone.utc)

    reminders = (
        db.query(Reminder)
        .filter(
            Reminder.status == "scheduled",
            Reminder.scheduled_at_utc <= now,
        )
        .all()
    )

    for r in reminders:
        try:
            await trigger_call(
                phone=r.phone,
                message=r.message,
            )
            r.status = "completed"
        except Exception as e:
            r.status = "failed"
            r.error = str(e)

    db.commit()
    db.close()
