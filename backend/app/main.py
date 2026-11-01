import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.auth import create_initial_admin, migrate_order_ownership
from app.routers import auth, menus, sessions, users
from app.schemas import MenuCreate, MenuResponse
from app.database import engine

app = FastAPI(title="Kantin Kampus Training Session API")

models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def seed_initial_admin():
    create_initial_admin()
    migrate_order_ownership()

development_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
configured_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
origins = configured_origins
if os.getenv("ENVIRONMENT", "development") != "production":
    origins = list(dict.fromkeys([*origins, *development_origins]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(sessions.router)
app.include_router(menus.router)
app.include_router(auth.router)
app.include_router(users.router)
