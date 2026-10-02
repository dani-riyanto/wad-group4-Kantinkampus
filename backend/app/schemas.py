from pydantic import BaseModel, Field
from typing import Optional

class SessionCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, description="Nama pelanggan")
    menu: str = Field(..., description="Pilihan menu dari dropdown")
    quantity: int = Field(..., ge=1, description="Jumlah pesanan (minimal 1)")
    status: str = Field(..., description="Status pesanan: Baru, Diproses, Selesai")
    notes: Optional[str] = Field("", description="Catatan pesanan, bisa kosong")
    total_price: int = Field(..., ge=0, description="Total harga dalam Rupiah")

class SessionResponse(SessionCreate):
    id: int
    order_number: str
    time: str

class MenuCreate(BaseModel):
    nama: str = Field(..., min_length=1, description="Nama menu")
    harga: int = Field(..., ge=0, description="Harga menu dalam Rupiah")
    kategori: str = Field(..., description="Kategori menu: Makanan, Minuman, dll")
    tersedia: bool = Field(True, description="Status ketersediaan menu")

class MenuResponse(MenuCreate):
    id: int
