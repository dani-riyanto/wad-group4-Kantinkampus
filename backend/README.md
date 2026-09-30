# Backend — Kantin Kampus Training Session API

Modul backend ini dibangun menggunakan **FastAPI** dengan arsitektur modular untuk menangani sistem pencatat sesi pelatihan internal domain **Kantin Kampus (Pesanan Makanan)**.

## Struktur Direktori Backend
```text
backend/
├── requirements.txt      # Daftar dependensi (FastAPI, Uvicorn, Pydantic)
└── app/
    ├── __init__.py
    ├── main.py           # Inisialisasi FastAPI & Middleware CORS
    ├── schemas.py        # Skema validasi Pydantic (In/Out terpisah)
    └── routers/
        ├── __init__.py
        └── sessions.py   # Logika endpoint /sessions (B1 - B4)