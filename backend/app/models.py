from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP, func, text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100), nullable=False, unique=True)
    harga = Column(Float, nullable=False)
    kategori = Column(String(50), nullable=False) 
    tersedia = Column(Boolean, server_default=text("1"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(20), nullable=True) # <--- Ini yang tadi hilang
    time = Column(String(10), nullable=True)         # <--- Ini juga
    customer_name = Column(String(100), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=True)
    quantity = Column(Integer, server_default=text("1"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(30), server_default="Baru", nullable=False)
    notes = Column(String(255), nullable=True)       # <--- Dan ini
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    menu_item = relationship("MenuItem")