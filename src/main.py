from fastapi import FastAPI
from api.events import router as events_router

app = FastAPI()
app.include_router(events_router, prefix='/api/events')


@app.get("/")
def hello_world():
    return {"message": "Hello Worldfbibksfs!"}



@app.get("/healthz")
def health_check():
    return {"status": "ok!"}