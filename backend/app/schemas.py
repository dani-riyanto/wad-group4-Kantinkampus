from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1)
    model_config = ConfigDict(extra="forbid")

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1)
    model_config = ConfigDict(extra="forbid")

class UserUpdate(BaseModel):
    display_name: str = Field(..., min_length=2, max_length=100)
    model_config = ConfigDict(extra="forbid")

class UserResponse(BaseModel):
    id: int
    username: str
    display_name: str
    role: str

    class Config:
        from_attributes = True

class AuthSessionResponse(BaseModel):
    user: UserResponse
    csrf_token: str

class SessionCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, description="Nama pelanggan")
    menu_item_id: int = Field(..., description="ID menu yang dipilih") # Ubah ke ID
    quantity: int = Field(..., ge=1, description="Jumlah pesanan (minimal 1)")
    notes: Optional[str] = Field("", description="Catatan pesanan, bisa kosong")

    model_config = ConfigDict(extra="forbid")

class SessionResponse(BaseModel):
    id: int
    owner_id: int
    customer_name: str
    menu_item_id: int
    quantity: int
    total_price: float
    status: str
    notes: Optional[str] = None
    order_number: Optional[str] = None
    time: Optional[str] = None
    menu_item: Optional["MenuResponse"] = None

    class Config:
        from_attributes = True

class SessionUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=2)
    menu_item_id: Optional[int] = None
    quantity: Optional[int] = Field(None, ge=1)
    status: Optional[str] = Field(None, pattern="^(Baru|Diproses|Selesai)$")
    notes: Optional[str] = Field(None, max_length=255)
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def require_update_fields(self):
        if not self.model_fields_set:
            raise ValueError("Minimal satu field harus diperbarui")
        for field_name in self.model_fields_set:
            if getattr(self, field_name) is None:
                raise ValueError("Field yang dikirim tidak boleh bernilai null")
        return self

class MenuCreate(BaseModel):
    nama: str = Field(..., min_length=1, description="Nama menu")
    harga: int = Field(..., ge=0, description="Harga menu dalam Rupiah")
    kategori: str = Field(..., description="Kategori menu: Makanan, Minuman, dll")
    tersedia: bool = Field(True, description="Status ketersediaan menu")

class MenuResponse(MenuCreate):
    id: int
    class Config:
        from_attributes = True

SessionResponse.model_rebuild()
