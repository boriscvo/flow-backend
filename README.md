## Installation

This backend powers the Call Me Reminder application.
It provides CRUD APIs for reminders, persists them in a SQLite database, and runs a background scheduler that triggers reminders when they become due.

For the purposes of this take-home assignment, the phone call integration is simulated via a service abstraction. The system is structured so that a real provider (e.g. Twilio + Vapi) can be plugged in without changing core logic. The project needs these inside .env (root file), as indicated in the requirements

```bash
VAPI_API_KEY=
VAPI_ASSISTANT_ID=
VAPI_PHONE_NUMBER_ID=
```

The installation process is

1. Clone the repository
2. Run

```bash
python -m venv venv
source venv/bin/activate (on Windows use `venv\Scripts\activate`)
pip install -r requirements.txt
```

3. Start the server with `uvicorn app.main:app --reload` which triggers api at http://localhost:8000

## Stack

- Python 3.10+
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

## The top level structure looks like this:

**main.py** - FastAPI app entrypoint
**database.py** - DB engine & session
**models.py** - SQLAlchemy models
**schemas.py** - Pydantic schemas
**reminders.py** - API routes and DB operations for this particular task
**vapi_service.py** - Service wrapper for triggering outbound phone calls via Vapi
**worker.py** - Background scheduler loop
