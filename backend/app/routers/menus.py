# backend/app/routers/menus.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.auth import get_current_user, require_admin
from app.schemas import MenuCreate, MenuResponse
from app.database import get_db
from app import models

router = APIRouter(prefix="/menus", tags=["Menus"])

# --- ENDPOINTS ---

@router.get("", response_model=List[MenuResponse])
def get_all_menus(
    db: Session = Depends(get_db),
    _user: models.User = Depends(get_current_user),
):
    menus = db.query(models.MenuItem).all()
    return menus

@router.post("", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(
    payload: MenuCreate,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(require_admin),
):
    new_menu = models.MenuItem(
        nama=payload.nama,
        harga=payload.harga,
        kategori=payload.kategori,
        tersedia=payload.tersedia
    )
    
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    
    return new_menu

@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu_by_id(
    menu_id: int,
    db: Session = Depends(get_db),
    _user: models.User = Depends(get_current_user),
):
    menu = db.query(models.MenuItem).filter(models.MenuItem.id == menu_id).first()
    
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Menu dengan id {menu_id} tidak ditemukan"
        )
    return menu

@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(require_admin),
):
    menu = db.query(models.MenuItem).filter(models.MenuItem.id == menu_id).first()
    
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Menu tidak dapat dihapus karena tidak ditemukan"
        )
    
    db.delete(menu)
    db.commit()
    
    return None