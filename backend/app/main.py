from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import sessions, menus 
from app.schemas import MenuCreate, MenuResponse

app = FastAPI(title="Kantin Kampus Training Session API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

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




