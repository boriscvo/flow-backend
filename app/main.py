from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .reminders import router as reminders_router
from .db import engine
from .models import Base

app = FastAPI()
app.include_router(reminders_router)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}
