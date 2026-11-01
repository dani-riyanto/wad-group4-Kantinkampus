# backend/app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base, sessionmaker

# load_dotenv() akan otomatis mencari file .env di folder backend/
load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL tidak ditemukan. Pastikan file .env sudah dibuat di folder backend.")

# Buat koneksi ke PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Fungsi dependency untuk mengambil sesi database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()