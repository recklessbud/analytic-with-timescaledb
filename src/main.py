from fastapi import FastAPI
from api.events import router as events_router
from api.db.session import initialize_db
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager 
async def lifespan(app: FastAPI):
    try:
        initialize_db()
    except Exception as e:
        print(f"Database initialization failed: {e}")
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(  
    CORSMiddleware,
    allow_origins=["*"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers)
    )
app.include_router(events_router, prefix='/api/events')


@app.get("/healthz")
def health_check():
    return {"status": "ok!"}