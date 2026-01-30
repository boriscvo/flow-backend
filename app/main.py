from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from .reminders import router as reminders_router
from .db import engine
from .models import Base
from .worker import process_due_reminders


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def loop():
        while True:
            await process_due_reminders()
            await asyncio.sleep(10)

    task = asyncio.create_task(loop())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)
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
