import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables
from routers.notes import router as notes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    max_retries = 30
    for i in range(max_retries):
        try:
            create_db_and_tables()
            print("Database initialized successfully")
            break
        except Exception as e:
            print(f"Database connection attempt {i+1}/{max_retries} failed: {e}")
            time.sleep(2)
    else:
        print("Failed to initialize database after max retries")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
