import sys
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional

root_path = str(Path(__file__).resolve().parents[3])
if root_path not in sys.path:
    sys.path.append(root_path)

from data.data import SESSIONS_DATA
from app.schemas import SessionCreate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["Sessions"])
sessions_db = SESSIONS_DATA

@router.get("", response_model=List[SessionResponse])
def get_sessions(
    search: Optional[str] = Query(None, description="Cari berdasarkan judul, trainer, atau menu makanan"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """B1: GET /sessions dengan pagination dan query param search"""
    data = sessions_db
    if search:
        query = search.lower()
        data = [
            s for s in data 
            if query in s["title"].lower() 
            or query in s["trainer"].lower() 
            or query in s["food_menu"].lower()
        ]
    return data[skip : skip + limit]

@router.get("/{session_id}", response_model=SessionResponse)
def get_session_by_id(session_id: int):
    """B2: GET /sessions/{id} mengembalikan 404 untuk id yang tidak ada"""
    for session in sessions_db:
        if session["id"] == session_id:
            return session
    raise HTTPException(status_code=404, detail="Session not found")

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreate):
    """B3: POST /sessions dengan validasi Pydantic, skema in/out terpisah, status 201"""
    new_id = max([s["id"] for s in sessions_db], default=0) + 1
    new_session = {"id": new_id, **payload.model_dump()}
    sessions_db.append(new_session)
    return new_session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int):
    """B4: DELETE /sessions/{id} mengembalikan 204"""
    for index, session in enumerate(sessions_db):
        if session["id"] == session_id:
            sessions_db.pop(index)
            return None
    raise HTTPException(status_code=404, detail="Session not found")