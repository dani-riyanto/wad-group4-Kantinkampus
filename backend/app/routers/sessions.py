from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# 1. GET
@router.get("", response_model=List[schemas.SessionResponse])
def get_sessions(
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Order)
    if current_user.role != "admin":
        query = query.filter(models.Order.owner_id == current_user.id)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.Order.customer_name.ilike(search_term)) |
            (models.Order.order_number.ilike(search_term))
        )

    return query.offset(skip).limit(limit).all()


def get_order_for_user(
    session_id: int, db: Session, current_user: models.User
) -> models.Order:
    query = db.query(models.Order).filter(models.Order.id == session_id)
    if current_user.role != "admin":
        query = query.filter(models.Order.owner_id == current_user.id)
    order = query.first()
    if order is None:
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")
    return order


@router.get("/{session_id}", response_model=schemas.SessionResponse)
def get_session_by_id(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_order_for_user(session_id, db, current_user)


@router.post("", response_model=schemas.SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: schemas.SessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    menu_item = db.query(models.MenuItem).filter(
        models.MenuItem.id == payload.menu_item_id
    ).first()
    if menu_item is None:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")
    if not menu_item.tersedia:
        raise HTTPException(status_code=409, detail="Menu sedang tidak tersedia")

    # Generate order number
    latest_order = db.query(models.Order).order_by(models.Order.id.desc()).first()
    latest_num = 1000
    if latest_order and latest_order.order_number:
        try:
            latest_num = int(latest_order.order_number.replace("#", ""))
        except ValueError:
            pass
            
    new_order_num = f"#{latest_num + 1}"
    current_time = datetime.now().strftime("%H.%M")

    # Buat object model SQLAlchemy
    new_session = models.Order(
        order_number=new_order_num,
        time=current_time,
        owner_id=current_user.id,
        customer_name=payload.customer_name,
        menu_item_id=payload.menu_item_id,
        quantity=payload.quantity,
        total_price=menu_item.harga * payload.quantity,
        status="Baru",
        notes=payload.notes
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.patch("/{session_id}", response_model=schemas.SessionResponse)
def update_session(
    session_id: int,
    payload: schemas.SessionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_session = get_order_for_user(session_id, db, current_user)
    changes = payload.model_dump(exclude_unset=True)
    if "status" in changes and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Hanya admin yang dapat mengubah status pesanan",
        )

    menu_item_id = changes.get("menu_item_id", db_session.menu_item_id)
    quantity = changes.get("quantity", db_session.quantity)
    menu_item = db.query(models.MenuItem).filter(
        models.MenuItem.id == menu_item_id
    ).first()
    if menu_item is None:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")
    if not menu_item.tersedia:
        raise HTTPException(status_code=409, detail="Menu sedang tidak tersedia")

    for key, value in changes.items():
        setattr(db_session, key, value)
    db_session.total_price = menu_item.harga * quantity

    db.commit()
    db.refresh(db_session)
    return db_session

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_session = get_order_for_user(session_id, db, current_user)
    db.delete(db_session)
    db.commit()
    return None