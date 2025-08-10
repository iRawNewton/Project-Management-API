from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes import auth
from app.db.database import init_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Startup logic
    await init_indexes()
    yield
    # 🔁 Optional: add shutdown logic here


app = FastAPI(
    title="Project Management API",
    description="API for authentication and project management",
    version="1.0.0",
    lifespan=lifespan  # 👈 use lifespan instead of @app.on_event
)


# Routes
app.include_router(auth.router, prefix="/api", tags=["Auth"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "API is up and running"}


# Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
