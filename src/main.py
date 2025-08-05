from fastapi import FastAPI
from api.events import router as events_router
from api.db.session import initialize_db
from contextlib import asynccontextmanager



@asynccontextmanager 
async def lifespan(app: FastAPI):
    initialize_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(events_router, prefix='/api/events')

@app.get("/")
def hello_world():
    return {"message": "Hello Worldfbibksfs!"}



@app.get("/healthz")
def health_check():
    return {"status": "ok!"}