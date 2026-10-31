from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routes import router
import os

# Create the ASGI app first so hosts can always load it
app = FastAPI(title="AI Receptionist", version="1.0.0")

# Create tables. Do not block startup if the database is not ready yet.
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass

if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
