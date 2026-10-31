"""ASGI entry point for local run and Render.

Render start command:
    uvicorn main:app --host 0.0.0.0 --port $PORT
"""
import os
import uvicorn
from app import app

# Re-export so `uvicorn main:app` works
__all__ = ["app"]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
