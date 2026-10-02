import sys
from pathlib import Path
from datetime import datetime
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
    search: Optional[str] = Query(None, description="Cari nama, menu, atau nomor..."),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    data = sessions_db
    if search:
        query = search.lower()
        data = [
            s for s in data 
            if query in s["customer_name"].lower() 
            or query in s["menu"].lower() 
            or query in s["order_number"].lower()
        ]
    return data[skip : skip + limit]

@router.get("/{session_id}", response_model=SessionResponse)
def get_session_by_id(session_id: int):
    for session in sessions_db:
        if session["id"] == session_id:
            return session
    raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreate):
    new_id = max([s["id"] for s in sessions_db], default=0) + 1
    
    latest_order = max([int(s["order_number"].replace("#", "")) for s in sessions_db], default=1000)
    new_order_num = f"#{latest_order + 1}"
    
    current_time = datetime.now().strftime("%H.%M")

    new_session = {
        "id": new_id,
        "order_number": new_order_num,
        "time": current_time,
        **payload.model_dump()
    }
    
    sessions_db.insert(0, new_session)
    return new_session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int):
    for index, session in enumerate(sessions_db):
        if session["id"] == session_id:
            sessions_db.pop(index)
            return None
    raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")